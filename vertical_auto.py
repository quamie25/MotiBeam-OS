#!/usr/bin/env python3
"""
MotiBeamOS v3.0 - Auto Vertical (HUD Demo)
Simulates in-car HUD for automotive licensing demos
Features: speedometer, turn-by-turn navigation, collision alerts, night drive mode
"""

import pygame
import math

# HUD Colors
COLOR_HUD_PRIMARY = (0, 220, 255)  # Cyan
COLOR_HUD_SECONDARY = (100, 180, 255)  # Light blue
COLOR_HUD_WARNING = (255, 200, 0)  # Yellow
COLOR_HUD_DANGER = (255, 60, 60)  # Red
COLOR_HUD_TEXT = (220, 240, 255)  # Light cyan
COLOR_HUD_DIM = (100, 140, 180)  # Dim blue
COLOR_NIGHT_BG = (5, 10, 20)  # Dark night background

# HUD State
_time = 0
_speed = 0
_target_speed = 0
_current_instruction = ""
_instruction_distance = 0
_collision_alert = False
_collision_flash_time = 0
_night_mode = True
_timeline_events = []
_current_event_idx = 0


class TimelineEvent:
    """Defines an event in the simulated drive"""

    def __init__(self, time, event_type, data):
        self.time = time  # Time in seconds
        self.event_type = event_type  # 'speed', 'turn', 'collision'
        self.data = data


def init_auto_vertical(screen):
    """Initialize Auto HUD"""
    global _time, _speed, _target_speed, _current_instruction, _instruction_distance
    global _collision_alert, _collision_flash_time, _timeline_events, _current_event_idx

    _time = 0
    _speed = 0
    _target_speed = 35
    _current_instruction = "Turn right in 500 ft"
    _instruction_distance = 500
    _collision_alert = False
    _collision_flash_time = 0
    _current_event_idx = 0

    # Define simulated drive timeline (all times in seconds)
    _timeline_events = [
        TimelineEvent(0, 'speed', 35),
        TimelineEvent(0, 'turn', {'instruction': 'Turn right in 500 ft', 'distance': 500}),

        TimelineEvent(3, 'turn', {'instruction': 'Turn right in 300 ft', 'distance': 300}),
        TimelineEvent(5, 'speed', 25),  # Slow down for turn
        TimelineEvent(6, 'turn', {'instruction': 'Turn right in 100 ft', 'distance': 100}),
        TimelineEvent(7.5, 'turn', {'instruction': 'Turn right NOW', 'distance': 0}),
        TimelineEvent(8.5, 'speed', 40),  # Speed up after turn
        TimelineEvent(9, 'turn', {'instruction': 'Continue straight', 'distance': 0}),

        TimelineEvent(12, 'speed', 45),
        TimelineEvent(14, 'collision', True),  # Collision alert!
        TimelineEvent(15, 'speed', 20),  # Emergency brake
        TimelineEvent(16, 'collision', False),  # Alert cleared
        TimelineEvent(17, 'speed', 35),

        TimelineEvent(19, 'turn', {'instruction': 'Turn left in 800 ft', 'distance': 800}),
        TimelineEvent(22, 'turn', {'instruction': 'Turn left in 400 ft', 'distance': 400}),
        TimelineEvent(24, 'speed', 30),
        TimelineEvent(25, 'turn', {'instruction': 'Turn left in 150 ft', 'distance': 150}),
        TimelineEvent(27, 'turn', {'instruction': 'Turn left NOW', 'distance': 0}),
        TimelineEvent(28, 'speed', 40),
        TimelineEvent(29, 'turn', {'instruction': 'Destination ahead', 'distance': 200}),
    ]


def update_auto_vertical(dt):
    """Update HUD state"""
    global _time, _speed, _target_speed, _current_instruction, _instruction_distance
    global _collision_alert, _collision_flash_time, _current_event_idx

    _time += dt * 0.001  # Convert to seconds

    # Process timeline events
    while _current_event_idx < len(_timeline_events):
        event = _timeline_events[_current_event_idx]

        if _time >= event.time:
            if event.event_type == 'speed':
                _target_speed = event.data
            elif event.event_type == 'turn':
                _current_instruction = event.data['instruction']
                _instruction_distance = event.data['distance']
            elif event.event_type == 'collision':
                _collision_alert = event.data
                if _collision_alert:
                    _collision_flash_time = _time

            _current_event_idx += 1
        else:
            break

    # Smooth speed transition
    speed_diff = _target_speed - _speed
    _speed += speed_diff * 0.05  # Smooth acceleration/deceleration

    # Update instruction distance (simulate driving)
    if _instruction_distance > 0:
        _instruction_distance = max(0, _instruction_distance - _speed * 0.1)


