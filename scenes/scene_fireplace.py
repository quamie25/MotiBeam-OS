#!/usr/bin/env python3
"""
Fireplace Ambient Scene
Warm gradient background with animated flickering flames
"""

import pygame
import random
import math

SCENE_NAME = "Fireplace"
SCENE_CATEGORY = "Ambient"

# Scene state
_flames = []
_embers = []
_time = 0


class Flame:
    """Individual flame particle"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(20, 60)
        self.speed = random.uniform(0.5, 2.0)
        self.flicker = random.uniform(0, math.pi * 2)
        self.life = random.randint(100, 200)
        self.max_life = self.life

    def update(self, dt):
        self.y -= self.speed
        self.life -= 1
        self.flicker += 0.1

    def is_alive(self):
        return self.life > 0


class Ember:
    """Glowing ember particle"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.speed = random.uniform(0.1, 0.5)
        self.drift_x = random.uniform(-0.5, 0.5)
        self.life = random.randint(150, 300)
        self.max_life = self.life
        self.glow = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self.y -= self.speed
        self.x += self.drift_x
        self.life -= 1
        self.glow += 0.05

    def is_alive(self):
        return self.life > 0


def init_scene(screen):
    """Initialize fireplace scene"""
    global _flames, _embers, _time
    _flames = []
    _embers = []
    _time = 0


def update_scene(dt):
    """Update flame and ember particles"""
    global _flames, _embers, _time

    _time += dt

    # Spawn new flames at bottom
    if random.random() < 0.3:
        x = random.randint(400, 880)
        y = 600
        _flames.append(Flame(x, y))

    # Spawn new embers
    if random.random() < 0.15:
        x = random.randint(300, 980)
        y = random.randint(500, 650)
        _embers.append(Ember(x, y))

    # Update and remove dead flames
    _flames = [f for f in _flames if f.is_alive()]
    for flame in _flames:
        flame.update(dt)

    # Update and remove dead embers
    _embers = [e for e in _embers if e.is_alive()]
    for ember in _embers:
        ember.update(dt)


def render_scene(screen):
    """Render fireplace scene"""
    width, height = screen.get_size()

    # Warm gradient background (dark orange to black)
    for y in range(height):
        progress = y / height
        r = int(40 * (1 - progress) + 10 * progress)
        g = int(20 * (1 - progress) + 5 * progress)
        b = int(5 * (1 - progress))
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # Draw flames
    for flame in _flames:
        alpha = flame.life / flame.max_life

        # Flame consists of multiple layers with different colors
        # Red-orange outer layer
        size = int(flame.size * (0.8 + 0.2 * math.sin(flame.flicker)))
        intensity = int(200 * alpha)
        color_outer = (255, int(100 + 50 * alpha), 0, intensity)
        pygame.draw.circle(screen, color_outer[:3], (int(flame.x), int(flame.y)), size)

        # Yellow inner layer
        size_inner = int(size * 0.6)
        color_inner = (255, 200, int(50 + 100 * alpha))
        pygame.draw.circle(screen, color_inner, (int(flame.x), int(flame.y - size * 0.2)), size_inner)

        # Bright white core (small)
        if alpha > 0.5:
            size_core = int(size * 0.3)
            pygame.draw.circle(screen, (255, 255, 200), (int(flame.x), int(flame.y - size * 0.3)), size_core)

    # Draw embers
    for ember in _embers:
        alpha = ember.life / ember.max_life
        glow = 0.7 + 0.3 * math.sin(ember.glow)

        # Orange glow
        intensity = int(255 * alpha * glow)
        color = (255, int(100 * glow), 0)

        # Ember particle
        pygame.draw.circle(screen, color, (int(ember.x), int(ember.y)), ember.size)

        # Small highlight
        if ember.size > 3:
            pygame.draw.circle(screen, (255, 200, 100), (int(ember.x), int(ember.y)), ember.size // 2)

    # Subtle foreground shadow (bottom)
    shadow_height = 150
    for y in range(shadow_height):
        alpha = int(80 * (1 - y / shadow_height))
        s = pygame.Surface((width, 1))
        s.set_alpha(alpha)
        s.fill((0, 0, 0))
        screen.blit(s, (0, height - shadow_height + y))
