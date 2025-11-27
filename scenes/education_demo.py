#!/usr/bin/env python3
"""
VERTICAL 2: Education / Learning Demo - Enhanced
Multi-deck flashcard system with Pomodoro timer and quiz mode
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime

class EducationDemo(MotiBeamScene):
    """Enhanced education scene with multi-deck flashcards and Pomodoro timer"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Education & Learning", standalone=standalone)

        # Card decks
        self.decks = {
            "Biology": [
                {"term": "Photosynthesis", "definition": "Process by which plants convert light into energy"},
                {"term": "DNA", "definition": "Deoxyribonucleic acid - molecule carrying genetic instructions"},
                {"term": "Cell", "definition": "Basic structural and functional unit of all living organisms"},
            ],
            "Physics": [
                {"term": "Gravity", "definition": "Force that attracts objects with mass toward each other"},
                {"term": "Force", "definition": "Push or pull on an object resulting from interaction"},
                {"term": "Energy", "definition": "Capacity to do work or produce change"},
            ],
            "History": [
                {"term": "Renaissance", "definition": "Cultural rebirth in Europe from 14th to 17th century"},
                {"term": "Industrial Revolution", "definition": "Period of major industrialization in late 1700s-1800s"},
                {"term": "Civil Rights Movement", "definition": "1950s-60s struggle for racial equality in America"},
            ]
        }

        self.deck_names = ["Biology", "Physics", "History"]
        self.current_deck_index = 0  # Start with Biology
        self.current_deck_name = self.deck_names[self.current_deck_index]
        self.current_card_index = 0

        # Timer state (Pomodoro-style)
        self.timer_seconds = 25 * 60  # 25 minutes
        self.timer_running = False
        self.timer_complete = False

        # Quiz mode
        self.quiz_mode = False
        self.definition_visible = True

        # Card transition animation
        self.card_slide_offset = 0.0  # Horizontal offset for slide animation
        self.card_slide_direction = 0  # 1 = from right, -1 = from left, 0 = no animation
        self.card_slide_duration = 0.25  # 0.25 seconds
        self.card_slide_timer = 0.0

        # Animation state
        self.fade_alpha = 0  # For fade-in effect (0 to 255)
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Activity feed
        self.activity_log = []
        self.max_activities = 4
        self._log("Session started")
        self._log(f"Loaded {self.current_deck_name} deck")

    def _log(self, message):
        """Add timestamped activity to log"""
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        self.activity_log.insert(0, f"{timestamp} - {message}")
        if len(self.activity_log) > self.max_activities:
            self.activity_log = self.activity_log[:self.max_activities]

    def _get_current_card(self):
        """Get the current flashcard"""
        deck = self.decks[self.current_deck_name]
        return deck[self.current_card_index]

    def _get_deck_color(self):
        """Get color for current deck"""
        colors = {
            "Biology": self.colors['green'],
            "Physics": self.colors['yellow'],
            "History": self.colors['purple']
        }
        return colors.get(self.current_deck_name, self.colors['cyan'])

    def _start_card_transition(self, direction):
        """Start a card slide transition animation"""
        self.card_slide_direction = direction  # 1 = from right, -1 = from left
        self.card_slide_timer = 0.0
        self.card_slide_offset = direction * 300  # Start 300px off-screen

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Start fade-out animation
                self.fade_out = True
                self._log("Exiting session...")

            # Deck selection
            elif event.key == pygame.K_1:
                self.current_deck_index = 0
                self.current_deck_name = self.deck_names[0]
                self.current_card_index = 0
                self._log(f"Switched to {self.current_deck_name} deck")
            elif event.key == pygame.K_2:
                self.current_deck_index = 1
                self.current_deck_name = self.deck_names[1]
                self.current_card_index = 0
                self._log(f"Switched to {self.current_deck_name} deck")
            elif event.key == pygame.K_3:
                self.current_deck_index = 2
                self.current_deck_name = self.deck_names[2]
                self.current_card_index = 0
                self._log(f"Switched to {self.current_deck_name} deck")

            # Card navigation with slide animation
            elif event.key == pygame.K_n or event.key == pygame.K_RIGHT:
                deck = self.decks[self.current_deck_name]
                self.current_card_index = (self.current_card_index + 1) % len(deck)
                card = self._get_current_card()
                self._log(f"Card {self.current_card_index + 1}/{len(deck)} - {card['term']}")
                self._start_card_transition(1)  # Slide from right
            elif event.key == pygame.K_p or event.key == pygame.K_LEFT:
                deck = self.decks[self.current_deck_name]
                self.current_card_index = (self.current_card_index - 1) % len(deck)
                card = self._get_current_card()
                self._log(f"Card {self.current_card_index + 1}/{len(deck)} - {card['term']}")
                self._start_card_transition(-1)  # Slide from left

            # Quiz mode toggle
            elif event.key == pygame.K_f or event.key == pygame.K_SPACE:
                self.quiz_mode = not self.quiz_mode
                if self.quiz_mode:
                    self.definition_visible = False
                    self._log("Quiz mode ON")
                else:
                    self.definition_visible = True
                    self._log("Quiz mode OFF")

            # Timer controls
            elif event.key == pygame.K_t:
                self.timer_running = not self.timer_running
                if self.timer_running:
                    self._log("Timer started")
                else:
                    self._log("Timer paused")
            elif event.key == pygame.K_r:
                self.timer_seconds = 25 * 60
                self.timer_complete = False
                self.timer_running = False
                self._log("Session restarted")

    def update(self, dt):
        """Update scene state with delta time"""
        # Update animation time
        self.animation_time += dt

        # Fade-in animation (0.7 seconds)
        if not self.fade_in_complete:
            self.fade_alpha = min(255, self.fade_alpha + (255 * dt / 0.7))
            if self.fade_alpha >= 255:
                self.fade_in_complete = True

        # Fade-out animation (0.5 seconds)
        if self.fade_out:
            self.fade_alpha = max(0, self.fade_alpha - (255 * dt / 0.5))
            if self.fade_alpha <= 0:
                self.running = False

        # Update card slide animation
        if self.card_slide_direction != 0:
            self.card_slide_timer += dt
            # Ease-out animation
            progress = min(1.0, self.card_slide_timer / self.card_slide_duration)
            # Smooth easing function
            eased_progress = 1.0 - (1.0 - progress) ** 3
            self.card_slide_offset = self.card_slide_direction * 300 * (1.0 - eased_progress)

            # End animation when complete
            if progress >= 1.0:
                self.card_slide_offset = 0.0
                self.card_slide_direction = 0

        # Update timer
        if self.timer_running and not self.timer_complete:
            self.timer_seconds -= dt
            if self.timer_seconds <= 0:
                self.timer_seconds = 0
                self.timer_complete = True
                self.timer_running = False
                self._log("Session completed - take a break!")

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

        # Get current deck info
        deck = self.decks[self.current_deck_name]
        deck_color = self._get_deck_color()
        card = self._get_current_card()

        # Header - Title
        title_text = "BREAK TIME" if self.timer_complete else "📚 STUDY SESSION"
        title_color = self.colors['orange'] if self.timer_complete else self.colors['green']

        # Add pulsing effect when timer complete
        if self.timer_complete:
            pulse = abs(math.sin(self.animation_time * 2))
            title_alpha = int(180 + 75 * pulse)
            title_surf = self.font_large.render(title_text, True, title_color)
            title_surf.set_alpha(title_alpha)
        else:
            title_surf = self.font_large.render(title_text, True, title_color)

        title_rect = title_surf.get_rect(centerx=self.width//2, top=40)
        self.screen.blit(title_surf, title_rect)

        # Subtitle - Deck indicator
        deck_info = f"Deck: {self.current_deck_name} ({self.current_deck_index + 1}/3) | 1=Bio  2=Physics  3=History"
        deck_surf = self.font_small.render(deck_info, True, self.colors['white'])
        deck_rect = deck_surf.get_rect(centerx=self.width//2, top=130)
        self.screen.blit(deck_surf, deck_rect)

        # Timer display (center top)
        minutes = int(self.timer_seconds // 60)
        seconds = int(self.timer_seconds % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Add subtle pulse to timer
        timer_pulse = 1.0 + 0.05 * abs(math.sin(self.animation_time * 2))
        timer_font = pygame.font.Font(None, int(140 * timer_pulse))
        timer_surf = timer_font.render(timer_text, True, title_color)
        timer_rect = timer_surf.get_rect(centerx=self.width//2, top=200)
        self.screen.blit(timer_surf, timer_rect)

        # Timer status
        if self.timer_running:
            status_text = "⏸ T to pause | R to reset"
        else:
            status_text = "▶ T to start | R to reset"
        status_surf = self.font_small.render(status_text, True, self.colors['gray'])
        status_rect = status_surf.get_rect(centerx=self.width//2, top=330)
        self.screen.blit(status_surf, status_rect)

        # Flashcard area with slide animation
        card_y_start = 390
        card_x_center = self.width // 2 + int(self.card_slide_offset)
        card_box_width = self.width - 500  # Reduced width to prevent overlap

        # Card border (with quiz mode pulse)
        card_border_rect = pygame.Rect(
            card_x_center - card_box_width // 2,
            card_y_start - 20,
            card_box_width,
            220
        )
        border_width = 3
        if self.quiz_mode:
            quiz_pulse = abs(math.sin(self.animation_time * 3))
            border_width = int(3 + quiz_pulse * 3)
            border_color = tuple(int(c * (0.7 + 0.3 * quiz_pulse)) for c in deck_color)
        else:
            border_color = deck_color

        pygame.draw.rect(self.screen, border_color, card_border_rect, border_width, border_radius=12)

        # Term label
        term_label = self.font_small.render("TERM:", True, deck_color)
        term_label_rect = term_label.get_rect(centerx=card_x_center, top=card_y_start)
        self.screen.blit(term_label, term_label_rect)

        # Term text
        term_surf = self.font_large.render(card['term'], True, self.colors['white'])
        term_rect = term_surf.get_rect(centerx=card_x_center, top=card_y_start + 50)
        self.screen.blit(term_surf, term_rect)

        # Definition (shown or hidden based on quiz mode)
        if self.quiz_mode and not self.definition_visible:
            # Show hint in quiz mode
            def_text = "Press F or SPACE to reveal"
            def_color = self.colors['gray']
            def_font = self.font_small
            def_surf = def_font.render(def_text, True, def_color)
            def_rect = def_surf.get_rect(centerx=card_x_center, top=card_y_start + 180)
            self.screen.blit(def_surf, def_rect)
        else:
            # Definition label
            def_label = self.font_small.render("DEFINITION:", True, deck_color)
            def_label_rect = def_label.get_rect(centerx=card_x_center, top=card_y_start + 140)
            self.screen.blit(def_label, def_label_rect)

            # Definition text with word wrapping (70% of card box width)
            max_def_width = int(card_box_width * 0.7)
            def_font = pygame.font.Font(None, 36)  # Slightly smaller font for definitions
            wrapped_lines = self._wrap_text(card['definition'], def_font, max_def_width)

            # Draw wrapped lines
            line_y = card_y_start + 175
            for line in wrapped_lines[:2]:  # Max 2 lines to fit in card
                line_surf = def_font.render(line, True, self.colors['white'])
                line_rect = line_surf.get_rect(centerx=card_x_center, top=line_y)
                self.screen.blit(line_surf, line_rect)
                line_y += 30

        # Progress bar
        progress_y = card_y_start + 240
        progress_width = 600
        progress_x = card_x_center - progress_width // 2

        # Background bar
        progress_bg = pygame.Rect(progress_x, progress_y, progress_width, 12)
        pygame.draw.rect(self.screen, (40, 40, 40), progress_bg, border_radius=6)

        # Fill bar
        progress = (self.current_card_index + 1) / len(deck)
        fill_width = int(progress_width * progress)
        if fill_width > 0:
            progress_fill = pygame.Rect(progress_x, progress_y, fill_width, 12)
            pygame.draw.rect(self.screen, deck_color, progress_fill, border_radius=6)

        # Border
        pygame.draw.rect(self.screen, deck_color, progress_bg, 2, border_radius=6)

        # Card counter
        counter_text = f"Card {self.current_card_index + 1} of {len(deck)}"
        counter_surf = self.font_small.render(counter_text, True, self.colors['gray'])
        counter_rect = counter_surf.get_rect(centerx=card_x_center, top=progress_y + 25)
        self.screen.blit(counter_surf, counter_rect)

        # Activity feed (bottom-right, moved further right by +120px)
        self._draw_activity_feed()

        # Footer with controls
        footer_text = "N/→=Next | P/←=Prev | F=Quiz | T=Timer | 1/2/3=Deck | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height - 15)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(deck_color)

        # Apply fade effect
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(255 - int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])
            self.screen.blit(fade_surface, (0, 0))

    def _draw_activity_feed(self):
        """Draw mini activity feed in bottom-right corner (moved +120px right)"""
        feed_x = self.width - 300  # Moved from -420 to -300 (+120px)
        feed_y = self.height - 200
        feed_width = 280  # Reduced from 400 to 280 to fit

        # Header
        header_surf = self.font_small.render("ACTIVITY", True, self.colors['cyan'])
        self.screen.blit(header_surf, (feed_x, feed_y))

        # Activity lines
        line_y = feed_y + 40
        line_height = 35

        for i, activity in enumerate(self.activity_log[:4]):
            # Fade older activities
            age_factor = 1.0 - (i * 0.15)
            text_color = tuple(int(c * age_factor) for c in self.colors['white'])

            # Truncate if too long (shorter limit for narrower panel)
            if len(activity) > 35:
                activity = activity[:32] + "..."

            activity_surf = self.font_small.render(activity, True, text_color)
            self.screen.blit(activity_surf, (feed_x, line_y))

            line_y += line_height

    def run(self, duration=1500):
        """Custom run loop with proper event and dt handling"""
        print(f"Starting {self.__class__.__name__}...")
        last_time = pygame.time.get_ticks()

        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time

            # Auto-exit after duration (if specified)
            if duration is not None:
                elapsed = (current_time - self.start_time) / 1000
                if elapsed > duration:
                    print(f"{duration} seconds elapsed, auto session end...")
                    self._log("Auto session end")
                    self.running = False

            # Handle events with individual event passing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_events(event)

            # Update with delta time
            self.update(dt)

            # Draw
            self.draw()

            # Flip display and tick clock
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS for smooth animations

        # Only quit pygame if standalone
        if self.standalone:
            pygame.quit()
        print("Scene complete.")

if __name__ == "__main__":
    demo = EducationDemo(standalone=True)
    demo.run(duration=1500)  # 25 minutes when standalone
