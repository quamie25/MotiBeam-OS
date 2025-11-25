#!/usr/bin/env python3
"""
VERTICAL 1: Clinical & Wellness - Enhanced with Sub-Menu
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
from datetime import datetime

class ClinicalWellnessEnhanced(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Clinical & Wellness", standalone=standalone)
        self.current_screen = "menu"
        
        # Data
        self.medications = [
            {"name": "Morning Vitamins", "time": "8:00 AM", "status": "due"},
            {"name": "Blood Pressure Med", "time": "12:00 PM", "status": "taken"},
            {"name": "Evening Supplement", "time": "6:00 PM", "status": "upcoming"},
        ]
        
        self.wellness = [
            {"metric": "💧 Hydration", "value": "6/8 glasses", "status": "good"},
            {"metric": "🚶 Steps", "value": "8,452 steps", "status": "excellent"},
            {"metric": "❤️  Heart Rate", "value": "72 bpm", "status": "normal"},
        ]
        
        self.sleep = {
            "last_night": "7.5 hours",
            "quality": "Good",
            "deep_sleep": "2.1 hours",
            "rem_sleep": "1.8 hours"
        }
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "menu":
                        self.running = False
                    else:
                        self.current_screen = "menu"
                elif event.key == pygame.K_1:
                    self.current_screen = "medication"
                elif event.key == pygame.K_2:
                    self.current_screen = "wellness"
                elif event.key == pygame.K_3:
                    self.current_screen = "sleep"
                elif event.key == pygame.K_4:
                    self.current_screen = "activity"
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        if self.current_screen == "menu":
            self.render_menu()
        elif self.current_screen == "medication":
            self.render_medication()
        elif self.current_screen == "wellness":
            self.render_wellness()
        elif self.current_screen == "sleep":
            self.render_sleep()
        elif self.current_screen == "activity":
            self.render_activity()
        
    def render_menu(self):
        self.draw_header("CLINICAL & WELLNESS", "Select Feature")

        menu_items = [
            ("1", "💊 Medication Schedule", self.colors['green']),
            ("2", "💪 Wellness Tracker", self.colors['cyan']),
            ("3", "😴 Sleep Analysis", self.colors['blue']),
            ("4", "📋 Activity Log", self.colors['purple']),
        ]

        y_pos = 260
        for key, name, color in menu_items:
            text = f"{key}. {name}"
            text_surf = self.font_large.render(text, True, color)
            text_rect = text_surf.get_rect(center=(self.width//2, y_pos))
            self.screen.blit(text_surf, text_rect)
            y_pos += 90
        
        self.draw_footer("Press 1-4 to select | ESC to exit")
        self.draw_corner_markers(self.colors['green'])
        
    def render_medication(self):
        self.draw_header("💊 MEDICATION SCHEDULE", datetime.now().strftime("%I:%M %p"))

        y_pos = 240
        for med in self.medications:
            if med['status'] == 'taken':
                color = self.colors['green']
                symbol = "✓"
            elif med['status'] == 'due':
                color = self.colors['orange']
                symbol = "!"
            else:
                color = self.colors['white']
                symbol = "◦"
                
            text = f"{symbol}  {med['name']} - {med['time']}"
            text_surf = self.font_medium.render(text, True, color)
            self.screen.blit(text_surf, (200, y_pos))
            y_pos += 70
        
        self.draw_footer("Voice: 'Medication taken' | ESC for menu")
        self.draw_corner_markers(self.colors['green'])
        
    def render_wellness(self):
        self.draw_header("💪 WELLNESS TRACKER", "Today's Metrics")

        y_pos = 240
        for item in self.wellness:
            name_surf = self.font_medium.render(item['metric'], True, self.colors['cyan'])
            self.screen.blit(name_surf, (200, y_pos))
            
            value_surf = self.font_large.render(item['value'], True, self.colors['white'])
            self.screen.blit(value_surf, (200, y_pos + 50))
            
            if item['status'] == 'excellent':
                status_color = self.colors['green']
            elif item['status'] == 'good':
                status_color = self.colors['cyan']
            else:
                status_color = self.colors['white']
            
            status_surf = self.font_small.render(item['status'].upper(), True, status_color)
            self.screen.blit(status_surf, (self.width - 300, y_pos + 50))
            
            y_pos += 130
        
        self.draw_footer("ESC for menu")
        self.draw_corner_markers(self.colors['cyan'])
        
    def render_sleep(self):
        self.draw_header("😴 SLEEP ANALYSIS", "Last Night")

        duration_surf = self.font_huge.render(self.sleep['last_night'], True, self.colors['blue'])
        duration_rect = duration_surf.get_rect(center=(self.width//2, 300))
        self.screen.blit(duration_surf, duration_rect)

        quality_text = f"Quality: {self.sleep['quality']}"
        quality_surf = self.font_large.render(quality_text, True, self.colors['green'])
        quality_rect = quality_surf.get_rect(center=(self.width//2, 420))
        self.screen.blit(quality_surf, quality_rect)

        y_pos = 510
        breakdown = [
            f"Deep Sleep: {self.sleep['deep_sleep']}",
            f"REM Sleep: {self.sleep['rem_sleep']}"
        ]
        
        for line in breakdown:
            line_surf = self.font_medium.render(line, True, self.colors['white'])
            line_rect = line_surf.get_rect(center=(self.width//2, y_pos))
            self.screen.blit(line_surf, line_rect)
            y_pos += 50
        
        self.draw_footer("ESC for menu")
        self.draw_corner_markers(self.colors['blue'])
        
    def render_activity(self):
        self.draw_header("📋 ACTIVITY LOG", "Recent Events")

        activities = [
            ("09:15 AM", "💊 Morning medication taken", self.colors['green']),
            ("10:30 AM", "🚶 15-minute walk completed", self.colors['cyan']),
            ("12:00 PM", "❤️  Blood pressure: 118/76", self.colors['white']),
            ("02:45 PM", "💧 Hydration reminder", self.colors['blue']),
        ]

        y_pos = 250
        for time, activity, color in activities:
            time_surf = self.font_small.render(time, True, self.colors['gray'])
            self.screen.blit(time_surf, (150, y_pos))
            
            activity_surf = self.font_medium.render(activity, True, color)
            self.screen.blit(activity_surf, (350, y_pos))
            
            y_pos += 80
        
        self.draw_footer("ESC for menu")
        self.draw_corner_markers(self.colors['purple'])

if __name__ == "__main__":
    demo = ClinicalWellnessEnhanced(standalone=True)
    demo.run(duration=300)
