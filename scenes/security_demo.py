#!/usr/bin/env python3
"""
VERTICAL 5: Security / Government Demo
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math

class SecurityDemo(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Security & Guardian", standalone=standalone)
        self.pulse = 0
        
    def update(self):
        self.pulse = (self.pulse + 0.1) % (2 * 3.14159)
        
    def render(self):
        self.screen.fill(self.colors['black'])
        self.draw_header("🛡️ GUARDIAN MODE ACTIVE", "Wellness & Safety Monitoring")

        # Guardian panel positioned for better vertical centering
        panel_top = 260
        pulse_size = 80 + int(20 * abs(math.sin(self.pulse)))
        alert_center = (self.width // 2, panel_top + 50)
        pygame.draw.circle(self.screen, self.colors['orange'], alert_center, pulse_size, 8)

        alert_symbol = self.font_huge.render("!", True, self.colors['orange'])
        alert_rect = alert_symbol.get_rect(center=alert_center)
        self.screen.blit(alert_symbol, alert_rect)

        alert_text = "INACTIVITY DETECTED"
        alert_surf = self.font_large.render(alert_text, True, self.colors['orange'])
        alert_text_rect = alert_surf.get_rect(center=(self.width//2, panel_top + 180))
        self.screen.blit(alert_surf, alert_text_rect)

        detail1 = self.font_medium.render("No movement for 2 hours", True, self.colors['white'])
        detail1_rect = detail1.get_rect(center=(self.width//2, panel_top + 260))
        self.screen.blit(detail1, detail1_rect)

        detail2 = self.font_small.render("Last activity: 3:45 PM (Kitchen)", True, self.colors['gray'])
        detail2_rect = detail2.get_rect(center=(self.width//2, panel_top + 310))
        self.screen.blit(detail2, detail2_rect)

        action_text = "Guardian notified - Check on resident"
        action_surf = self.font_medium.render(action_text, True, self.colors['cyan'])
        action_rect = action_surf.get_rect(center=(self.width//2, panel_top + 370))
        self.screen.blit(action_surf, action_rect)
        
        self.draw_footer("Monitoring: Motion | Activity | Wellness patterns")
        self.draw_corner_markers(self.colors['orange'])

if __name__ == "__main__":
    demo = SecurityDemo(standalone=True)
    demo.run(duration=30)
