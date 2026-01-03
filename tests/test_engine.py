"""Tests for game engine."""

import io
import pytest
from src.engine import GameEngine
from src.models import RoomType


class TestGameEngine:
    """Tests for GameEngine class."""

    def create_engine(self, inputs: list[str]) -> tuple[GameEngine, io.StringIO]:
        """Create a game engine with mocked input/output."""
        input_stream = io.StringIO("\n".join(inputs) + "\n")
        output_stream = io.StringIO()
        engine = GameEngine(
            input_stream=input_stream,
            output_stream=output_stream,
        )
        return engine, output_stream

    def test_engine_initialization(self) -> None:
        """Test engine initializes correctly."""
        engine, _ = self.create_engine([])
        assert engine.state.current_room_id == "entrance"
        assert len(engine.rooms) > 0
        assert "entrance" in engine.rooms

    def test_enter_room(self) -> None:
        """Test entering a room updates state correctly."""
        engine, _ = self.create_engine([])
        engine.enter_room("hall_of_mirrors")

        assert engine.state.current_room_id == "hall_of_mirrors"
        assert engine.state.has_visited("hall_of_mirrors")
        assert engine.state.turns == 1

    def test_enter_room_gives_item(self) -> None:
        """Test entering a room with on_enter_item gives item."""
        engine, _ = self.create_engine([])
        engine.enter_room("shadow_accepted")

        assert engine.state.has_item("shadow_key")

    def test_enter_room_item_only_once(self) -> None:
        """Test entering a room twice only gives item once."""
        engine, _ = self.create_engine([])
        engine.enter_room("shadow_accepted")
        engine.state.inventory.clear()
        engine.enter_room("shadow_accepted")

        assert not engine.state.has_item("shadow_key")

    def test_enter_invalid_room_raises(self) -> None:
        """Test entering non-existent room raises error."""
        engine, _ = self.create_engine([])
        with pytest.raises(ValueError, match="not found"):
            engine.enter_room("nonexistent_room")

    def test_display_room_output(self) -> None:
        """Test room display includes key elements."""
        engine, output = self.create_engine([])
        room = engine.rooms["entrance"]
        engine.display_room(room)

        output_text = output.getvalue()
        assert room.name.upper() in output_text
        assert room.literary_quote in output_text if room.literary_quote else True

    def test_display_inventory_empty(self) -> None:
        """Test empty inventory display."""
        engine, output = self.create_engine([])
        engine.display_inventory()

        assert "empty" in output.getvalue().lower()

    def test_display_inventory_with_items(self) -> None:
        """Test inventory display with items."""
        engine, output = self.create_engine([])
        engine.state.add_item("shadow_key")
        engine.display_inventory()

        output_text = output.getvalue()
        assert "Shadow Key" in output_text

    def test_display_reflections_empty(self) -> None:
        """Test empty reflections display."""
        engine, output = self.create_engine([])
        engine.display_reflections()

        assert "not yet recorded" in output.getvalue().lower()

    def test_display_reflections_with_entries(self) -> None:
        """Test reflections display with entries."""
        engine, output = self.create_engine([])
        engine.state.add_reflection("Test question?", "Test answer")
        engine.display_reflections()

        output_text = output.getvalue()
        assert "Test question?" in output_text
        assert "Test answer" in output_text

    def test_reflection_prompt_stores_response(self) -> None:
        """Test reflection prompt stores player response."""
        engine, _ = self.create_engine(["My reflection"])
        prompt = "What do you seek?"
        engine.prompt_reflection(prompt)

        assert engine.state.reflections[prompt] == "My reflection"

    def test_reflection_prompt_empty_skips(self) -> None:
        """Test empty reflection response is not stored."""
        engine, _ = self.create_engine([""])
        prompt = "What do you seek?"
        engine.prompt_reflection(prompt)

        assert prompt not in engine.state.reflections

    def test_quit_choice(self) -> None:
        """Test quit sets has_quit flag."""
        engine, _ = self.create_engine(["Q"])
        available = engine.rooms["entrance"].choices
        result = engine.get_player_choice(available)

        assert result is None
        assert engine.state.has_quit

    def test_valid_numeric_choice(self) -> None:
        """Test valid numeric input returns correct choice."""
        engine, _ = self.create_engine(["1"])
        available = engine.rooms["entrance"].choices[:2]
        result = engine.get_player_choice(available)

        assert result == available[0]


class TestGameCompletion:
    """Tests for complete game paths."""

    def test_winning_path(self) -> None:
        """Test a complete winning path through the game."""
        # Path: entrance -> hidden_inscription -> hall -> shadow -> accepted
        #       -> hall -> light -> accepted -> hall -> garden
        #       -> library -> current_life -> garden -> final_door -> exit
        inputs = [
            "",       # Press enter to start
            "2",      # Examine archway (hidden inscription)
            "1",      # Enter with wisdom (reflection prompt)
            "",       # Skip reflection
            "1",      # Approach shadow mirror
            "1",      # Acknowledge shadow (reflection prompt)
            "",       # Skip reflection
            "2",      # Approach light mirror (back in hall)
            "1",      # Accept light (reflection prompt)
            "",       # Skip reflection
            "3",      # Walk straight ahead to garden
            "1",      # Path of roses (library)
            "1",      # Read your life book (reflection prompt)
            "",       # Skip reflection
            "3",      # Walk to shimmering door
            "1",      # Use all three keys
        ]
        input_stream = io.StringIO("\n".join(inputs) + "\n")
        output_stream = io.StringIO()
        engine = GameEngine(input_stream=input_stream, output_stream=output_stream)

        engine.run()

        assert engine.state.has_won
        assert "CONGRATULATIONS" in output_stream.getvalue()
