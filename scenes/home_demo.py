#!/usr/bin/env python3
"""
MotiBeam OS - Smart Home / Family Dashboard
Ambient display for connected home status and family activity
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
from datetime import datetime

class HomeDashboardScene(MotiBeamScene):
    """Smart Home / Family Dashboard - Ambient home overlay"""

    def __init__(self, standalone=True):
        super().__init__(
            title="FAMILY DASHBOARD",
            standalone=standalone
        )

        # Home status data
        self.home_status = [
            {"label": "Lights", "value": "ON", "color": self.colors['green']},
            {"label": "Thermostat", "value": "72°F (Comfort Mode)", "color": self.colors['cyan']},
            {"label": "Front Door", "value": "LOCKED", "color": self.colors['green']},
            {"label": "Garage", "value": "CLOSED", "color": self.colors['green']},
            {"label": "Alarm", "value": "ARMED (STAY)", "color": self.colors['yellow']},
        ]

        # Recent activity feed
        self.recent_activity = [
            "Package delivered – 2:30 PM",
            "Front door unlocked – 3:45 PM",
            "Thermostat adjusted – 4:00 PM",
            "New message from Mom – 3:15 PM",
            "Motion detected – Backyard – 4:12 PM",
        ]

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update scene state"""
        pass

    def render(self):
        """Render the family dashboard"""
        # Black background
        self.screen.fill(self.colors['black'])

        # Title
        title_surf = self.font_large.render("🏠 FAMILY DASHBOARD", True, self.colors['cyan'])
        title_rect = title_surf.get_rect(center=(self.width//2, 60))
        self.screen.blit(title_surf, title_rect)

        # Subtitle
        subtitle_surf = self.font_small.render("Home Status • Ambient Smart Home Overlay", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(center=(self.width//2, 120))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Current time and date (centered)
        now = datetime.now()
        time_text = now.strftime("%I:%M %p")
        date_text = now.strftime("%A, %B %d, %Y")

        time_surf = self.font_huge.render(time_text, True, self.colors['green'])
        time_rect = time_surf.get_rect(center=(self.width//2, 200))
        self.screen.blit(time_surf, time_rect)

        date_surf = self.font_medium.render(date_text, True, self.colors['white'])
        date_rect = date_surf.get_rect(center=(self.width//2, 280))
        self.screen.blit(date_surf, date_rect)

        # Left column: HOME STATUS
        left_x = 250
        left_y = 360

        status_header = self.font_medium.render("HOME STATUS", True, self.colors['cyan'])
        status_header_rect = status_header.get_rect(left=left_x, top=left_y)
        self.screen.blit(status_header, status_header_rect)

        y_offset = left_y + 60
        for item in self.home_status:
            # Label
            label_surf = self.font_small.render(f"{item['label']}:", True, self.colors['white'])
            label_rect = label_surf.get_rect(left=left_x + 20, top=y_offset)
            self.screen.blit(label_surf, label_rect)

            # Value with color
            value_surf = self.font_small.render(item['value'], True, item['color'])
            value_rect = value_surf.get_rect(left=left_x + 200, top=y_offset)
            self.screen.blit(value_surf, value_rect)

            y_offset += 50

        # Right column: RECENT ACTIVITY
        right_x = 730
        right_y = 360

        activity_header = self.font_medium.render("RECENT ACTIVITY", True, self.colors['cyan'])
        activity_header_rect = activity_header.get_rect(left=right_x, top=right_y)
        self.screen.blit(activity_header, activity_header_rect)

        y_offset = right_y + 60
        for activity in self.recent_activity:
            # Activity text with bullet
            activity_text = f"• {activity}"
            activity_surf = self.font_small.render(activity_text, True, self.colors['white'])
            activity_rect = activity_surf.get_rect(left=right_x + 20, top=y_offset)
            self.screen.blit(activity_surf, activity_rect)

            y_offset += 50

        # Footer
        footer_text = "ESC – Return to Menu  |  Future: Live sync with smart devices"
        self.draw_footer(footer_text)

        # Corner markers
        self.draw_corner_markers(self.colors['blue'])

    def run(self, duration=None):
        """Main scene loop"""
        start_time = pygame.time.get_ticks()

        while self.running:
            # Check duration
            if duration and (pygame.time.get_ticks() - start_time) / 1000 > duration:
                break

            # Handle events
            self.handle_events()

            # Update
            self.update()

            # Render
            self.render()

            # Display
            pygame.display.flip()
            self.clock.tick(30)

        # Cleanup if standalone
        if self.standalone:
            pygame.quit()

if __name__ == "__main__":
    demo = HomeDashboardScene(standalone=True)
    demo.run(duration=300)  # 5 minutes
