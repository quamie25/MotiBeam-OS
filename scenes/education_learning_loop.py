#!/usr/bin/env python3
"""
MotiBeam OS - Education Learning Loop
Continuous ambient learning with rotating study materials
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import time

class EducationLearningLoop(MotiBeamScene):
    """Continuous learning loop with fade animations - optimized for Pi"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Learning Loop", standalone=standalone)

        # Learning items - vocabulary, facts, formulas, principles
        self.items = [
            # Science
            {"title": "Biology", "content": "Mitochondria produce ATP energy for cells"},
            {"title": "Chemistry", "content": "Water (H₂O) is the universal solvent"},
            {"title": "Physics", "content": "E = mc² - Energy equals mass times speed of light squared"},
            {"title": "Biology", "content": "DNA contains the genetic blueprint for life"},
            {"title": "Astronomy", "content": "Light from the Sun takes 8 minutes to reach Earth"},

            # Math
            {"title": "Math", "content": "Quadratic formula: x = (-b ± √(b²-4ac)) / 2a"},
            {"title": "Math", "content": "Pythagorean theorem: a² + b² = c²"},
            {"title": "Math", "content": "Area of circle: A = πr²"},
            {"title": "Math", "content": "Slope formula: m = (y₂-y₁) / (x₂-x₁)"},
            {"title": "Math", "content": "Sum of angles in a triangle = 180°"},

            # History
            {"title": "History", "content": "The Roman Empire fell in 476 AD"},
            {"title": "History", "content": "World War II ended in 1945"},
            {"title": "History", "content": "The Renaissance began in 14th century Italy"},
            {"title": "History", "content": "The printing press was invented around 1440"},
            {"title": "History", "content": "American Declaration of Independence: July 4, 1776"},

            # Languages
            {"title": "Spanish", "content": "Hola = Hello | Buenos días = Good morning"},
            {"title": "Spanish", "content": "Gracias = Thank you | Por favor = Please"},
            {"title": "French", "content": "Bonjour = Hello | Merci = Thank you"},
            {"title": "German", "content": "Guten Tag = Good day | Danke = Thank you"},
            {"title": "Latin", "content": "Carpe diem = Seize the day"},

            # Psychology & Learning
            {"title": "Psychology", "content": "Memory improves with spaced repetition"},
            {"title": "Psychology", "content": "The brain can form new neural connections at any age"},
            {"title": "Learning", "content": "Active recall strengthens memory more than re-reading"},
            {"title": "Learning", "content": "Sleep consolidates memories from the day"},
            {"title": "Learning", "content": "Teaching others is one of the best ways to learn"},

            # Productivity
            {"title": "Productivity", "content": "Deep work improves focus by 4×"},
            {"title": "Productivity", "content": "The Pomodoro Technique: 25 min work, 5 min break"},
            {"title": "Productivity", "content": "Batch similar tasks to reduce context switching"},
            {"title": "Productivity", "content": "Morning hours often have peak mental clarity"},
            {"title": "Productivity", "content": "Break large goals into small, actionable steps"},

            # Literature & Writing
            {"title": "Literature", "content": "Shakespeare wrote 37 plays and 154 sonnets"},
            {"title": "Writing", "content": "Show, don't tell - engage the reader's senses"},
            {"title": "Writing", "content": "Every sentence should serve a purpose"},
            {"title": "Grammar", "content": "Subject-verb agreement is essential for clarity"},

            # Philosophy
            {"title": "Philosophy", "content": "Socrates: The unexamined life is not worth living"},
            {"title": "Philosophy", "content": "Descartes: I think, therefore I am"},
            {"title": "Philosophy", "content": "Aristotle: We are what we repeatedly do"},

            # Computer Science
            {"title": "Programming", "content": "Functions reduce code duplication and improve clarity"},
            {"title": "Programming", "content": "Variables store data that can change during execution"},
            {"title": "CS", "content": "Algorithms are step-by-step problem-solving procedures"},

            # Geography
            {"title": "Geography", "content": "Mount Everest is 8,849 meters tall"},
            {"title": "Geography", "content": "The Amazon River is the largest by volume"},
            {"title": "Geography", "content": "Africa has 54 countries, the most of any continent"},

            # Economics
            {"title": "Economics", "content": "Supply and demand determine market prices"},
            {"title": "Economics", "content": "Compound interest: A = P(1 + r/n)^(nt)"},

            # Health
            {"title": "Health", "content": "7-9 hours of sleep per night supports optimal health"},
            {"title": "Health", "content": "Regular exercise improves both physical and mental health"},
            {"title": "Nutrition", "content": "Hydration is essential - drink water throughout the day"},
        ]

        # Animation state
        self.current_index = 0
        self.phase = "fade_in"  # fade_in, hold, fade_out
        self.phase_start = time.time()

        # Timing (seconds) - optimized for learning retention
        self.FADE_IN = 1.2
        self.HOLD = 7.0
        self.FADE_OUT = 1.2

        # Manual navigation
        self.auto_advance = True
        self.last_manual_input = time.time()

    def handle_events(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RIGHT:
                    # Manual advance to next
                    self.current_index = (self.current_index + 1) % len(self.items)
                    self.phase = "fade_in"
                    self.phase_start = time.time()
                    self.last_manual_input = time.time()
                    self.auto_advance = False
                elif event.key == pygame.K_LEFT:
                    # Manual go back
                    self.current_index = (self.current_index - 1) % len(self.items)
                    self.phase = "fade_in"
                    self.phase_start = time.time()
                    self.last_manual_input = time.time()
                    self.auto_advance = False

    def update(self):
        """Update animation phase and auto-advance"""
        now = time.time()
        elapsed = now - self.phase_start

        # Re-enable auto-advance after 10 seconds of no manual input
        if not self.auto_advance and (now - self.last_manual_input) > 10.0:
            self.auto_advance = True

        # State machine for fade animations
        if self.phase == "fade_in":
            if elapsed >= self.FADE_IN:
                self.phase = "hold"
                self.phase_start = now
        elif self.phase == "hold":
            if elapsed >= self.HOLD:
                self.phase = "fade_out"
                self.phase_start = now
        elif self.phase == "fade_out":
            if elapsed >= self.FADE_OUT:
                if self.auto_advance:
                    # Auto-advance to next item
                    self.current_index = (self.current_index + 1) % len(self.items)
                self.phase = "fade_in"
                self.phase_start = now

    def get_alpha(self):
        """Calculate current alpha value based on phase"""
        elapsed = time.time() - self.phase_start

        if self.phase == "fade_in":
            progress = min(elapsed / self.FADE_IN, 1.0)
            # Ease-out for smoother fade
            alpha = int(255 * progress)
        elif self.phase == "hold":
            alpha = 255
        elif self.phase == "fade_out":
            progress = min(elapsed / self.FADE_OUT, 1.0)
            # Ease-in for smoother fade
            alpha = int(255 * (1.0 - progress))
        else:
            alpha = 0

        return max(0, min(255, alpha))

    def render(self):
        """Render current learning item with fade effect"""
        # Pure black background
        self.screen.fill((0, 0, 0))

        # Get current item and alpha
        item = self.items[self.current_index]
        alpha = self.get_alpha()

        # Create text surfaces
        title_surf = self.font_medium.render("Learning Loop", True, (120, 80, 200))
        title_surf.set_alpha(min(alpha, 180))  # Slightly dimmer title

        subject_surf = self.font_large.render(item["title"], True, (100, 200, 255))
        subject_surf.set_alpha(alpha)

        content_surf = self.font_medium.render(item["content"], True, (220, 220, 230))
        content_surf.set_alpha(alpha)

        # Position elements
        # Top title
        title_rect = title_surf.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Subject category (middle-upper)
        subject_rect = subject_surf.get_rect(center=(self.width // 2, self.height // 2 - 80))
        self.screen.blit(subject_surf, subject_rect)

        # Main content (center)
        content_rect = content_surf.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(content_surf, content_rect)

        # Progress indicator (subtle)
        progress_text = f"{self.current_index + 1} / {len(self.items)}"
        progress_surf = self.font_small.render(progress_text, True, (80, 80, 90))
        progress_surf.set_alpha(100)
        progress_rect = progress_surf.get_rect(center=(self.width // 2, self.height - 80))
        self.screen.blit(progress_surf, progress_rect)

        # Controls hint (very subtle)
        if self.auto_advance:
            hint = "Auto-loop active  |  ← → to navigate  |  ESC to exit"
        else:
            hint = "Manual mode  |  ← → to navigate  |  ESC to exit"
        hint_surf = self.font_small.render(hint, True, (60, 60, 70))
        hint_surf.set_alpha(80)
        hint_rect = hint_surf.get_rect(center=(self.width // 2, self.height - 40))
        self.screen.blit(hint_surf, hint_rect)

if __name__ == "__main__":
    loop = EducationLearningLoop(standalone=True)
    loop.run(duration=300)  # 5 minutes
