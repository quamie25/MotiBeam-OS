#!/usr/bin/env python3
"""
Neon Sunset Ambient Scene
Vaporwave/retro style sunset with horizon and scanlines
"""

import pygame
import math

SCENE_NAME = "Neon Sunset"
SCENE_CATEGORY = "Ambient"

# Scene state
_time = 0


def init_scene(screen):
    """Initialize neon sunset scene"""
    global _time
    _time = 0


def update_scene(dt):
    """Update sunset animation"""
    global _time
    _time += dt * 0.0005  # Very slow movement


def render_scene(screen):
    """Render neon sunset scene"""
    width, height = screen.get_size()

    # Gradient background (purple/pink to orange)
    for y in range(height):
        progress = y / height

        if progress < 0.5:
            # Sky: purple to pink
            sky_progress = progress * 2
            r = int(80 + 120 * sky_progress)
            g = int(40 + 60 * sky_progress)
            b = int(120 - 40 * sky_progress)
        else:
            # Lower: pink to orange
            lower_progress = (progress - 0.5) * 2
            r = int(200 + 55 * lower_progress)
            g = int(100 + 55 * lower_progress)
            b = int(80 - 80 * lower_progress)

        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Horizon line
    horizon_y = int(height * 0.55)

    # Draw grid floor (perspective grid)
    grid_color = (255, 100, 200)
    grid_lines = 15
    grid_spacing = 30

    for i in range(grid_lines):
        # Horizontal lines
        y = horizon_y + i * grid_spacing

        # Create perspective by making lines thinner at distance
        line_width = max(1, 3 - i // 5)

        # Slight wave effect
        wave_offset = int(math.sin(_time * 2 + i * 0.3) * 5)

        if y < height:
            pygame.draw.line(screen, grid_color, (0, y + wave_offset), (width, y + wave_offset), line_width)

    # Vertical grid lines (perspective)
    num_vertical = 20
    for i in range(num_vertical):
        # Calculate perspective
        x_top = (i / num_vertical) * width
        x_bottom_left = width * 0.2
        x_bottom_right = width * 0.8
        x_bottom = x_bottom_left + (x_bottom_right - x_bottom_left) * (i / num_vertical)

        # Draw line from horizon to bottom
        pygame.draw.line(screen, grid_color, (int(x_top), horizon_y), (int(x_bottom), height), 1)

    # Sun circle with glow
    sun_y = horizon_y - 80
    sun_x = width // 2

    # Animated sun position (slight movement)
    sun_x += int(math.sin(_time * 0.5) * 20)

    # Glow layers
    for glow_size in range(5, 0, -1):
        glow_radius = 50 + glow_size * 15
        alpha = 30 * glow_size

        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 150 - glow_size * 20, 200, alpha), (sun_x, sun_y), glow_radius)
        screen.blit(surf, (0, 0))

    # Main sun
    sun_radius = 50
    pygame.draw.circle(screen, (255, 200, 100), (sun_x, sun_y), sun_radius)

    # Sun inner glow
    pygame.draw.circle(screen, (255, 255, 150), (sun_x, sun_y), sun_radius - 10)

    # Horizontal scanlines overlay
    scanline_spacing = 4
    for y in range(0, height, scanline_spacing):
        alpha = int(20 + 10 * math.sin(_time * 3 + y * 0.1))
        surf = pygame.Surface((width, 2), pygame.SRCALPHA)
        surf.fill((0, 0, 0, alpha))
        screen.blit(surf, (0, y))

    # Reflection effect on grid (below horizon)
    reflection_surf = pygame.Surface((width, height - horizon_y), pygame.SRCALPHA)
    reflection_surf.fill((255, 200, 100, 30))
    screen.blit(reflection_surf, (0, horizon_y))
