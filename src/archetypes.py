"""Character archetypes for Labyrinth of the Mind."""

from dataclasses import dataclass


@dataclass
class Archetype:
    """A character archetype that affects gameplay."""
    id: str
    name: str
    title: str
    description: str
    icon: str
    starting_traits: dict[str, int]
    special_ability: str
    color: str


# Available archetypes
ARCHETYPES: dict[str, Archetype] = {
    "seeker": Archetype(
        id="seeker",
        name="The Seeker",
        title="Seeker of Truth",
        description="You are driven by an insatiable curiosity. Questions matter more than answers, and every shadow hides a lesson.",
        icon="🔍",
        starting_traits={"wisdom": 1, "introspection": 1},
        special_ability="Reflection prompts reveal deeper insights",
        color="#3b82f6",
    ),
    "warrior": Archetype(
        id="warrior",
        name="The Warrior",
        title="Warrior of Light",
        description="You face challenges head-on, believing that courage transforms fear into strength. No shadow is too dark to confront.",
        icon="⚔️",
        starting_traits={"courage": 2},
        special_ability="Challenge rooms feel less intimidating",
        color="#ef4444",
    ),
    "healer": Archetype(
        id="healer",
        name="The Healer",
        title="Wounded Healer",
        description="Your own pain has taught you compassion. You seek not to defeat the darkness, but to understand and integrate it.",
        icon="💚",
        starting_traits={"acceptance": 1, "hope": 1},
        special_ability="Memory rooms offer deeper healing",
        color="#10b981",
    ),
    "mystic": Archetype(
        id="mystic",
        name="The Mystic",
        title="Mystic Wanderer",
        description="You walk between worlds, comfortable with mystery. The labyrinth speaks to you in symbols and dreams.",
        icon="🌙",
        starting_traits={"introspection": 2},
        special_ability="Literary quotes resonate more deeply",
        color="#8b5cf6",
    ),
    "shadow": Archetype(
        id="shadow",
        name="The Shadow",
        title="Shadow Walker",
        description="You have already begun the work of integration. The darkness is not your enemy—it is your teacher.",
        icon="🌑",
        starting_traits={"acceptance": 2},
        special_ability="Shadow encounters are transformative",
        color="#1f2937",
    ),
}


def get_archetype(archetype_id: str) -> Archetype | None:
    """Get an archetype by ID."""
    return ARCHETYPES.get(archetype_id)


def get_all_archetypes() -> list[Archetype]:
    """Get all available archetypes."""
    return list(ARCHETYPES.values())
