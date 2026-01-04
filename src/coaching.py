"""Coaching and Guide system for Labyrinth of the Mind."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState


@dataclass
class CoachingInsight:
    """A coaching insight or observation."""
    title: str
    observation: str
    question: str
    action: str


# Guide messages based on room transitions and choices
GUIDE_OBSERVATIONS = {
    "shadow_accepted": CoachingInsight(
        title="Shadow Integration",
        observation="I notice you chose to acknowledge your shadow self. This takes courage—most people spend their lives running from the parts they find uncomfortable.",
        question="What would change in your daily life if you fully accepted this part of yourself?",
        action="This week, when you notice self-criticism arising, try saying 'I see you' instead of pushing it away."
    ),
    "shadow_rejected": CoachingInsight(
        title="A Pattern to Explore",
        observation="You chose to reject your shadow. This is a natural protective response—we all have parts we're not ready to face yet.",
        question="What might your shadow be trying to protect you from?",
        action="Consider journaling about what 'rejection' means to you. Sometimes our resistance points to our deepest growth edges."
    ),
    "light_accepted": CoachingInsight(
        title="Embracing Potential",
        observation="You declared yourself worthy of becoming your best self. This is often harder than facing darkness—believing in our own light requires trust.",
        question="What small step could you take tomorrow that aligns with this highest version of yourself?",
        action="Write a letter from your future self to your current self. What advice would they give?"
    ),
    "light_rejected": CoachingInsight(
        title="The Fear of Greatness",
        observation="You felt unable to claim your radiant potential. Many of us carry this fear—that our light might be 'too much' or that we'll fail to live up to it.",
        question="Whose voice told you that you couldn't become this? Is it still true?",
        action="List three moments when you surprised yourself with your own capability."
    ),
    "flowing_present": CoachingInsight(
        title="Presence Practice",
        observation="You chose to flow with time rather than fight it. This suggests a capacity for surrender and trust in the process.",
        question="Where in your life are you still gripping too tightly to outcomes?",
        action="Set three 'presence alarms' on your phone this week. When they ring, take three breaths and notice where you are."
    ),
    "creation_complete": CoachingInsight(
        title="The Maker's Spirit",
        observation="You picked up the hammer and created something. This reveals a core truth: you are fundamentally a creator, not just a consumer.",
        question="What project have you been postponing because it doesn't feel 'perfect' yet?",
        action="Commit to spending 15 minutes this week on something you create purely for yourself."
    ),
    "abandoned_dreams": CoachingInsight(
        title="Unfinished Business",
        observation="You looked at your abandoned dreams. Most people avoid this room entirely. Your willingness to face what you've left behind is significant.",
        question="Which abandoned dream still has energy when you think about it?",
        action="Choose one abandoned project. Give it just 10 minutes this week. See what happens."
    ),
    "inner_voice": CoachingInsight(
        title="The Still Small Voice",
        observation="You sat in silence and found your inner voice. In a world of constant noise, this is a rare and valuable skill.",
        question="What is your inner voice trying to tell you that you've been too busy to hear?",
        action="Create a daily 5-minute silence practice. Guard it like an important meeting."
    ),
    "gratitude_offered": CoachingInsight(
        title="The Gratitude Circuit",
        observation="You chose to offer gratitude rather than just receive it. This completes the circuit—gratitude flows when it moves in both directions.",
        question="Who in your life needs to hear your appreciation but hasn't?",
        action="Send one message of genuine thanks this week to someone who doesn't expect it."
    ),
    "current_life_reflection": CoachingInsight(
        title="Authoring Your Story",
        observation="You opened the book of your own life. This meta-awareness—seeing yourself as both author and character—is the foundation of intentional living.",
        question="If you were editing your life story, what chapter would you rewrite?",
        action="Write one paragraph describing your life as you want it to be in one year. Read it daily."
    ),
}

# Personality pattern interpretations (consulting-style)
PATTERN_INTERPRETATIONS = {
    "courage_wisdom": {
        "pattern": "The Thoughtful Warrior",
        "description": "You combine action with reflection. You don't rush in blindly, but you also don't get stuck in analysis paralysis.",
        "strength": "Making decisive moves backed by understanding.",
        "growth_edge": "Sometimes knowledge can become a barrier to action. Trust your instincts more.",
        "question": "Where might 'more research' be your way of avoiding a decision you already know the answer to?"
    },
    "courage_introspection": {
        "pattern": "The Conscious Adventurer",
        "description": "You face challenges while staying connected to your inner landscape. This is rare—most people either avoid or charge through.",
        "strength": "Learning from difficulty rather than just surviving it.",
        "growth_edge": "Don't let reflection become rumination. Sometimes the lesson is to move on.",
        "question": "What challenge are you ready to face now that you've been preparing for unknowingly?"
    },
    "wisdom_introspection": {
        "pattern": "The Inner Scholar",
        "description": "You seek deep understanding of yourself and the world. You're not satisfied with surface explanations.",
        "strength": "Rich inner life and genuine self-awareness.",
        "growth_edge": "Knowledge without action can become a comfortable prison. What are you not doing that you know you should?",
        "question": "How might you use your insights to help someone else today?"
    },
    "acceptance_hope": {
        "pattern": "The Grounded Optimist",
        "description": "You hold space for both what is and what could be. This integration of realism and vision is powerful.",
        "strength": "Inspiring others while staying authentic.",
        "growth_edge": "Ensure your hope is rooted in action, not just positive thinking.",
        "question": "What bridge are you building between your current reality and your vision?"
    },
    "acceptance_introspection": {
        "pattern": "The Shadow Alchemist",
        "description": "You transform difficulty into growth. Rather than avoiding the dark, you mine it for gold.",
        "strength": "Resilience that comes from integration, not denial.",
        "growth_edge": "Remember to also celebrate the light. Not everything needs to be transmuted.",
        "question": "What joy are you ready to receive without needing to earn it?"
    },
}

# End-of-game coaching report sections
def generate_coaching_summary(state: "GameState") -> dict:
    """Generate a comprehensive coaching summary based on the player's journey."""
    
    # Collect insights from visited rooms
    insights = []
    for room_id in state.visited_rooms:
        if room_id in GUIDE_OBSERVATIONS:
            insights.append(GUIDE_OBSERVATIONS[room_id])
    
    # Determine primary patterns
    traits = state.traits
    patterns = []
    
    if traits.get("courage", 0) >= 2 and traits.get("wisdom", 0) >= 2:
        patterns.append(PATTERN_INTERPRETATIONS["courage_wisdom"])
    if traits.get("courage", 0) >= 2 and traits.get("introspection", 0) >= 2:
        patterns.append(PATTERN_INTERPRETATIONS["courage_introspection"])
    if traits.get("wisdom", 0) >= 2 and traits.get("introspection", 0) >= 2:
        patterns.append(PATTERN_INTERPRETATIONS["wisdom_introspection"])
    if traits.get("acceptance", 0) >= 2 and traits.get("hope", 0) >= 2:
        patterns.append(PATTERN_INTERPRETATIONS["acceptance_hope"])
    if traits.get("acceptance", 0) >= 2 and traits.get("introspection", 0) >= 2:
        patterns.append(PATTERN_INTERPRETATIONS["acceptance_introspection"])
    
    # Generate action items based on journey
    action_items = []
    for insight in insights[:3]:  # Top 3 most relevant
        action_items.append({
            "title": insight.title,
            "action": insight.action,
            "question": insight.question
        })
    
    # Journey style analysis
    journey_style = analyze_journey_style(state)
    
    return {
        "insights": insights,
        "patterns": patterns,
        "action_items": action_items,
        "journey_style": journey_style,
        "summary_paragraphs": generate_summary_paragraphs(state, patterns, journey_style)
    }


