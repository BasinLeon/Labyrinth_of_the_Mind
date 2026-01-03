"""Room definitions for the Labyrinth of the Mind."""

from .models import Choice, Room, RoomType, GameState


def create_labyrinth() -> dict[str, Room]:
    """Create and return all rooms in the labyrinth."""
    rooms = {}

    # === ENTRANCE ===
    rooms["entrance"] = Room(
        id="entrance",
        name="The Threshold",
        description=(
            "You stand before an ancient archway carved from obsidian stone. "
            "Ivy creeps along its edges, and beyond lies a swirling mist that "
            "seems to whisper forgotten memories. A weathered sign reads: "
            "'Enter, traveler, and discover what lies within.'"
        ),
        room_type=RoomType.ENTRANCE,
        literary_quote="The only journey is the one within.",
        literary_source="Rainer Maria Rilke",
        choices=[
            Choice(
                text="Step through the archway into the mist",
                next_room_id="hall_of_mirrors",
                reflection_prompt="What do you hope to find within yourself?"
            ),
            Choice(
                text="Examine the archway more closely",
                next_room_id="hidden_inscription",
            ),
        ]
    )

    # === HIDDEN INSCRIPTION ===
    rooms["hidden_inscription"] = Room(
        id="hidden_inscription",
        name="The Hidden Inscription",
        description=(
            "Running your fingers along the cold stone, you discover faint "
            "carvings beneath the ivy. They form words in an ancient script "
            "that somehow you can read: 'Three keys unlock the final door: "
            "Truth of self, acceptance of shadow, embrace of light.'"
        ),
        room_type=RoomType.REFLECTION,
        on_enter_item="ancient_knowledge",
        on_enter_text="You have gained the Ancient Knowledge.",
        choices=[
            Choice(
                text="Enter the labyrinth with this wisdom",
                next_room_id="hall_of_mirrors",
                reflection_prompt="What do you hope to find within yourself?"
            ),
        ]
    )

    # === HALL OF MIRRORS ===
    rooms["hall_of_mirrors"] = Room(
        id="hall_of_mirrors",
        name="The Hall of Mirrors",
        description=(
            "Countless mirrors line the walls, each reflecting a different "
            "version of yourself. Some show you as a child, others as an elder. "
            "One mirror shows you wreathed in shadow, another bathed in light. "
            "The reflections seem to move independently, each living their own life. "
            "In one corner, a mirror shows nothing at all—just stillness."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="We are what we pretend to be, so we must be careful about what we pretend to be.",
        literary_source="Kurt Vonnegut, Mother Night",
        choices=[
            Choice(
                text="Approach the mirror showing your shadow self",
                next_room_id="shadow_chamber",
            ),
            Choice(
                text="Approach the mirror showing your radiant self",
                next_room_id="light_chamber",
            ),
            Choice(
                text="Walk straight ahead, ignoring the mirrors",
                next_room_id="garden_of_forking_paths",
            ),
            Choice(
                text="Approach the empty, still mirror",
                next_room_id="temple_of_silence",
            ),
        ]
    )

    # === SHADOW CHAMBER ===
    rooms["shadow_chamber"] = Room(
        id="shadow_chamber",
        name="The Shadow Chamber",
        description=(
            "The mirror dissolves as you touch it, and you step into darkness. "
            "Your shadow stands before you, solid and real. It speaks with your "
            "voice: 'I am everything you deny. Every fear, every doubt, every "
            "regret you've buried. Will you acknowledge me, or will you run?'"
        ),
        room_type=RoomType.CHALLENGE,
        literary_quote="One does not become enlightened by imagining figures of light, but by making the darkness conscious.",
        literary_source="Carl Jung",
        choices=[
            Choice(
                text="'I acknowledge you. You are part of me.'",
                next_room_id="shadow_accepted",
                reflection_prompt="What part of yourself have you been avoiding?"
            ),
            Choice(
                text="'You are not real. I reject you.'",
                next_room_id="shadow_rejected",
            ),
            Choice(
                text="Attempt to flee back through the mirror",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === SHADOW ACCEPTED ===
    rooms["shadow_accepted"] = Room(
        id="shadow_accepted",
        name="Shadow's Embrace",
        description=(
            "Your shadow smiles—not cruelly, but with something like relief. "
            "'Thank you,' it whispers, and merges back into you. You feel "
            "heavier, but also more complete. In your hand materializes a key "
            "of dark iron, warm to the touch."
        ),
        room_type=RoomType.REVELATION,
        on_enter_item="shadow_key",
        on_enter_text="You have received the Shadow Key.",
        literary_quote="The wound is the place where the Light enters you.",
        literary_source="Rumi",
        choices=[
            Choice(
                text="Return to the Hall of Mirrors",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === SHADOW REJECTED ===
    rooms["shadow_rejected"] = Room(
        id="shadow_rejected",
        name="The Fractured Self",
        description=(
            "Your shadow laughs bitterly and dissolves into countless whispers "
            "that follow you like a cold wind. 'You cannot escape yourself,' "
            "they hiss. The darkness feels oppressive, incomplete. You find "
            "yourself back in the hall, but something feels missing."
        ),
        room_type=RoomType.REFLECTION,
        choices=[
            Choice(
                text="Continue through the labyrinth",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === LIGHT CHAMBER ===
    rooms["light_chamber"] = Room(
        id="light_chamber",
        name="The Chamber of Light",
        description=(
            "You step into blinding radiance. As your eyes adjust, you see "
            "yourself—but idealized, perfect, glowing with potential. This "
            "luminous self speaks: 'I am who you could become. Your highest "
            "aspirations made manifest. Do you believe you deserve to be me?'"
        ),
        room_type=RoomType.CHALLENGE,
        literary_quote="Our deepest fear is not that we are inadequate. Our deepest fear is that we are powerful beyond measure.",
        literary_source="Marianne Williamson",
        choices=[
            Choice(
                text="'I am worthy of becoming my best self.'",
                next_room_id="light_accepted",
                reflection_prompt="What is the best version of yourself you aspire to become?"
            ),
            Choice(
                text="'I could never be that. It's impossible.'",
                next_room_id="light_rejected",
            ),
            Choice(
                text="Return to the Hall of Mirrors",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === LIGHT ACCEPTED ===
    rooms["light_accepted"] = Room(
        id="light_accepted",
        name="Light's Blessing",
        description=(
            "Your radiant self smiles with infinite compassion. 'Then begin,' "
            "it says simply, and embraces you. The light doesn't blind—it "
            "illuminates. You understand that potential is not a destination "
            "but a direction. A crystalline key appears in your palm."
        ),
        room_type=RoomType.REVELATION,
        on_enter_item="light_key",
        on_enter_text="You have received the Light Key.",
        literary_quote="There is a crack in everything. That's how the light gets in.",
        literary_source="Leonard Cohen",
        choices=[
            Choice(
                text="Return to the Hall of Mirrors",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === LIGHT REJECTED ===
    rooms["light_rejected"] = Room(
        id="light_rejected",
        name="Dimmed Potential",
        description=(
            "Your radiant self dims, looking at you with sadness rather than "
            "judgment. 'Perhaps another time,' it says softly. The light fades, "
            "leaving you in comfortable shadow, but you sense an opportunity "
            "has slipped away—for now."
        ),
        room_type=RoomType.REFLECTION,
        choices=[
            Choice(
                text="Return to the Hall of Mirrors",
                next_room_id="hall_of_mirrors",
            ),
        ]
    )

    # === GARDEN OF FORKING PATHS ===
    rooms["garden_of_forking_paths"] = Room(
        id="garden_of_forking_paths",
        name="The Garden of Forking Paths",
        description=(
            "You emerge into an impossible garden where every path branches "
            "infinitely. Flowers bloom and wither in seconds. Trees grow and "
            "fall in moments. Time seems meaningless here. At the garden's "
            "heart, you glimpse a door that shimmers with all colors."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="In all fictional works, each time a man is confronted with several alternatives, he chooses one and eliminates the others.",
        literary_source="Jorge Luis Borges, The Garden of Forking Paths",
        choices=[
            Choice(
                text="Follow the path of blooming roses",
                next_room_id="library_of_lives",
            ),
            Choice(
                text="Follow the path of ancient oaks",
                next_room_id="well_of_memory",
            ),
            Choice(
                text="Follow the path of flowing water",
                next_room_id="river_of_time",
            ),
            Choice(
                text="Follow the path of dancing flames",
                next_room_id="forge_of_creation",
            ),
            Choice(
                text="Walk directly toward the shimmering door",
                next_room_id="final_door",
            ),
        ]
    )

    # === RIVER OF TIME ===
    rooms["river_of_time"] = Room(
        id="river_of_time",
        name="The River of Time",
        description=(
            "A silver river flows through a canyon of crystallized moments. "
            "You see frozen scenes along its banks: a child's first steps, "
            "an elderly hand reaching out, a wedding, a funeral. The water "
            "whispers: 'Nothing stays. Everything flows. Will you stand still "
            "or flow with me?'"
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="No man ever steps in the same river twice, for it's not the same river and he's not the same man.",
        literary_source="Heraclitus",
        choices=[
            Choice(
                text="Step into the river and let it carry you",
                next_room_id="flowing_present",
                reflection_prompt="What are you holding onto that you need to let go?"
            ),
            Choice(
                text="Sit on the bank and watch time pass",
                next_room_id="observer_of_time",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === FLOWING PRESENT ===
    rooms["flowing_present"] = Room(
        id="flowing_present",
        name="The Eternal Now",
        description=(
            "The river carries you gently, washing away regrets of the past "
            "and anxieties about the future. For one perfect moment, you exist "
            "only in the present. Time becomes irrelevant. You are neither young "
            "nor old—you simply are. The river deposits you on a shore of soft sand, "
            "somehow renewed."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="The present moment is filled with joy and happiness. If you are attentive, you will see it.",
        literary_source="Thich Nhat Hanh",
        choices=[
            Choice(
                text="Return to the garden with newfound presence",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === OBSERVER OF TIME ===
    rooms["observer_of_time"] = Room(
        id="observer_of_time",
        name="The Still Point",
        description=(
            "From the bank, you watch time flow without being swept away. "
            "You see patterns: how joy follows sorrow, how endings birth beginnings. "
            "The river's music is both melancholy and hopeful. You understand "
            "that impermanence is not loss—it is the very essence of being alive."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="At the still point of the turning world. Neither flesh nor fleshless; Neither from nor towards; at the still point, there the dance is.",
        literary_source="T.S. Eliot, Burnt Norton",
        choices=[
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === FORGE OF CREATION ===
    rooms["forge_of_creation"] = Room(
        id="forge_of_creation",
        name="The Forge of Creation",
        description=(
            "Heat embraces you as you enter a vast forge. Here, ideas take shape "
            "in molten metal. Unfinished sculptures line the walls—projects abandoned, "
            "dreams deferred. In the center, an anvil awaits, and beside it, "
            "tools that seem made for your hands alone."
        ),
        room_type=RoomType.CHALLENGE,
        literary_quote="Every child is an artist. The problem is how to remain an artist once we grow up.",
        literary_source="Pablo Picasso",
        choices=[
            Choice(
                text="Pick up the hammer and begin to create",
                next_room_id="creation_complete",
                reflection_prompt="What have you always wanted to create but haven't yet?"
            ),
            Choice(
                text="Examine the abandoned works",
                next_room_id="abandoned_dreams",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === CREATION COMPLETE ===
    rooms["creation_complete"] = Room(
        id="creation_complete",
        name="The Maker's Joy",
        description=(
            "Your hands move with surprising certainty. The metal bends to your will, "
            "and something beautiful emerges—not perfect, but unmistakably yours. "
            "As you hold your creation, you remember: you have always been a maker. "
            "Every word spoken, every meal prepared, every garden tended. "
            "Creation is not separate from life—it is life."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="The desire to create is one of the deepest yearnings of the human soul.",
        literary_source="Dieter F. Uchtdorf",
        choices=[
            Choice(
                text="Return to the garden, inspired",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === ABANDONED DREAMS ===
    rooms["abandoned_dreams"] = Room(
        id="abandoned_dreams",
        name="The Gallery of What-If",
        description=(
            "Each unfinished piece tells a story: the novel never written, "
            "the song never sung, the business never started. They don't accuse "
            "you—they wait. 'We are still here,' they seem to say. "
            "'It is never too late to pick us up again.'"
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="It is never too late to be what you might have been.",
        literary_source="George Eliot",
        choices=[
            Choice(
                text="Return to the forge with renewed purpose",
                next_room_id="forge_of_creation",
                reflection_prompt="What abandoned dream would you like to revisit?"
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === TEMPLE OF SILENCE ===
    rooms["temple_of_silence"] = Room(
        id="temple_of_silence",
        name="The Temple of Silence",
        description=(
            "A path you hadn't noticed before leads to a temple of white stone. "
            "Inside, absolute silence. No wind, no birds, no heartbeat. "
            "The silence is not empty—it is full. Full of everything unsaid, "
            "unthought, unfelt. A single cushion sits in the center."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Silence is the language of God, all else is poor translation.",
        literary_source="Rumi",
        choices=[
            Choice(
                text="Sit in silence and listen",
                next_room_id="inner_voice",
                reflection_prompt="When was the last time you sat in complete silence?"
            ),
            Choice(
                text="Speak aloud to break the silence",
                next_room_id="echoing_words",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === INNER VOICE ===
    rooms["inner_voice"] = Room(
        id="inner_voice",
        name="The Voice Within",
        description=(
            "In the silence, you hear it: a voice that has always been there, "
            "beneath the noise of daily life. It does not give answers. "
            "It asks questions. And in the asking, you find a peace that "
            "requires no answers. The silence becomes a companion, not an absence."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="Be still and know.",
        literary_source="Psalm 46:10",
        choices=[
            Choice(
                text="Carry this silence with you",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === ECHOING WORDS ===
    rooms["echoing_words"] = Room(
        id="echoing_words",
        name="The Echo Chamber",
        description=(
            "Your words shatter the silence and echo forever, multiplying, "
            "distorting, becoming noise. You realize how much of life is noise "
            "that drowns out what matters. The echoes eventually fade, "
            "and the silence returns—patient, forgiving, still."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Speech is silver, silence is golden.",
        literary_source="Thomas Carlyle",
        choices=[
            Choice(
                text="Try sitting in silence this time",
                next_room_id="inner_voice",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === CHAMBER OF GRATITUDE ===
    rooms["chamber_of_gratitude"] = Room(
        id="chamber_of_gratitude",
        name="The Chamber of Gratitude",
        description=(
            "Hidden in a corner of the garden is a small chamber lined with "
            "glowing orbs. Each orb contains a moment of grace from your life: "
            "a kind word, a helping hand, an unexpected beauty. Some orbs "
            "you recognize. Others you had forgotten entirely."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Gratitude turns what we have into enough.",
        literary_source="Aesop",
        choices=[
            Choice(
                text="Add a new orb to the chamber",
                next_room_id="gratitude_offered",
                reflection_prompt="What are you most grateful for today?"
            ),
            Choice(
                text="Simply bask in the accumulated grace",
                next_room_id="gratitude_received",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === GRATITUDE OFFERED ===
    rooms["gratitude_offered"] = Room(
        id="gratitude_offered",
        name="Gift Given",
        description=(
            "A new orb forms in your hands, warm with the energy of genuine thanks. "
            "You place it among the others, and its light mingles with theirs. "
            "The chamber grows slightly brighter. You understand: gratitude is not "
            "just receiving—it is also giving. Both directions complete the circuit."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them.",
        literary_source="John F. Kennedy",
        choices=[
            Choice(
                text="Return to the garden, grateful",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === GRATITUDE RECEIVED ===
    rooms["gratitude_received"] = Room(
        id="gratitude_received",
        name="Abundance Remembered",
        description=(
            "Standing among the orbs, you feel their warmth seep into you. "
            "So much good. So much that was given freely. The scarcity you "
            "sometimes feel dissolves. Not because nothing is lacking, but because "
            "what you have is more than enough. It always was."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Enough is a feast.",
        literary_source="Buddhist Proverb",
        choices=[
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === LIBRARY OF LIVES ===
    rooms["library_of_lives"] = Room(
        id="library_of_lives",
        name="The Library of Unlived Lives",
        description=(
            "Towering bookshelves contain volumes with your name on every spine. "
            "Each book describes a life you could have lived—different choices, "
            "different paths. Some are thick with adventure, others thin with "
            "quiet contentment. One book glows faintly: 'The Life You Are Living.'"
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="The library is infinite and cyclical.",
        literary_source="Jorge Luis Borges, The Library of Babel",
        choices=[
            Choice(
                text="Read 'The Life You Are Living'",
                next_room_id="current_life_reflection",
                reflection_prompt="If your life were a book, what would its title be?"
            ),
            Choice(
                text="Browse the lives you didn't choose",
                next_room_id="unchosen_lives",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === CURRENT LIFE REFLECTION ===
    rooms["current_life_reflection"] = Room(
        id="current_life_reflection",
        name="Your Story",
        description=(
            "The book opens to a page that is still being written. Words appear "
            "as you watch, describing this very moment. The narrative is neither "
            "tragedy nor comedy—it simply is, beautiful in its authenticity. "
            "A golden key falls from between the pages."
        ),
        room_type=RoomType.REVELATION,
        on_enter_item="truth_key",
        on_enter_text="You have received the Truth Key.",
        literary_quote="We tell ourselves stories in order to live.",
        literary_source="Joan Didion",
        choices=[
            Choice(
                text="Return to the garden with new understanding",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === UNCHOSEN LIVES ===
    rooms["unchosen_lives"] = Room(
        id="unchosen_lives",
        name="The Paths Not Taken",
        description=(
            "You pull book after book from the shelves. In one, you're a sailor "
            "crossing unknown seas. In another, a hermit in mountain solitude. "
            "Some lives seem happier than yours, others far worse. But none of "
            "them feel quite... right. They're missing something essential."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Two roads diverged in a wood, and I— I took the one less traveled by, And that has made all the difference.",
        literary_source="Robert Frost, The Road Not Taken",
        choices=[
            Choice(
                text="Return to the library's center",
                next_room_id="library_of_lives",
                reflection_prompt="What choice in your life are you most grateful for?",
            ),
        ]
    )

    # === WELL OF MEMORY ===
    rooms["well_of_memory"] = Room(
        id="well_of_memory",
        name="The Well of Memory",
        description=(
            "An ancient well sits beneath the oldest oak. Its waters are dark "
            "but not threatening—they swirl with images of the past. Your past. "
            "Some memories shimmer invitingly; others lurk in the depths. A "
            "brass ladle hangs from a hook."
        ),
        room_type=RoomType.REFLECTION,
        literary_quote="Memory is the diary that we all carry about with us.",
        literary_source="Oscar Wilde",
        choices=[
            Choice(
                text="Drink from a happy memory",
                next_room_id="happy_memory",
                reflection_prompt="What is a moment of joy you never want to forget?"
            ),
            Choice(
                text="Drink from a painful memory",
                next_room_id="painful_memory",
                reflection_prompt="What is a difficult memory that shaped who you are?"
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === HAPPY MEMORY ===
    rooms["happy_memory"] = Room(
        id="happy_memory",
        name="Remembered Joy",
        description=(
            "The water tastes like childhood summers and the warmth of being "
            "loved. For a moment, you're there again—in that perfect moment. "
            "Then you return, but the warmth remains. You understand that joy "
            "isn't just in the past; it lives in you still."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="Happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
        literary_source="J.K. Rowling, Harry Potter and the Prisoner of Azkaban",
        choices=[
            Choice(
                text="Return to the well",
                next_room_id="well_of_memory",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === PAINFUL MEMORY ===
    rooms["painful_memory"] = Room(
        id="painful_memory",
        name="Remembered Sorrow",
        description=(
            "The water is bitter, bringing tears to your eyes. You experience "
            "the pain again—but this time, as an observer. You see how you "
            "survived. How you grew. The memory hasn't changed, but your "
            "relationship to it has. It no longer owns you."
        ),
        room_type=RoomType.REVELATION,
        literary_quote="What hurts you, blesses you. Darkness is your candle.",
        literary_source="Rumi",
        choices=[
            Choice(
                text="Return to the well",
                next_room_id="well_of_memory",
            ),
            Choice(
                text="Return to the garden",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === FINAL DOOR ===
    rooms["final_door"] = Room(
        id="final_door",
        name="The Final Door",
        description=(
            "The door stands before you, ancient and patient. Three keyholes "
            "are set into its surface: one of dark iron, one of crystal, one "
            "of gold. Beyond it, you sense something profound—not an ending, "
            "but a beginning."
        ),
        room_type=RoomType.CHALLENGE,
        literary_quote="The cave you fear to enter holds the treasure you seek.",
        literary_source="Joseph Campbell",
        choices=[
            Choice(
                text="Use all three keys to open the door",
                next_room_id="the_exit",
                requires_item="shadow_key",
                condition=lambda s: s.has_item("light_key") and s.has_item("truth_key"),
            ),
            Choice(
                text="Try to force the door open",
                next_room_id="door_remains_closed",
                condition=lambda s: not (s.has_item("shadow_key") and s.has_item("light_key") and s.has_item("truth_key")),
            ),
            Choice(
                text="Return to the garden to continue exploring",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === DOOR REMAINS CLOSED ===
    rooms["door_remains_closed"] = Room(
        id="door_remains_closed",
        name="The Unyielding Door",
        description=(
            "The door doesn't budge. Not through force, but through absence—you "
            "sense that something is missing. The keyholes seem to whisper: "
            "shadow, light, truth. Perhaps the labyrinth still has secrets to reveal."
        ),
        room_type=RoomType.REFLECTION,
        choices=[
            Choice(
                text="Return to explore the labyrinth",
                next_room_id="garden_of_forking_paths",
            ),
        ]
    )

    # === THE EXIT ===
    rooms["the_exit"] = Room(
        id="the_exit",
        name="Beyond the Labyrinth",
        description=(
            "The door swings open, and you step through—not into another room, "
            "but into clarity. The labyrinth, you realize, was never a prison. "
            "It was a mirror. And now you see yourself clearly: shadow and light, "
            "past and future, all woven into the truth of who you are.\n\n"
            "The mist parts, and you find yourself standing outside the archway "
            "where you began. But you are not the same person who entered. The "
            "labyrinth remains, patient and eternal, ready for whenever you need "
            "to look within again."
        ),
        room_type=RoomType.EXIT,
        literary_quote="We shall not cease from exploration, and the end of all our exploring will be to arrive where we started and know the place for the first time.",
        literary_source="T.S. Eliot, Little Gidding",
        choices=[]
    )

    return rooms
