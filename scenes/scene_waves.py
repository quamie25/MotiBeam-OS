#!/usr/bin/env python3
"""
Waves Ambient Scene
Horizontal wave lines moving with sine functions - calming ocean effect
"""

import pygame
import math

SCENE_NAME = "Waves"
SCENE_CATEGORY = "Ambient"

# Scene state
_time = 0


def init_scene(screen):
    """Initialize waves scene"""
    global _time
    _time = 0


def update_scene(dt):
    """Update wave animation"""
    global _time
    _time += dt * 0.001


def render_scene(screen):
    """Render waves scene"""
    width, height = screen.get_size()

    # Ocean gradient background (dark blue to lighter blue)
    for y in range(height):
        progress = y / height
        r = int(20 + 30 * progress)
        g = int(50 + 80 * progress)
        b = int(100 + 100 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw wave layers (3 layers with different speeds)
    wave_layers = [
        {"y_base": height * 0.4, "amplitude": 30, "frequency": 0.01, "speed": 0.5, "color": (50, 120, 180, 100)},
        {"y_base": height * 0.6, "amplitude": 40, "frequency": 0.008, "speed": 0.3, "color": (40, 100, 160, 120)},
        {"y_base": height * 0.8, "amplitude": 50, "frequency": 0.006, "speed": 0.4, "color": (30, 80, 140, 140)},
    ]

    for layer in wave_layers:
        # Create points for wave
        points = []
        num_points = 100

        for i in range(num_points + 1):
            x = (i / num_points) * width

            # Combine multiple sine waves for more organic movement
            wave1 = math.sin(x * layer["frequency"] + _time * layer["speed"]) * layer["amplitude"]
            wave2 = math.sin(x * layer["frequency"] * 1.5 - _time * layer["speed"] * 0.7) * (layer["amplitude"] * 0.5)

            y = layer["y_base"] + wave1 + wave2

            points.append((x, y))

        # Close the polygon at bottom
        points.append((width, height))
        points.append((0, height))

        # Draw wave as filled polygon with transparency
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        if len(points) >= 3:
            pygame.draw.polygon(surf, layer["color"], points)

        screen.blit(surf, (0, 0))

    # Add wave crests (highlights)
    crest_layer = wave_layers[0]
    crest_points = []
    num_points = 100

    for i in range(num_points + 1):
        x = (i / num_points) * width
        wave1 = math.sin(x * crest_layer["frequency"] + _time * crest_layer["speed"]) * crest_layer["amplitude"]
        wave2 = math.sin(x * crest_layer["frequency"] * 1.5 - _time * crest_layer["speed"] * 0.7) * (
                    crest_layer["amplitude"] * 0.5)
        y = crest_layer["y_base"] + wave1 + wave2
        crest_points.append((int(x), int(y)))

    # Draw crest line
    if len(crest_points) > 1:
        pygame.draw.lines(screen, (150, 200, 255), False, crest_points, 2)

    # Foam effect on crests (small dots)
    for i, (x, y) in enumerate(crest_points):
        if i % 5 == 0:  # Sparse foam
            foam_alpha = int(100 + 50 * math.sin(_time * 2 + x * 0.05))
            pygame.draw.circle(screen, (200, 230, 255), (x, y), 3)