def analyze_journey_style(state: "GameState") -> dict:
    """Analyze the player's journey style."""
    rooms_visited = len(state.visited_rooms)
    reflections = len(state.reflections)
    turns = state.turns
    
    # Exploration style
    if rooms_visited >= 20:
        exploration = "Thorough Explorer"
        exploration_desc = "You left no stone unturned. Your curiosity drives you to understand the complete picture before moving forward."
    elif rooms_visited >= 12:
        exploration = "Balanced Traveler"
        exploration_desc = "You explored meaningfully without getting lost. You know when to go deeper and when to move on."
    else:
        exploration = "Focused Navigator"
        exploration_desc = "You moved with purpose toward your goal. You trust your instincts about what's essential."
    
    # Reflection depth
    if reflections >= 5:
        reflection_style = "Deep Diver"
        reflection_desc = "You engaged fully with the reflective prompts. Writing helps you process and integrate experiences."
    elif reflections >= 2:
        reflection_style = "Thoughtful Responder"
        reflection_desc = "You paused to reflect when it mattered. You balance action with contemplation."
    else:
        reflection_style = "Action-Oriented"
        reflection_desc = "You prefer learning through doing rather than analyzing. Sometimes the journey itself is the teacher."
    
    # Pace
    if turns <= 10:
        pace = "Swift"
        pace_desc = "You trust your gut and move decisively."
    elif turns <= 20:
        pace = "Measured"
        pace_desc = "You take the time you need without rushing or stalling."
    else:
        pace = "Contemplative"
        pace_desc = "You allow experiences to unfold fully before moving forward."
    
    return {
        "exploration": {"style": exploration, "description": exploration_desc},
        "reflection": {"style": reflection_style, "description": reflection_desc},
        "pace": {"style": pace, "description": pace_desc}
    }


