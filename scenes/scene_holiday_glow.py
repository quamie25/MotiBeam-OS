#!/usr/bin/env python3
"""
Holiday Glow Scene
Soft pulsing gradients in festive colors - very low motion, ideal idle display
"""

import pygame
import math

SCENE_NAME = "Holiday Glow"
SCENE_CATEGORY = "Holiday"

# Scene state
_time = 0
_glow_orbs = []


class GlowOrb:
    """Soft glowing orb that pulses"""

    def __init__(self, x, y, color, size, speed):
        self.x = x
        self.y = y
        self.base_color = color
        self.size = size
        self.speed = speed
        self.phase = 0


def init_scene(screen):
    """Initialize holiday glow scene"""
    global _time, _glow_orbs

    _time = 0
    _glow_orbs = []

    width, height = screen.get_size()

    # Create several glowing orbs at different positions
    orbs_config = [
        (width * 0.25, height * 0.3, (200, 50, 50), 200, 1.0),  # Red
        (width * 0.7, height * 0.4, (50, 150, 50), 180, 0.8),  # Green
        (width * 0.5, height * 0.7, (220, 180, 50), 220, 0.6),  # Gold
        (width * 0.15, height * 0.6, (200, 100, 100), 160, 1.2),  # Light red
        (width * 0.85, height * 0.55, (100, 200, 100), 170, 0.9),  # Light green
    ]

    for x, y, color, size, speed in orbs_config:
        orb = GlowOrb(x, y, color, size, speed)
        _glow_orbs.append(orb)


def update_scene(dt):
    """Update glow animation"""
    global _time
    _time += dt * 0.0003  # Very slow


def render_scene(screen):
    """Render holiday glow scene"""
    width, height = screen.get_size()

    # Dark background gradient
    for y in range(height):
        progress = y / height
        r = int(15 + 10 * progress)
        g = int(10 + 15 * progress)
        b = int(20 + 15 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw glowing orbs with layers
    for orb in _glow_orbs:
        # Calculate pulse
        pulse = 0.6 + 0.4 * math.sin(_time * orb.speed)

        # Draw multiple layers for smooth glow
        num_layers = 8
        for layer in range(num_layers, 0, -1):
            layer_size = int(orb.size * pulse * (layer / num_layers))
            alpha = int(40 * (layer / num_layers) * pulse)

            # Create surface for this layer
            glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)

            # Blend color with alpha
            color_with_alpha = (*orb.base_color, alpha)

            pygame.draw.circle(glow_surf, color_with_alpha, (int(orb.x), int(orb.y)), layer_size)

            screen.blit(glow_surf, (0, 0))

    # Add soft blended overlay gradient
    overlay_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # Subtle color cycling
    cycle_offset = math.sin(_time * 0.5) * math.pi / 6

    # Top to bottom gradient overlay
    for y in range(0, height, 10):
        progress = y / height

        # Cycle between red and green tints
        r_tint = int(30 * (0.5 + 0.5 * math.sin(cycle_offset + progress * math.pi)))
        g_tint = int(30 * (0.5 + 0.5 * math.cos(cycle_offset + progress * math.pi)))
        b_tint = 10

        alpha = 20

        pygame.draw.rect(overlay_surf, (r_tint, g_tint, b_tint, alpha), (0, y, width, 10))

    screen.blit(overlay_surf, (0, 0))

    # Add some subtle floating particles (very sparse)
    num_particles = 15
    for i in range(num_particles):
        # Deterministic but varied positions based on time
        x_base = (i * 83) % width
        y_base = (i * 127) % height

        # Slow drift
        x = x_base + int(math.sin(_time * 0.3 + i) * 30)
        y = y_base + int(math.cos(_time * 0.2 + i * 0.5) * 20)

        # Fading in and out
        fade = 0.5 + 0.5 * math.sin(_time * 0.8 + i * 0.3)

        if fade > 0.4:
            particle_size = 2 + int(fade * 2)
            particle_alpha = int(150 * fade)

            particle_color = (220, 200, 100) if i % 2 == 0 else (200, 220, 200)

            particle_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*particle_color, particle_alpha), (x % width, y % height),
                               particle_size)
            screen.blit(particle_surf, (0, 0))
