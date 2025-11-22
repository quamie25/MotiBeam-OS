#!/usr/bin/env python3
"""
MotiBeam Boot Sequence - Professional Startup Screen
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math

class BootScreen(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam OS - Starting...", standalone=standalone)
        self.boot_progress = 0
        self.boot_stage = 0
        self.boot_messages = [
            "Initializing MotiBeam OS...",
            "Loading projection engine...",
            "Detecting sensors...",
            "Calibrating display...",
            "System ready!"
        ]
        
    def update(self):
        # Animate boot progress
        self.boot_progress += 0.02
        if self.boot_progress >= 1.0:
            self.boot_stage = min(self.boot_stage + 1, len(self.boot_messages) - 1)
            if self.boot_stage >= len(self.boot_messages) - 1:
                # Boot complete after 5 seconds total
                elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
                if elapsed > 5:
                    self.running = False
            self.boot_progress = 0
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        # MotiBeam logo (large text with glow effect)
        logo_text = "MotiBeam"
        logo_surf = self.font_huge.render(logo_text, True, self.colors['cyan'])
        logo_rect = logo_surf.get_rect(center=(self.width//2, 250))
        
        # Glow effect
        pulse = 0.8 + 0.2 * abs(math.sin(pygame.time.get_ticks() / 500))
        glow_color = tuple(int(c * pulse) for c in self.colors['cyan'])
        glow_surf = self.font_huge.render(logo_text, True, glow_color)
        self.screen.blit(glow_surf, logo_rect)
        
        # Tagline
        tagline = "Ambient Computing Platform"
        tagline_surf = self.font_small.render(tagline, True, self.colors['white'])
        tagline_rect = tagline_surf.get_rect(center=(self.width//2, 370))
        self.screen.blit(tagline_surf, tagline_rect)
        
        # Boot message
        if self.boot_stage < len(self.boot_messages):
            msg = self.boot_messages[self.boot_stage]
            msg_surf = self.font_medium.render(msg, True, self.colors['green'])
            msg_rect = msg_surf.get_rect(center=(self.width//2, 480))
            self.screen.blit(msg_surf, msg_rect)
        
        # Progress bar
        bar_width = 600
        bar_height = 20
        bar_x = (self.width - bar_width) // 2
        bar_y = 550
        
        # Background
        pygame.draw.rect(self.screen, self.colors['gray'], 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Progress fill
        overall_progress = (self.boot_stage + self.boot_progress) / len(self.boot_messages)
        fill_width = int(bar_width * overall_progress)
        pygame.draw.rect(self.screen, self.colors['cyan'],
                        (bar_x, bar_y, fill_width, bar_height))
        
        # Version info
        version = "v3.0 | Multi-Vertical Platform"
        version_surf = self.font_small.render(version, True, self.colors['gray'])
        version_rect = version_surf.get_rect(center=(self.width//2, self.height - 50))
        self.screen.blit(version_surf, version_rect)

if __name__ == "__main__":
    boot = BootScreen(standalone=True)
    boot.run(duration=10)
