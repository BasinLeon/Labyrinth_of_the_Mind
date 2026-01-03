# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Labyrinth of the Mind is an interactive text-based adventure game built in Python with a Streamlit web interface. Players navigate through a metaphorical labyrinth representing self-reflection, encountering rooms inspired by classic literature. The goal is to collect three keys (Shadow, Light, and Truth) by making meaningful choices and engaging with reflection prompts.

## Commands

### Run the web app (Streamlit)
```bash
streamlit run app.py
```

### Run the CLI version
```bash
python main.py
```

### Run tests
```bash
python -m pytest tests/ -v
```

### Run a single test file
```bash
python -m pytest tests/test_models.py -v
```

### Run a specific test
```bash
python -m pytest tests/test_models.py::TestGameState::test_add_item -v
```

### Lint (requires ruff)
```bash
ruff check src/ tests/
```

### Type check (requires mypy)
```bash
mypy src/
```

## Architecture

### Core Components

**`src/models.py`** - Data structures
- `GameState`: Tracks current room, inventory, visited rooms, reflections, choices made, and personality traits
- `Room`: Represents a location with description, literary quote, room type, and available choices
- `Choice`: Player action with optional item requirements, conditions, and reflection prompts
- `RoomType`: Enum categorizing rooms (ENTRANCE, REFLECTION, CHALLENGE, REVELATION, EXIT)

**`src/rooms.py`** - Content
- `create_labyrinth()`: Factory function returning all room definitions as a dict keyed by room ID
- Contains ~20 interconnected rooms with literary themes

**`src/engine.py`** - CLI game loop
- `GameEngine`: Manages I/O, room display, player input, and state transitions
- Supports dependency injection of input/output streams for testing

**`src/achievements.py`** - Achievement system
- `Achievement`: Dataclass with id, name, description, icon, and condition function
- `check_achievements()`: Returns newly unlocked achievements given current state
- 18 achievements including secret ones

**`src/archetypes.py`** - Character classes
- `Archetype`: Dataclass with starting traits and special abilities
- 5 archetypes: Seeker, Warrior, Healer, Mystic, Shadow (unlock progressively)

**`src/profile.py`** - Persistent player data
- `PlayerProfile`: Tracks completions, achievements, unlocks, best runs, and preferences
- Saves to `~/.labyrinth_of_the_mind/profile.json`

**`src/map_viz.py`** - Map visualization
- `generate_map_svg()`: Creates SVG visualization of explored rooms

**`app.py`** - Streamlit web interface
- Main menu, character selection, gameplay, victory screens
- Features: save/load, timed mode, accessibility options, shareable result cards

### Game Flow

1. Player chooses archetype (affects starting traits)
2. Navigate rooms, make choices that affect personality traits
3. Reflection prompts store player responses and boost introspection trait
4. Collect three keys to unlock the final door
5. Ending determined by traits, reflections, and playstyle
6. Achievements unlock, profile updated, new archetypes may unlock

### Key Design Patterns

- **Room graph**: Rooms form a directed graph via `Choice.next_room_id`
- **Trait analysis**: Choices analyzed for keywords to build personality profile
- **Progressive unlocks**: Archetypes unlock after N completions
- **Multiple endings**: 6 endings based on player behavior
- **Persistent profile**: Cross-session progress via JSON file

## Adding New Content

### New Rooms
1. Add room definition in `src/rooms.py` within `create_labyrinth()`
2. Add position in `src/map_viz.py` `ROOM_POSITIONS` dict
3. Run connectivity test: `python -m pytest tests/test_rooms.py::TestLabyrinthStructure::test_all_choices_lead_to_valid_rooms`

### New Achievements
1. Add `Achievement` to `ACHIEVEMENTS` list in `src/achievements.py`
2. Use `secret=True` for hidden achievements

### New Archetypes
1. Add to `ARCHETYPES` dict in `src/archetypes.py`
2. Update unlock conditions in `src/profile.py` `record_completion()`