def generate_summary_paragraphs(state: "GameState", patterns: list, journey_style: dict) -> list[str]:
    """Generate personalized summary paragraphs."""
    paragraphs = []
    
    # Opening
    rooms = len(state.visited_rooms)
    paragraphs.append(
        f"In your journey through the labyrinth, you visited {rooms} rooms and made "
        f"{state.turns} choices. Each decision revealed something about how you navigate "
        "uncertainty, face difficulty, and relate to yourself."
    )
    
    # Pattern summary
    if patterns:
        pattern = patterns[0]  # Primary pattern
        paragraphs.append(
            f"**Your Primary Pattern: {pattern['pattern']}**\n\n{pattern['description']} "
            f"Your key strength is {pattern['strength'].lower()}. "
            f"A growth edge to consider: {pattern['growth_edge'].lower()}"
        )
    
    # Journey style
    style = journey_style
    paragraphs.append(
        f"**Your Journey Style**\n\n"
        f"• **Exploration:** {style['exploration']['style']} — {style['exploration']['description']}\n"
        f"• **Reflection:** {style['reflection']['style']} — {style['reflection']['description']}\n"
        f"• **Pace:** {style['pace']['style']} — {style['pace']['description']}"
    )
    
    # Keys analysis
    keys_found = sum(1 for k in ["shadow_key", "light_key", "truth_key"] if k in state.inventory)
    if keys_found == 3:
        paragraphs.append(
            "You collected all three keys—Shadow, Light, and Truth. This suggests a willingness "
            "to engage with the full spectrum of self-discovery: acknowledging what's hidden, "
            "embracing your potential, and accepting your authentic story."
        )
    elif "shadow_key" in state.inventory and "light_key" not in state.inventory:
        paragraphs.append(
            "You found the Shadow Key but not the Light Key. You're comfortable facing difficulty, "
            "but you may be more hesitant to claim your own brilliance. Consider: what would "
            "change if you believed in your potential as fully as you face your challenges?"
        )
    elif "light_key" in state.inventory and "shadow_key" not in state.inventory:
        paragraphs.append(
            "You found the Light Key but not the Shadow Key. You believe in your potential, "
            "but there may be parts of yourself you're not yet ready to acknowledge. "
            "Integration comes from embracing the whole self—light and shadow together."
        )
    
    # Closing
    paragraphs.append(
        "**A Question to Sit With**\n\n"
        "The labyrinth is a mirror. What did you see in yourself today that you want to carry forward? "
        "And what did you see that you're now ready to release?"
    )
    
    return paragraphs


