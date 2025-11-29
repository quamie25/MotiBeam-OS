#!/usr/bin/env python3
"""
MotiBeamOS v4.0 - Global Input Manager
Handles global keyboard commands that work from ANY vertical/demo
"""

import pygame


class GlobalInputManager:
    """Manages global keyboard commands across all verticals"""

    def __init__(self, app_instance):
        self.app = app_instance
        self.last_input_time = pygame.time.get_ticks()
        self.quick_settings_open = False

    def update_activity(self):
        """Update last input time for cursor auto-hide"""
        self.last_input_time = pygame.time.get_ticks()

    def should_hide_cursor(self):
        """Check if cursor should be hidden (3 seconds of inactivity)"""
        return (pygame.time.get_ticks() - self.last_input_time) > 3000

    def handle_global_commands(self, event):
        """
        Handle global keyboard commands that work from anywhere
        Returns: True if command was handled, False otherwise
        """
        if event.type != pygame.KEYDOWN:
            return False

        self.update_activity()

        # ESC - Return to main menu from ANY vertical/demo
        if event.key == pygame.K_ESCAPE:
            print("[GLOBAL] ESC pressed -> Returning to main menu")
            self.return_to_main_menu()
            return True

        # SPACE - Quick settings/overlay menu
        elif event.key == pygame.K_SPACE:
            print("[GLOBAL] SPACE pressed -> Toggle quick settings")
            self.toggle_quick_settings()
            return True

        # TAB - Cycle through vertical demos
        elif event.key == pygame.K_TAB:
            print("[GLOBAL] TAB pressed -> Cycle to next vertical")
            self.cycle_verticals()
            return True

        # M - Master system menu
        elif event.key == pygame.K_m:
            print("[GLOBAL] M pressed -> Toggle master menu")
            self.toggle_master_menu()
            return True

        return False

    def return_to_main_menu(self):
        """Return to main menu from current vertical"""
        if hasattr(self.app, 'current_mode'):
            print(f"[GLOBAL] Exiting {self.app.current_mode} mode, returning to menu")
            self.app.current_mode = 'menu'
            # Signal to exit current demo/vertical
            if hasattr(self.app, 'demo_running'):
                self.app.demo_running = False
            if hasattr(self.app, 'ambient_running'):
                self.app.ambient_running = False
            if hasattr(self.app, 'auto_running'):
                self.app.auto_running = False

    def toggle_quick_settings(self):
        """Show/hide quick settings overlay"""
        self.quick_settings_open = not self.quick_settings_open
        print(f"[GLOBAL] Quick settings: {'OPEN' if self.quick_settings_open else 'CLOSED'}")

    def render_quick_settings(self, screen):
        """Render quick settings overlay if open"""
        if not self.quick_settings_open:
            return

        width, height = screen.get_size()

        # Semi-transparent overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Quick settings panel
        panel_width = 400
        panel_height = 300
        panel_x = (width - panel_width) // 2
        panel_y = (height - panel_height) // 2

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((30, 30, 40, 250))
        pygame.draw.rect(panel, (0, 200, 160), panel.get_rect(), 3, border_radius=10)

        # Title
        font_large = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 36)

        title = font_large.render("Quick Menu", True, (0, 220, 180))
        title_rect = title.get_rect(centerx=panel_width // 2, top=20)
        panel.blit(title, title_rect)

        # Options
        options = [
            "ESC - Return to Menu",
            "SPACE - Close This Menu",
            "TAB - Next Vertical",
            "M - Master Menu",
            "S - Full Settings"
        ]

        y = 100
        for opt in options:
            opt_surf = font_small.render(opt, True, (220, 220, 220))
            opt_rect = opt_surf.get_rect(centerx=panel_width // 2, top=y)
            panel.blit(opt_surf, opt_rect)
            y += 40

        screen.blit(panel, (panel_x, panel_y))

    def cycle_verticals(self):
        """Cycle to next vertical demo"""
        # Import here to avoid circular dependency
        try:
            from config.vertical_config import VERTICAL_DEMOS

            if not VERTICAL_DEMOS:
                print("[GLOBAL] No verticals configured")
                return

            # Find current vertical index
            current_idx = 0
            if hasattr(self.app, 'current_vertical'):
                for i, (key, name, cls) in enumerate(VERTICAL_DEMOS):
                    if name == self.app.current_vertical:
                        current_idx = i
                        break

            # Get next vertical
            next_idx = (current_idx + 1) % len(VERTICAL_DEMOS)
            key, name, vertical_class = VERTICAL_DEMOS[next_idx]

            print(f"[GLOBAL] Cycling from {current_idx} to {next_idx}: {name}")

            # Run the next vertical
            self.app.current_vertical = name
            self.run_vertical(vertical_class, name)

        except ImportError:
            print("[GLOBAL] vertical_config not found, TAB cycling disabled")

    def run_vertical(self, vertical_class, name):
        """Run a vertical demo safely"""
        try:
            from core.error_handler import SystemErrorHandler
            error_handler = SystemErrorHandler(self.app)
            vertical_instance = error_handler.safe_vertical_loading(vertical_class)

            if vertical_instance:
                print(f"[GLOBAL] Running vertical: {name}")
                # Run the vertical
                if hasattr(vertical_instance, 'screen'):
                    vertical_instance.screen = self.app.screen
                if hasattr(vertical_instance, 'run'):
                    vertical_instance.run(duration=300)

        except Exception as e:
            print(f"[GLOBAL] Error running vertical {name}: {e}")

    def toggle_master_menu(self):
        """Toggle master system menu"""
        print("[GLOBAL] Master menu toggle (navigating to settings)")
        # Navigate to settings panel
        if hasattr(self.app, 'run_settings_mode'):
            self.app.run_settings_mode()
