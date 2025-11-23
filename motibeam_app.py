#!/usr/bin/env python3
"""
MotiBeam OS - Unified Multi-Vertical Application
Main application with all 7 verticals integrated
"""

import pygame
import sys
from datetime import datetime

# Import our custom demos
from education_demo import EducationDemo
from home_demo import HomeDemo

# Display configuration
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS = 30

# Color palette - pure black for "wall looks alive" effect
COLORS = {
    'bg': (0, 0, 0),  # Pure black - wall looks alive, not like TV
    'accent': (0, 255, 180),
    'text': (240, 245, 255),
    'warning': (255, 180, 0),
    'success': (80, 255, 120),
    'muted': (120, 130, 150),
    'clinical': (255, 100, 150),
    'automotive': (100, 200, 255),
    'emergency': (255, 80, 80),
    'industrial': (255, 200, 100),
    'security': (150, 100, 255),
    'education': (80, 255, 120),
    'home': (0, 255, 180),
}


class MotiBeamOS:
    """Unified MotiBeam OS Application with all verticals"""

    def __init__(self):
        """Initialize MotiBeam OS"""
        pygame.init()

        # Create fullscreen display
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("MotiBeam OS - Multi-Vertical Platform")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "boot"  # boot, menu, or vertical name

        # Boot animation state
        self.boot_progress = 0.0
        self.boot_start_time = pygame.time.get_ticks()
        self.boot_duration = 2000  # 2 seconds boot animation

        # Fonts - Larger for projection
        self.font_small = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_large = pygame.font.Font(None, 72)
        self.font_huge = pygame.font.Font(None, 110)

        # Demo instances (created when needed)
        self.education_demo = None
        self.home_demo = None

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

    def render_boot_screen(self):
        """Render boot animation"""
        self.screen.fill(COLORS['bg'])

        # Calculate progress
        elapsed = pygame.time.get_ticks() - self.boot_start_time
        self.boot_progress = min(1.0, elapsed / self.boot_duration)

        # MotiBeam logo
        self.draw_text("MotiBeam OS", (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 100),
                      self.font_huge, COLORS['accent'], align='center')

        # Subtitle
        self.draw_text("Multi-Vertical Ambient Computing Platform",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2),
                      self.font_medium, COLORS['text'], align='center')

        # Progress bar
        bar_width = 600
        bar_height = 20
        bar_x = (DISPLAY_WIDTH - bar_width) // 2
        bar_y = DISPLAY_HEIGHT // 2 + 100

        # Background
        pygame.draw.rect(self.screen, COLORS['muted'],
                        (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)

        # Progress fill
        fill_width = int(bar_width * self.boot_progress)
        if fill_width > 0:
            pygame.draw.rect(self.screen, COLORS['accent'],
                           (bar_x, bar_y, fill_width, bar_height), border_radius=10)

        # Loading text
        loading_text = f"Loading... {int(self.boot_progress * 100)}%"
        self.draw_text(loading_text, (DISPLAY_WIDTH // 2, bar_y + 50),
                      self.font_small, COLORS['muted'], align='center')

        # Check if boot complete
        if self.boot_progress >= 1.0:
            self.current_screen = "menu"

    def render_menu(self):
        """Render main menu with all verticals"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("MotiBeam OS", (DISPLAY_WIDTH // 2, 80),
                      self.font_huge, COLORS['accent'], align='center')

        # Subtitle
        timestamp = datetime.now().strftime("%I:%M %p")
        self.draw_text(f"Multi-Vertical Platform | {timestamp}",
                      (DISPLAY_WIDTH // 2, 150),
                      self.font_small, COLORS['muted'], align='center')

        # Vertical options - two columns
        verticals = [
            ("1", "Clinical Care", COLORS['clinical'], "Medication tracking & health monitoring"),
            ("2", "Automotive", COLORS['automotive'], "Vehicle maintenance & diagnostics"),
            ("3", "Emergency Response", COLORS['emergency'], "Emergency procedures & guidance"),
            ("4", "Industrial", COLORS['industrial'], "Work assistance & safety protocols"),
            ("5", "Security", COLORS['security'], "Security monitoring & alerts"),
            ("6", "Education", COLORS['education'], "5th grade learning & sleep mode"),
            ("7", "Smart Home", COLORS['home'], "Home control & family dashboard"),
        ]

        y_start = 220
        y_spacing = 68

        for i, (key, name, color, desc) in enumerate(verticals):
            y_pos = y_start + (i * y_spacing)

            # Key and name - centered
            full_text = f"{key} - {name}"
            self.draw_text(full_text, (DISPLAY_WIDTH // 2, y_pos),
                          self.font_medium, color, align='center')

            # Description - centered below
            self.draw_text(desc, (DISPLAY_WIDTH // 2, y_pos + 40),
                          self.font_small, COLORS['muted'], align='center')

        # Footer instructions
        self.draw_text("Press number key to launch vertical | ESC to exit",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_placeholder(self, title, color):
        """Render placeholder for verticals not yet implemented"""
        self.screen.fill(COLORS['bg'])

        # Title
        self.draw_text(title, (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 100),
                      self.font_large, color, align='center')

        # Coming soon
        self.draw_text("This vertical is coming soon",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2),
                      self.font_medium, COLORS['text'], align='center')

        # Demo text
        self.draw_text("Press ESC to return to main menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 100),
                      self.font_small, COLORS['muted'], align='center')

    def handle_events(self):
        """Handle keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False

            elif event.type == pygame.KEYDOWN:
                # Boot screen - skip to menu
                if self.current_screen == "boot":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.current_screen = "menu"

                # Main menu navigation
                elif self.current_screen == "menu":
                    if event.key == pygame.K_ESCAPE:
                        # Exit application
                        self.screen.fill((0, 0, 0))
                        pygame.display.flip()
                        self.running = False
                        return False

                    elif event.key == pygame.K_1:
                        self.current_screen = "clinical"
                    elif event.key == pygame.K_2:
                        self.current_screen = "automotive"
                    elif event.key == pygame.K_3:
                        self.current_screen = "emergency"
                    elif event.key == pygame.K_4:
                        self.current_screen = "industrial"
                    elif event.key == pygame.K_5:
                        self.current_screen = "security"
                    elif event.key == pygame.K_6:
                        # Launch education demo
                        self.education_demo = EducationDemo(screen=self.screen, standalone=False)
                        self.current_screen = "education"
                    elif event.key == pygame.K_7:
                        # Launch home demo
                        self.home_demo = HomeDemo(screen=self.screen, standalone=False)
                        self.current_screen = "home"

                # Placeholder screens
                elif self.current_screen in ["clinical", "automotive", "emergency", "industrial", "security"]:
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"

        return True

    def update(self):
        """Update application state"""
        # Update education demo if active
        if self.current_screen == "education" and self.education_demo:
            # Education demo handles its own events
            if not self.education_demo.handle_events():
                # Demo requested exit
                self.current_screen = "menu"
                self.education_demo = None

        # Update home demo if active
        if self.current_screen == "home" and self.home_demo:
            # Home demo handles its own events
            if not self.home_demo.handle_events():
                # Demo requested exit
                self.current_screen = "menu"
                self.home_demo = None

    def render(self):
        """Render current screen"""
        if self.current_screen == "boot":
            self.render_boot_screen()

        elif self.current_screen == "menu":
            self.render_menu()

        elif self.current_screen == "education" and self.education_demo:
            self.education_demo.render()

        elif self.current_screen == "home" and self.home_demo:
            self.home_demo.render()

        elif self.current_screen == "clinical":
            self.render_placeholder("CLINICAL CARE", COLORS['clinical'])

        elif self.current_screen == "automotive":
            self.render_placeholder("AUTOMOTIVE", COLORS['automotive'])

        elif self.current_screen == "emergency":
            self.render_placeholder("EMERGENCY RESPONSE", COLORS['emergency'])

        elif self.current_screen == "industrial":
            self.render_placeholder("INDUSTRIAL", COLORS['industrial'])

        elif self.current_screen == "security":
            self.render_placeholder("SECURITY", COLORS['security'])

        pygame.display.flip()

    def run(self):
        """Main application loop"""
        print("🚀 MotiBeam OS Starting...")
        print("=" * 60)
        print("Multi-Vertical Ambient Computing Platform")
        print("Education & Smart Home verticals active")
        print("Press ESC to exit")
        print("=" * 60)

        try:
            while self.running:
                if not self.handle_events():
                    break

                self.update()
                self.render()
                self.clock.tick(FPS)

        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")

        finally:
            pygame.quit()
            print("✅ MotiBeam OS shutdown complete")


def main():
    """Entry point"""
    app = MotiBeamOS()
    app.run()


if __name__ == "__main__":
    main()
