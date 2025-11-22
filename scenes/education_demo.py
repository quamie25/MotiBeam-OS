#!/usr/bin/env python3
"""
VERTICAL 6: Education / Learning Demo
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame

class EducationDemo(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Education & Learning", standalone=standalone)
        self.study_items = [
            {"word": "Photosynthesis", "definition": "Process by which plants convert light into energy"},
            {"word": "Theorem", "definition": "A mathematical statement proven using logic"},
            {"word": "Catalyst", "definition": "Substance that speeds up a chemical reaction"},
        ]
        self.current_item = 0
        self.timer_seconds = 25 * 60
        
    def update(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.timer_seconds = max(0, (25 * 60) - int(elapsed))
        
    def render(self):
        self.screen.fill(self.colors['black'])
        self.draw_header("📚 STUDY SESSION", "Vocabulary & Concept Review")
        
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        timer_surf = self.font_huge.render(timer_text, True, self.colors['green'])
        timer_rect = timer_surf.get_rect(center=(self.width//2, 200))
        self.screen.blit(timer_surf, timer_rect)
        
        item = self.study_items[self.current_item]
        
        word_label = self.font_small.render("TERM:", True, self.colors['cyan'])
        word_label_rect = word_label.get_rect(centerx=self.width//2, top=300)
        self.screen.blit(word_label, word_label_rect)
        
        word_surf = self.font_large.render(item['word'], True, self.colors['white'])
        word_rect = word_surf.get_rect(center=(self.width//2, 380))
        self.screen.blit(word_surf, word_rect)
        
        def_label = self.font_small.render("DEFINITION:", True, self.colors['cyan'])
        def_label_rect = def_label.get_rect(centerx=self.width//2, top=460)
        self.screen.blit(def_label, def_label_rect)
        
        def_surf = self.font_small.render(item['definition'], True, self.colors['white'])
        def_rect = def_surf.get_rect(center=(self.width//2, 520))
        self.screen.blit(def_surf, def_rect)
        
        progress_text = f"Card {self.current_item + 1} of {len(self.study_items)}"
        progress_surf = self.font_small.render(progress_text, True, self.colors['gray'])
        progress_rect = progress_surf.get_rect(center=(self.width//2, 600))
        self.screen.blit(progress_surf, progress_rect)
        
        self.draw_footer("Focus mode: Distraction-free learning environment")
        self.draw_corner_markers(self.colors['purple'])

if __name__ == "__main__":
    demo = EducationDemo(standalone=True)
    demo.run(duration=30)
