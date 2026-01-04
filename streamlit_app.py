"""Premium Streamlit web interface for Labyrinth of the Mind - Full Featured Edition."""

import json
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
from src.models import GameState, RoomType
from src.rooms import create_labyrinth
from src.achievements import check_achievements, get_all_achievements, Achievement
from src.archetypes import get_archetype, get_all_archetypes, Archetype
from src.profile import load_profile, save_profile, PlayerProfile
from src.map_viz import generate_map_svg
from src.coaching import (
    generate_coaching_summary,
    get_guide_message_for_room,
    get_room_image,
    GUIDE_OBSERVATIONS,
)

# === CONSTANTS ===
SAVE_DIR = Path.home() / ".labyrinth_of_the_mind"
SAVE_FILE = SAVE_DIR / "savegame.json"

# Trait keywords for personality analysis
TRAIT_KEYWORDS = {
    "courage": ["acknowledge", "accept", "face", "confront", "worthy"],
    "wisdom": ["examine", "read", "knowledge", "wisdom", "understand"],
    "introspection": ["reflect", "memory", "past", "within"],
    "avoidance": ["reject", "flee", "ignore", "skip", "never"],
    "hope": ["light", "radiant", "best", "aspire", "become"],
    "acceptance": ["shadow", "darkness", "acknowledge", "part of me"],
}

# Room themes
ROOM_THEMES = {
    RoomType.ENTRANCE: {"accent": "#e94560", "emoji": "🚪"},
    RoomType.REFLECTION: {"accent": "#c9b1ff", "emoji": "🪞"},
    RoomType.CHALLENGE: {"accent": "#ffd700", "emoji": "⚔️"},
    RoomType.REVELATION: {"accent": "#00ff88", "emoji": "✨"},
    RoomType.EXIT: {"accent": "#ffffff", "emoji": "🌅"},
}

# Personality insights
PERSONALITY_INSIGHTS = {
    "courage": {"high": "You face challenges head-on, embracing discomfort as a path to growth.", "low": "You prefer safer paths, valuing security."},
    "wisdom": {"high": "You seek understanding before action, valuing knowledge.", "low": "You trust instincts over analysis."},
    "introspection": {"high": "You dive deep into self-examination.", "low": "You prefer forward motion."},
    "hope": {"high": "You believe in your potential and positive change.", "low": "You maintain realistic expectations."},
    "acceptance": {"high": "You embrace all aspects of yourself.", "low": "You strive for ideals."},
}

# Multiple endings
ENDINGS = {
    "complete_enlightenment": {
        "id": "complete_enlightenment",
        "condition": lambda s: len(s.reflections) >= 4 and s.traits.get("acceptance", 0) >= 2,
        "title": "The Enlightened One",
        "description": "You walked the full path of self-discovery, embracing shadow and light alike.",
        "color": "#ffd700",
    },
    "shadow_master": {
        "id": "shadow_master",
        "condition": lambda s: s.traits.get("acceptance", 0) >= 2 and s.traits.get("introspection", 0) >= 2,
        "title": "Shadow Walker",
        "description": "You made peace with the darkness within. Your shadow is now your ally.",
        "color": "#8b5cf6",
    },
    "light_seeker": {
        "id": "light_seeker",
        "condition": lambda s: s.traits.get("hope", 0) >= 2 and s.traits.get("courage", 0) >= 2,
        "title": "Light Seeker",
        "description": "You reached toward your highest potential with unwavering faith.",
        "color": "#f59e0b",
    },
    "swift_passage": {
        "id": "swift_passage",
        "condition": lambda s: s.turns <= 8,
        "title": "The Swift Traveler",
        "description": "You moved through with purpose. The direct path has its own wisdom.",
        "color": "#10b981",
    },
    "wanderer": {
        "id": "wanderer",
        "condition": lambda s: len(s.visited_rooms) >= 12,
        "title": "The Wanderer",
        "description": "You explored every corner, discovering secrets others missed.",
        "color": "#3b82f6",
    },
    "default": {
        "id": "default",
        "condition": lambda s: True,
        "title": "The Journeyer",
        "description": "You completed the labyrinth in your own unique way.",
        "color": "#6b7280",
    },
}


# === HELPER FUNCTIONS ===

