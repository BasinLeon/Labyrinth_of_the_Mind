# 🌀 Labyrinth of the Mind

An interactive text-based adventure game of self-reflection and discovery, inspired by classic literature.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎮 Play Now

**[▶️ Play Online](https://labyrinth-of-the-mind.streamlit.app)** *(coming soon)*

Or run locally:
```bash
pip install streamlit
streamlit run app.py
```

## 📖 About

Navigate through a metaphorical labyrinth representing the journey inward. Each room presents choices that reveal aspects of your personality, accompanied by quotes from literary masters like Rilke, Borges, Jung, and Rumi.

**Your goal:** Collect three keys — Shadow, Light, and Truth — to unlock the final door and complete your journey.

## ✨ Features

### Core Experience
- 🏰 **20+ Interconnected Rooms** — Each with unique themes and literary quotes
- 💭 **Reflection Prompts** — Journaling moments that become part of your story
- 🗝️ **Three Keys to Collect** — Shadow (acceptance), Light (hope), Truth (authenticity)
- 📜 **6 Unique Endings** — Based on your choices and playstyle

### Progression System
- 🎭 **5 Character Archetypes** — Seeker, Warrior, Healer, Mystic, Shadow
- 🏆 **18 Achievements** — Including 3 secret ones to discover
- 📊 **Personality Insights** — Analysis of your choices reveals traits
- 🔓 **New Game+** — Unlock new archetypes by completing journeys

### Features
- 🗺️ **Visual Map** — Watch your path unfold as you explore
- ⏱️ **Timed Challenge Mode** — Complete the labyrinth in 5 minutes
- 📥 **Journal Export** — Download your reflections as markdown
- 📤 **Shareable Results** — Generate a card showing your ending
- ♿ **Accessibility** — High contrast and large text modes
- 💾 **Save/Load** — Continue your journey anytime

## 🎯 How to Play

1. **Choose an Archetype** — Each affects your starting personality traits
2. **Navigate the Labyrinth** — Read room descriptions and choose your path
3. **Reflect** — When prompted, take a moment to answer honestly (or skip)
4. **Collect Keys** — Make meaningful choices to earn the three keys
5. **Reach the Exit** — Your ending depends on your journey

## 🏗️ Project Structure

```
├── app.py                 # Streamlit web interface
├── main.py                # CLI version
├── src/
│   ├── models.py          # Core data structures
│   ├── rooms.py           # Room definitions & content
│   ├── engine.py          # CLI game engine
│   ├── achievements.py    # Achievement system
│   ├── archetypes.py      # Character classes
│   ├── profile.py         # Persistent player data
│   └── map_viz.py         # SVG map generation
└── tests/                 # Unit tests
```

## 🛠️ Development

```bash
# Install dependencies
pip install streamlit pytest ruff mypy

# Run tests
python -m pytest tests/ -v

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## 📚 Literary Inspirations

The game features quotes from:
- **Rainer Maria Rilke** — On the inner journey
- **Jorge Luis Borges** — The Garden of Forking Paths, The Library of Babel
- **Carl Jung** — Shadow work and integration
- **Rumi** — Transformation through darkness
- **T.S. Eliot** — Returning to know the place for the first time
- And many more...

## 🤝 Contributing

Contributions welcome! Ideas for expansion:
- New rooms and story branches
- Additional archetypes
- More achievements
- Translations/localization
- Audio/visual enhancements

## 📄 License

MIT License — feel free to use, modify, and share.

---

*"The only journey is the one within." — Rainer Maria Rilke*
