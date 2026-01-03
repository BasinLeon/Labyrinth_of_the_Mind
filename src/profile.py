"""Player profile management for persistent progress."""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


PROFILE_DIR = Path.home() / ".labyrinth_of_the_mind"
PROFILE_FILE = PROFILE_DIR / "profile.json"


@dataclass
class PlayerProfile:
    """Persistent player profile across game sessions."""
    # Basic stats
    total_completions: int = 0
    total_playtime_seconds: int = 0
    first_played: str | None = None
    last_played: str | None = None

    # Achievements
    unlocked_achievements: list[str] = field(default_factory=list)

    # New Game+ unlocks
    unlocked_archetypes: list[str] = field(default_factory=lambda: ["seeker"])  # Start with seeker
    unlocked_endings: list[str] = field(default_factory=list)

    # Best runs
    fastest_completion: int | None = None  # Fewest steps
    most_reflections: int = 0
    most_rooms_visited: int = 0

    # Preferences
    preferred_archetype: str | None = None
    high_contrast_mode: bool = False
    large_text_mode: bool = False
    sound_enabled: bool = True

    # Statistics
    total_reflections_written: int = 0
    total_rooms_visited: int = 0
    endings_achieved: dict[str, int] = field(default_factory=dict)

    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement. Returns True if newly unlocked."""
        if achievement_id not in self.unlocked_achievements:
            self.unlocked_achievements.append(achievement_id)
            return True
        return False

    def unlock_archetype(self, archetype_id: str) -> bool:
        """Unlock an archetype. Returns True if newly unlocked."""
        if archetype_id not in self.unlocked_archetypes:
            self.unlocked_archetypes.append(archetype_id)
            return True
        return False

    def record_completion(self, steps: int, reflections: int, rooms: int, ending_id: str) -> dict[str, Any]:
        """Record a game completion and return what was unlocked."""
        unlocks = {
            "new_best_time": False,
            "new_reflection_record": False,
            "new_exploration_record": False,
            "new_ending": False,
            "new_archetypes": [],
        }

        self.total_completions += 1
        self.last_played = datetime.now().isoformat()

        # Check records
        if self.fastest_completion is None or steps < self.fastest_completion:
            self.fastest_completion = steps
            unlocks["new_best_time"] = True

        if reflections > self.most_reflections:
            self.most_reflections = reflections
            unlocks["new_reflection_record"] = True

        if rooms > self.most_rooms_visited:
            self.most_rooms_visited = rooms
            unlocks["new_exploration_record"] = True

        # Track ending
        if ending_id not in self.unlocked_endings:
            self.unlocked_endings.append(ending_id)
            unlocks["new_ending"] = True

        self.endings_achieved[ending_id] = self.endings_achieved.get(ending_id, 0) + 1

        # Update totals
        self.total_reflections_written += reflections
        self.total_rooms_visited += rooms

        # Unlock archetypes based on progress
        if self.total_completions >= 1 and self.unlock_archetype("warrior"):
            unlocks["new_archetypes"].append("warrior")
        if self.total_completions >= 2 and self.unlock_archetype("healer"):
            unlocks["new_archetypes"].append("healer")
        if self.total_completions >= 3 and self.unlock_archetype("mystic"):
            unlocks["new_archetypes"].append("mystic")
        if self.total_completions >= 5 and self.unlock_archetype("shadow"):
            unlocks["new_archetypes"].append("shadow")

        return unlocks

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerProfile":
        """Create from dictionary."""
        return cls(**data)


def load_profile() -> PlayerProfile:
    """Load player profile from disk."""
    try:
        if PROFILE_FILE.exists():
            with open(PROFILE_FILE) as f:
                data = json.load(f)
            return PlayerProfile.from_dict(data)
    except Exception:
        pass
    return PlayerProfile(first_played=datetime.now().isoformat())


def save_profile(profile: PlayerProfile) -> bool:
    """Save player profile to disk."""
    try:
        PROFILE_DIR.mkdir(exist_ok=True)
        profile.last_played = datetime.now().isoformat()
        with open(PROFILE_FILE, "w") as f:
            json.dump(profile.to_dict(), f, indent=2)
        return True
    except Exception:
        return False
