#!/usr/bin/env python3
"""
VERTICAL 4: Enterprise / Industrial Demo
Warehouse safety zones and task overlay
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame

class IndustrialDemo(MotiBeamScene):
    def __init__(self):
        super().__init__(title="MotiBeam - Industrial Safety")
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        # Header
        self.draw_header("INDUSTRIAL SAFETY", "Smart Warehouse Zone Management")
        
        # Split screen into zones
        zone_height = 200
        zone_y_start = 250
        
        # SAFE ZONE (Green)
        safe_zone = pygame.Rect(50, zone_y_start, (self.width - 100) // 2 - 20, zone_height)
        pygame.draw.rect(self.screen, self.colors['green'], safe_zone, 5)
        pygame.draw.rect(self.screen, (0, 40, 20), safe_zone)  # Dark green fill
        
        safe_text = self.font_large.render("SAFE ZONE", True, self.colors['green'])
        safe_rect = safe_text.get_rect(center=(safe_zone.centerx, safe_zone.centery - 30))
        self.screen.blit(safe_text, safe_rect)
        
        safe_info = self.font_small.render("Personnel Allowed", True, self.colors['white'])
        safe_info_rect = safe_info.get_rect(center=(safe_zone.centerx, safe_zone.centery + 30))
        self.screen.blit(safe_info, safe_info_rect)
        
        # ACTIVE ZONE (Yellow/Orange)
        active_zone = pygame.Rect(self.width//2 + 20, zone_y_start, (self.width - 100) // 2 - 20, zone_height)
        pygame.draw.rect(self.screen, self.colors['orange'], active_zone, 5)
        pygame.draw.rect(self.screen, (40, 30, 0), active_zone)  # Dark orange fill
        
        active_text = self.font_large.render("FORKLIFT ACTIVE", True, self.colors['orange'])
        active_rect = active_text.get_rect(center=(active_zone.centerx, active_zone.centery - 30))
        self.screen.blit(active_text, active_rect)
        
        active_info = self.font_small.render("⚠ Caution Required", True, self.colors['white'])
        active_info_rect = active_info.get_rect(center=(active_zone.centerx, active_zone.centery + 30))
        self.screen.blit(active_info, active_info_rect)
        
        # Task overlay
        task_y = 500
        task_title = self.font_medium.render("CURRENT TASK", True, self.colors['cyan'])
        task_rect = task_title.get_rect(centerx=self.width//2, top=task_y)
        self.screen.blit(task_title, task_rect)
        
        task_desc = self.font_small.render("Inventory Check: Aisle 7, Rack B-14", True, self.colors['white'])
        task_desc_rect = task_desc.get_rect(centerx=self.width//2, top=task_y + 60)
        self.screen.blit(task_desc, task_desc_rect)
        
        # Footer
        self.draw_footer("Real-time zone monitoring | Task guidance overlay")
        
        # Corner markers
        self.draw_corner_markers(self.colors['cyan'])

if __name__ == "__main__":
    demo = IndustrialDemo()
    demo.run(duration=30)