def get_css(profile: PlayerProfile) -> str:
    """Generate CSS based on accessibility settings."""
    font_size = "1.1rem" if profile.large_text_mode else "1rem"
    contrast_bg = "#000000" if profile.high_contrast_mode else "rgba(30, 30, 40, 0.6)"
    contrast_text = "#ffffff" if profile.high_contrast_mode else "inherit"
    contrast_border = "#ffffff" if profile.high_contrast_mode else "rgba(255, 255, 255, 0.1)"

    return f"""
    <style>
        .main-content {{ font-size: {font_size}; }}
        .room-card {{
            background: {contrast_bg};
            border: 1px solid {contrast_border};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: {contrast_text};
        }}
        .literary-quote {{
            font-style: italic;
            color: #a0a0a0;
            border-left: 3px solid #667eea;
            padding: 1rem;
            margin: 1.5rem 0;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 0 10px 10px 0;
        }}
        .quote-source {{ font-size: 0.9rem; color: #888; margin-top: 0.5rem; }}
        .key-container {{ display: flex; justify-content: center; gap: 15px; margin: 1rem 0; }}
        .key-indicator {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 55px; height: 55px; border-radius: 50%; font-size: 1.5rem;
        }}
        .key-obtained {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
            animation: pulse 2s infinite;
        }}
        .key-missing {{ background: rgba(50, 50, 60, 0.5); opacity: 0.3; }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }}
            50% {{ transform: scale(1.08); box-shadow: 0 0 25px rgba(102, 126, 234, 0.8); }}
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(15px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-in {{ animation: fadeIn 0.4s ease-out; }}
        .achievement-badge {{
            display: inline-flex; align-items: center; gap: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 0.5rem 1rem; border-radius: 20px;
            margin: 0.3rem; font-size: 0.9rem;
        }}
        .achievement-locked {{
            background: rgba(50, 50, 60, 0.5); color: #666;
        }}
        .archetype-card {{
            background: rgba(40, 40, 50, 0.8); border-radius: 15px;
            padding: 1.5rem; margin: 0.5rem 0; cursor: pointer;
            border: 2px solid transparent; transition: all 0.3s ease;
        }}
        .archetype-card:hover {{ border-color: #667eea; transform: translateY(-2px); }}
        .archetype-selected {{ border-color: #667eea; background: rgba(102, 126, 234, 0.2); }}
        .timer-display {{
            font-size: 2rem; font-weight: bold; text-align: center;
            color: #ffd700; margin: 1rem 0;
        }}
        .timer-warning {{ color: #ef4444; animation: pulse 0.5s infinite; }}
        .insight-card {{
            background: rgba(102, 126, 234, 0.1); border-radius: 10px;
            padding: 1rem; margin: 0.5rem 0;
        }}
        .new-unlock {{
            background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
            color: #000; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
            animation: fadeIn 0.5s ease-out;
        }}
    </style>
    """


def init_game(archetype_id: str | None = None) -> None:
    """Initialize or reset the game state."""
    st.session_state.rooms = create_labyrinth()
    st.session_state.state = GameState()
    st.session_state.state.visit_room("entrance")
    st.session_state.pending_reflection = None
    st.session_state.message = None
    st.session_state.new_achievements = []
    st.session_state.game_phase = "playing"

    # Apply archetype bonuses
    if archetype_id:
        archetype = get_archetype(archetype_id)
        if archetype:
            st.session_state.archetype = archetype
            for trait, points in archetype.starting_traits.items():
                st.session_state.state.add_trait(trait, points)
    else:
        st.session_state.archetype = None

    # Timer mode
    if st.session_state.get("timed_mode"):
        st.session_state.start_time = time.time()
        st.session_state.time_limit = 300  # 5 minutes
    else:
        st.session_state.start_time = None


def analyze_choice_traits(choice_text: str, room_id: str) -> dict[str, int]:
    """Analyze a choice for personality traits."""
    traits = {}
    combined = f"{choice_text.lower()} {room_id.lower()}"
    for trait, keywords in TRAIT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined:
                traits[trait] = traits.get(trait, 0) + 1
    return traits


def get_ending(state: GameState) -> dict:
    """Determine the player's ending."""
    for ending_id, ending in ENDINGS.items():
        if ending_id != "default" and ending["condition"](state):
            return ending
    return ENDINGS["default"]


def get_personality_summary(state: GameState) -> list[dict]:
    """Generate personality insights."""
    insights = []
    for trait, points in sorted(state.traits.items(), key=lambda x: -x[1]):
        if points >= 1 and trait in PERSONALITY_INSIGHTS:
            level = "high" if points >= 2 else "low"
            insights.append({"trait": trait.title(), "insight": PERSONALITY_INSIGHTS[trait][level], "points": points})
    return insights[:4]


