"""Game engine for Labyrinth of the Mind."""

import textwrap
from typing import TextIO
import sys

from .models import Choice, GameState, Room, RoomType
from .rooms import create_labyrinth


class GameEngine:
    """Main game engine that handles the game loop and state."""

    def __init__(
        self,
        input_stream: TextIO = sys.stdin,
        output_stream: TextIO = sys.stdout,
        wrap_width: int = 80,
    ):
        self.rooms = create_labyrinth()
        self.state = GameState()
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.wrap_width = wrap_width

    def write(self, text: str) -> None:
        """Write text to the output stream."""
        self.output_stream.write(text)
        self.output_stream.flush()

    def writeln(self, text: str = "") -> None:
        """Write a line to the output stream."""
        self.write(text + "\n")

    def write_wrapped(self, text: str) -> None:
        """Write text wrapped to the configured width."""
        wrapped = textwrap.fill(text, width=self.wrap_width)
        self.writeln(wrapped)

    def read_input(self, prompt: str = "") -> str:
        """Read input from the input stream."""
        if prompt:
            self.write(prompt)
        return self.input_stream.readline().strip()

    def clear_screen(self) -> None:
        """Clear the screen (if terminal supports it)."""
        self.write("\033[2J\033[H")

    def display_title(self) -> None:
        """Display the game title."""
        title = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              L A B Y R I N T H   O F   T H E   M I N D                   ║
