"""Map visualization for the labyrinth."""

from .rooms import create_labyrinth
from .models import RoomType


# Room positions for visualization (x, y coordinates)
ROOM_POSITIONS: dict[str, tuple[int, int]] = {
    "entrance": (50, 10),
    "hidden_inscription": (20, 10),
    "hall_of_mirrors": (50, 25),
    "shadow_chamber": (25, 35),
    "shadow_accepted": (10, 45),
    "shadow_rejected": (25, 50),
    "light_chamber": (75, 35),
    "light_accepted": (90, 45),
    "light_rejected": (75, 50),
    "garden_of_forking_paths": (50, 50),
    "library_of_lives": (20, 60),
    "current_life_reflection": (10, 70),
    "unchosen_lives": (20, 75),
    "well_of_memory": (80, 60),
    "happy_memory": (90, 70),
    "painful_memory": (80, 75),
    # New rooms
    "river_of_time": (35, 60),
    "flowing_present": (30, 70),
    "observer_of_time": (40, 70),
    "forge_of_creation": (65, 60),
    "creation_complete": (70, 70),
    "abandoned_dreams": (60, 70),
    "temple_of_silence": (45, 62),
    "inner_voice": (42, 72),
    "echoing_words": (48, 72),
    "chamber_of_gratitude": (55, 62),
    "gratitude_offered": (52, 72),
    "gratitude_received": (58, 72),
    # Final area
    "final_door": (50, 82),
    "door_remains_closed": (50, 88),
    "the_exit": (50, 95),
}

# Room type colors
ROOM_COLORS: dict[RoomType, str] = {
    RoomType.ENTRANCE: "#e94560",
    RoomType.REFLECTION: "#c9b1ff",
    RoomType.CHALLENGE: "#ffd700",
    RoomType.REVELATION: "#00ff88",
    RoomType.EXIT: "#ffffff",
}


def generate_map_svg(visited_rooms: set[str], current_room_id: str) -> str:
    """Generate an SVG map of the labyrinth."""
    rooms = create_labyrinth()

    svg_parts = [
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#1a1a2e;border-radius:10px;">',
        # Add a subtle grid
        '<defs>',
        '<pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">',
        '<path d="M 10 0 L 0 0 0 10" fill="none" stroke="#2a2a3e" stroke-width="0.2"/>',
        '</pattern>',
        '</defs>',
        '<rect width="100" height="100" fill="url(#grid)"/>',
    ]

    # Draw connections first (so they're behind nodes)
    for room_id, room in rooms.items():
        if room_id not in ROOM_POSITIONS:
            continue
        x1, y1 = ROOM_POSITIONS[room_id]

        for choice in room.choices:
            next_id = choice.next_room_id
            if next_id not in ROOM_POSITIONS:
                continue
            x2, y2 = ROOM_POSITIONS[next_id]

            # Determine line style based on visited status
            if room_id in visited_rooms and next_id in visited_rooms:
                stroke = "#667eea"
                opacity = "0.8"
                width = "0.4"
            elif room_id in visited_rooms:
                stroke = "#444"
                opacity = "0.5"
                width = "0.2"
            else:
                stroke = "#333"
                opacity = "0.2"
                width = "0.1"

            svg_parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"/>'
            )

    # Draw room nodes
    for room_id, (x, y) in ROOM_POSITIONS.items():
        room = rooms.get(room_id)
        if not room:
            continue

        # Determine appearance based on status
        if room_id == current_room_id:
            fill = "#667eea"
            stroke = "#ffffff"
            radius = 3
            opacity = 1
        elif room_id in visited_rooms:
            fill = ROOM_COLORS.get(room.room_type, "#666")
            stroke = "#ffffff"
            radius = 2
            opacity = 0.9
        else:
            fill = "#333"
            stroke = "#444"
            radius = 1.5
            opacity = 0.3

        # Draw node
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="0.3" opacity="{opacity}"/>'
        )

        # Add pulsing animation for current room
        if room_id == current_room_id:
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{radius + 1}" '
                f'fill="none" stroke="#667eea" stroke-width="0.2" opacity="0.5">'
                f'<animate attributeName="r" values="{radius};{radius + 2};{radius}" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/>'
                f'</circle>'
            )

    # Add legend
    svg_parts.append('<text x="5" y="98" fill="#666" font-size="2" font-family="sans-serif">● Visited  ○ Undiscovered  ◉ Current</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def get_room_connections() -> dict[str, list[str]]:
    """Get all room connections as an adjacency list."""
    rooms = create_labyrinth()
    connections = {}
    for room_id, room in rooms.items():
        connections[room_id] = [c.next_room_id for c in room.choices]
    return connections
