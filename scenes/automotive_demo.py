#!/usr/bin/env python3
"""
VERTICAL 2: Automotive Safety Demo
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame

class AutomotiveDemo(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Automotive Safety", standalone=standalone)
        self.animation_offset = 0
        
    def update(self):
        self.animation_offset = (self.animation_offset + 5) % 100
        
    def render(self):
        self.screen.fill(self.colors['black'])
        self.draw_header("🚗 AUTOMOTIVE SAFETY", "Pedestrian Crossing System")
        
        msg_surf = self.font_huge.render("PLEASE CROSS", True, self.colors['yellow'])
        msg_rect = msg_surf.get_rect(center=(self.width//2, 300))
        self.screen.blit(msg_surf, msg_rect)
        
        arrow_y = 450
        arrow_x = self.width//2 - 200 + self.animation_offset
        
        for i in range(3):
            x_pos = arrow_x + (i * 100)
            if x_pos < self.width - 100:
                points = [
                    (x_pos, arrow_y),
                    (x_pos - 40, arrow_y - 40),
                    (x_pos - 40, arrow_y + 40)
                ]
                alpha = 255 - (i * 80)
                color = (255, 255, min(100 + alpha, 255))
                pygame.draw.polygon(self.screen, color, points)
        
        info_text = "DELIVERY FOR APT 204"
        info_surf = self.font_medium.render(info_text, True, self.colors['white'])
        info_rect = info_surf.get_rect(center=(self.width//2, 550))
        self.screen.blit(info_surf, info_rect)
        
        pygame.draw.rect(self.screen, self.colors['yellow'], 
                        (50, self.height - 150, self.width - 100, 10))
        zone_text = self.font_small.render("SAFE CROSSING ZONE", True, self.colors['yellow'])
        zone_rect = zone_text.get_rect(center=(self.width//2, self.height - 100))
        self.screen.blit(zone_text, zone_rect)
        
        self.draw_footer("Sensor: Pedestrian detected | Status: Safe to cross")
        self.draw_corner_markers(self.colors['yellow'])

if __name__ == "__main__":
    demo = AutomotiveDemo(standalone=True)
    demo.run(duration=30)
