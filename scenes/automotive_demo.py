#!/usr/bin/env python3
"""
VERTICAL 2: Automotive Safety Demo
Projection-based pedestrian crossing and delivery notifications
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math

class AutomotiveDemo(MotiBeamScene):
    def __init__(self):
        super().__init__(title="MotiBeam - Automotive Safety")
        self.animation_offset = 0
        
    def update(self):
        # Animate the arrow
        self.animation_offset = (self.animation_offset + 5) % 100
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        # Header
        self.draw_header("AUTOMOTIVE SAFETY", "Pedestrian Crossing System")
        
        # Main message - large and bright
        msg_surf = self.font_huge.render("PLEASE CROSS", True, self.colors['yellow'])
        msg_rect = msg_surf.get_rect(center=(self.width//2, 300))
        self.screen.blit(msg_surf, msg_rect)
        
        # Animated directional arrow
        arrow_y = 450
        arrow_x = self.width//2 - 200 + self.animation_offset
        
        # Draw multiple arrows for motion effect
        for i in range(3):
            x_pos = arrow_x + (i * 100)
            if x_pos < self.width - 100:
                # Arrow triangle
                points = [
                    (x_pos, arrow_y),
                    (x_pos - 40, arrow_y - 40),
                    (x_pos - 40, arrow_y + 40)
                ]
                alpha = 255 - (i * 80)
                color = (255, 255, min(100 + alpha, 255))
                pygame.draw.polygon(self.screen, color, points)
        
        # Secondary info
        info_text = "DELIVERY FOR APT 204"
        info_surf = self.font_medium.render(info_text, True, self.colors['white'])
        info_rect = info_surf.get_rect(center=(self.width//2, 550))
        self.screen.blit(info_surf, info_rect)
        
        # Safety zone indicator
        pygame.draw.rect(self.screen, self.colors['yellow'], 
                        (50, self.height - 150, self.width - 100, 10))
        zone_text = self.font_small.render("SAFE CROSSING ZONE", True, self.colors['yellow'])
        zone_rect = zone_text.get_rect(center=(self.width//2, self.height - 100))
        self.screen.blit(zone_text, zone_rect)  # FIXED: was zone_surf, now zone_text
        
        # Footer
        self.draw_footer("Sensor: Pedestrian detected | Status: Safe to cross")
        
        # Corner markers
        self.draw_corner_markers(self.colors['yellow'])

if __name__ == "__main__":
    demo = AutomotiveDemo()
    demo.run(duration=30)