def render_auto_vertical(screen):
    """Render Auto HUD"""
    width, height = screen.get_size()

    # Background
    if _night_mode:
        # Night sky with stars
        screen.fill(COLOR_NIGHT_BG)

        # Simple star field
        import random
        random.seed(42)  # Deterministic stars
        for _ in range(60):
            x = random.randint(0, width)
            y = random.randint(0, height // 2)
            brightness = random.randint(100, 200)
            size = random.choice([1, 2])
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    else:
        # Day mode - lighter background
        screen.fill((30, 40, 60))

    # === Collision Alert (full screen) ===
    if _collision_alert:
        flash_intensity = abs(math.sin((_time - _collision_flash_time) * 10))

        # Red border flash
        border_thickness = 15
        alpha = int(150 * flash_intensity)

        alert_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(alert_surf, (255, 0, 0, alpha), (0, 0, width, height), border_thickness)
        screen.blit(alert_surf, (0, 0))

        # Alert text
        font_large = pygame.font.Font(None, 120)
        alert_text = font_large.render("BRAKE!", True, COLOR_HUD_DANGER)
        alert_rect = alert_text.get_rect(center=(width // 2, height // 2 - 100))

        # Text with glow
        glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        for offset in range(5, 0, -1):
            glow_alpha = int(60 * flash_intensity / offset)
            glow_text = font_large.render("BRAKE!", True, (*COLOR_HUD_DANGER, glow_alpha))
            glow_rect = glow_text.get_rect(center=(width // 2, height // 2 - 100))
            glow_surf.blit(glow_text, glow_rect)

        screen.blit(glow_surf, (0, 0))
        screen.blit(alert_text, alert_rect)

    # === Speedometer (bottom center) ===
    speed_center_x = width // 2
    speed_center_y = height - 200

    # Speed arc background
    arc_radius = 100
    arc_thickness = 12
    arc_start_angle = math.pi * 0.75  # Start at bottom left
    arc_end_angle = math.pi * 2.25  # End at bottom right

    # Background arc
    _draw_arc(screen, (speed_center_x, speed_center_y), arc_radius, arc_thickness,
              arc_start_angle, arc_end_angle, COLOR_HUD_DIM)

    # Speed fill arc
    max_speed = 60
    speed_progress = min(_speed / max_speed, 1.0)
    speed_arc_end = arc_start_angle + (arc_end_angle - arc_start_angle) * speed_progress

    _draw_arc(screen, (speed_center_x, speed_center_y), arc_radius, arc_thickness,
              arc_start_angle, speed_arc_end, COLOR_HUD_PRIMARY)

    # Digital speed readout
    font_huge = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None, 40)

    speed_text = font_huge.render(f"{int(_speed)}", True, COLOR_HUD_TEXT)
    speed_rect = speed_text.get_rect(center=(speed_center_x, speed_center_y))
    screen.blit(speed_text, speed_rect)

    mph_text = font_small.render("mph", True, COLOR_HUD_DIM)
    mph_rect = mph_text.get_rect(center=(speed_center_x, speed_center_y + 50))
    screen.blit(mph_text, mph_rect)

    # === Turn-by-turn Navigation (top center) ===
    nav_y = 120

    font_medium = pygame.font.Font(None, 60)

    # Instruction text
    instruction_text = font_medium.render(_current_instruction, True, COLOR_HUD_TEXT)
    instruction_rect = instruction_text.get_rect(center=(width // 2, nav_y))

    # Background panel
    panel_padding = 20
    panel_rect = pygame.Rect(
        instruction_rect.left - panel_padding,
        instruction_rect.top - panel_padding,
        instruction_rect.width + panel_padding * 2,
        instruction_rect.height + panel_padding * 2
    )

    # Semi-transparent background
    panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (0, 20, 40, 180), panel_surf.get_rect(), border_radius=10)
    pygame.draw.rect(panel_surf, COLOR_HUD_PRIMARY, panel_surf.get_rect(), 2, border_radius=10)
    screen.blit(panel_surf, panel_rect.topleft)

    screen.blit(instruction_text, instruction_rect)

    # Direction arrow (if turning)
    if "right" in _current_instruction.lower():
        _draw_arrow(screen, (width // 2 + 350, nav_y), "right", COLOR_HUD_PRIMARY)
    elif "left" in _current_instruction.lower():
        _draw_arrow(screen, (width // 2 - 350, nav_y), "left", COLOR_HUD_PRIMARY)

    # Distance indicator (if applicable)
    if _instruction_distance > 0:
        distance_text = font_small.render(f"{int(_instruction_distance)} ft", True, COLOR_HUD_DIM)
        distance_rect = distance_text.get_rect(center=(width // 2, nav_y + 50))
        screen.blit(distance_text, distance_rect)

    # === Night Mode indicator ===
    if _night_mode:
        mode_text = font_small.render("NIGHT DRIVE", True, COLOR_HUD_SECONDARY)
        mode_rect = mode_text.get_rect(topright=(width - 30, 30))
        screen.blit(mode_text, mode_rect)


def _draw_arc(screen, center, radius, thickness, start_angle, end_angle, color):
    """Draw a circular arc"""
    num_segments = 50
    angle_range = end_angle - start_angle

    for i in range(num_segments):
        angle1 = start_angle + (i / num_segments) * angle_range
        angle2 = start_angle + ((i + 1) / num_segments) * angle_range

        x1 = center[0] + radius * math.cos(angle1)
        y1 = center[1] - radius * math.sin(angle1)
        x2 = center[0] + radius * math.cos(angle2)
        y2 = center[1] - radius * math.sin(angle2)

        pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)


def _draw_arrow(screen, pos, direction, color):
    """Draw a directional arrow"""
    arrow_size = 40

    if direction == "right":
        # Right-pointing arrow
        points = [
            (pos[0] - arrow_size // 2, pos[1] - arrow_size // 2),
            (pos[0] + arrow_size // 2, pos[1]),
            (pos[0] - arrow_size // 2, pos[1] + arrow_size // 2),
        ]
    elif direction == "left":
        # Left-pointing arrow
        points = [
            (pos[0] + arrow_size // 2, pos[1] - arrow_size // 2),
            (pos[0] - arrow_size // 2, pos[1]),
            (pos[0] + arrow_size // 2, pos[1] + arrow_size // 2),
        ]
    else:
        return

    # Draw arrow
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, color, points, 3)


# Public API
__all__ = [
    'init_auto_vertical',
    'update_auto_vertical',
    'render_auto_vertical'
]
