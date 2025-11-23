#!/usr/bin/env python3
"""
MotiBeam OS v4.0 - Multi-Vertical Ambient Computing Platform
All 7 verticals implemented with cinematic visual style
"""

import pygame
import sys
import time
from datetime import datetime

# Import existing demos
from education_demo import EducationDemo
from home_demo import HomeDemo

# Display configuration
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS = 30

# Color palette - pure black for "wall looks alive" effect
COLORS = {
    'bg': (0, 0, 0),  # Pure black - wall looks alive
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
    """MotiBeam OS v4.0 - All 7 Verticals"""

    def __init__(self):
        """Initialize MotiBeam OS"""
        pygame.init()

        # Create fullscreen display
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("MotiBeam OS v4.0")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "boot"  # boot, menu, or vertical name

        # Boot animation state
        self.boot_progress = 0.0
        self.boot_start_time = pygame.time.get_ticks()
        self.boot_duration = 2000  # 2 seconds

        # Fonts - Large for projection
        self.font_tiny = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_large = pygame.font.Font(None, 72)
        self.font_huge = pygame.font.Font(None, 110)

        # Menu selection
        self.menu_index = 0
        self.menu_items = [
            ("clinical", "[MED] Clinical Care", "Medication • routines • guardian checks"),
            ("automotive", "[AUTO] Automotive", "Curb messages • safety cues • reminders"),
            ("emergency", "[EMER] Emergency Response", "CPR • choking • fire • weather"),
            ("industrial", "[IND] Industrial / Enterprise", "PPE • hazards • workflows"),
            ("security", "[SEC] Security / Guardian", "Inactivity • motion • occupancy"),
            ("education", "[EDU] Education", "Learning overlays for home & school"),
            ("home", "[HOME] Smart Home", "Family board • door • packages"),
        ]

        # Demo instances
        self.education_demo = None
        self.home_demo = None

        # Clinical care state
        self.medications = [
            {"time": "08:00", "name": "Sertraline 50 mg", "status": "TAKEN"},
            {"time": "09:30", "name": "Multivitamin", "status": "TAKEN"},
            {"time": "13:00", "name": "Hydration + snack", "status": "DUE"},
            {"time": "18:30", "name": "Evening meds", "status": "DUE"},
            {"time": "21:00", "name": "Wind-down routine", "status": "PLAN"},
        ]
        self.guardian_inactive_minutes = 47
        self.guardian_checkin_minutes = 13

        # Automotive state
        self.delivery_apt = "APT 204"
        self.delivery_message = "PLEASE PULL FORWARD"
        self.arrow_pulse = 0

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
        return text_rect

    def draw_panel(self, rect, color, border_width=2):
        """Draw a panel with border"""
        pygame.draw.rect(self.screen, color, rect, border_width, border_radius=10)

    def render_boot_screen(self):
        """Render boot animation"""
        self.screen.fill(COLORS['bg'])

        # Calculate progress
        elapsed = pygame.time.get_ticks() - self.boot_start_time
        self.boot_progress = min(1.0, elapsed / self.boot_duration)

        # MotiBeam logo
        self.draw_text("MotiBeam OS", (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 100),
                      self.font_huge, COLORS['accent'], align='center')

        # Version
        self.draw_text("v4.0 • Ambient Projection Hub",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2),
                      self.font_medium, COLORS['text'], align='center')

        # Progress bar
        bar_width = 600
        bar_height = 20
        bar_x = (DISPLAY_WIDTH - bar_width) // 2
        bar_y = DISPLAY_HEIGHT // 2 + 100

        pygame.draw.rect(self.screen, COLORS['muted'],
                        (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)

        fill_width = int(bar_width * self.boot_progress)
        if fill_width > 0:
            pygame.draw.rect(self.screen, COLORS['accent'],
                           (bar_x, bar_y, fill_width, bar_height), border_radius=10)

        loading_text = f"Loading... {int(self.boot_progress * 100)}%"
        self.draw_text(loading_text, (DISPLAY_WIDTH // 2, bar_y + 50),
                      self.font_small, COLORS['muted'], align='center')

        # Check if boot complete
        if self.boot_progress >= 1.0:
            self.current_screen = "menu"

    def render_menu(self):
        """Render main menu - v4 style"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("MotiBeam OS", (DISPLAY_WIDTH // 2, 60),
                      self.font_huge, COLORS['accent'], align='center')

        # Subtitle
        self.draw_text("Ambient Projection Hub • Select a vertical to demo",
                      (DISPLAY_WIDTH // 2, 140),
                      self.font_small, COLORS['muted'], align='center')

        # Menu items
        y_start = 220
        y_spacing = 70

        for i, (key, name, desc) in enumerate(self.menu_items):
            y_pos = y_start + (i * y_spacing)

            # Highlight selected item
            if i == self.menu_index:
                highlight_rect = pygame.Rect(200, y_pos - 10, DISPLAY_WIDTH - 400, 65)
                self.draw_panel(highlight_rect, COLORS['accent'], border_width=3)
                name_color = COLORS['accent']
            else:
                name_color = COLORS['text']

            # Key number and name
            key_num = str(i + 1)
            full_text = f"{key_num} - {name}"
            self.draw_text(full_text, (DISPLAY_WIDTH // 2, y_pos),
                          self.font_medium, name_color, align='center')

            # Description
            self.draw_text(desc, (DISPLAY_WIDTH // 2, y_pos + 38),
                          self.font_small, COLORS['muted'], align='center')

        # Controls
        self.draw_text("↑/↓ or W/S: Navigate  |  1-7: Jump  |  ENTER: Select  |  ESC: Exit",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_clinical(self):
        """Clinical Care - Medication + Guardian Mode"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("Clinical Care", (DISPLAY_WIDTH // 2, 60),
                      self.font_large, COLORS['clinical'], align='center')
        self.draw_text("Veteran Support • Medication & Guardian Mode",
                      (DISPLAY_WIDTH // 2, 120),
                      self.font_small, COLORS['muted'], align='center')

        # Left panel - Medication schedule
        left_x = 100
        med_y = 180

        self.draw_text("Today's Medication Schedule:", (left_x, med_y),
                      self.font_medium, COLORS['text'])

        med_y += 60
        for med in self.medications:
            if med['status'] == 'TAKEN':
                status_color = COLORS['success']
                status_label = "[TAKEN]"
            elif med['status'] == 'DUE':
                status_color = COLORS['warning']
                status_label = "[DUE]  "
            else:
                status_color = COLORS['muted']
                status_label = "[PLAN] "

            med_text = f"{med['time']}  {status_label} {med['name']}"
            self.draw_text(med_text, (left_x + 20, med_y),
                          self.font_small, status_color)
            med_y += 45

        # Right panel - Guardian Mode
        guard_x = DISPLAY_WIDTH // 2 + 50
        guard_y = 180

        guard_rect = pygame.Rect(guard_x - 20, guard_y - 20, 520, 380)
        self.draw_panel(guard_rect, COLORS['clinical'], border_width=3)

        self.draw_text("[GUARDIAN MODE]", (guard_x, guard_y),
                      self.font_medium, COLORS['clinical'])

        guard_y += 60
        guardian_info = [
            f"Last motion: Living room • {self.guardian_inactive_minutes} minutes ago",
            f"Next check-in cue in: {self.guardian_checkin_minutes} minutes",
            "",
            "If no response:",
            "  • Project CHECK-IN alert",
            "  • Ping caregiver & neighbor group",
            "  • Log to daily safety summary",
        ]

        for line in guardian_info:
            self.draw_text(line, (guard_x, guard_y), self.font_small, COLORS['text'])
            guard_y += 38

        # Footer
        self.draw_text("SPACE: Toggle next DUE → TAKEN  |  ESC: Main Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_automotive(self):
        """Automotive - Curbside Projection"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("Automotive", (DISPLAY_WIDTH // 2, 60),
                      self.font_large, COLORS['automotive'], align='center')
        self.draw_text("Curbside Projection • Delivery Guidance",
                      (DISPLAY_WIDTH // 2, 120),
                      self.font_small, COLORS['muted'], align='center')

        # Big banner
        banner_rect = pygame.Rect(200, 220, DISPLAY_WIDTH - 400, 180)
        self.draw_panel(banner_rect, COLORS['automotive'], border_width=4)

        self.draw_text("[DELIVERY]", (DISPLAY_WIDTH // 2, 260),
                      self.font_large, COLORS['automotive'], align='center')

        delivery_text = f"{self.delivery_apt} • {self.delivery_message}"
        self.draw_text(delivery_text, (DISPLAY_WIDTH // 2, 340),
                      self.font_medium, COLORS['text'], align='center')

        # Arrow with pulse animation
        self.arrow_pulse = (self.arrow_pulse + 0.1) % (2 * 3.14159)
        arrow_offset = int(20 * abs(pygame.math.Vector2(1, 0).rotate(self.arrow_pulse * 180 / 3.14159).x))

        arrow_x = DISPLAY_WIDTH // 2 + 300 + arrow_offset
        arrow_y = 450

        # Draw arrow pointing right
        arrow_points = [
            (arrow_x, arrow_y),
            (arrow_x + 60, arrow_y),
            (arrow_x + 60, arrow_y - 30),
            (arrow_x + 100, arrow_y + 20),
            (arrow_x + 60, arrow_y + 70),
            (arrow_x + 60, arrow_y + 40),
            (arrow_x, arrow_y + 40),
        ]
        pygame.draw.polygon(self.screen, COLORS['automotive'], arrow_points)

        # Bottom labels
        self.draw_text("[SLOW] Residential zone", (250, DISPLAY_HEIGHT - 80),
                      self.font_small, COLORS['warning'])
        self.draw_text("[WATCH] Kids & pets", (DISPLAY_WIDTH - 250, DISPLAY_HEIGHT - 80),
                      self.font_small, COLORS['warning'], align='right')

        # Footer
        self.draw_text("ESC: Main Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_emergency(self):
        """Emergency Response - CPR Steps"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("Emergency Response", (DISPLAY_WIDTH // 2, 60),
                      self.font_large, COLORS['emergency'], align='center')
        self.draw_text("At-a-Glance Steps • Not medical advice • visual prompts only",
                      (DISPLAY_WIDTH // 2, 115),
                      self.font_tiny, COLORS['muted'], align='center')

        # Flashing emergency banner
        flash = int(time.time() * 2) % 2 == 0
        if flash:
            banner_rect = pygame.Rect(150, 160, DISPLAY_WIDTH - 300, 60)
            pygame.draw.rect(self.screen, COLORS['emergency'], banner_rect, border_radius=10)
            self.draw_text("[EMERGENCY] CALL 911 FIRST IF SAFE TO DO SO",
                          (DISPLAY_WIDTH // 2, 190),
                          self.font_medium, COLORS['text'], align='center')

        # CPR Steps
        steps_y = 260
        self.draw_text("CPR Steps (Adult):", (DISPLAY_WIDTH // 2, steps_y),
                      self.font_medium, COLORS['emergency'], align='center')

        steps_y += 60
        steps = [
            "1) Check responsiveness & breathing.",
            "2) Call 911 or direct someone to call.",
            "3) Hands center chest, interlocked.",
            "4) Push hard and fast: 100-120 / minute.",
            "5) Let chest fully rise between compressions.",
            "6) Continue until help arrives or you cannot.",
        ]

        for step in steps:
            self.draw_text(step, (DISPLAY_WIDTH // 2, steps_y),
                          self.font_small, COLORS['text'], align='center')
            steps_y += 45

        # Footer
        self.draw_text("ESC: Main Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_industrial(self):
        """Industrial - Safety Zones"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("Industrial / Enterprise Safety", (DISPLAY_WIDTH // 2, 60),
                      self.font_large, COLORS['industrial'], align='center')
        self.draw_text("PPE • Hazards • Safe Workflows",
                      (DISPLAY_WIDTH // 2, 120),
                      self.font_small, COLORS['muted'], align='center')

        # Two-panel layout
        panel_y = 200
        panel_height = 380

        # Left panel - Safe Lane
        left_rect = pygame.Rect(80, panel_y, 520, panel_height)
        self.draw_panel(left_rect, COLORS['success'], border_width=3)

        self.draw_text("[SAFE LANE]", (340, panel_y + 30),
                      self.font_medium, COLORS['success'], align='center')
        self.draw_text("Walk-only corridor", (340, panel_y + 75),
                      self.font_small, COLORS['text'], align='center')

        safe_items = [
            "• Hi-vis vest: OPTIONAL",
            "• No powered equipment",
            "• Use for foot traffic only",
            "• Report spills immediately",
        ]

        item_y = panel_y + 140
        for item in safe_items:
            self.draw_text(item, (120, item_y), self.font_small, COLORS['text'])
            item_y += 50

        # Center boundary line with pulse
        pulse = int(time.time() * 4) % 2 == 0
        boundary_color = COLORS['industrial'] if pulse else COLORS['muted']
        pygame.draw.line(self.screen, boundary_color,
                        (DISPLAY_WIDTH // 2, panel_y),
                        (DISPLAY_WIDTH // 2, panel_y + panel_height), 5)

        # Right panel - Hazard Zone
        right_rect = pygame.Rect(680, panel_y, 520, panel_height)
        self.draw_panel(right_rect, COLORS['emergency'], border_width=3)

        self.draw_text("[HAZARD]", (940, panel_y + 30),
                      self.font_medium, COLORS['emergency'], align='center')
        self.draw_text("Forklift crossing", (940, panel_y + 75),
                      self.font_small, COLORS['text'], align='center')

        hazard_items = [
            "• Hi-vis vest: REQUIRED",
            "• Watch for forklifts",
            "• No pedestrians without escort",
            "• Lockout/tagout for repairs",
        ]

        item_y = panel_y + 140
        for item in hazard_items:
            self.draw_text(item, (720, item_y), self.font_small, COLORS['text'])
            item_y += 50

        # Footer
        self.draw_text("ESC: Main Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def render_security(self):
        """Security - Guardian Watch"""
        self.screen.fill(COLORS['bg'])

        # Header
        self.draw_text("Security", (DISPLAY_WIDTH // 2, 60),
                      self.font_large, COLORS['security'], align='center')
        self.draw_text("Guardian Watch • Inactivity Monitor",
                      (DISPLAY_WIDTH // 2, 120),
                      self.font_small, COLORS['muted'], align='center')

        # Main guardian panel
        panel_rect = pygame.Rect(240, 200, DISPLAY_WIDTH - 480, 320)
        self.draw_panel(panel_rect, COLORS['security'], border_width=3)

        panel_y = 230
        self.draw_text("[GUARDIAN MODE] ACTIVE", (DISPLAY_WIDTH // 2, panel_y),
                      self.font_large, COLORS['security'], align='center')

        panel_y += 80
        guardian_details = [
            f"Last motion: Living room • {self.guardian_inactive_minutes} minutes ago",
            f"Next check-in cue in: {self.guardian_checkin_minutes} minutes",
            "",
            "If no response:",
            "  - Project CHECK-IN alert",
            "  - Ping caregiver & neighbor group",
            "  - Log to daily safety summary",
        ]

        for line in guardian_details:
            self.draw_text(line, (DISPLAY_WIDTH // 2, panel_y),
                          self.font_small, COLORS['text'], align='center')
            panel_y += 38

        # Bottom badges
        badge_y = 570
        left_badge_rect = pygame.Rect(200, badge_y, 450, 80)
        self.draw_panel(left_badge_rect, COLORS['success'], border_width=3)
        self.draw_text("CHECK-IN REMINDER SENT", (425, badge_y + 40),
                      self.font_small, COLORS['success'], align='center')

        right_badge_rect = pygame.Rect(DISPLAY_WIDTH - 650, badge_y, 450, 80)
        self.draw_panel(right_badge_rect, COLORS['emergency'], border_width=3)
        self.draw_text("ESCALATE IF NO RESPONSE", (DISPLAY_WIDTH - 425, badge_y + 40),
                      self.font_small, COLORS['emergency'], align='center')

        # Footer
        self.draw_text("ESC: Main Menu",
                      (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 40),
                      self.font_small, COLORS['muted'], align='center')

    def handle_events(self):
        """Handle keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False

            elif event.type == pygame.KEYDOWN:
                # Boot screen - skip
                if self.current_screen == "boot":
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.current_screen = "menu"

                # Main menu navigation
                elif self.current_screen == "menu":
                    if event.key == pygame.K_ESCAPE:
                        # Exit application cleanly
                        self.screen.fill((0, 0, 0))
                        pygame.display.flip()
                        self.running = False
                        return False

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_items)

                    elif event.key == pygame.K_RETURN:
                        # Select current menu item
                        screen_key = self.menu_items[self.menu_index][0]
                        if screen_key == "education":
                            self.education_demo = EducationDemo(screen=self.screen, standalone=False)
                        elif screen_key == "home":
                            self.home_demo = HomeDemo(screen=self.screen, standalone=False)
                        self.current_screen = screen_key

                    # Direct number keys
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
                        self.education_demo = EducationDemo(screen=self.screen, standalone=False)
                        self.current_screen = "education"
                    elif event.key == pygame.K_7:
                        self.home_demo = HomeDemo(screen=self.screen, standalone=False)
                        self.current_screen = "home"

                # Clinical screen
                elif self.current_screen == "clinical":
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"
                    elif event.key == pygame.K_SPACE:
                        # Toggle next DUE to TAKEN
                        for med in self.medications:
                            if med['status'] == 'DUE':
                                med['status'] = 'TAKEN'
                                break

                # Other vertical screens
                elif self.current_screen in ["automotive", "emergency", "industrial", "security"]:
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"

        return True

    def update(self):
        """Update application state"""
        # Update education demo if active
        if self.current_screen == "education" and self.education_demo:
            if not self.education_demo.handle_events():
                self.current_screen = "menu"
                self.education_demo = None

        # Update home demo if active
        if self.current_screen == "home" and self.home_demo:
            if not self.home_demo.handle_events():
                self.current_screen = "menu"
                self.home_demo = None

    def render(self):
        """Render current screen"""
        if self.current_screen == "boot":
            self.render_boot_screen()
        elif self.current_screen == "menu":
            self.render_menu()
        elif self.current_screen == "clinical":
            self.render_clinical()
        elif self.current_screen == "automotive":
            self.render_automotive()
        elif self.current_screen == "emergency":
            self.render_emergency()
        elif self.current_screen == "industrial":
            self.render_industrial()
        elif self.current_screen == "security":
            self.render_security()
        elif self.current_screen == "education" and self.education_demo:
            self.education_demo.render()
        elif self.current_screen == "home" and self.home_demo:
            self.home_demo.render()

        pygame.display.flip()

    def run(self):
        """Main application loop"""
        print("🚀 MotiBeam OS v4.0 Starting...")
        print("=" * 60)
        print("All 7 Verticals Operational")
        print("Pure Black Design • Wall Looks Alive")
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
            # Clean exit
            pygame.quit()
            print("✅ MotiBeam OS v4.0 shutdown complete")
            sys.exit(0)  # Explicit exit to prevent service restart


def main():
    """Entry point"""
    app = MotiBeamOS()
    app.run()


if __name__ == "__main__":
    main()
