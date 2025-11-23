#!/usr/bin/env python3
"""
MotiBeam OS - Smart Home Demo
Compete with Ring, Nest, Alexa, Apple Home
"""

import pygame
import sys
import time
from datetime import datetime

# Display configuration
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS = 30

# Color palette
COLORS = {
    'bg': (15, 20, 35),
    'accent': (0, 255, 180),
    'text': (240, 245, 255),
    'warning': (255, 180, 0),
    'success': (80, 255, 120),
    'muted': (120, 130, 150),
    'error': (255, 80, 80),
}

class HomeDemo:
    """Smart Home Control Demo"""

    def __init__(self, screen=None, standalone=True):
        """Initialize the home demo

        Args:
            screen: Existing pygame screen (if None, creates new one)
            standalone: If True, runs as standalone app with own event loop
        """
        self.standalone = standalone

        if standalone:
            pygame.init()
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
            pygame.display.set_caption("MotiBeam OS - Smart Home")
        else:
            self.screen = screen

        self.clock = pygame.time.Clock()
        self.running = True

        # Current screen state
        self.current_screen = "menu"  # menu, dashboard, doorbell, packages, controls, messages

        # Fonts
        self.font_small = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 64)

        # Smart home state
        self.lights_on = True
        self.thermostat_temp = 72
        self.door_locked = True
        self.garage_closed = True

        # Package tracking
        self.packages = [
            {"name": "Amazon Package", "status": "Delivered", "time": "2:30 PM"},
            {"name": "USPS Mail", "status": "In Transit", "time": "Expected 5 PM"},
        ]

        # Family messages
        self.messages = [
            {"from": "Mom", "text": "Dinner at 6 PM", "time": "3:15 PM"},
            {"from": "Dad", "text": "Running late, be home at 7", "time": "4:30 PM"},
        ]

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

    def draw_header(self, title):
        """Draw header with title"""
        pygame.draw.rect(self.screen, COLORS['accent'], (20, 20, 200, 60), 3, border_radius=10)
        self.draw_text("MotiBeam", (40, 30), self.font_medium, COLORS['accent'])
        self.draw_text("OS", (180, 50), self.font_small, COLORS['text'])

        # Title
        self.draw_text(title, (DISPLAY_WIDTH // 2, 50), self.font_large, COLORS['accent'], align='center')

        # Time
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.draw_text(timestamp, (DISPLAY_WIDTH - 20, 30), self.font_medium, COLORS['muted'], align='right')

    def draw_button(self, rect, text, color, selected=False):
        """Draw a button"""
        # Background
        bg_color = color if not selected else COLORS['text']
        text_color = COLORS['text'] if not selected else COLORS['bg']

        pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, color, rect, 3, border_radius=10)

        # Text
        text_surf = self.font_medium.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def render_menu(self):
        """Main menu for home demo"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("SMART HOME CONTROL")

        # Menu options
        options = [
            ("1", "Family Dashboard", COLORS['accent']),
            ("2", "Doorbell Monitor", COLORS['success']),
            ("3", "Package Tracker", COLORS['warning']),
            ("4", "Smart Home Controls", COLORS['accent']),
            ("5", "Family Messages", COLORS['success']),
        ]

        y_pos = 200
        for key, label, color in options:
            text = f"{key} - {label}"
            self.draw_text(text, (DISPLAY_WIDTH // 2, y_pos),
                          self.font_medium, color, align='center')
            y_pos += 80

        # Instructions
        self.draw_text("Press number key to select",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 80),
                      self.font_small, COLORS['muted'], align='center')
        self.draw_text("ESC - Exit",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_dashboard(self):
        """Family dashboard with quick overview"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("FAMILY DASHBOARD")

        # Time and date
        now = datetime.now()
        self.draw_text(now.strftime("%A, %B %d, %Y"),
                      (DISPLAY_WIDTH // 2, 140), self.font_medium, COLORS['text'], align='center')
        self.draw_text(now.strftime("%I:%M %p"),
                      (DISPLAY_WIDTH // 2, 190), self.font_large, COLORS['accent'], align='center')

        # Quick status grid
        y_base = 280
        col_width = DISPLAY_WIDTH // 2

        # Left column
        self.draw_text("HOME STATUS", (50, y_base), self.font_medium, COLORS['accent'])
        status_items = [
            ("Lights", "ON" if self.lights_on else "OFF", COLORS['success'] if self.lights_on else COLORS['muted']),
            ("Thermostat", f"{self.thermostat_temp}F", COLORS['success']),
            ("Front Door", "LOCKED" if self.door_locked else "UNLOCKED", COLORS['success'] if self.door_locked else COLORS['error']),
            ("Garage", "CLOSED" if self.garage_closed else "OPEN", COLORS['success'] if self.garage_closed else COLORS['warning']),
        ]

        item_y = y_base + 50
        for label, value, color in status_items:
            self.draw_text(f"{label}:", (70, item_y), self.font_small, COLORS['text'])
            self.draw_text(value, (300, item_y), self.font_small, color)
            item_y += 45

        # Right column - Recent activity
        self.draw_text("RECENT ACTIVITY", (col_width + 50, y_base), self.font_medium, COLORS['accent'])
        activities = [
            "Package delivered - 2:30 PM",
            "Front door unlocked - 3:45 PM",
            "Thermostat adjusted - 4:00 PM",
            "New message from Mom - 3:15 PM",
        ]

        activity_y = y_base + 50
        for activity in activities:
            self.draw_text(activity, (col_width + 70, activity_y), self.font_small, COLORS['text'])
            activity_y += 45

        # Bottom instruction
        self.draw_text("ESC - Return to Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_doorbell(self):
        """Doorbell monitor screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("DOORBELL MONITOR")

        # Camera feed placeholder
        camera_rect = pygame.Rect(240, 180, 800, 450)
        pygame.draw.rect(self.screen, (50, 50, 50), camera_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['accent'], camera_rect, 3, border_radius=15)

        self.draw_text("FRONT DOOR CAMERA",
                      (DISPLAY_WIDTH // 2, 250), self.font_large, COLORS['muted'], align='center')
        self.draw_text("No activity detected",
                      (DISPLAY_WIDTH // 2, 350), self.font_medium, COLORS['muted'], align='center')

        # Status indicator
        self.draw_text("LIVE", (280, 200), self.font_small, COLORS['success'])
        pygame.draw.circle(self.screen, COLORS['success'], (260, 207), 8)

        # Recent visitors
        self.draw_text("Recent Visitors: None today",
                      (DISPLAY_WIDTH // 2, 560), self.font_small, COLORS['text'], align='center')

        # Bottom instruction
        self.draw_text("ESC - Return to Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_packages(self):
        """Package tracking screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("PACKAGE TRACKER")

        # Package list
        y_pos = 180
        for i, package in enumerate(self.packages):
            # Package box
            box_rect = pygame.Rect(100, y_pos, DISPLAY_WIDTH - 200, 120)

            if package["status"] == "Delivered":
                border_color = COLORS['success']
            elif package["status"] == "In Transit":
                border_color = COLORS['warning']
            else:
                border_color = COLORS['muted']

            pygame.draw.rect(self.screen, (30, 35, 50), box_rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, box_rect, 3, border_radius=10)

            # Package info
            self.draw_text(package["name"], (130, y_pos + 20), self.font_medium, COLORS['text'])
            self.draw_text(f"Status: {package['status']}", (130, y_pos + 60), self.font_small, border_color)
            self.draw_text(package["time"], (DISPLAY_WIDTH - 130, y_pos + 40),
                          self.font_small, COLORS['muted'], align='right')

            y_pos += 150

        # Bottom instruction
        self.draw_text("ESC - Return to Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_controls(self):
        """Smart home controls screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("SMART HOME CONTROLS")

        # Control grid
        controls_y = 180
        col1_x = 150
        col2_x = DISPLAY_WIDTH // 2 + 100

        # Lights control
        self.draw_text("LIGHTS", (col1_x, controls_y), self.font_medium, COLORS['accent'])
        light_status = "ON" if self.lights_on else "OFF"
        light_color = COLORS['success'] if self.lights_on else COLORS['muted']
        self.draw_text(f"Status: {light_status}", (col1_x, controls_y + 50), self.font_small, light_color)
        self.draw_text("Press L to toggle", (col1_x, controls_y + 85), self.font_small, COLORS['muted'])

        # Thermostat control
        self.draw_text("THERMOSTAT", (col2_x, controls_y), self.font_medium, COLORS['accent'])
        self.draw_text(f"Temperature: {self.thermostat_temp}F", (col2_x, controls_y + 50),
                      self.font_small, COLORS['success'])
        self.draw_text("Press +/- to adjust", (col2_x, controls_y + 85), self.font_small, COLORS['muted'])

        # Door lock control
        controls_y += 180
        self.draw_text("FRONT DOOR", (col1_x, controls_y), self.font_medium, COLORS['accent'])
        door_status = "LOCKED" if self.door_locked else "UNLOCKED"
        door_color = COLORS['success'] if self.door_locked else COLORS['error']
        self.draw_text(f"Status: {door_status}", (col1_x, controls_y + 50), self.font_small, door_color)
        self.draw_text("Press D to toggle", (col1_x, controls_y + 85), self.font_small, COLORS['muted'])

        # Garage control
        self.draw_text("GARAGE", (col2_x, controls_y), self.font_medium, COLORS['accent'])
        garage_status = "CLOSED" if self.garage_closed else "OPEN"
        garage_color = COLORS['success'] if self.garage_closed else COLORS['warning']
        self.draw_text(f"Status: {garage_status}", (col2_x, controls_y + 50), self.font_small, garage_color)
        self.draw_text("Press G to toggle", (col2_x, controls_y + 85), self.font_small, COLORS['muted'])

        # Bottom instructions
        self.draw_text("L=Lights | D=Door | G=Garage | +/-=Temp | ESC=Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_messages(self):
        """Family messages screen"""
        self.screen.fill(COLORS['bg'])
        self.draw_header("FAMILY MESSAGES")

        # Message list
        y_pos = 180
        for message in self.messages:
            # Message box
            msg_rect = pygame.Rect(100, y_pos, DISPLAY_WIDTH - 200, 100)
            pygame.draw.rect(self.screen, (30, 35, 50), msg_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS['accent'], msg_rect, 2, border_radius=10)

            # Message content
            self.draw_text(f"From: {message['from']}", (130, y_pos + 15), self.font_medium, COLORS['success'])
            self.draw_text(message['text'], (130, y_pos + 50), self.font_small, COLORS['text'])
            self.draw_text(message['time'], (DISPLAY_WIDTH - 130, y_pos + 35),
                          self.font_small, COLORS['muted'], align='right')

            y_pos += 130

        # Bottom instruction
        self.draw_text("ESC - Return to Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

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

                # Menu navigation
                elif self.current_screen == "menu":
                    if event.key == pygame.K_1:
                        self.current_screen = "dashboard"
                    elif event.key == pygame.K_2:
                        self.current_screen = "doorbell"
                    elif event.key == pygame.K_3:
                        self.current_screen = "packages"
                    elif event.key == pygame.K_4:
                        self.current_screen = "controls"
                    elif event.key == pygame.K_5:
                        self.current_screen = "messages"

                # Controls screen - device controls
                elif self.current_screen == "controls":
                    if event.key == pygame.K_l:
                        self.lights_on = not self.lights_on
                    elif event.key == pygame.K_d:
                        self.door_locked = not self.door_locked
                    elif event.key == pygame.K_g:
                        self.garage_closed = not self.garage_closed
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.thermostat_temp = min(85, self.thermostat_temp + 1)
                    elif event.key == pygame.K_MINUS:
                        self.thermostat_temp = max(60, self.thermostat_temp - 1)

        return True

    def render(self):
        """Render current screen"""
        if self.current_screen == "menu":
            self.render_menu()
        elif self.current_screen == "dashboard":
            self.render_dashboard()
        elif self.current_screen == "doorbell":
            self.render_doorbell()
        elif self.current_screen == "packages":
            self.render_packages()
        elif self.current_screen == "controls":
            self.render_controls()
        elif self.current_screen == "messages":
            self.render_messages()

        pygame.display.flip()

    def run(self):
        """Main loop for standalone mode"""
        if not self.standalone:
            print("Error: run() should only be called in standalone mode")
            return

        print("🏠 Smart Home Demo Running")
        print("Press 1-5 to select features, ESC to exit")

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

        print("✅ Smart Home demo closed")


def main():
    """Entry point for standalone execution"""
    demo = HomeDemo(standalone=True)
    demo.run()


if __name__ == "__main__":
    main()
