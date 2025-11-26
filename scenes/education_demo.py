#!/usr/bin/env python3
"""
MotiBeam OS - Education / Learning Vertical

Modes:
- Study Session (Pomodoro timer with flashcards)
- Homework Focus Wall (distraction-free task display)
- Language Learning Wall (vocabulary practice)
- Sleep Learning Loop (ambient, auto-looping content)
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
import time

class EducationDemo(MotiBeamScene):
    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Education & Learning", standalone=standalone)

        # Modes
        self.modes = [
            "Study Session",
            "Homework Wall",
            "Language Wall",
            "Sleep Learning Loop"
        ]
        self.current_mode = None
        self.in_menu = True

        # Study Session data
        self.study_items = [
            {"word": "Photosynthesis", "definition": "Process plants use to convert light into energy"},
            {"word": "Mitochondria", "definition": "The powerhouse of the cell - generates ATP"},
            {"word": "Catalyst", "definition": "Substance that speeds up a chemical reaction"},
            {"word": "Theorem", "definition": "Mathematical statement proven using logic"},
            {"word": "Algorithm", "definition": "Step-by-step procedure for solving a problem"},
        ]
        self.current_card = 0
        self.timer_seconds = 25 * 60  # 25 minute Pomodoro

        # Homework Wall data
        self.homework_tasks = [
            {"subject": "Math", "task": "Complete Chapter 7 exercises (problems 1-20)"},
            {"subject": "History", "task": "Read pages 145-167, answer discussion questions"},
            {"subject": "Chemistry", "task": "Lab report due Friday - molecular bonding"},
        ]

        # Language Wall data
        self.language_vocab = [
            {"spanish": "Hola", "english": "Hello", "pronunciation": "OH-lah"},
            {"spanish": "Gracias", "english": "Thank you", "pronunciation": "GRAH-see-as"},
            {"spanish": "Por favor", "english": "Please", "pronunciation": "por fah-VOR"},
            {"spanish": "Buenos días", "english": "Good morning", "pronunciation": "BWAY-nos DEE-as"},
        ]
        self.current_vocab = 0

        # Sleep Learning data
        self.sleep_facts = [
            "The human brain contains approximately 86 billion neurons",
            "Your brain uses 20% of your body's total oxygen and energy",
            "The speed of information in neurons can reach up to 268 mph",
            "Your brain generates about 12-25 watts of electricity",
            "The brain can't feel pain - it has no pain receptors",
            "During sleep, your brain consolidates memories and learning",
            "Neuroplasticity allows your brain to rewire itself",
            "The average human brain weighs about 3 pounds",
        ]
        self.current_fact = 0
        self.sleep_cycle_time = 0
        self.fact_display_duration = 10  # seconds per fact

    def handle_events(self, event):
        """Handle mode-specific input"""
        if self.in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_mode = "Study Session"
                    self.in_menu = False
                    self.start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_2:
                    self.current_mode = "Homework Wall"
                    self.in_menu = False
                    self.start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_3:
                    self.current_mode = "Language Wall"
                    self.in_menu = False
                    self.start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_4:
                    self.current_mode = "Sleep Learning Loop"
                    self.in_menu = False
                    self.start_time = pygame.time.get_ticks()
                    self.sleep_cycle_time = time.time()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to mode menu
                    self.in_menu = True
                    self.current_mode = None
                elif self.current_mode == "Study Session":
                    if event.key == pygame.K_LEFT:
                        self.current_card = (self.current_card - 1) % len(self.study_items)
                    elif event.key == pygame.K_RIGHT:
                        self.current_card = (self.current_card + 1) % len(self.study_items)
                elif self.current_mode == "Language Wall":
                    if event.key == pygame.K_LEFT:
                        self.current_vocab = (self.current_vocab - 1) % len(self.language_vocab)
                    elif event.key == pygame.K_RIGHT:
                        self.current_vocab = (self.current_vocab + 1) % len(self.language_vocab)

    def update(self):
        """Update mode-specific logic"""
        if self.current_mode == "Study Session":
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            self.timer_seconds = max(0, (25 * 60) - int(elapsed))
        elif self.current_mode == "Sleep Learning Loop":
            # Auto-cycle through facts
            elapsed = time.time() - self.sleep_cycle_time
            if elapsed >= self.fact_display_duration:
                self.current_fact = (self.current_fact + 1) % len(self.sleep_facts)
                self.sleep_cycle_time = time.time()

    def render(self):
        """Render current mode or menu"""
        self.screen.fill(self.colors['black'])

        if self.in_menu:
            self.render_mode_menu()
        elif self.current_mode == "Study Session":
            self.render_study_session()
        elif self.current_mode == "Homework Wall":
            self.render_homework_wall()
        elif self.current_mode == "Language Wall":
            self.render_language_wall()
        elif self.current_mode == "Sleep Learning Loop":
            self.render_sleep_learning()

    def render_mode_menu(self):
        """Render the mode selection menu"""
        # Animated background
        t = pygame.time.get_ticks() / 1000.0
        for i in range(5):
            x = 150 + i * 250
            y = 360 + int(20 * math.sin(t + i * 0.8))
            radius = 100
            pygame.draw.circle(self.screen, (*self.colors['purple'][:3], 15), (x, y), radius, 2)

        # Header
        title = self.font_huge.render("EDUCATION", True, self.colors['purple'])
        title_rect = title.get_rect(center=(self.width//2, 100))
        self.screen.blit(title, title_rect)

        subtitle = self.font_medium.render("Learning & Focus Platform", True, self.colors['white'])
        subtitle_rect = subtitle.get_rect(center=(self.width//2, 170))
        self.screen.blit(subtitle, subtitle_rect)

        # Mode options
        menu_y = 280
        spacing = 80

        for i, mode in enumerate(self.modes):
            mode_text = f"{i+1}. {mode}"
            mode_surf = self.font_medium.render(mode_text, True, self.colors['cyan'])
            mode_rect = mode_surf.get_rect(center=(self.width//2, menu_y + i * spacing))
            self.screen.blit(mode_surf, mode_rect)

        # Footer
        footer = self.font_small.render("Select mode 1-4 | ESC to exit", True, self.colors['gray'])
        footer_rect = footer.get_rect(center=(self.width//2, self.height - 40))
        self.screen.blit(footer, footer_rect)

        # Corner markers
        self.draw_corner_markers(self.colors['purple'])

    def render_study_session(self):
        """Render Pomodoro study session with flashcards"""
        self.draw_header("📚 STUDY SESSION", "Pomodoro Focus Timer")

        # Timer
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        timer_surf = self.font_huge.render(timer_text, True, self.colors['green'])
        timer_rect = timer_surf.get_rect(center=(self.width//2, 180))
        self.screen.blit(timer_surf, timer_rect)

        # Current flashcard
        card = self.study_items[self.current_card]

        term_label = self.font_small.render("TERM:", True, self.colors['cyan'])
        term_label_rect = term_label.get_rect(centerx=self.width//2, top=280)
        self.screen.blit(term_label, term_label_rect)

        term_surf = self.font_large.render(card['word'], True, self.colors['white'])
        term_rect = term_surf.get_rect(center=(self.width//2, 350))
        self.screen.blit(term_surf, term_rect)

        def_label = self.font_small.render("DEFINITION:", True, self.colors['cyan'])
        def_label_rect = def_label.get_rect(centerx=self.width//2, top=420)
        self.screen.blit(def_label, def_label_rect)

        # Word wrap definition
        def_surf = self.font_small.render(card['definition'], True, self.colors['white'])
        def_rect = def_surf.get_rect(center=(self.width//2, 480))
        self.screen.blit(def_surf, def_rect)

        # Progress
        progress = f"Card {self.current_card + 1}/{len(self.study_items)} | ← → to navigate"
        progress_surf = self.font_small.render(progress, True, self.colors['gray'])
        progress_rect = progress_surf.get_rect(center=(self.width//2, 580))
        self.screen.blit(progress_surf, progress_rect)

        self.draw_footer("Focus mode: Distraction-free learning | ESC for menu")
        self.draw_corner_markers(self.colors['purple'])

    def render_homework_wall(self):
        """Render homework task wall"""
        self.draw_header("📝 HOMEWORK WALL", "Current Assignments")

        # Display tasks
        y_pos = 220
        for i, task in enumerate(self.homework_tasks):
            # Subject header
            subject_surf = self.font_large.render(task['subject'], True, self.colors['cyan'])
            subject_rect = subject_surf.get_rect(centerx=self.width//2, top=y_pos)
            self.screen.blit(subject_surf, subject_rect)

            # Task description
            task_surf = self.font_small.render(task['task'], True, self.colors['white'])
            task_rect = task_surf.get_rect(centerx=self.width//2, top=y_pos + 60)
            self.screen.blit(task_surf, task_rect)

            # Separator
            pygame.draw.line(self.screen, self.colors['gray'],
                           (300, y_pos + 120), (self.width - 300, y_pos + 120), 1)

            y_pos += 150

        self.draw_footer("Stay organized, stay focused | ESC for menu")
        self.draw_corner_markers(self.colors['purple'])

    def render_language_wall(self):
        """Render language learning vocabulary"""
        self.draw_header("🌍 LANGUAGE WALL", "Spanish Vocabulary")

        vocab = self.language_vocab[self.current_vocab]

        # Spanish word (large)
        spanish_surf = self.font_huge.render(vocab['spanish'], True, self.colors['yellow'])
        spanish_rect = spanish_surf.get_rect(center=(self.width//2, 220))
        self.screen.blit(spanish_surf, spanish_rect)

        # Pronunciation
        pron_surf = self.font_medium.render(f"[ {vocab['pronunciation']} ]", True, self.colors['gray'])
        pron_rect = pron_surf.get_rect(center=(self.width//2, 320))
        self.screen.blit(pron_surf, pron_rect)

        # English translation
        english_label = self.font_small.render("TRANSLATION:", True, self.colors['cyan'])
        english_label_rect = english_label.get_rect(centerx=self.width//2, top=400)
        self.screen.blit(english_label, english_label_rect)

        english_surf = self.font_large.render(vocab['english'], True, self.colors['white'])
        english_rect = english_surf.get_rect(center=(self.width//2, 470))
        self.screen.blit(english_surf, english_rect)

        # Progress
        progress = f"Word {self.current_vocab + 1}/{len(self.language_vocab)} | ← → to navigate"
        progress_surf = self.font_small.render(progress, True, self.colors['gray'])
        progress_rect = progress_surf.get_rect(center=(self.width//2, 580))
        self.screen.blit(progress_surf, progress_rect)

        self.draw_footer("Practice makes perfect | ESC for menu")
        self.draw_corner_markers(self.colors['purple'])

    def render_sleep_learning(self):
        """Render ambient sleep learning loop"""
        # Dark, minimal background for sleep mode
        self.screen.fill((10, 10, 20))

        # Gentle pulsing effect
        t = time.time()
        pulse = 0.7 + 0.3 * abs(math.sin(t * 0.5))
        glow_color = tuple(int(c * pulse) for c in self.colors['purple'])

        # Current fact (centered, large)
        fact = self.sleep_facts[self.current_fact]

        # Word wrap for long facts
        words = fact.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.font_medium.render(test_line, True, self.colors['white'])
            if test_surf.get_width() > self.width - 200:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        # Render lines
        y_start = (self.height - len(lines) * 70) // 2
        for i, line in enumerate(lines):
            line_surf = self.font_medium.render(line, True, glow_color)
            line_rect = line_surf.get_rect(center=(self.width//2, y_start + i * 70))
            self.screen.blit(line_surf, line_rect)

        # Subtle progress indicator
        progress = f"{self.current_fact + 1}/{len(self.sleep_facts)}"
        progress_surf = self.font_small.render(progress, True, (80, 80, 100))
        progress_rect = progress_surf.get_rect(center=(self.width//2, self.height - 60))
        self.screen.blit(progress_surf, progress_rect)

        # Very subtle footer
        footer = self.font_small.render("Sleep Learning Mode - Auto Loop | ESC for menu", True, (60, 60, 80))
        footer_rect = footer.get_rect(center=(self.width//2, self.height - 30))
        self.screen.blit(footer, footer_rect)

if __name__ == "__main__":
    demo = EducationDemo(standalone=True)
    demo.run(duration=300)  # 5 minutes
