#!/usr/bin/env python3
"""
Rain Ambient Scene
Dark bluish background with falling raindrops and splash effects
"""

import pygame
import random

SCENE_NAME = "Rain"
SCENE_CATEGORY = "Ambient"

# Scene state
_raindrops = []
_splashes = []


class Raindrop:
    """Individual raindrop"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(8, 15)
        self.length = random.randint(10, 25)
        self.thickness = random.choice([1, 2])

    def update(self, dt):
        self.y += self.speed

    def is_off_screen(self, height):
        return self.y > height


class Splash:
    """Raindrop splash effect"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 10
        self.max_life = 10
        self.size = random.randint(3, 8)

    def update(self, dt):
        self.life -= 1

    def is_alive(self):
        return self.life > 0


def init_scene(screen):
    """Initialize rain scene"""
    global _raindrops, _splashes

    _raindrops = []
    _splashes = []

    # Pre-populate with raindrops
    width, height = screen.get_size()
    for _ in range(150):
        x = random.randint(0, width)
        y = random.randint(-height, height)
        _raindrops.append(Raindrop(x, y))


def update_scene(dt):
    """Update raindrops and splashes"""
    global _raindrops, _splashes

    # Spawn new raindrops at top
    if random.random() < 0.5:
        width = 1280  # Assume standard width
        x = random.randint(0, width)
        y = -20
        _raindrops.append(Raindrop(x, y))

    # Update raindrops
    height = 720  # Assume standard height
    for drop in _raindrops:
        drop.update(dt)

        # Create splash when hitting bottom
        if drop.y >= height - 10:
            _splashes.append(Splash(drop.x, height - 10))

    # Remove off-screen raindrops
    _raindrops = [d for d in _raindrops if not d.is_off_screen(height)]

    # Update splashes
    _splashes = [s for s in _splashes if s.is_alive()]
    for splash in _splashes:
        splash.update(dt)


def render_scene(screen):
    """Render rain scene"""
    width, height = screen.get_size()

    # Dark bluish gradient background
    for y in range(height):
        progress = y / height
        r = int(15 + 20 * progress)
        g = int(20 + 30 * progress)
        b = int(35 + 45 * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw raindrops
    for drop in _raindrops:
        # Raindrop is a vertical line
        start_pos = (int(drop.x), int(drop.y))
        end_pos = (int(drop.x), int(drop.y + drop.length))

        # Color with slight transparency
        color = (150, 180, 220)

        if drop.thickness == 1:
            pygame.draw.line(screen, color, start_pos, end_pos, 1)
        else:
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

    # Draw splashes
    for splash in _splashes:
        alpha = splash.life / splash.max_life

        # Splash is expanding circles
        size = int(splash.size * (1 - alpha))
        if size > 0:
            intensity = int(200 * alpha)
            color = (100 + intensity // 2, 150 + intensity // 3, 200 + intensity // 4)

            # Outer ring
            pygame.draw.circle(screen, color, (int(splash.x), int(splash.y)), size, 1)

            # Inner ring
            if size > 2:
                pygame.draw.circle(screen, color, (int(splash.x), int(splash.y)), size // 2, 1)

    # Ambient fog/mist layer (subtle)
    fog_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(50, 150)
        pygame.draw.circle(fog_surf, (200, 220, 240, 5), (x, y), size)

    screen.blit(fog_surf, (0, 0))
