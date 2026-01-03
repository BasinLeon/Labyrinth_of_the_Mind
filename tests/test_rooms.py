"""Tests for room definitions."""

import pytest
from src.models import GameState, RoomType
from src.rooms import create_labyrinth


class TestLabyrinthStructure:
    """Tests for the labyrinth room structure."""

    @pytest.fixture
    def rooms(self) -> dict:
        """Create the labyrinth for testing."""
        return create_labyrinth()

    def test_labyrinth_has_entrance(self, rooms: dict) -> None:
        """Test that labyrinth has an entrance room."""
        assert "entrance" in rooms
        assert rooms["entrance"].room_type == RoomType.ENTRANCE

    def test_labyrinth_has_exit(self, rooms: dict) -> None:
        """Test that labyrinth has an exit room."""
        assert "the_exit" in rooms
        assert rooms["the_exit"].room_type == RoomType.EXIT

    def test_all_room_ids_match(self, rooms: dict) -> None:
        """Test that all room IDs match their dictionary keys."""
        for room_id, room in rooms.items():
            assert room.id == room_id

    def test_all_choices_lead_to_valid_rooms(self, rooms: dict) -> None:
        """Test that all choices lead to rooms that exist."""
        for room_id, room in rooms.items():
            for choice in room.choices:
                assert choice.next_room_id in rooms, (
                    f"Choice in {room_id} leads to non-existent room {choice.next_room_id}"
                )

    def test_exit_has_no_choices(self, rooms: dict) -> None:
        """Test that the exit room has no further choices."""
        assert len(rooms["the_exit"].choices) == 0

    def test_key_rooms_give_items(self, rooms: dict) -> None:
        """Test that key revelation rooms provide items."""
        key_rooms = ["shadow_accepted", "light_accepted", "current_life_reflection"]
        expected_items = ["shadow_key", "light_key", "truth_key"]

        for room_id, expected_item in zip(key_rooms, expected_items):
            assert rooms[room_id].on_enter_item == expected_item

    def test_final_door_requires_all_keys(self, rooms: dict) -> None:
        """Test that the final door requires all three keys."""
        final_door = rooms["final_door"]
        unlock_choice = next(
            c for c in final_door.choices if c.next_room_id == "the_exit"
        )

        state = GameState()

        # Should not be available without keys
        assert not unlock_choice.is_available(state)

        # Should not be available with only some keys
        state.add_item("shadow_key")
        assert not unlock_choice.is_available(state)

        state.add_item("light_key")
        assert not unlock_choice.is_available(state)

        # Should be available with all three keys
        state.add_item("truth_key")
        assert unlock_choice.is_available(state)


class TestLiteraryContent:
    """Tests for literary quotes and sources."""

    @pytest.fixture
    def rooms(self) -> dict:
        """Create the labyrinth for testing."""
        return create_labyrinth()

    def test_entrance_has_quote(self, rooms: dict) -> None:
        """Test that entrance has a literary quote."""
        entrance = rooms["entrance"]
        assert entrance.literary_quote is not None
        assert entrance.literary_source is not None

    def test_exit_has_quote(self, rooms: dict) -> None:
        """Test that exit has a literary quote."""
        exit_room = rooms["the_exit"]
        assert exit_room.literary_quote is not None
        assert exit_room.literary_source is not None

    def test_quotes_have_sources(self, rooms: dict) -> None:
        """Test that all rooms with quotes have sources."""
        for room_id, room in rooms.items():
            if room.literary_quote:
                assert room.literary_source, (
                    f"Room {room_id} has quote but no source"
                )
