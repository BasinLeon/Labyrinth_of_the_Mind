"""Achievements system for Labyrinth of the Mind."""

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState


@dataclass
class Achievement:
    """An unlockable achievement."""
    id: str
    name: str
    description: str
    icon: str
    condition: Callable[["GameState"], bool]
    secret: bool = False  # Hidden until unlocked


# All available achievements
ACHIEVEMENTS: list[Achievement] = [
    # Completion achievements
    Achievement(
        id="first_journey",
        name="First Steps",
        description="Complete the labyrinth for the first time",
        icon="🎯",
        condition=lambda s: s.has_won,
    ),
    Achievement(
        id="speed_runner",
        name="Speed Runner",
        description="Complete the labyrinth in 10 or fewer steps",
        icon="⚡",
        condition=lambda s: s.has_won and s.turns <= 10,
    ),
    Achievement(
        id="thorough_explorer",
        name="Thorough Explorer",
        description="Visit at least 15 rooms in a single journey",
        icon="🗺️",
        condition=lambda s: len(s.visited_rooms) >= 15,
    ),
    Achievement(
        id="completionist",
        name="Completionist",
        description="Visit every room in the labyrinth",
        icon="🏆",
        condition=lambda s: len(s.visited_rooms) >= 18,
    ),

    # Key achievements
    Achievement(
        id="shadow_keeper",
        name="Shadow Keeper",
        description="Obtain the Shadow Key",
        icon="🗝️",
        condition=lambda s: "shadow_key" in s.inventory,
    ),
    Achievement(
        id="light_bearer",
        name="Light Bearer",
        description="Obtain the Light Key",
        icon="✨",
        condition=lambda s: "light_key" in s.inventory,
    ),
    Achievement(
        id="truth_seeker",
        name="Truth Seeker",
        description="Obtain the Truth Key",
        icon="🔑",
        condition=lambda s: "truth_key" in s.inventory,
    ),
    Achievement(
        id="key_master",
        name="Key Master",
        description="Collect all three keys",
        icon="👑",
        condition=lambda s: all(k in s.inventory for k in ["shadow_key", "light_key", "truth_key"]),
    ),

    # Reflection achievements
    Achievement(
        id="first_reflection",
        name="Self-Aware",
        description="Record your first reflection",
        icon="💭",
        condition=lambda s: len(s.reflections) >= 1,
    ),
    Achievement(
        id="deep_thinker",
        name="Deep Thinker",
        description="Record 3 or more reflections",
        icon="🧠",
        condition=lambda s: len(s.reflections) >= 3,
    ),
    Achievement(
        id="philosopher",
        name="Philosopher",
        description="Record 5 or more reflections",
        icon="📜",
        condition=lambda s: len(s.reflections) >= 5,
    ),

    # Special achievements
    Achievement(
        id="ancient_wisdom",
        name="Ancient Wisdom",
        description="Discover the hidden inscription",
        icon="📖",
        condition=lambda s: "ancient_knowledge" in s.inventory,
    ),
    Achievement(
        id="shadow_accepted",
        name="Shadow Integration",
        description="Accept your shadow self",
        icon="🌑",
        condition=lambda s: "shadow_accepted" in s.visited_rooms,
    ),
    Achievement(
        id="light_accepted",
        name="Radiant Self",
        description="Embrace your potential",
        icon="☀️",
        condition=lambda s: "light_accepted" in s.visited_rooms,
    ),
    Achievement(
        id="memory_keeper",
        name="Memory Keeper",
        description="Visit both the happy and painful memory rooms",
        icon="🎭",
        condition=lambda s: "happy_memory" in s.visited_rooms and "painful_memory" in s.visited_rooms,
    ),

    # Secret achievements
    Achievement(
        id="door_knocker",
        name="Persistent",
        description="Try to force the final door without all keys",
        icon="🚪",
        condition=lambda s: "door_remains_closed" in s.visited_rooms,
        secret=True,
    ),
    Achievement(
        id="full_circle",
        name="Full Circle",
        description="Return to the Hall of Mirrors 3 or more times",
        icon="🔄",
        condition=lambda s: s.choices_made.count("hall_of_mirrors") >= 2,
        secret=True,
    ),
    Achievement(
        id="balanced_soul",
        name="Balanced Soul",
        description="Accept both shadow and light",
        icon="☯️",
        condition=lambda s: "shadow_accepted" in s.visited_rooms and "light_accepted" in s.visited_rooms,
        secret=True,
    ),
    
    # New room achievements
    Achievement(
        id="time_traveler",
        name="Time Traveler",
        description="Flow with the River of Time",
        icon="⏳",
        condition=lambda s: "flowing_present" in s.visited_rooms,
    ),
    Achievement(
        id="soul_forge",
        name="Soul Forge",
        description="Create something in the Forge of Creation",
        icon="🔥",
        condition=lambda s: "creation_complete" in s.visited_rooms,
    ),
    Achievement(
        id="silent_sage",
        name="Silent Sage",
        description="Find your inner voice in the Temple of Silence",
        icon="🧘",
        condition=lambda s: "inner_voice" in s.visited_rooms,
    ),
    Achievement(
        id="grateful_heart",
        name="Grateful Heart",
        description="Offer gratitude in the Chamber of Gratitude",
        icon="💝",
        condition=lambda s: "gratitude_offered" in s.visited_rooms,
    ),
    Achievement(
        id="dreamer_awakened",
        name="Dreamer Awakened",
        description="Confront your abandoned dreams",
        icon="💫",
        condition=lambda s: "abandoned_dreams" in s.visited_rooms,
        secret=True,
    ),
    Achievement(
        id="echo_breaker",
        name="Echo Breaker",
        description="Break and then find silence",
        icon="🔇",
        condition=lambda s: "echoing_words" in s.visited_rooms and "inner_voice" in s.visited_rooms,
        secret=True,
    ),
]


def check_achievements(state: "GameState", unlocked_ids: set[str]) -> list[Achievement]:
    """Check which new achievements have been unlocked."""
    newly_unlocked = []
    for achievement in ACHIEVEMENTS:
        if achievement.id not in unlocked_ids:
            try:
                if achievement.condition(state):
                    newly_unlocked.append(achievement)
            except Exception:
                pass  # Skip if condition fails
    return newly_unlocked


def get_all_achievements() -> list[Achievement]:
    """Get all achievements."""
    return ACHIEVEMENTS


def get_achievement_by_id(achievement_id: str) -> Achievement | None:
    """Get an achievement by its ID."""
    for a in ACHIEVEMENTS:
        if a.id == achievement_id:
            return a
    return None
