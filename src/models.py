"""Data models for the Labyrinth of the Mind game."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class RoomType(Enum):
    """Types of rooms in the labyrinth."""
    ENTRANCE = "entrance"
    REFLECTION = "reflection"
    CHALLENGE = "challenge"
    REVELATION = "revelation"
    EXIT = "exit"


@dataclass
class Choice:
    """A choice available to the player in a room."""
    text: str
    next_room_id: str
    reflection_prompt: str | None = None
    requires_item: str | None = None
    gives_item: str | None = None
    condition: Callable[["GameState"], bool] | None = None

    def is_available(self, state: "GameState") -> bool:
        """Check if this choice is available given the current game state."""
        if self.requires_item and self.requires_item not in state.inventory:
            return False
        if self.condition and not self.condition(state):
            return False
        return True


@dataclass
class Room:
    """A room in the labyrinth."""
    id: str
    name: str
    description: str
    room_type: RoomType
    literary_quote: str | None = None
    literary_source: str | None = None
    choices: list[Choice] = field(default_factory=list)
    on_enter_text: str | None = None
    on_enter_item: str | None = None


@dataclass
class GameState:
    """The current state of the game."""
    current_room_id: str = "entrance"
    inventory: set[str] = field(default_factory=set)
    visited_rooms: set[str] = field(default_factory=set)
    reflections: dict[str, str] = field(default_factory=dict)
    choices_made: list[str] = field(default_factory=list)  # Track choice history
    traits: dict[str, int] = field(default_factory=dict)  # Personality traits
    turns: int = 0
    has_won: bool = False
    has_quit: bool = False

    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory."""
        self.inventory.add(item)

    def record_choice(self, room_id: str, choice_text: str) -> None:
        """Record a choice for personality analysis."""
        self.choices_made.append(f"{room_id}:{choice_text}")

    def add_trait(self, trait: str, points: int = 1) -> None:
        """Add points to a personality trait."""
        self.traits[trait] = self.traits.get(trait, 0) + points

    def has_item(self, item: str) -> bool:
        """Check if the player has an item."""
        return item in self.inventory

    def visit_room(self, room_id: str) -> None:
        """Mark a room as visited."""
        self.visited_rooms.add(room_id)

    def has_visited(self, room_id: str) -> bool:
        """Check if a room has been visited."""
        return room_id in self.visited_rooms

    def add_reflection(self, prompt: str, response: str) -> None:
        """Store a player's reflection."""
        self.reflections[prompt] = response
