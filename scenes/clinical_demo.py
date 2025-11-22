#!/usr/bin/env python3
"""
VERTICAL 1: Clinical & Wellness Demo
Medication adherence and wellness routine projection
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
from datetime import datetime

class ClinicalWellnessDemo(MotiBeamScene):
    def __init__(self):
        super().__init__(title="MotiBeam - Clinical & Wellness")
        
        # Medication schedule
        self.medications = [
            {"name": "Morning Vitamins", "time": "8:00 AM", "status": "due"},
            {"name": "Blood Pressure Med", "time": "12:00 PM", "status": "taken"},
            {"name": "Evening Supplement", "time": "6:00 PM", "status": "upcoming"},
        ]
        
        # Wellness reminders
        self.wellness = [
            "💧 Hydrate - 6 glasses today",
            "🚶 Walk - 15 minutes completed",
            "😴 Sleep - 7.5 hours last night",
        ]
        
    def render(self):
        self.screen.fill(self.colors['black'])
        
        # Header
        self.draw_header("CLINICAL & WELLNESS", "Medication Adherence System")
        
        # Current time
        current_time = datetime.now().strftime("%I:%M %p")
        time_surf = self.font_medium.render(current_time, True, self.colors['green'])
        time_rect = time_surf.get_rect(centerx=self.width//2, top=250)
        self.screen.blit(time_surf, time_rect)
        
        # Medication schedule
        y_pos = 350
        title_surf = self.font_small.render("MEDICATION SCHEDULE", True, self.colors['cyan'])
        self.screen.blit(title_surf, (100, y_pos))
        
        y_pos += 60
        for med in self.medications:
            # Status indicator
            if med['status'] == 'taken':
                color = self.colors['green']
                symbol = "✓"
            elif med['status'] == 'due':
                color = self.colors['orange']
                symbol = "!"
            else:
                color = self.colors['white']
                symbol = "◦"
                
            # Draw medication entry
            text = f"{symbol}  {med['name']} - {med['time']}"
            med_surf = self.font_small.render(text, True, color)
            self.screen.blit(med_surf, (120, y_pos))
            y_pos += 50
            
        # Wellness metrics (right side)
        y_pos = 350
        wellness_title = self.font_small.render("WELLNESS TRACKER", True, self.colors['blue'])
        self.screen.blit(wellness_title, (self.width - 580, y_pos))
        
        y_pos += 60
        for item in self.wellness:
            item_surf = self.font_small.render(item, True, self.colors['white'])
            self.screen.blit(item_surf, (self.width - 560, y_pos))
            y_pos += 50
            
        # Footer with instructions
        self.draw_footer("Voice: 'Medication taken' | Gesture: Nod to confirm")
        
        # Corner markers
        self.draw_corner_markers(self.colors['green'])

if __name__ == "__main__":
    demo = ClinicalWellnessDemo()
    demo.run(duration=30)  # Run for 30 seconds