║                                                                           ║
║         An interactive journey of self-reflection and discovery          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
        self.writeln(title)

    def display_room(self, room: Room) -> None:
        """Display a room's description and available choices."""
        self.writeln()
        self.writeln("=" * self.wrap_width)
        self.writeln(f"  {room.name.upper()}")
        self.writeln("=" * self.wrap_width)
        self.writeln()

        # Show entry text if any
        if room.on_enter_text and not self.state.has_visited(room.id):
            self.write_wrapped(f"✨ {room.on_enter_text}")
            self.writeln()

        # Show description
        self.write_wrapped(room.description)
        self.writeln()

        # Show literary quote if present
        if room.literary_quote:
            self.writeln()
            self.writeln(f'  "{room.literary_quote}"')
            if room.literary_source:
                self.writeln(f"    — {room.literary_source}")
        self.writeln()

    def display_choices(self, room: Room) -> list[Choice]:
        """Display available choices and return the list of valid choices."""
        available_choices = [c for c in room.choices if c.is_available(self.state)]

        if not available_choices:
            return []

        self.writeln("-" * 40)
        self.writeln("What do you do?")
        self.writeln()

        for i, choice in enumerate(available_choices, 1):
            self.writeln(f"  [{i}] {choice.text}")

        self.writeln()
        self.writeln("  [I] View inventory")
        self.writeln("  [R] Review your reflections")
        self.writeln("  [Q] Quit game")
        self.writeln()

        return available_choices

    def display_inventory(self) -> None:
        """Display the player's inventory."""
        self.writeln()
        self.writeln("-" * 40)
        self.writeln("INVENTORY")
        self.writeln("-" * 40)

        if not self.state.inventory:
            self.writeln("  Your inventory is empty.")
        else:
            item_names = {
                "shadow_key": "Shadow Key (dark iron)",
                "light_key": "Light Key (crystalline)",
                "truth_key": "Truth Key (golden)",
                "ancient_knowledge": "Ancient Knowledge",
            }
            for item in sorted(self.state.inventory):
                display_name = item_names.get(item, item.replace("_", " ").title())
                self.writeln(f"  • {display_name}")
        self.writeln()

    def display_reflections(self) -> None:
        """Display the player's recorded reflections."""
        self.writeln()
        self.writeln("-" * 40)
        self.writeln("YOUR REFLECTIONS")
        self.writeln("-" * 40)

        if not self.state.reflections:
            self.writeln("  You have not yet recorded any reflections.")
        else:
            for prompt, response in self.state.reflections.items():
                self.writeln()
                self.write_wrapped(f"Q: {prompt}")
                self.write_wrapped(f"A: {response}")
        self.writeln()

    def prompt_reflection(self, prompt: str) -> None:
        """Prompt the player for a reflection and store it."""
        self.writeln()
        self.writeln("-" * 40)
        self.writeln("MOMENT OF REFLECTION")
        self.writeln("-" * 40)
        self.writeln()
        self.write_wrapped(prompt)
        self.writeln()
        self.writeln("(Your answer is for you alone. Press Enter to skip.)")
        self.writeln()

        response = self.read_input("> ")
        if response:
            self.state.add_reflection(prompt, response)
            self.writeln()
            self.writeln("Your reflection has been recorded.")
        self.writeln()

    def get_player_choice(self, available_choices: list[Choice]) -> Choice | None:
        """Get the player's choice from available options."""
        while True:
            choice_input = self.read_input("Your choice: ").strip().upper()

            if choice_input == "Q":
                self.state.has_quit = True
                return None

            if choice_input == "I":
                self.display_inventory()
                continue

            if choice_input == "R":
                self.display_reflections()
                continue

            try:
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(available_choices):
                    return available_choices[choice_num - 1]
                else:
                    self.writeln(f"Please enter a number between 1 and {len(available_choices)}.")
            except ValueError:
                self.writeln("Please enter a valid choice.")

    def enter_room(self, room_id: str) -> None:
        """Enter a room and handle entry effects."""
        room = self.rooms.get(room_id)
        if not room:
            raise ValueError(f"Room '{room_id}' not found")

        self.state.current_room_id = room_id

        # Handle entry item
        if room.on_enter_item and not self.state.has_visited(room_id):
            self.state.add_item(room.on_enter_item)

        self.state.visit_room(room_id)
        self.state.turns += 1

    def display_victory(self) -> None:
        """Display the victory message."""
        self.writeln()
        self.writeln("=" * self.wrap_width)
        self.writeln()
        self.writeln("  🌟 CONGRATULATIONS 🌟")
        self.writeln()
        self.writeln("=" * self.wrap_width)
        self.writeln()
        self.write_wrapped(
            "You have completed your journey through the Labyrinth of the Mind. "
            "The keys you gathered—shadow, light, and truth—represent the parts "
            "of yourself you chose to acknowledge and embrace."
        )
        self.writeln()

        if self.state.reflections:
            self.writeln("Along the way, you reflected on these questions:")
            self.writeln()
            for prompt in self.state.reflections:
                self.writeln(f"  • {prompt}")
            self.writeln()

        self.write_wrapped(
            "Remember: the labyrinth is always within you, ready whenever you "
            "need to look inward again."
        )
        self.writeln()
        self.writeln(f"Journey completed in {self.state.turns} steps.")
        self.writeln()

    def display_farewell(self) -> None:
        """Display the farewell message when quitting."""
        self.writeln()
        self.writeln("-" * 40)
        self.write_wrapped(
            "You step back from the labyrinth. Its mists swirl invitingly, "
            "patient as always. The journey inward awaits whenever you're ready."
        )
        self.writeln()
        self.writeln("Thank you for playing.")
        self.writeln()

    def run(self) -> None:
        """Run the main game loop."""
        self.clear_screen()
        self.display_title()

        self.writeln("Press Enter to begin your journey...")
        self.read_input()

        self.enter_room("entrance")

        while not self.state.has_won and not self.state.has_quit:
            current_room = self.rooms[self.state.current_room_id]

            self.display_room(current_room)

            # Check for victory
            if current_room.room_type == RoomType.EXIT:
                self.state.has_won = True
                self.display_victory()
                break

            available_choices = self.display_choices(current_room)

            if not available_choices:
                self.writeln("There are no available paths forward.")
                break

            choice = self.get_player_choice(available_choices)

            if choice is None:
                self.display_farewell()
                break

            # Handle reflection prompt
            if choice.reflection_prompt:
                self.prompt_reflection(choice.reflection_prompt)

            # Handle item from choice
            if choice.gives_item:
                self.state.add_item(choice.gives_item)
                self.writeln(f"✨ You received: {choice.gives_item.replace('_', ' ').title()}")

            # Move to next room
            self.enter_room(choice.next_room_id)


def main() -> None:
    """Main entry point for the game."""
    engine = GameEngine()
    try:
        engine.run()
    except KeyboardInterrupt:
        engine.writeln()
        engine.writeln("Journey interrupted. Until next time...")
    except EOFError:
        engine.writeln()
        engine.writeln("Journey ended.")


if __name__ == "__main__":
    main()
