#!/usr/bin/env python3
"""
Aurora Ambient Scene
Dark sky with moving, wavy colored aurora bands
"""

import pygame
import math
import random

SCENE_NAME = "Aurora"
SCENE_CATEGORY = "Ambient"

# Scene state
_time = 0
_wave_offsets = []
_stars = []


def init_scene(screen):
    """Initialize aurora scene"""
    global _time, _wave_offsets, _stars

    _time = 0
    _wave_offsets = [random.uniform(0, math.pi * 2) for _ in range(5)]

    # Generate random stars
    width, height = screen.get_size()
    _stars = []
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height // 2)
        brightness = random.randint(100, 255)
        size = random.randint(1, 2)
        _stars.append((x, y, brightness, size))


def update_scene(dt):
    """Update aurora animation"""
    global _time
    _time += dt * 0.001  # Slow movement


def render_scene(screen):
    """Render aurora scene"""
    width, height = screen.get_size()

    # Dark sky gradient (black to deep blue)
    for y in range(height):
        progress = y / height
        r = int(5 * progress)
        g = int(10 * progress)
        b = int(30 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw stars
    for x, y, brightness, size in _stars:
        twinkle = 0.8 + 0.2 * math.sin(_time * 2 + x * 0.01)
        color = int(brightness * twinkle)
        pygame.draw.circle(screen, (color, color, color), (x, y), size)

    # Draw aurora bands (multiple layers)
    aurora_colors = [
        (0, 255, 150),  # Green
        (100, 200, 255),  # Blue
        (150, 100, 255),  # Purple
        (0, 255, 200),  # Cyan
    ]

    num_bands = 3
    for band_idx in range(num_bands):
        color = aurora_colors[band_idx % len(aurora_colors)]
        offset = _wave_offsets[band_idx]

        # Create list of points for wavy band
        points = []
        num_points = 40

        for i in range(num_points + 1):
            x = (i / num_points) * width

            # Multiple sine waves for organic movement
            wave1 = math.sin(x * 0.01 + _time * 0.5 + offset) * 40
            wave2 = math.sin(x * 0.02 + _time * 0.3 + offset * 1.5) * 25
            wave3 = math.sin(x * 0.005 + _time * 0.7 + offset * 0.8) * 60

            y_center = 200 + band_idx * 80
            y = y_center + wave1 + wave2 + wave3

            points.append((x, y))

        # Draw the band as semi-transparent curves
        if len(points) > 2:
            # Draw multiple offset versions for glow effect
            for glow_offset in range(3):
                alpha = 40 - glow_offset * 10
                glow_height = 30 + glow_offset * 15

                # Create surface for transparency
                surf = pygame.Surface((width, height), pygame.SRCALPHA)

                # Draw upper and lower bounds of band
                upper_points = [(x, y - glow_height) for x, y in points]
                lower_points = [(x, y + glow_height) for x, y in reversed(points)]

                all_points = upper_points + lower_points

                if len(all_points) >= 3:
                    pygame.draw.polygon(surf, (*color, alpha), all_points)

                screen.blit(surf, (0, 0))

    # Subtle vignette effect
    vignette_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(vignette_surf, (0, 0, 0, 60), (0, 0, width, height))
    pygame.draw.ellipse(vignette_surf, (0, 0, 0, 0), (width // 4, height // 4, width // 2, height // 2))
    screen.blit(vignette_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