def get_guide_message_for_room(room_id: str, state: "GameState") -> str | None:
    """Get a contextual guide message for a room transition."""
    
    # Special messages based on patterns
    messages = []
    
    if room_id == "hall_of_mirrors":
        if not state.visited_rooms or len(state.visited_rooms) <= 2:
            return "🧭 *The Guide whispers:* \"Every mirror here shows a truth. There are no wrong doors—only different paths to understanding.\""
    
    if room_id == "shadow_chamber":
        return "🧭 *The Guide observes:* \"What we resist persists. What we embrace transforms. This encounter offers both possibilities.\""
    
    if room_id == "light_chamber":
        return "🧭 *The Guide reflects:* \"Our deepest fear is not inadequacy—it's the responsibility that comes with recognizing our own power.\""
    
    if room_id == "garden_of_forking_paths":
        visit_count = sum(1 for c in state.choices_made if "garden" in c.lower())
        if visit_count >= 2:
            return "🧭 *The Guide notes:* \"You've returned here several times. Perhaps there's something in this garden still calling to you.\""
        return "🧭 *The Guide suggests:* \"There's no rush. Explore where curiosity leads. The door will wait.\""
    
    if room_id == "final_door":
        keys = sum(1 for k in ["shadow_key", "light_key", "truth_key"] if k in state.inventory)
        if keys < 3:
            return f"🧭 *The Guide pauses:* \"You have {keys} of 3 keys. The labyrinth still has gifts to offer, if you wish to explore further.\""
        return "🧭 *The Guide smiles:* \"You carry all three keys. You've done the inner work. The door recognizes you.\""
    
    return None


# Room image mappings
ROOM_IMAGES = {
    "entrance": "assets/room_entrance.png",
    "hidden_inscription": "assets/room_entrance.png",
    "hall_of_mirrors": "assets/room_mirrors.png",
    "shadow_chamber": "assets/room_shadow.png",
    "shadow_accepted": "assets/room_shadow.png",
    "shadow_rejected": "assets/room_shadow.png",
    "light_chamber": "assets/room_light.png",
    "light_accepted": "assets/room_light.png",
    "light_rejected": "assets/room_light.png",
    "garden_of_forking_paths": "assets/room_garden.png",
    "library_of_lives": "assets/room_library.png",
    "current_life_reflection": "assets/room_library.png",
    "unchosen_lives": "assets/room_library.png",
    "well_of_memory": "assets/room_well.png",
    "happy_memory": "assets/room_well.png",
    "painful_memory": "assets/room_well.png",
    "river_of_time": "assets/room_garden.png",
    "flowing_present": "assets/room_garden.png",
    "observer_of_time": "assets/room_garden.png",
    "forge_of_creation": "assets/room_shadow.png",
    "creation_complete": "assets/room_light.png",
    "abandoned_dreams": "assets/room_library.png",
    "temple_of_silence": "assets/room_entrance.png",
    "inner_voice": "assets/room_light.png",
    "echoing_words": "assets/room_mirrors.png",
    "chamber_of_gratitude": "assets/room_light.png",
    "gratitude_offered": "assets/room_light.png",
    "gratitude_received": "assets/room_light.png",
    "final_door": "assets/room_entrance.png",
    "door_remains_closed": "assets/room_entrance.png",
    "the_exit": "assets/room_exit.png",
}


def get_room_image(room_id: str) -> str | None:
    """Get the image path for a room."""
    return ROOM_IMAGES.get(room_id)
