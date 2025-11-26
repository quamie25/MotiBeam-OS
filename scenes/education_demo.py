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

        # Sleep Learning Loop state - calming affirmations with fade animations
        self.sleep_cards = [
            {
                "title": "YOUR BRAIN IS RESTING & LEARNING",
                "line1": "Even during sleep, your brain is sorting memories.",
                "line2": "It keeps what matters and lets go of the rest.",
            },
            {
                "title": "YOU ARE SAFE HERE",
                "line1": "Your breathing is slow and steady.",
                "line2": "Every exhale lets tension leave your body.",
            },
            {
                "title": "FOCUS TOMORROW STARTS NOW",
                "line1": "Quality sleep recharges attention and memory.",
                "line2": "You are giving your future self an advantage.",
            },
            {
                "title": "GENTLE BRAIN FACT",
                "line1": "Your brain uses about 20% of your body's energy.",
                "line2": "Rest tonight so it can power your goals tomorrow.",
            },
            {
                "title": "YOU ARE GROWING STRONGER",
                "line1": "Every rest period rebuilds your mental resilience.",
                "line2": "Tomorrow you will wake up more capable than today.",
            },
            {
                "title": "LEARNING HAPPENS IN STILLNESS",
                "line1": "Your brain is processing everything from today.",
                "line2": "Deep rest makes those lessons permanent.",
            },
        ]
        self.sleep_index = 0
        self.sleep_loop_start = None

        # Fade timings (seconds)
        self.sleep_fade_in = 2.0
        self.sleep_hold = 8.0
        self.sleep_fade_out = 2.0

        # Additional colors and fonts for Sleep Learning Loop
        self.colors['muted'] = (100, 100, 120)  # Soft gray-blue
        self.colors['accent'] = (150, 120, 255)  # Soft purple
        self.colors['text'] = (200, 200, 210)  # Light gray
        self.font_tiny = pygame.font.Font(None, 30)

    def handle_events(self):
        """Handle mode-specific input - overrides base class"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.in_menu:
                    # Mode selection menu
                    if event.key == pygame.K_ESCAPE:
                        # Exit to main MotiBeam menu
                        self.running = False
                    elif event.key == pygame.K_1:
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
                        self.sleep_loop_start = None  # Reset fade animation timer
                else:
                    # Inside a mode
                    if event.key == pygame.K_ESCAPE:
                        # Return to Education mode menu
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

    def _get_sleep_loop_state(self):
        """Return (card_index, alpha) based on elapsed time for fade animation."""
        if self.sleep_loop_start is None:
            self.sleep_loop_start = time.time()

        now = time.time()
        elapsed = now - self.sleep_loop_start

        cycle = self.sleep_fade_in + self.sleep_hold + self.sleep_fade_out
        if cycle <= 0:
            cycle = 1.0

        # Which card are we on?
        card_index = int(elapsed // cycle) % len(self.sleep_cards)

        # Where in the fade cycle are we?
        t = elapsed % cycle

        if t < self.sleep_fade_in:
            # Fade in 0 → 255
            alpha = int(255 * (t / self.sleep_fade_in))
        elif t < self.sleep_fade_in + self.sleep_hold:
            # Fully visible
            alpha = 255
        else:
            # Fade out 255 → 0
            t_out = t - (self.sleep_fade_in + self.sleep_hold)
            alpha = int(255 * max(0.0, 1.0 - (t_out / self.sleep_fade_out)))

        return card_index, max(0, min(255, alpha))

    def update(self):
        """Update mode-specific logic"""
        if self.current_mode == "Study Session":
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            self.timer_seconds = max(0, (25 * 60) - int(elapsed))
        # Sleep Learning Loop uses _get_sleep_loop_state() for automatic fade cycling

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
        """Sleep Learning Loop - calming affirmations with smooth fade animations"""
        # Soft dark background
        self.screen.fill((10, 10, 20))

        # Top label
        title_surf = self.font_large.render("SLEEP LEARNING LOOP", True, self.colors['purple'])
        title_rect = title_surf.get_rect(center=(self.width // 2, int(self.height * 0.18)))
        self.screen.blit(title_surf, title_rect)

        subtitle = "Gentle facts + affirmations while you rest"
        sub_surf = self.font_small.render(subtitle, True, self.colors['muted'])
        sub_rect = sub_surf.get_rect(center=(self.width // 2, int(self.height * 0.23)))
        self.screen.blit(sub_surf, sub_rect)

        # Get which card + alpha we should show
        idx, alpha = self._get_sleep_loop_state()
        card = self.sleep_cards[idx]

        # Prepare text surfaces with variable alpha
        center_y = int(self.height * 0.50)

        card_title = self.font_medium.render(card["title"], True, self.colors['accent'])
        line1 = self.font_small.render(card["line1"], True, self.colors['text'])
        line2 = self.font_small.render(card["line2"], True, self.colors['text'])

        # Apply fade alpha to all text surfaces
        for surf in (card_title, line1, line2):
            surf.set_alpha(alpha)

        # Position card title + lines
        title_rect2 = card_title.get_rect(center=(self.width // 2, center_y - 30))
        line1_rect = line1.get_rect(center=(self.width // 2, center_y + 10))
        line2_rect = line2.get_rect(center=(self.width // 2, center_y + 40))

        self.screen.blit(card_title, title_rect2)
        self.screen.blit(line1, line1_rect)
        self.screen.blit(line2, line2_rect)

        # Footer hint (very low brightness)
        footer = "ESC - Return to Education Menu"
        footer_surf = self.font_tiny.render(footer, True, self.colors['muted'])
        footer_surf.set_alpha(120)
        footer_rect = footer_surf.get_rect(center=(self.width // 2, self.height - 40))
        self.screen.blit(footer_surf, footer_rect)

if __name__ == "__main__":
    demo = EducationDemo(standalone=True)
    demo.run(duration=300)  # 5 minutes
