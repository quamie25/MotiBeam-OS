#!/usr/bin/env python3
"""
VERTICAL 2: Education / Learning Demo v2.0
Focused flashcard system with subject/level hierarchy and Pomodoro timer
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime

class EducationDemo(MotiBeamScene):
    """Focused education scene with subject/level flashcards and Pomodoro timer"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Education & Learning v2.0", standalone=standalone)

        # Subject/Level hierarchy
        self.subjects = [
            {
                "name": "Biology",
                "theme_color": self.colors["green"],
                "levels": [
                    {
                        "name": "General Biology",
                        "cards": [
                            {"term": "Photosynthesis", "definition": "Process by which plants convert light energy into chemical energy"},
                            {"term": "DNA", "definition": "Deoxyribonucleic acid carrying genetic instructions for life"},
                            {"term": "Cell", "definition": "Basic structural and functional unit of all living organisms"},
                        ]
                    }
                ]
            },
            {
                "name": "Physics",
                "theme_color": self.colors["yellow"],
                "levels": [
                    {
                        "name": "General Physics",
                        "cards": [
                            {"term": "Gravity", "definition": "Force that attracts objects with mass toward each other"},
                            {"term": "Force", "definition": "Push or pull on an object resulting from interaction"},
                            {"term": "Energy", "definition": "Capacity to do work or produce change in a system"},
                        ]
                    }
                ]
            },
            {
                "name": "History",
                "theme_color": self.colors["purple"],
                "levels": [
                    {
                        "name": "World History",
                        "cards": [
                            {"term": "Renaissance", "definition": "Cultural rebirth in Europe from 14th to 17th century"},
                            {"term": "Industrial Revolution", "definition": "Period of major industrialization in late 1700s to 1800s"},
                            {"term": "Civil Rights Movement", "definition": "1950s-60s struggle for racial equality in America"},
                        ]
                    }
                ]
            },
            {
                "name": "Math",
                "theme_color": self.colors["orange"],
                "levels": [
                    {
                        "name": "5th Grade Math",
                        "cards": [
                            {"term": "Pizza Slices", "definition": "A pizza is cut into 8 slices. If you eat 3 slices, what fraction of the pizza remains?"},
                            {"term": "Garden Perimeter", "definition": "A square garden has sides of 12 feet. What is the perimeter?"},
                            {"term": "Movie Time", "definition": "A movie starts at 2:45 PM and runs for 1 hour 50 minutes. When does it end?"},
                        ]
                    },
                    {
                        "name": "6th Grade Math",
                        "cards": [
                            {"term": "Train Meeting", "definition": "Two trains 120 miles apart travel toward each other at 40 mph and 20 mph. How long until they meet?"},
                            {"term": "Rectangle Area", "definition": "A rectangle has length twice its width. If perimeter is 36 units, what is the area?"},
                            {"term": "Discount & Tax", "definition": "A $50 item is discounted 20% then taxed at 8%. What is the final price?"},
                        ]
                    },
                ]
            },
            {
                "name": "Vocabulary",
                "theme_color": self.colors["cyan"],
                "levels": [
                    {
                        "name": "Middle School Vocab",
                        "cards": [
                            {"term": "Eager", "definition": "Showing keen interest or enthusiasm"},
                            {"term": "Reliable", "definition": "Consistently good in quality or performance; dependable"},
                            {"term": "Fortunate", "definition": "Favored by or involving good luck; lucky"},
                        ]
                    },
                    {
                        "name": "High School Vocab",
                        "cards": [
                            {"term": "Resilient", "definition": "Able to withstand or recover quickly from difficult conditions"},
                            {"term": "Innovative", "definition": "Featuring new methods; advanced and original"},
                            {"term": "Pragmatic", "definition": "Dealing with things sensibly and realistically"},
                        ]
                    },
                    {
                        "name": "College / Higher Ed Vocab",
                        "cards": [
                            {"term": "Ubiquitous", "definition": "Present, appearing, or found everywhere; omnipresent"},
                            {"term": "Ephemeral", "definition": "Lasting for a very short time; transient"},
                            {"term": "Intrepid", "definition": "Fearless; adventurous, often in challenging situations"},
                        ]
                    },
                ]
            },
        ]

        # Current position in hierarchy
        self.current_subject_index = 0
        self.current_level_index = 0
        self.current_card_index = 0

        # Timer state (Pomodoro-style)
        self.timer_seconds = 25 * 60  # 25 minutes
        self.timer_running = False
        self.timer_complete = False

        # Quiz mode
        self.quiz_mode = False

        # Sleep mode (soft/deep states)
        self.sleep_state = "none"  # "none", "soft", "deep"
        self.sleep_pulse = 0.0
        self.breath_time = 0.0
        self.last_sleep_toggle_time = 0.0
        self.last_key_time = pygame.time.get_ticks() / 1000.0

        # Whispering sleep mode messages
        self.sleep_messages = [
            "You are safe. One breath at a time.",
            "Your mind grows stronger, even in rest.",
            "Relax your shoulders. Unclench your jaw.",
            "Tiny steps today become big wins tomorrow.",
            "Curiosity is your superpower.",
            "Stillness restores clarity.",
            "Your brain is learning beneath the silence.",
        ]

        self.sleep_msg_index = 0
        self.sleep_msg_alpha = 0.0
        self.sleep_msg_phase = "fade_in"  # fade_in → hold → fade_out
        self.sleep_msg_timer = 0.0

        # Activity panel
        self.activity_visible = False
        self.activity_log = []
        self.max_activities = 3

        # Card transition animation
        self.card_slide_offset = 0.0
        self.card_slide_direction = 0  # 1 = right, -1 = left, 0 = none
        self.card_slide_duration = 0.25
        self.card_slide_timer = 0.0

        # Animation state
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Initial log
        self._log("Session started")
        subject = self._get_current_subject()
        level = self._get_current_level()
        self._log(f"{subject['name']} - {level['name']}")

    def _log(self, message):
        """Add timestamped activity to log"""
        timestamp = datetime.now().strftime("%I:%M %p")
        self.activity_log.insert(0, f"{timestamp} {message}")
        if len(self.activity_log) > self.max_activities:
            self.activity_log = self.activity_log[:self.max_activities]

    def _get_current_subject(self):
        """Get the current subject"""
        return self.subjects[self.current_subject_index]

    def _get_current_level(self):
        """Get the current level"""
        subject = self._get_current_subject()
        return subject["levels"][self.current_level_index]

    def _get_current_card(self):
        """Get the current flashcard"""
        level = self._get_current_level()
        return level["cards"][self.current_card_index]

    def _get_theme_color(self):
        """Get theme color for current subject"""
        return self._get_current_subject()["theme_color"]

    def _start_card_transition(self, direction):
        """Start a card slide transition animation"""
        self.card_slide_direction = direction
        self.card_slide_timer = 0.0
        self.card_slide_offset = direction * 300

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            # Update last key time for all keys
            current_time = pygame.time.get_ticks() / 1000.0

            if event.key == pygame.K_ESCAPE:
                self.fade_out = True
                self._log("Exiting...")
                self.last_key_time = current_time

            # Sleep mode toggle (S key with double-tap detection)
            elif event.key == pygame.K_s:
                time_since_last_sleep_toggle = current_time - self.last_sleep_toggle_time

                if self.sleep_state == "none":
                    self.sleep_state = "soft"
                    self._log("Sleep mode (soft) enabled")
                    self.sleep_msg_index = 0
                    self.sleep_msg_timer = 0.0
                    self.sleep_msg_alpha = 0.0
                    self.sleep_msg_phase = "fade_in"
                elif self.sleep_state == "soft":
                    if time_since_last_sleep_toggle < 0.5:
                        # Double-tap detected - enter deep sleep
                        self.sleep_state = "deep"
                        self._log("Sleep mode (deep) enabled")
                    else:
                        # Single tap after delay - exit sleep
                        self.sleep_state = "none"
                        self._log("Sleep mode disabled")
                elif self.sleep_state == "deep":
                    self.sleep_state = "none"
                    self._log("Sleep mode disabled")

                self.last_sleep_toggle_time = current_time
                self.last_key_time = current_time

            # Subject selection (1-5)
            elif event.key == pygame.K_1:
                self.current_subject_index = 0
                self.current_level_index = 0
                self.current_card_index = 0
                subject = self._get_current_subject()
                level = self._get_current_level()
                self._log(f"{subject['name']} - {level['name']}")
                self.last_key_time = current_time
            elif event.key == pygame.K_2:
                self.current_subject_index = 1
                self.current_level_index = 0
                self.current_card_index = 0
                subject = self._get_current_subject()
                level = self._get_current_level()
                self._log(f"{subject['name']} - {level['name']}")
                self.last_key_time = current_time
            elif event.key == pygame.K_3:
                self.current_subject_index = 2
                self.current_level_index = 0
                self.current_card_index = 0
                subject = self._get_current_subject()
                level = self._get_current_level()
                self._log(f"{subject['name']} - {level['name']}")
                self.last_key_time = current_time
            elif event.key == pygame.K_4:
                self.current_subject_index = 3
                self.current_level_index = 0
                self.current_card_index = 0
                subject = self._get_current_subject()
                level = self._get_current_level()
                self._log(f"{subject['name']} - {level['name']}")
                self.last_key_time = current_time
            elif event.key == pygame.K_5:
                self.current_subject_index = 4
                self.current_level_index = 0
                self.current_card_index = 0
                subject = self._get_current_subject()
                level = self._get_current_level()
                self._log(f"{subject['name']} - {level['name']}")
                self.last_key_time = current_time

            # Level selection (UP/DOWN)
            elif event.key == pygame.K_UP:
                subject = self._get_current_subject()
                num_levels = len(subject["levels"])
                self.current_level_index = (self.current_level_index - 1) % num_levels
                self.current_card_index = 0
                level = self._get_current_level()
                self._log(f"Level: {level['name']}")
                self.last_key_time = current_time
            elif event.key == pygame.K_DOWN:
                subject = self._get_current_subject()
                num_levels = len(subject["levels"])
                self.current_level_index = (self.current_level_index + 1) % num_levels
                self.current_card_index = 0
                level = self._get_current_level()
                self._log(f"Level: {level['name']}")
                self.last_key_time = current_time

            # Card navigation
            elif event.key == pygame.K_n or event.key == pygame.K_RIGHT:
                level = self._get_current_level()
                self.current_card_index = (self.current_card_index + 1) % len(level["cards"])
                card = self._get_current_card()
                self._log(f"Card: {card['term']}")
                self._start_card_transition(1)
                self.last_key_time = current_time
            elif event.key == pygame.K_p or event.key == pygame.K_LEFT:
                level = self._get_current_level()
                self.current_card_index = (self.current_card_index - 1) % len(level["cards"])
                card = self._get_current_card()
                self._log(f"Card: {card['term']}")
                self._start_card_transition(-1)
                self.last_key_time = current_time

            # Quiz mode toggle
            elif event.key == pygame.K_f or event.key == pygame.K_SPACE:
                self.quiz_mode = not self.quiz_mode
                mode_text = "ON" if self.quiz_mode else "OFF"
                self._log(f"Quiz mode {mode_text}")
                self.last_key_time = current_time

            # Activity panel toggle
            elif event.key == pygame.K_a:
                self.activity_visible = not self.activity_visible
                status = "shown" if self.activity_visible else "hidden"
                self._log(f"Activity {status}")
                self.last_key_time = current_time

            # Timer controls
            elif event.key == pygame.K_t:
                self.timer_running = not self.timer_running
                if self.timer_running:
                    self._log("Timer started")
                else:
                    self._log("Timer paused")
                self.last_key_time = current_time
            elif event.key == pygame.K_r:
                self.timer_seconds = 25 * 60
                self.timer_complete = False
                self.timer_running = False
                self._log("Timer reset")
                self.last_key_time = current_time

    def update(self, dt):
        """Update scene state with delta time"""
        # Update animation time
        self.animation_time += dt

        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_alpha = min(255, self.fade_alpha + (255 * dt / 0.7))
            if self.fade_alpha >= 255:
                self.fade_in_complete = True

        # Fade-out animation
        if self.fade_out:
            self.fade_alpha = max(0, self.fade_alpha - (255 * dt / 0.5))
            if self.fade_alpha <= 0:
                self.running = False

        # Card slide animation
        if self.card_slide_direction != 0:
            self.card_slide_timer += dt
            progress = min(1.0, self.card_slide_timer / self.card_slide_duration)
            eased_progress = 1.0 - (1.0 - progress) ** 3  # Cubic ease-out
            self.card_slide_offset = self.card_slide_direction * 300 * (1.0 - eased_progress)

            if progress >= 1.0:
                self.card_slide_offset = 0.0
                self.card_slide_direction = 0

        # Sleep mode animations + whisper timing
        if self.sleep_state == "soft":
            # Breathing circle animation
            self.breath_time += dt * 0.5
            if self.breath_time > math.tau:
                self.breath_time -= math.tau

            # Whisper timing logic
            self.sleep_msg_timer += dt

            if self.sleep_msg_phase == "fade_in":
                self.sleep_msg_alpha += dt / 1.0
                if self.sleep_msg_alpha >= 1.0:
                    self.sleep_msg_alpha = 1.0
                    self.sleep_msg_phase = "hold"
                    self.sleep_msg_timer = 0.0

            elif self.sleep_msg_phase == "hold":
                if self.sleep_msg_timer >= 4.0:
                    self.sleep_msg_phase = "fade_out"
                    self.sleep_msg_timer = 0.0

            elif self.sleep_msg_phase == "fade_out":
                self.sleep_msg_alpha -= dt / 1.0
                if self.sleep_msg_alpha <= 0.0:
                    self.sleep_msg_alpha = 0.0
                    self.sleep_msg_phase = "fade_in"
                    self.sleep_msg_timer = 0.0
                    self.sleep_msg_index = (self.sleep_msg_index + 1) % len(self.sleep_messages)

        elif self.sleep_state == "deep":
            self.sleep_pulse += dt * 1.5
            if self.sleep_pulse > math.tau:
                self.sleep_pulse -= math.tau

        # Auto-sleep after 180 seconds of inactivity
        if self.sleep_state == "none" and self.timer_running:
            current_time = pygame.time.get_ticks() / 1000.0
            time_since_last_key = current_time - self.last_key_time
            if time_since_last_key >= 180.0:
                self.sleep_state = "soft"
                self._log("Auto sleep enabled after 3 minutes of inactivity")
                self.last_key_time = current_time  # Reset to avoid repeated triggers
                self.sleep_msg_index = 0
                self.sleep_msg_timer = 0.0
                self.sleep_msg_alpha = 0.0
                self.sleep_msg_phase = "fade_in"

        # Update timer (continues even in sleep mode)
        if self.timer_running and not self.timer_complete:
            self.timer_seconds -= dt
            if self.timer_seconds <= 0:
                self.timer_seconds = 0
                self.timer_complete = True
                self.timer_running = False
                self._log("Session complete!")

    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width, returning list of lines"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = font.render(test_line, True, (255, 255, 255))

            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw(self):
        """Render the scene"""
        self.screen.fill(self.colors['black'])

        # Get current context
        subject = self._get_current_subject()
        level = self._get_current_level()
        card = self._get_current_card()
        theme_color = self._get_theme_color()

        # Soft sleep mode overlay
        if self.sleep_state == "soft":
            # Dark overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # Title
            title_surf = self.font_medium.render("SLEEP MODE", True, theme_color)
            title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 80))
            self.screen.blit(title_surf, title_rect)

            # Message
            msg = "Screen dimmed · Rest your eyes · Press S to resume"
            msg_surf = self.font_small.render(msg, True, self.colors["gray"])
            msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height // 2 - 30))
            self.screen.blit(msg_surf, msg_rect)

            # Breathing circle
            radius = int(40 + 6 * math.sin(self.breath_time))
            breath_surf = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
            breath_color = (*theme_color, 60)  # Low opacity
            pygame.draw.circle(breath_surf, breath_color, (radius + 5, radius + 5), radius, 2)
            breath_rect = breath_surf.get_rect(center=(self.width // 2, self.height // 2 + 40))
            self.screen.blit(breath_surf, breath_rect)

            # Inhale/Exhale text (alternates every ~pi seconds)
            breath_phase = int(self.breath_time / math.pi) % 2
            breath_text = "Inhale" if breath_phase == 0 else "Exhale"
            breath_text_surf = self.font_small.render(breath_text, True, theme_color)
            breath_text_surf.set_alpha(120)
            breath_text_rect = breath_text_surf.get_rect(center=(self.width // 2, self.height // 2 + 40))
            self.screen.blit(breath_text_surf, breath_text_rect)

            # Whisper text – gentle, centered, fading
            message = self.sleep_messages[self.sleep_msg_index]
            # Use medium font so it's readable but not overwhelming
            text_surf = self.font_small.render(message, True, self.colors['white'])
            text_surf.set_alpha(int(255 * self.sleep_msg_alpha))

            text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 + 80))
            self.screen.blit(text_surf, text_rect)

            # Apply fade effect
            if self.fade_alpha < 255:
                fade_surface = pygame.Surface((self.width, self.height))
                fade_surface.set_alpha(255 - int(self.fade_alpha))
                fade_surface.fill(self.colors['black'])
                self.screen.blit(fade_surface, (0, 0))

            return  # Skip rendering everything else

        # Deep sleep mode overlay
        if self.sleep_state == "deep":
            # Very dark overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 235))
            self.screen.blit(overlay, (0, 0))

            # Tiny dot in bottom-right
            dot_x = self.width - 30
            dot_y = self.height - 30
            pulse_alpha = int(150 + 60 * abs(math.sin(self.sleep_pulse)))
            dot_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(dot_surf, (*theme_color, pulse_alpha), (6, 6), 5)
            self.screen.blit(dot_surf, (dot_x - 6, dot_y - 6))

            # Tiny "S to wake" text
            wake_text = "S to wake"
            wake_surf = self.font_small.render(wake_text, True, self.colors["gray"])
            wake_surf.set_alpha(100)
            wake_rect = wake_surf.get_rect(center=(dot_x, dot_y - 20))
            self.screen.blit(wake_surf, wake_rect)

            # Apply fade effect
            if self.fade_alpha < 255:
                fade_surface = pygame.Surface((self.width, self.height))
                fade_surface.set_alpha(255 - int(self.fade_alpha))
                fade_surface.fill(self.colors['black'])
                self.screen.blit(fade_surface, (0, 0))

            return  # Skip rendering everything else

        # Normal rendering (sleep_state == "none")

        # Main header - Level name (large)
        header_text = level["name"].upper()
        header_surf = self.font_large.render(header_text, True, theme_color)
        header_rect = header_surf.get_rect(centerx=self.width // 2, top=30)
        self.screen.blit(header_surf, header_rect)

        # Subtitle - Subject and stats
        num_levels = len(subject["levels"])
        num_cards = len(level["cards"])
        subtitle = f"Subject: {subject['name']} · Level: {level['name']} · Cards: {num_cards}"
        subtitle_surf = self.font_small.render(subtitle, True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=self.width // 2, top=90)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Timer (above card, smaller and subtle)
        timer_y = 140
        minutes = int(self.timer_seconds // 60)
        seconds = int(self.timer_seconds % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Very subtle pulse on timer
        timer_pulse = 1.0 + 0.02 * abs(math.sin(self.animation_time * 2))
        timer_color = self.colors['orange'] if self.timer_complete else self.colors['cyan']
        timer_font = pygame.font.Font(None, int(80 * timer_pulse))
        timer_surf = timer_font.render(timer_text, True, timer_color)
        timer_rect = timer_surf.get_rect(centerx=self.width // 2, top=timer_y)
        self.screen.blit(timer_surf, timer_rect)

        # Timer controls
        timer_help = "T to start | R to reset"
        timer_help_surf = self.font_small.render(timer_help, True, self.colors['gray'])
        timer_help_rect = timer_help_surf.get_rect(centerx=self.width // 2, top=timer_y + 75)
        self.screen.blit(timer_help_surf, timer_help_rect)

        # Flashcard - centered in middle third of screen
        card_y_start = 280
        card_width = 700
        card_height = 260
        card_x = (self.width - card_width) // 2 + int(self.card_slide_offset)

        # Card background and border
        card_rect = pygame.Rect(card_x, card_y_start, card_width, card_height)

        # Draw card background
        pygame.draw.rect(self.screen, (20, 20, 20), card_rect, border_radius=16)

        # Draw border
        border_width = 3
        if self.quiz_mode:
            quiz_pulse = abs(math.sin(self.animation_time * 3))
            border_width = int(3 + quiz_pulse * 2)
            border_color = tuple(int(c * (0.7 + 0.3 * quiz_pulse)) for c in theme_color)
        else:
            border_color = theme_color
        pygame.draw.rect(self.screen, border_color, card_rect, border_width, border_radius=16)

        # Term
        term_label = "TERM"
        term_label_surf = self.font_small.render(term_label, True, theme_color)
        term_label_rect = term_label_surf.get_rect(centerx=self.width // 2, top=card_y_start + 20)
        self.screen.blit(term_label_surf, term_label_rect)

        term_surf = self.font_medium.render(card['term'], True, self.colors['white'])
        term_rect = term_surf.get_rect(centerx=self.width // 2, top=card_y_start + 55)
        self.screen.blit(term_surf, term_rect)

        # Definition
        def_y = card_y_start + 120
        if self.quiz_mode:
            # Show hint in quiz mode
            hint_text = "Press F or SPACE to reveal"
            hint_surf = self.font_small.render(hint_text, True, self.colors['gray'])
            hint_rect = hint_surf.get_rect(centerx=self.width // 2, top=def_y + 40)
            self.screen.blit(hint_surf, hint_rect)
        else:
            # Show definition
            def_label = "DEFINITION"
            def_label_surf = self.font_small.render(def_label, True, theme_color)
            def_label_rect = def_label_surf.get_rect(centerx=self.width // 2, top=def_y)
            self.screen.blit(def_label_surf, def_label_rect)

            # Wrap definition text
            max_def_width = card_width - 100
            def_font = pygame.font.Font(None, 32)
            wrapped_lines = self._wrap_text(card['definition'], def_font, max_def_width)

            # Draw up to 3 lines
            line_y = def_y + 35
            for line in wrapped_lines[:3]:
                line_surf = def_font.render(line, True, self.colors['white'])
                line_rect = line_surf.get_rect(centerx=self.width // 2, top=line_y)
                self.screen.blit(line_surf, line_rect)
                line_y += 28

        # Progress bar (below card)
        progress_y = card_y_start + card_height + 25
        progress_width = 500
        progress_x = (self.width - progress_width) // 2

        # Background
        progress_bg = pygame.Rect(progress_x, progress_y, progress_width, 10)
        pygame.draw.rect(self.screen, (40, 40, 40), progress_bg, border_radius=5)

        # Fill
        progress = (self.current_card_index + 1) / num_cards
        fill_width = int(progress_width * progress)
        if fill_width > 0:
            progress_fill = pygame.Rect(progress_x, progress_y, fill_width, 10)
            pygame.draw.rect(self.screen, theme_color, progress_fill, border_radius=5)

        # Border
        pygame.draw.rect(self.screen, theme_color, progress_bg, 2, border_radius=5)

        # Card counter
        counter_text = f"Card {self.current_card_index + 1} of {num_cards}"
        counter_surf = self.font_small.render(counter_text, True, self.colors['gray'])
        counter_rect = counter_surf.get_rect(centerx=self.width // 2, top=progress_y + 20)
        self.screen.blit(counter_surf, counter_rect)

        # Activity panel (bottom-center, when visible)
        if self.activity_visible:
            self._draw_activity_panel()

        # Footer
        footer_y = self.height - 25
        footer_text = "N/→=Next | P/←=Prev | F=Quiz | S=Sleep | T=Timer | 1-5=Subject | ↑/↓=Level | A=Activity | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width // 2, bottom=footer_y)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(theme_color)

        # Apply fade effect
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(255 - int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])
            self.screen.blit(fade_surface, (0, 0))

    def _draw_activity_panel(self):
        """Draw activity panel at bottom-center"""
        panel_width = 600
        panel_height = 110
        panel_x = (self.width - panel_width) // 2
        panel_y = self.height - 90

        # Background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (15, 15, 15), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['cyan'], panel_rect, 2, border_radius=10)

        # Header
        header_surf = self.font_small.render("RECENT ACTIVITY", True, self.colors['cyan'])
        header_rect = header_surf.get_rect(centerx=self.width // 2, top=panel_y + 8)
        self.screen.blit(header_surf, header_rect)

        # Activity lines
        line_y = panel_y + 35
        for i, activity in enumerate(self.activity_log[:3]):
            # Fade older activities
            age_factor = 1.0 - (i * 0.25)
            text_color = tuple(int(c * age_factor) for c in self.colors['white'])

            # Truncate if too long
            if len(activity) > 65:
                activity = activity[:62] + "..."

            activity_surf = self.font_small.render(activity, True, text_color)
            activity_rect = activity_surf.get_rect(centerx=self.width // 2, top=line_y)
            self.screen.blit(activity_surf, activity_rect)

            line_y += 22

    def run(self, duration=1500):
        """Custom run loop with proper event and dt handling"""
        print(f"Starting {self.__class__.__name__}...")
        last_time = pygame.time.get_ticks()

        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0
            last_time = current_time

            # Auto-exit after duration (if specified)
            if duration is not None:
                elapsed = (current_time - self.start_time) / 1000
                if elapsed > duration:
                    print(f"{duration} seconds elapsed, auto session end...")
                    self._log("Auto session end")
                    self.running = False

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_events(event)

            # Update
            self.update(dt)

            # Draw
            self.draw()

            # Flip and tick
            pygame.display.flip()
            self.clock.tick(60)

        # Cleanup
        if self.standalone:
            pygame.quit()
        print("Scene complete.")

if __name__ == "__main__":
    demo = EducationDemo(standalone=True)
    demo.run(duration=1500)
