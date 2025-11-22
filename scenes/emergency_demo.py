#!/usr/bin/env python3
"""
VERTICAL 3: Emergency / Maritime / Aviation Demo
Emergency exit and evacuation route projection
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math

class EmergencyDemo(MotiBeamScene):
    def __init__(self):
        super().__init__(title="MotiBeam - Emergency Systems")
        self.flash_state = 0
        
    def update(self):
        self.flash_state = (self.flash_state + 1) % 30
        
    def render(self):
        # Flashing background for urgency
        if self.flash_state < 15:
            self.screen.fill((20, 0, 0))  # Dark red
        else:
            self.screen.fill(self.colors['black'])
        
        # Header with alert color
        self.draw_header("EMERGENCY ALERT", "Evacuation System Active")
        
        # Main alert message
        alert_surf = self.font_huge.render("EMERGENCY EXIT", True, self.colors['red'])
        alert_rect = alert_surf.get_rect(center=(self.width//2, 280))
        self.screen.blit(alert_surf, alert_rect)
        
        # Large directional arrow
        arrow_x = self.width - 300
        arrow_y = 400
        arrow_size = 80
        
        # Right-pointing arrow
        points = [
            (arrow_x + arrow_size, arrow_y),
            (arrow_x, arrow_y - arrow_size),
            (arrow_x, arrow_y + arrow_size)
        ]
        pygame.draw.polygon(self.screen, self.colors['red'], points)
        
        # Arrow stem
        pygame.draw.rect(self.screen, self.colors['red'],
                        (arrow_x - 200, arrow_y - 30, 200, 60))
        
        # Route information
        route_text = "EVACUATION ROUTE B"
        route_surf = self.font_large.render(route_text, True, self.colors['orange'])
        route_rect = route_surf.get_rect(center=(self.width//2, 500))
        self.screen.blit(route_surf, route_rect)
        
        # Distance to exit
        distance_text = "150 FEET TO SAFETY"
        dist_surf = self.font_medium.render(distance_text, True, self.colors['white'])
        dist_rect = dist_surf.get_rect(center=(self.width//2, 580))
        self.screen.blit(dist_surf, dist_rect)
        
        # Footer with emergency info
        self.draw_footer("REMAIN CALM | FOLLOW PROJECTED PATH | DO NOT USE ELEVATORS")
        
        # Corner markers in red
        self.draw_corner_markers(self.colors['red'])

if __name__ == "__main__":
    demo = EmergencyDemo()
    demo.run(duration=30)
