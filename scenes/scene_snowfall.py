#!/usr/bin/env python3
"""
Snowfall Ambient Scene
Gentle snowfall with parallax effect - varying sizes and speeds
"""

import pygame
import random
import math

SCENE_NAME = "Snowfall"
SCENE_CATEGORY = "Holiday"  # Can work as ambient too

# Scene state
_snowflakes = []


class Snowflake:
    """Individual snowflake with drift"""

    def __init__(self, x, y, size=None):
        self.x = x
        self.y = y
        self.size = size or random.choice([2, 3, 4, 5, 6])

        # Larger flakes fall faster (parallax)
        self.speed = self.size * 0.3 + random.uniform(0.2, 0.8)

        # Drift (horizontal movement)
        self.drift_speed = random.uniform(-0.3, 0.3)
        self.drift_offset = random.uniform(0, math.pi * 2)

        # Rotation for visual interest
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-1, 1)

    def update(self, dt):
        self.y += self.speed
        self.x += self.drift_speed

        # Gentle sine wave drift
        self.drift_offset += 0.02
        self.x += math.sin(self.drift_offset) * 0.5

        self.rotation += self.rotation_speed

    def is_off_screen(self, width, height):
        return self.y > height or self.x < -20 or self.x > width + 20


def init_scene(screen):
    """Initialize snowfall scene"""
    global _snowflakes

    _snowflakes = []

    # Pre-populate with snowflakes
    width, height = screen.get_size()
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(-height, height)
        _snowflakes.append(Snowflake(x, y))


def update_scene(dt):
    """Update snowflake positions"""
    global _snowflakes

    # Spawn new snowflakes at top
    if random.random() < 0.3:
        width = 1280  # Assume standard width
        x = random.randint(-50, width + 50)
        y = -10
        _snowflakes.append(Snowflake(x, y))

    # Update snowflakes
    height = 720  # Assume standard height
    width = 1280

    for flake in _snowflakes:
        flake.update(dt)

    # Remove off-screen snowflakes
    _snowflakes = [f for f in _snowflakes if not f.is_off_screen(width, height)]


def render_scene(screen):
    """Render snowfall scene"""
    width, height = screen.get_size()

    # Soft gradient background (dark blue-gray to lighter)
    for y in range(height):
        progress = y / height
        r = int(25 + 35 * progress)
        g = int(30 + 45 * progress)
        b = int(45 + 60 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Sort snowflakes by size for depth effect (draw smaller first)
    sorted_flakes = sorted(_snowflakes, key=lambda f: f.size)

    # Draw snowflakes
    for flake in sorted_flakes:
        # Color intensity based on size (larger = brighter for depth)
        intensity = int(150 + (flake.size / 6) * 105)
        color = (intensity, intensity, intensity)

        x = int(flake.x)
        y = int(flake.y)

        # Draw snowflake as simple circle
        pygame.draw.circle(screen, color, (x, y), flake.size)

        # Add sparkle to larger flakes
        if flake.size >= 4:
            # Small highlight
            highlight_offset = int(flake.size * 0.3)
            pygame.draw.circle(screen, (255, 255, 255), (x - highlight_offset, y - highlight_offset),
                               max(1, flake.size // 3))

        # Optional: Draw snowflake pattern for larger flakes
        if flake.size >= 5:
            # Simple cross pattern
            arm_length = flake.size + 2

            # Rotate based on flake rotation
            angle_rad = math.radians(flake.rotation)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            # Draw 4 arms
            for angle_offset in [0, 90, 180, 270]:
                angle = math.radians(angle_offset)
                dx = int(arm_length * math.cos(angle) * cos_a)
                dy = int(arm_length * math.sin(angle) * sin_a)

                pygame.draw.line(screen, (200, 220, 255), (x, y), (x + dx, y + dy), 1)

    # Subtle vignette
    vignette_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(vignette_surf, (10, 15, 25, 40), (0, 0, width, height))
    screen.blit(vignette_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
