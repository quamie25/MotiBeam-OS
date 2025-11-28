#!/usr/bin/env python3
"""
Christmas Tree Glow Holiday Scene
Stylized tree with pulsing ornaments and light strings
"""

import pygame
import random
import math

SCENE_NAME = "Christmas Tree Glow"
SCENE_CATEGORY = "Holiday"

# Scene state
_time = 0
_ornaments = []
_lights = []


class Ornament:
    """Ornament on the tree"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(6, 12)
        self.pulse_offset = random.uniform(0, math.pi * 2)

    def update(self, dt, time):
        # Pulse animation
        pass


class Light:
    """Twinkling light on tree"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 6)
        self.brightness_offset = random.uniform(0, math.pi * 2)
        self.color = random.choice([
            (255, 200, 100),  # Warm white
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
        ])


def init_scene(screen):
    """Initialize Christmas tree scene"""
    global _time, _ornaments, _lights

    _time = 0
    _ornaments = []
    _lights = []

    width, height = screen.get_size()
    tree_center_x = width // 2

    # Generate tree layers (triangular shape)
    num_layers = 12
    for layer in range(num_layers):
        layer_y = 150 + layer * 40
        layer_width = 50 + layer * 30

        # Add ornaments to this layer
        num_ornaments = 2 + layer // 2
        for i in range(num_ornaments):
            x = tree_center_x + random.randint(-layer_width, layer_width)
            y = layer_y + random.randint(-15, 15)

            color = random.choice([
                (255, 50, 50),  # Red
                (255, 215, 0),  # Gold
                (100, 200, 255),  # Blue
                (200, 50, 200),  # Purple
            ])

            _ornaments.append(Ornament(x, y, color))

        # Add lights to this layer
        num_lights = 3 + layer
        for i in range(num_lights):
            x = tree_center_x + random.randint(-layer_width, layer_width)
            y = layer_y + random.randint(-15, 15)
            _lights.append(Light(x, y))


def update_scene(dt):
    """Update tree animation"""
    global _time
    _time += dt * 0.001


def render_scene(screen):
    """Render Christmas tree scene"""
    width, height = screen.get_size()

    # Dark night background
    screen.fill((10, 10, 25))

    tree_center_x = width // 2

    # Draw tree (layered triangular shape)
    num_layers = 12
    for layer in range(num_layers):
        layer_y = 150 + layer * 40
        layer_width = 50 + layer * 30

        # Green triangle segment
        top_y = layer_y - 20
        bottom_y = layer_y + 20
        left_x = tree_center_x - layer_width
        right_x = tree_center_x + layer_width

        points = [
            (tree_center_x, top_y),
            (left_x, bottom_y),
            (right_x, bottom_y)
        ]

        # Gradient green
        green_intensity = 60 + layer * 5
        tree_color = (30, green_intensity, 30)

        pygame.draw.polygon(screen, tree_color, points)

        # Darker outline
        pygame.draw.polygon(screen, (20, 40, 20), points, 2)

    # Draw tree trunk
    trunk_width = 60
    trunk_height = 80
    trunk_rect = pygame.Rect(tree_center_x - trunk_width // 2, 150 + num_layers * 40, trunk_width, trunk_height)
    pygame.draw.rect(screen, (80, 50, 30), trunk_rect)
    pygame.draw.rect(screen, (60, 40, 20), trunk_rect, 3)

    # Draw ornaments
    for ornament in _ornaments:
        # Pulsing effect
        pulse = 0.8 + 0.2 * math.sin(_time * 2 + ornament.pulse_offset)
        size = int(ornament.size * pulse)

        # Draw ornament with glow
        glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*ornament.color, 60), (int(ornament.x), int(ornament.y)), size + 5)
        screen.blit(glow_surf, (0, 0))

        # Main ornament
        pygame.draw.circle(screen, ornament.color, (int(ornament.x), int(ornament.y)), size)

        # Highlight
        if size > 5:
            highlight_x = int(ornament.x - size * 0.3)
            highlight_y = int(ornament.y - size * 0.3)
            pygame.draw.circle(screen, (255, 255, 255), (highlight_x, highlight_y), max(2, size // 3))

    # Draw twinkling lights
    for light in _lights:
        # Twinkling brightness
        brightness = 0.5 + 0.5 * math.sin(_time * 3 + light.brightness_offset)

        # Modulate color by brightness
        color = tuple(int(c * brightness) for c in light.color)

        # Glow effect
        glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        glow_alpha = int(80 * brightness)
        pygame.draw.circle(glow_surf, (*light.color, glow_alpha), (int(light.x), int(light.y)), light.size + 8)
        screen.blit(glow_surf, (0, 0))

        # Light bulb
        pygame.draw.circle(screen, color, (int(light.x), int(light.y)), light.size)

        # Bright core
        if brightness > 0.7:
            pygame.draw.circle(screen, (255, 255, 255), (int(light.x), int(light.y)), light.size // 2)

    # Star on top
    star_x = tree_center_x
    star_y = 120
    star_size = 25

    # Glowing star
    star_pulse = 0.8 + 0.2 * math.sin(_time * 4)
    star_glow_size = int(star_size * 1.5 * star_pulse)

    glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (255, 215, 0, 100), (star_x, star_y), star_glow_size)
    screen.blit(glow_surf, (0, 0))

    # Star shape (5-pointed)
    star_points = []
    for i in range(5):
        angle = math.pi / 2 + (i * 2 * math.pi / 5)
        x = star_x + star_size * math.cos(angle)
        y = star_y - star_size * math.sin(angle)
        star_points.append((x, y))

        # Inner point
        angle_inner = angle + math.pi / 5
        inner_size = star_size * 0.4
        x_inner = star_x + inner_size * math.cos(angle_inner)
        y_inner = star_y - inner_size * math.sin(angle_inner)
        star_points.append((x_inner, y_inner))

    pygame.draw.polygon(screen, (255, 215, 0), star_points)
    pygame.draw.polygon(screen, (255, 255, 150), star_points, 2)
