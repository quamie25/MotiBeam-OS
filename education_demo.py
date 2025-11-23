#!/usr/bin/env python3
"""
MotiBeam OS - 5th Grade Education Demo
Simplified sleep mode with no background, ASCII symbols, proper text wrapping
"""

import pygame
import sys
import time
import random
from datetime import datetime

# Display configuration
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS = 30

# Color palette
COLORS = {
    'bg': (0, 0, 0),  # Pure black - wall looks alive, not like TV
    'accent': (0, 255, 180),
    'text': (240, 245, 255),
    'warning': (255, 180, 0),
    'success': (80, 255, 120),
    'muted': (120, 130, 150),
}

class EducationDemo:
    """5th Grade Education Demo with Sleep Mode"""

    def __init__(self, screen=None, standalone=True):
        """Initialize the education demo

        Args:
            screen: Existing pygame screen (if None, creates new one)
            standalone: If True, runs as standalone app with own event loop
        """
        self.standalone = standalone

        if standalone:
            pygame.init()
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
            pygame.display.set_caption("MotiBeam OS - 5th Grade Education")
        else:
            self.screen = screen

        self.clock = pygame.time.Clock()
        self.running = True

        # Current screen state
        self.current_screen = "menu"  # menu, math, vocab, sleep

        # Sleep mode state
        self.sleep_items = [
            {"type": "vocab", "main": "Habitat", "sub": "Natural home of plants/animals", "symbol": "[VOCAB]"},
            {"type": "math", "main": "48 / 6 = 8", "sub": "Division practice", "symbol": "[DIV]"},
            {"type": "vocab", "main": "Photosynthesis", "sub": "How plants make food from sunlight", "symbol": "[VOCAB]"},
            {"type": "math", "main": "3/4 + 1/4 = 1", "sub": "Adding fractions", "symbol": "[FRAC]"},
            {"type": "vocab", "main": "Evaporation", "sub": "Liquid turning into gas", "symbol": "[VOCAB]"},
            {"type": "math", "main": "9 x 7 = 63", "sub": "Multiplication facts", "symbol": "[MULT]"},
            {"type": "vocab", "main": "Democracy", "sub": "Government by the people", "symbol": "[VOCAB]"},
            {"type": "math", "main": "100 - 47 = 53", "sub": "Subtraction", "symbol": "[SUB]"},
        ]
        self.sleep_index = 0
        self.sleep_start_time = time.time()
        self.sleep_display_duration = 4.0  # Show each item for 4 seconds
        self.fade_alpha = 0  # Current fade alpha (0-255)

        # Math problem state
        self.current_math_problem = None
        self.show_math_answer = False

        # Fonts
        self.font_small = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 64)
        self.font_huge = pygame.font.Font(None, 96)

        # Math word problems for 5th grade
        self.math_problems = [
            {
                "question": "Sarah has 24 cookies. She wants to share them equally with 5 friends (6 people total). How many cookies does each person get?",
                "answer": "24 / 6 = 4 cookies each",
                "hint": "Divide total cookies by number of people"
            },
            {
                "question": "A rectangular garden is 12 feet long and 8 feet wide. What is the area of the garden?",
                "answer": "12 x 8 = 96 square feet",
                "hint": "Area = length x width"
            },
            {
                "question": "Tom read 3/4 of a book on Monday and 1/8 on Tuesday. What fraction of the book did he read total?",
                "answer": "3/4 + 1/8 = 6/8 + 1/8 = 7/8",
                "hint": "Find common denominator first"
            },
        ]

        # Vocabulary words for 5th grade
        self.vocab_words = [
            {"word": "Habitat", "definition": "The natural home or environment of a plant, animal, or organism"},
            {"word": "Photosynthesis", "definition": "The process by which green plants make food from sunlight"},
            {"word": "Democracy", "definition": "A system of government by the whole population through elected representatives"},
            {"word": "Evaporation", "definition": "The process of liquid turning into vapor or gas"},
        ]

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width, returns list of lines"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # Try adding this word to current line
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, (255, 255, 255))

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                # Line is too long, start new line
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        # Add remaining words
        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_text(self, text, pos, font, color=None, align='left'):
        """Draw text with alignment"""
        if color is None:
            color = COLORS['text']

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align == 'center':
            text_rect.center = pos
        elif align == 'right':
            text_rect.right = pos[0]
            text_rect.top = pos[1]
        else:
            text_rect.topleft = pos

        self.screen.blit(text_surface, text_rect)
        return text_rect.height

    def draw_header(self):
        """Draw header with MotiBeam branding"""
        pygame.draw.rect(self.screen, COLORS['accent'], (20, 20, 200, 60), 3, border_radius=10)
        self.draw_text("MotiBeam", (40, 30), self.font_medium, COLORS['accent'])
        self.draw_text("OS", (180, 50), self.font_small, COLORS['text'])

        # Time
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.draw_text(timestamp, (DISPLAY_WIDTH - 20, 30), self.font_medium, COLORS['muted'], align='right')

    def render_menu(self):
        """Main menu for education demo"""
        self.screen.fill(COLORS['bg'])
        self.draw_header()

        # Title
        self.draw_text("5TH GRADE LEARNING CENTER",
                      (DISPLAY_WIDTH // 2, 150), self.font_large, COLORS['accent'], align='center')

        # Menu options
        options = [
            "1 - Math Word Problems",
            "2 - Vocabulary Builder",
            "3 - Sleep Mode (Ambient Learning)",
        ]

        y_pos = 300
        for option in options:
            self.draw_text(option, (DISPLAY_WIDTH // 2, y_pos),
                          self.font_medium, COLORS['text'], align='center')
            y_pos += 70

        # Instructions
        self.draw_text("Press number key to select",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 100),
                      self.font_small, COLORS['muted'], align='center')
        self.draw_text("ESC - Return to Menu / Exit",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50),
                      self.font_small, COLORS['muted'], align='center')

    def render_math(self):
        """Math word problems screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header()

        # Title
        self.draw_text("MATH WORD PROBLEMS",
                      (DISPLAY_WIDTH // 2, 120), self.font_large, COLORS['success'], align='center')

        # Select random problem if none selected
        if self.current_math_problem is None:
            self.current_math_problem = random.choice(self.math_problems)
            self.show_math_answer = False

        # Draw question with proper wrapping
        question_y = 200
        self.draw_text("Question:", (100, question_y), self.font_medium, COLORS['accent'])

        # Wrap the question text
        max_width = DISPLAY_WIDTH - 200  # Leave margins
        wrapped_lines = self.wrap_text(self.current_math_problem["question"], self.font_small, max_width)

        line_y = question_y + 50
        for line in wrapped_lines:
            self.draw_text(line, (100, line_y), self.font_small, COLORS['text'])
            line_y += 40

        # Hint
        hint_y = line_y + 30
        self.draw_text("Hint: " + self.current_math_problem["hint"],
                      (100, hint_y), self.font_small, COLORS['warning'])

        # Answer (shown when SPACE is pressed)
        answer_y = hint_y + 80
        if self.show_math_answer:
            self.draw_text("Answer:", (100, answer_y), self.font_medium, COLORS['success'])
            self.draw_text(self.current_math_problem["answer"],
                          (100, answer_y + 50), self.font_medium, COLORS['success'])
        else:
            self.draw_text("Press SPACE to see answer",
                          (100, answer_y), self.font_small, COLORS['muted'])

        # Controls
        self.draw_text("SPACE - Show Answer  |  N - Next Problem  |  ESC - Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50),
                      self.font_small, COLORS['muted'], align='center')

    def render_vocab(self):
        """Vocabulary builder screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header()

        # Title
        self.draw_text("VOCABULARY BUILDER",
                      (DISPLAY_WIDTH // 2, 120), self.font_large, COLORS['accent'], align='center')

        # Display all vocabulary words
        y_pos = 220
        for vocab in self.vocab_words:
            # Word
            self.draw_text(vocab["word"], (100, y_pos), self.font_medium, COLORS['success'])

            # Definition with wrapping
            max_width = DISPLAY_WIDTH - 200
            wrapped_def = self.wrap_text(vocab["definition"], self.font_small, max_width)

            def_y = y_pos + 45
            for line in wrapped_def:
                self.draw_text(line, (120, def_y), self.font_small, COLORS['text'])
                def_y += 35

            y_pos = def_y + 25

        # Controls
        self.draw_text("ESC - Return to Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50),
                      self.font_small, COLORS['muted'], align='center')

    def render_sleep_mode(self):
        """Sleep mode - fading text on transparent background"""
        # NO background fill - just transparent overlay
        # Create a transparent surface for the fade effect
        fade_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

        # Calculate fade alpha based on time
        elapsed = time.time() - self.sleep_start_time

        # Fade in first 1 second, hold for 2 seconds, fade out last 1 second
        if elapsed < 1.0:
            # Fading in
            self.fade_alpha = int(255 * elapsed)
        elif elapsed < 3.0:
            # Full brightness
            self.fade_alpha = 255
        elif elapsed < 4.0:
            # Fading out
            self.fade_alpha = int(255 * (1.0 - (elapsed - 3.0)))
        else:
            # Move to next item
            self.sleep_index = (self.sleep_index + 1) % len(self.sleep_items)
            self.sleep_start_time = time.time()
            self.fade_alpha = 0

        # Get current sleep item
        item = self.sleep_items[self.sleep_index]

        # Draw symbol (ASCII, not emoji)
        symbol_surf = self.font_huge.render(item['symbol'], True, (255, 255, 255, self.fade_alpha))
        symbol_rect = symbol_surf.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 80))

        # Draw main text
        main_surf = self.font_large.render(item['main'], True, (255, 255, 255, self.fade_alpha))
        main_rect = main_surf.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))

        # Draw subtitle
        sub_surf = self.font_medium.render(item['sub'], True, (200, 200, 200, self.fade_alpha))
        sub_rect = sub_surf.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 60))

        # Apply fade to all elements
        fade_surface.blit(symbol_surf, symbol_rect)
        fade_surface.blit(main_surf, main_rect)
        fade_surface.blit(sub_surf, sub_rect)

        # Set overall alpha
        fade_surface.set_alpha(self.fade_alpha)

        # Blit to screen (screen already cleared by main loop or will be black naturally)
        self.screen.blit(fade_surface, (0, 0))

        # Small exit hint in corner (always visible, not fading)
        self.draw_text("ESC - Exit Sleep Mode", (DISPLAY_WIDTH - 20, DISPLAY_HEIGHT - 30),
                      self.font_small, (100, 100, 100), align='right')

    def handle_events(self):
        """Handle keyboard events with proper ESC handling"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False

            elif event.type == pygame.KEYDOWN:
                # ESC key handling - proper state management
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "menu":
                        # Exit application
                        self.running = False
                        return False
                    else:
                        # Return to menu from any screen
                        self.current_screen = "menu"
                        self.current_math_problem = None
                        self.show_math_answer = False

                # Menu navigation
                elif self.current_screen == "menu":
                    if event.key == pygame.K_1:
                        self.current_screen = "math"
                    elif event.key == pygame.K_2:
                        self.current_screen = "vocab"
                    elif event.key == pygame.K_3:
                        self.current_screen = "sleep"
                        self.sleep_start_time = time.time()
                        self.fade_alpha = 0

                # Math screen controls
                elif self.current_screen == "math":
                    if event.key == pygame.K_SPACE:
                        self.show_math_answer = True
                    elif event.key == pygame.K_n:
                        self.current_math_problem = None
                        self.show_math_answer = False

        return True

    def render(self):
        """Render current screen"""
        if self.current_screen == "menu":
            self.render_menu()
        elif self.current_screen == "math":
            self.render_math()
        elif self.current_screen == "vocab":
            self.render_vocab()
        elif self.current_screen == "sleep":
            # For sleep mode, fill with black first to have clean background
            self.screen.fill((0, 0, 0))
            self.render_sleep_mode()

        pygame.display.flip()

    def run(self):
        """Main loop for standalone mode"""
        if not self.standalone:
            print("Error: run() should only be called in standalone mode")
            return

        print("🎓 Education Demo Running")
        print("Press 1-3 to select mode, ESC to exit")

        try:
            while self.running:
                if not self.handle_events():
                    break

                self.render()
                self.clock.tick(FPS)

        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")

        finally:
            if self.standalone:
                pygame.quit()

        print("✅ Education demo closed")


def main():
    """Entry point for standalone execution"""
    demo = EducationDemo(standalone=True)
    demo.run()


if __name__ == "__main__":
    main()
