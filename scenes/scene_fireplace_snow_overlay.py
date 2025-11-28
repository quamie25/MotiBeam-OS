#!/usr/bin/env python3
"""
Fireplace + Snow Window Holiday Scene
Combines warm fireplace (bottom) with snowy window view (top)
Creates cozy indoor/outdoor contrast
"""

import pygame
import random
import math

SCENE_NAME = "Fireplace + Snow Window"
SCENE_CATEGORY = "Holiday"

# Scene state
_flames = []
_embers = []
_snowflakes = []
_time = 0


class Flame:
    """Fireplace flame particle"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(15, 40)
        self.speed = random.uniform(0.5, 1.5)
        self.flicker = random.uniform(0, math.pi * 2)
        self.life = random.randint(80, 150)
        self.max_life = self.life

    def update(self, dt):
        self.y -= self.speed
        self.life -= 1
        self.flicker += 0.1

    def is_alive(self):
        return self.life > 0


class Ember:
    """Glowing ember"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.1, 0.4)
        self.drift_x = random.uniform(-0.3, 0.3)
        self.life = random.randint(100, 200)
        self.max_life = self.life
        self.glow = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self.y -= self.speed
        self.x += self.drift_x
        self.life -= 1
        self.glow += 0.05

    def is_alive(self):
        return self.life > 0


class Snowflake:
    """Snowflake falling outside window"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.choice([2, 3, 4])
        self.speed = self.size * 0.2 + random.uniform(0.1, 0.4)
        self.drift = random.uniform(-0.2, 0.2)

    def update(self, dt):
        self.y += self.speed
        self.x += self.drift

    def is_off_screen(self, height):
        return self.y > height


def init_scene(screen):
    """Initialize combined scene"""
    global _flames, _embers, _snowflakes, _time

    _flames = []
    _embers = []
    _snowflakes = []
    _time = 0

    # Pre-populate snowflakes
    width, height = screen.get_size()
    window_height = height // 2

    for _ in range(80):
        x = random.randint(0, width)
        y = random.randint(0, window_height)
        _snowflakes.append(Snowflake(x, y))


def update_scene(dt):
    """Update all scene elements"""
    global _flames, _embers, _snowflakes, _time

    _time += dt

    # Update fireplace (bottom half)
    if random.random() < 0.25:
        x = random.randint(450, 830)
        y = 650
        _flames.append(Flame(x, y))

    if random.random() < 0.12:
        x = random.randint(400, 880)
        y = random.randint(600, 680)
        _embers.append(Ember(x, y))

    _flames = [f for f in _flames if f.is_alive()]
    for flame in _flames:
        flame.update(dt)

    _embers = [e for e in _embers if e.is_alive()]
    for ember in _embers:
        ember.update(dt)

    # Update snowfall (top half)
    if random.random() < 0.2:
        x = random.randint(0, 1280)
        y = -10
        _snowflakes.append(Snowflake(x, y))

    for flake in _snowflakes:
        flake.update(dt)

    _snowflakes = [f for f in _snowflakes if not f.is_off_screen(360)]


def render_scene(screen):
    """Render combined fireplace and snow scene"""
    width, height = screen.get_size()
    split_y = height // 2

    # === TOP HALF: Snowy Window View ===
    # Dark blue-gray winter sky
    for y in range(split_y):
        progress = y / split_y
        r = int(40 + 30 * progress)
        g = int(50 + 40 * progress)
        b = int(70 + 50 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw snowflakes
    for flake in _snowflakes:
        color = (220, 230, 255)
        pygame.draw.circle(screen, color, (int(flake.x), int(flake.y)), flake.size)

        # Highlight
        if flake.size >= 3:
            pygame.draw.circle(screen, (255, 255, 255), (int(flake.x - 1), int(flake.y - 1)), 1)

    # Window frame overlay
    frame_color = (60, 40, 30)
    frame_width = 15

    # Horizontal divider
    pygame.draw.rect(screen, frame_color, (0, split_y - frame_width // 2, width, frame_width))

    # Vertical dividers (create panes)
    pane_width = width // 3
    for i in range(1, 3):
        x = i * pane_width
        pygame.draw.rect(screen, frame_color, (x - frame_width // 2, 0, frame_width, split_y))

    # === BOTTOM HALF: Fireplace ===
    # Warm gradient
    for y in range(split_y, height):
        progress = (y - split_y) / split_y
        r = int(40 * (1 - progress) + 15 * progress)
        g = int(25 * (1 - progress) + 10 * progress)
        b = int(10 * (1 - progress) + 5 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw flames
    for flame in _flames:
        alpha = flame.life / flame.max_life
        size = int(flame.size * (0.8 + 0.2 * math.sin(flame.flicker)))

        # Only draw if in bottom half
        if flame.y >= split_y:
            # Outer flame
            intensity = int(180 * alpha)
            color_outer = (255, int(80 + 40 * alpha), 0)
            pygame.draw.circle(screen, color_outer, (int(flame.x), int(flame.y)), size)

            # Inner flame
            size_inner = int(size * 0.6)
            color_inner = (255, 180, int(40 + 80 * alpha))
            pygame.draw.circle(screen, color_inner, (int(flame.x), int(flame.y - size * 0.2)), size_inner)

            # Core
            if alpha > 0.5:
                size_core = int(size * 0.3)
                pygame.draw.circle(screen, (255, 255, 180), (int(flame.x), int(flame.y - size * 0.3)), size_core)

    # Draw embers
    for ember in _embers:
        if ember.y >= split_y:
            alpha = ember.life / ember.max_life
            glow = 0.7 + 0.3 * math.sin(ember.glow)
            intensity = int(255 * alpha * glow)
            color = (255, int(100 * glow), 0)

            pygame.draw.circle(screen, color, (int(ember.x), int(ember.y)), ember.size)

            if ember.size > 3:
                pygame.draw.circle(screen, (255, 200, 100), (int(ember.x), int(ember.y)), ember.size // 2)

    # Fireplace hearth (decorative)
    hearth_rect = pygame.Rect(350, height - 80, 580, 80)
    pygame.draw.rect(screen, (80, 50, 30), hearth_rect)
    pygame.draw.rect(screen, (60, 40, 25), hearth_rect, 3)

    # Warm glow from fireplace
    glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    glow_intensity = int(30 + 10 * math.sin(_time * 0.002))
    pygame.draw.circle(glow_surf, (255, 100, 0, glow_intensity), (640, 640), 300)
    screen.blit(glow_surf, (0, 0))
