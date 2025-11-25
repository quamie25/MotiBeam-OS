#!/usr/bin/env python3
"""
VERTICAL 3: Emergency / Maritime / Aviation Demo
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame

class EmergencyDemo(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Emergency Systems", standalone=standalone)
        self.flash_state = 0
        
    def update(self):
        self.flash_state = (self.flash_state + 1) % 30
        
    def render(self):
        if self.flash_state < 15:
            self.screen.fill((20, 0, 0))
        else:
            self.screen.fill(self.colors['black'])
        
        self.draw_header("🚨 EMERGENCY ALERT", "Evacuation System Active")

        # Emergency banner positioned lower for better vertical centering
        banner_y = 250
        alert_surf = self.font_huge.render("EMERGENCY EXIT", True, self.colors['red'])
        alert_rect = alert_surf.get_rect(center=(self.width//2, banner_y))
        self.screen.blit(alert_surf, alert_rect)

        arrow_x = self.width - 300
        arrow_y = banner_y + 120
        arrow_size = 80
        
        points = [
            (arrow_x + arrow_size, arrow_y),
            (arrow_x, arrow_y - arrow_size),
            (arrow_x, arrow_y + arrow_size)
        ]
        pygame.draw.polygon(self.screen, self.colors['red'], points)
        pygame.draw.rect(self.screen, self.colors['red'],
                        (arrow_x - 200, arrow_y - 30, 200, 60))
        
        route_text = "EVACUATION ROUTE B"
        route_surf = self.font_large.render(route_text, True, self.colors['orange'])
        route_rect = route_surf.get_rect(center=(self.width//2, banner_y + 230))
        self.screen.blit(route_surf, route_rect)

        distance_text = "150 FEET TO SAFETY"
        dist_surf = self.font_medium.render(distance_text, True, self.colors['white'])
        dist_rect = dist_surf.get_rect(center=(self.width//2, banner_y + 310))
        self.screen.blit(dist_surf, dist_rect)
        
        self.draw_footer("REMAIN CALM | FOLLOW PROJECTED PATH")
        self.draw_corner_markers(self.colors['red'])

if __name__ == "__main__":
    demo = EmergencyDemo(standalone=True)
    demo.run(duration=30)