def save_game() -> bool:
    """Save game state."""
    try:
        SAVE_DIR.mkdir(exist_ok=True)
        state = st.session_state.state
        save_data = {
            "current_room_id": state.current_room_id,
            "inventory": list(state.inventory),
            "visited_rooms": list(state.visited_rooms),
            "reflections": state.reflections,
            "choices_made": state.choices_made,
            "traits": state.traits,
            "turns": state.turns,
            "archetype_id": st.session_state.archetype.id if st.session_state.get("archetype") else None,
            "saved_at": datetime.now().isoformat(),
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception:
        return False


def load_game() -> bool:
    """Load saved game."""
    try:
        if not SAVE_FILE.exists():
            return False
        with open(SAVE_FILE) as f:
            data = json.load(f)
        st.session_state.rooms = create_labyrinth()
        state = GameState()
        state.current_room_id = data["current_room_id"]
        state.inventory = set(data["inventory"])
        state.visited_rooms = set(data["visited_rooms"])
        state.reflections = data["reflections"]
        state.choices_made = data.get("choices_made", [])
        state.traits = data.get("traits", {})
        state.turns = data["turns"]
        st.session_state.state = state
        st.session_state.pending_reflection = None
        st.session_state.game_phase = "playing"
        if data.get("archetype_id"):
            st.session_state.archetype = get_archetype(data["archetype_id"])
        st.session_state.message = f"Game loaded!"
        return True
    except Exception:
        return False


def export_journal() -> str:
    """Export reflections as markdown."""
    state = st.session_state.state
    lines = [
        "# Labyrinth of the Mind - Personal Journal",
        f"\n*{datetime.now().strftime('%B %d, %Y')}*\n",
        "---\n## Your Reflections\n",
    ]
    if state.reflections:
        for i, (prompt, response) in enumerate(state.reflections.items(), 1):
            lines.extend([f"### {i}. {prompt}", f"{response}\n"])
    else:
        lines.append("*No reflections recorded.*\n")

    insights = get_personality_summary(state)
    if insights:
        lines.append("---\n## Personality Insights\n")
        for ins in insights:
            lines.append(f"**{ins['trait']}:** {ins['insight']}\n")

    if state.has_won:
        ending = get_ending(state)
        lines.append(f"---\n## Your Ending: {ending['title']}\n{ending['description']}")

    lines.append(f"\n---\n*Steps: {state.turns} | Rooms: {len(state.visited_rooms)}*")
    return "\n".join(lines)


def enter_room(room_id: str) -> None:
    """Enter a room."""
    rooms = st.session_state.rooms
    state = st.session_state.state
    profile = st.session_state.profile

    room = rooms[room_id]
    state.current_room_id = room_id

    if room.on_enter_item and not state.has_visited(room_id):
        state.add_item(room.on_enter_item)
        st.session_state.message = f"✨ {room.on_enter_text}"

    state.visit_room(room_id)
    state.turns += 1

    # Check achievements
    new_achievements = check_achievements(state, set(profile.unlocked_achievements))
    for ach in new_achievements:
        profile.unlock_achievement(ach.id)
        st.session_state.new_achievements.append(ach)
    save_profile(profile)


def make_choice(choice_idx: int) -> None:
    """Process player choice."""
    rooms = st.session_state.rooms
    state = st.session_state.state
    current_room = rooms[state.current_room_id]

    available = [c for c in current_room.choices if c.is_available(state)]
    choice = available[choice_idx]

    state.record_choice(current_room.id, choice.text)
    traits = analyze_choice_traits(choice.text, current_room.id)
    for trait, points in traits.items():
        state.add_trait(trait, points)

    if choice.reflection_prompt:
        st.session_state.pending_reflection = {"prompt": choice.reflection_prompt, "next_room": choice.next_room_id}
    else:
        enter_room(choice.next_room_id)


def submit_reflection(response: str) -> None:
    """Submit reflection."""
    pending = st.session_state.pending_reflection
    if response.strip():
        st.session_state.state.add_reflection(pending["prompt"], response.strip())
        st.session_state.state.add_trait("introspection", 1)
    enter_room(pending["next_room"])
    st.session_state.pending_reflection = None


def generate_share_card(state: GameState, ending: dict, archetype: Archetype | None) -> str:
    """Generate shareable SVG result card."""
    archetype_text = f"as {archetype.name}" if archetype else ""
    return f'''<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#1a1a2e"/><stop offset="100%" style="stop-color:#16213e"/>
        </linearGradient></defs>
        <rect width="400" height="250" fill="url(#bg)" rx="15"/>
        <text x="200" y="40" text-anchor="middle" fill="#667eea" font-size="18" font-family="sans-serif">🌀 Labyrinth of the Mind</text>
        <text x="200" y="90" text-anchor="middle" fill="{ending['color']}" font-size="24" font-family="sans-serif" font-weight="bold">{ending['title']}</text>
        <text x="200" y="120" text-anchor="middle" fill="#888" font-size="12" font-family="sans-serif">{archetype_text}</text>
        <text x="200" y="160" text-anchor="middle" fill="#fff" font-size="14" font-family="sans-serif">🚶 {state.turns} steps | 🗺️ {len(state.visited_rooms)} rooms | 📝 {len(state.reflections)} reflections</text>
        <text x="200" y="200" text-anchor="middle" fill="#667eea" font-size="11" font-family="sans-serif">🗝️ Shadow {"✓" if "shadow_key" in state.inventory else "○"} | ✨ Light {"✓" if "light_key" in state.inventory else "○"} | 🔑 Truth {"✓" if "truth_key" in state.inventory else "○"}</text>
        <text x="200" y="235" text-anchor="middle" fill="#444" font-size="10" font-family="sans-serif">labyrinth-of-the-mind</text>
    </svg>'''


# === PAGE CONFIG ===
st.set_page_config(page_title="Labyrinth of the Mind", page_icon="🌀", layout="centered", initial_sidebar_state="expanded")

# Initialize profile
if "profile" not in st.session_state:
    st.session_state.profile = load_profile()

profile = st.session_state.profile
st.markdown(get_css(profile), unsafe_allow_html=True)

# === GAME PHASES ===

# Character Selection Phase
if st.session_state.get("game_phase") == "character_select":
    st.markdown("# 🌀 Choose Your Path")
    st.markdown("*Select an archetype to begin your journey*")

    archetypes = get_all_archetypes()
    unlocked = set(profile.unlocked_archetypes)

    cols = st.columns(2)
    for i, arch in enumerate(archetypes):
        with cols[i % 2]:
            is_unlocked = arch.id in unlocked
            if is_unlocked:
                selected = st.session_state.get("selected_archetype") == arch.id
                card_class = "archetype-card archetype-selected" if selected else "archetype-card"
                st.markdown(f"""
                <div class="{card_class}">
                    <h3>{arch.icon} {arch.name}</h3>
                    <p style="color:#888;font-size:0.9rem;">{arch.description}</p>
                    <p style="color:#667eea;font-size:0.85rem;">✦ {arch.special_ability}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Choose {arch.name}", key=f"arch_{arch.id}", use_container_width=True):
                    st.session_state.selected_archetype = arch.id
            else:
                st.markdown(f"""
                <div class="archetype-card" style="opacity:0.5;">
                    <h3>🔒 {arch.name}</h3>
                    <p style="color:#666;">Complete more journeys to unlock</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    timed = st.checkbox("⏱️ Timed Challenge Mode (5 minutes)", value=False)
    st.session_state.timed_mode = timed

    if st.button("🚀 Begin Journey", type="primary", use_container_width=True):
        init_game(st.session_state.get("selected_archetype"))
        st.session_state.game_phase = "playing"
        st.rerun()

    if st.button("← Back to Menu"):
        st.session_state.game_phase = None
        st.rerun()

# Main Menu Phase
elif st.session_state.get("game_phase") is None or st.session_state.get("game_phase") == "menu":
    st.markdown("# 🌀 Labyrinth of the Mind")
    st.markdown("*An interactive journey of self-reflection*")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 New Journey", use_container_width=True, type="primary"):
            st.session_state.game_phase = "character_select"
            st.rerun()
    with col2:
        if SAVE_FILE.exists():
            if st.button("📂 Continue", use_container_width=True):
                if load_game():
                    st.session_state.game_phase = "playing"
                    st.rerun()

    st.markdown("---")

    # Profile Stats
    st.markdown("### 📊 Your Journey")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completions", profile.total_completions)
    with col2:
        st.metric("Best Time", f"{profile.fastest_completion or '—'} steps")
    with col3:
        st.metric("Achievements", f"{len(profile.unlocked_achievements)}/{len(get_all_achievements())}")

    # Achievements
    with st.expander("🏆 Achievements"):
        for ach in get_all_achievements():
            unlocked = ach.id in profile.unlocked_achievements
            if unlocked or not ach.secret:
                badge_class = "achievement-badge" if unlocked else "achievement-badge achievement-locked"
                name = ach.name if unlocked or not ach.secret else "???"
                desc = ach.description if unlocked else ("???" if ach.secret else ach.description)
                st.markdown(f'<span class="{badge_class}">{ach.icon} {name}</span> {desc}', unsafe_allow_html=True)

    # Settings
    with st.expander("⚙️ Accessibility"):
        hc = st.checkbox("High Contrast Mode", value=profile.high_contrast_mode)
        lt = st.checkbox("Large Text", value=profile.large_text_mode)
        if hc != profile.high_contrast_mode or lt != profile.large_text_mode:
            profile.high_contrast_mode = hc
            profile.large_text_mode = lt
            save_profile(profile)
            st.rerun()

# Playing Phase
elif st.session_state.get("game_phase") == "playing":
    if "state" not in st.session_state:
        init_game()

    rooms = st.session_state.rooms
    state = st.session_state.state
    current_room = rooms[state.current_room_id]
    theme = ROOM_THEMES[current_room.room_type]
    archetype = st.session_state.get("archetype")

    # Timer check
    if st.session_state.get("start_time"):
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.time_limit - elapsed
        if remaining <= 0 and not state.has_won:
            st.session_state.game_phase = "timeout"
            st.rerun()

    # Show new achievements
    if st.session_state.get("new_achievements"):
        for ach in st.session_state.new_achievements:
            st.markdown(f'<div class="new-unlock">🏆 Achievement Unlocked: {ach.icon} {ach.name}</div>', unsafe_allow_html=True)
        st.session_state.new_achievements = []

    # Sidebar
    with st.sidebar:
        st.markdown("## 🌀 Labyrinth")
        if archetype:
            st.caption(f"{archetype.icon} {archetype.title}")

        # Timer
        if st.session_state.get("start_time"):
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, st.session_state.time_limit - elapsed)
            mins, secs = divmod(int(remaining), 60)
            timer_class = "timer-display timer-warning" if remaining < 60 else "timer-display"
            st.markdown(f'<div class="{timer_class}">⏱️ {mins}:{secs:02d}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Keys
        st.markdown("### 🗝️ Keys")
        keys_html = '<div class="key-container">'
        for key_id, emoji in [("shadow_key", "🗝️"), ("light_key", "✨"), ("truth_key", "🔑")]:
            css = "key-obtained" if key_id in state.inventory else "key-missing"
            keys_html += f'<div class="key-indicator {css}">{emoji}</div>'
        keys_html += '</div>'
        st.markdown(keys_html, unsafe_allow_html=True)
        st.progress(sum(1 for k in ["shadow_key", "light_key", "truth_key"] if k in state.inventory) / 3)

        st.markdown("---")

        # Map
        with st.expander("🗺️ Map"):
            map_svg = generate_map_svg(state.visited_rooms, state.current_room_id)
            st.markdown(map_svg, unsafe_allow_html=True)

        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Steps", state.turns)
        with col2:
            st.metric("Rooms", len(state.visited_rooms))

        st.markdown("---")

        # Save/Load
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                if save_game():
                    st.toast("Saved!")
        with col2:
            if st.button("🏠 Menu", use_container_width=True):
                st.session_state.game_phase = "menu"
                st.rerun()

    # Victory
    if current_room.room_type == RoomType.EXIT:
        state.has_won = True
        ending = get_ending(state)

        # Record completion
        unlocks = profile.record_completion(state.turns, len(state.reflections), len(state.visited_rooms), ending["id"])
        new_achs = check_achievements(state, set(profile.unlocked_achievements))
        for ach in new_achs:
            profile.unlock_achievement(ach.id)
        save_profile(profile)

        st.balloons()
        st.markdown(f'<h1 style="text-align:center;color:{ending["color"]};">🌟 {ending["title"]} 🌟</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="room-card animate-in">{current_room.description}</div>', unsafe_allow_html=True)

        if current_room.literary_quote:
            st.markdown(f'<div class="literary-quote">"{current_room.literary_quote}"<div class="quote-source">— {current_room.literary_source}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.info(ending["description"])
        st.success(f"**{state.turns}** steps | **{len(state.visited_rooms)}** rooms | **{len(state.reflections)}** reflections")

        # Unlocks
        if any([unlocks["new_best_time"], unlocks["new_archetypes"], new_achs]):
            st.markdown("### 🎉 New Unlocks!")
            if unlocks["new_best_time"]:
                st.markdown('<div class="new-unlock">⚡ New Best Time!</div>', unsafe_allow_html=True)
            for arch_id in unlocks["new_archetypes"]:
                arch = get_archetype(arch_id)
                st.markdown(f'<div class="new-unlock">{arch.icon} Unlocked: {arch.name}</div>', unsafe_allow_html=True)
            for ach in new_achs:
                st.markdown(f'<div class="new-unlock">🏆 {ach.icon} {ach.name}</div>', unsafe_allow_html=True)
        # === COACHING REPORT ===
        st.markdown("---")
        st.markdown("## 🧭 Your Personal Coaching Report")
        
        # Generate comprehensive coaching summary
        coaching = generate_coaching_summary(state)
        
        # Summary paragraphs
        for para in coaching["summary_paragraphs"]:
            st.markdown(para)
            st.markdown("")
        
        # Action Items
        if coaching["action_items"]:
            st.markdown("### 📋 Your Action Items")
            st.markdown("*Based on the choices you made, here are some practices to consider:*")
            for item in coaching["action_items"]:
                with st.expander(f"🎯 {item['title']}"):
                    st.markdown(f"**Action:** {item['action']}")
                    st.markdown(f"**Question to explore:** *{item['question']}*")
        
        # Reflections
        if state.reflections:
            with st.expander("📝 Your Reflections"):
                for prompt, response in state.reflections.items():
                    st.markdown(f"**{prompt}**\n\n{response}\n\n---")

        st.markdown("---")

        # Share card
        with st.expander("📤 Share Your Journey"):
            card_svg = generate_share_card(state, ending, archetype)
            st.markdown(card_svg, unsafe_allow_html=True)
            st.download_button("Download Card", card_svg, "labyrinth_result.svg", "image/svg+xml")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Journal", export_journal(), "journal.md", "text/markdown", use_container_width=True)
        with col2:
            if st.button("🔄 New Journey", type="primary", use_container_width=True):
                st.session_state.game_phase = "character_select"
                st.rerun()

    # Reflection
    elif st.session_state.get("pending_reflection"):
        pending = st.session_state.pending_reflection
        st.markdown('<div class="room-card animate-in"><h3>💭 Moment of Reflection</h3></div>', unsafe_allow_html=True)
        st.markdown(f"### *{pending['prompt']}*")

        response = st.text_area("Your reflection:", height=120, placeholder="Take a moment...", label_visibility="collapsed")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Continue", type="primary", use_container_width=True):
                submit_reflection(response)
                st.rerun()
        with col2:
            if st.button("Skip →", use_container_width=True):
                submit_reflection("")
                st.rerun()

    # Normal gameplay
    else:
        if st.session_state.get("message"):
            st.success(st.session_state.message)
            st.session_state.message = None

        st.markdown(f"# {theme['emoji']} Labyrinth of the Mind")
        
        # Display room image if available
        room_image = get_room_image(state.current_room_id)
        if room_image:
            try:
                st.image(room_image, use_container_width=True)
            except Exception:
                pass  # Image not found, continue without it
        
        st.markdown(f'<div class="room-card animate-in"><h2>{theme["emoji"]} {current_room.name}</h2><p>{current_room.description}</p></div>', unsafe_allow_html=True)

        if current_room.literary_quote:
            st.markdown(f'<div class="literary-quote">"{current_room.literary_quote}"<div class="quote-source">— {current_room.literary_source}</div></div>', unsafe_allow_html=True)

        # Display Guide message if available
        guide_msg = get_guide_message_for_room(state.current_room_id, state)
        if guide_msg:
            st.markdown(f'<div style="background: rgba(102, 126, 234, 0.15); border-left: 3px solid #667eea; padding: 1rem; margin: 1rem 0; border-radius: 0 10px 10px 0; font-style: italic;">{guide_msg}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### What do you do?")

        for idx, choice in enumerate([c for c in current_room.choices if c.is_available(state)]):
            if st.button(f"→ {choice.text}", key=f"choice_{idx}", use_container_width=True):
                make_choice(idx)
                st.rerun()

# Timeout Phase
elif st.session_state.get("game_phase") == "timeout":
    st.markdown("# ⏱️ Time's Up!")
    st.markdown("The mists of the labyrinth have enveloped you...")
    st.markdown("*Perhaps with more time, you could have found your way.*")

    if st.button("🔄 Try Again", type="primary", use_container_width=True):
        st.session_state.game_phase = "character_select"
        st.rerun()
