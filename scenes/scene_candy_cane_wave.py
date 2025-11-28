#!/usr/bin/env python3
"""
Candy Cane Wave Holiday Scene
Red and white stripes with wave motion
"""

import pygame
import math

SCENE_NAME = "Candy Cane Wave"
SCENE_CATEGORY = "Holiday"

# Scene state
_time = 0


def init_scene(screen):
    """Initialize candy cane wave scene"""
    global _time
    _time = 0


def update_scene(dt):
    """Update wave animation"""
    global _time
    _time += dt * 0.001


def render_scene(screen):
    """Render candy cane wave scene"""
    width, height = screen.get_size()

    # Background
    screen.fill((240, 240, 245))

    # Stripe width and count
    num_stripes = 20
    stripe_width = width // num_stripes

    # Draw diagonal stripes with wave distortion
    for i in range(num_stripes * 2):
        # Alternate red and white
        if i % 2 == 0:
            color = (220, 30, 50)  # Red
        else:
            color = (255, 255, 255)  # White

        # Calculate diagonal stripe position
        # Stripes move to create scrolling effect
        x_offset = (i * stripe_width - _time * 50) % (num_stripes * 2 * stripe_width)

        # Draw wavy stripe using polygons
        points = []
        num_segments = 50

        for seg in range(num_segments + 1):
            y = (seg / num_segments) * height

            # Apply sine wave distortion
            wave1 = math.sin(y * 0.01 + _time * 0.5) * 30
            wave2 = math.sin(y * 0.02 - _time * 0.3) * 20

            x_left = x_offset + wave1 + wave2
            x_right = x_left + stripe_width

            # Add points for this segment
            if seg == 0:
                points.append((x_left, y))
            elif seg == num_segments:
                points.append((x_left, y))
                points.append((x_right, y))
            else:
                points.append((x_left, y))

        # Add right edge points in reverse
        for seg in range(num_segments, -1, -1):
            y = (seg / num_segments) * height
            wave1 = math.sin(y * 0.01 + _time * 0.5) * 30
            wave2 = math.sin(y * 0.02 - _time * 0.3) * 20
            x_right = x_offset + stripe_width + wave1 + wave2
            points.append((x_right, y))

        # Draw the stripe
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)

    # Add some sparkle effects
    sparkle_positions = [
        (width * 0.2, height * 0.3),
        (width * 0.7, height * 0.5),
        (width * 0.4, height * 0.7),
        (width * 0.8, height * 0.2),
        (width * 0.5, height * 0.6),
    ]

    for i, (base_x, base_y) in enumerate(sparkle_positions):
        # Animate sparkles
        pulse = math.sin(_time * 2 + i * math.pi / 3)

        if pulse > 0.5:
            # Draw star sparkle
            sparkle_size = 15 + 10 * pulse
            sparkle_x = int(base_x)
            sparkle_y = int(base_y)

            # 4-pointed star
            points = [
                (sparkle_x, sparkle_y - sparkle_size),
                (sparkle_x + 3, sparkle_y - 3),
                (sparkle_x + sparkle_size, sparkle_y),
                (sparkle_x + 3, sparkle_y + 3),
                (sparkle_x, sparkle_y + sparkle_size),
                (sparkle_x - 3, sparkle_y + 3),
                (sparkle_x - sparkle_size, sparkle_y),
                (sparkle_x - 3, sparkle_y - 3),
            ]

            # White sparkle with transparency
            sparkle_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            alpha = int(200 * pulse)
            pygame.draw.polygon(sparkle_surf, (255, 255, 255, alpha), points)
            screen.blit(sparkle_surf, (0, 0))

    # Add subtle vignette
    vignette_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(vignette_surf, (0, 0, 0, 30), (0, 0, width, height))
    pygame.draw.ellipse(vignette_surf, (0, 0, 0, 0), (width // 6, height // 6, width * 2 // 3, height * 2 // 3))
    screen.blit(vignette_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
