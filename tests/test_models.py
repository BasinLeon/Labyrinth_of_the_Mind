"""Tests for game models."""

import pytest
from src.models import Choice, GameState, Room, RoomType


class TestGameState:
    """Tests for GameState class."""

    def test_initial_state(self) -> None:
        """Test default initial state."""
        state = GameState()
        assert state.current_room_id == "entrance"
        assert len(state.inventory) == 0
        assert len(state.visited_rooms) == 0
        assert len(state.reflections) == 0
        assert state.turns == 0
        assert state.has_won is False
        assert state.has_quit is False

    def test_add_item(self) -> None:
        """Test adding items to inventory."""
        state = GameState()
        state.add_item("shadow_key")
        assert "shadow_key" in state.inventory
        assert state.has_item("shadow_key")

    def test_has_item_returns_false_for_missing(self) -> None:
        """Test has_item returns False for items not in inventory."""
        state = GameState()
        assert not state.has_item("nonexistent_item")

    def test_visit_room(self) -> None:
        """Test visiting rooms."""
        state = GameState()
        assert not state.has_visited("hall_of_mirrors")
        state.visit_room("hall_of_mirrors")
        assert state.has_visited("hall_of_mirrors")

    def test_add_reflection(self) -> None:
        """Test adding reflections."""
        state = GameState()
        prompt = "What is your greatest fear?"
        response = "Being alone"
        state.add_reflection(prompt, response)
        assert state.reflections[prompt] == response


class TestChoice:
    """Tests for Choice class."""

    def test_basic_choice_always_available(self) -> None:
        """Test that a basic choice is always available."""
        choice = Choice(text="Go forward", next_room_id="next_room")
        state = GameState()
        assert choice.is_available(state)

    def test_choice_requires_item(self) -> None:
        """Test choice availability based on required item."""
        choice = Choice(
            text="Use the key",
            next_room_id="locked_room",
            requires_item="shadow_key",
        )
        state = GameState()
        assert not choice.is_available(state)

        state.add_item("shadow_key")
        assert choice.is_available(state)

    def test_choice_with_condition(self) -> None:
        """Test choice availability based on condition function."""
        choice = Choice(
            text="Enter the secret passage",
            next_room_id="secret_room",
            condition=lambda s: len(s.visited_rooms) >= 3,
        )
        state = GameState()
        assert not choice.is_available(state)

        state.visit_room("room1")
        state.visit_room("room2")
        state.visit_room("room3")
        assert choice.is_available(state)

    def test_choice_with_item_and_condition(self) -> None:
        """Test choice requiring both item and condition."""
        choice = Choice(
            text="Open the final door",
            next_room_id="ending",
            requires_item="key",
            condition=lambda s: s.has_item("light_key"),
        )
        state = GameState()

        # Neither requirement met
        assert not choice.is_available(state)

        # Only item requirement met
        state.add_item("key")
        assert not choice.is_available(state)

        # Both requirements met
        state.add_item("light_key")
        assert choice.is_available(state)


class TestRoom:
    """Tests for Room class."""

    def test_room_creation(self) -> None:
        """Test creating a basic room."""
        room = Room(
            id="test_room",
            name="Test Room",
            description="A room for testing.",
            room_type=RoomType.REFLECTION,
        )
        assert room.id == "test_room"
        assert room.name == "Test Room"
        assert room.room_type == RoomType.REFLECTION
        assert room.literary_quote is None
        assert len(room.choices) == 0

    def test_room_with_choices(self) -> None:
        """Test room with multiple choices."""
        choices = [
            Choice(text="Go left", next_room_id="left_room"),
            Choice(text="Go right", next_room_id="right_room"),
        ]
        room = Room(
            id="fork",
            name="The Fork",
            description="Two paths diverge.",
            room_type=RoomType.CHALLENGE,
            choices=choices,
        )
        assert len(room.choices) == 2

    def test_room_type_enum(self) -> None:
        """Test RoomType enum values."""
        assert RoomType.ENTRANCE.value == "entrance"
        assert RoomType.REFLECTION.value == "reflection"
        assert RoomType.CHALLENGE.value == "challenge"
        assert RoomType.REVELATION.value == "revelation"
        assert RoomType.EXIT.value == "exit"
