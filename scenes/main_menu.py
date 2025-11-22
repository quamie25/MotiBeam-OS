#!/usr/bin/env python3
"""
MotiBeam Main Menu - Vertical Selection
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame

class MainMenu(MotiBeamScene):
    def __init__(self):
        super().__init__(title="MotiBeam OS - Main Menu")
        self.verticals = [
            {"name": "Clinical & Wellness", "key": "1", "color": self.colors['green']},
            {"name": "Automotive Safety", "key": "2", "color": self.colors['yellow']},
            {"name": "Emergency Systems", "key": "3", "color": self.colors['red']},
            {"name": "Enterprise/Industrial", "key": "4", "color": self.colors['cyan']},
            {"name": "Security/Government", "key": "5", "color": self.colors['orange']},
            {"name": "Education/Learning", "key": "6", "color": self.colors['purple']},
        ]
        self.selected = None
        
    def handle_events(self):
        """Handle menu selection"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.selected = "clinical"
                    self.running = False
                elif event.key == pygame.K_2:
                    self.selected = "automotive"
                    self.running = False
                elif event.key == pygame.K_3:
                    self.selected = "emergency"
                    self.running = False
                elif event.key == pygame.K_4:
                    self.selected = "industrial"
                    self.running = False
                elif event.key == pygame.K_5:
                    self.selected = "security"
                    self.running = False
                elif event.key == pygame.K_6:
                    self.selected = "education"
                    self.running = False
                elif event.key == pygame.K_a:
                    self.selected = "all"
                    self.running = False
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        # Header
        logo = self.font_huge.render("MotiBeam OS", True, self.colors['cyan'])
        logo_rect = logo.get_rect(center=(self.width//2, 120))
        self.screen.blit(logo, logo_rect)
        
        tagline = self.font_small.render("Multi-Vertical Ambient Computing Platform", True, self.colors['white'])
        tagline_rect = tagline.get_rect(center=(self.width//2, 200))
        self.screen.blit(tagline, tagline_rect)
        
        # Menu items
        y_start = 280
        y_spacing = 60
        
        title_surf = self.font_medium.render("SELECT VERTICAL:", True, self.colors['cyan'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=y_start)
        self.screen.blit(title_surf, title_rect)
        
        y_pos = y_start + 70
        for vertical in self.verticals:
            text = f"{vertical['key']}. {vertical['name']}"
            text_surf = self.font_small.render(text, True, vertical['color'])
            text_rect = text_surf.get_rect(centerx=self.width//2, top=y_pos)
            self.screen.blit(text_surf, text_rect)
            y_pos += y_spacing
        
        # Run all option
        all_text = "A. Run All Demos"
        all_surf = self.font_small.render(all_text, True, self.colors['white'])
        all_rect = all_surf.get_rect(center=(self.width//2, y_pos + 20))
        self.screen.blit(all_surf, all_rect)
        
        # Footer
        self.draw_footer("Press number key to select | ESC to exit")
        
        # Corner markers
        self.draw_corner_markers()

if __name__ == "__main__":
    menu = MainMenu()
    menu.run(duration=300)  # 5 minutes timeout
    print(f"Selected: {menu.selected}")
