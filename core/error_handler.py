#!/usr/bin/env python3
"""
MotiBeamOS v4.0 - System Error Handler
Robust error handling and graceful degradation
"""

import pygame
import traceback


class SystemErrorHandler:
    """Handles errors gracefully with fallback displays"""

    def __init__(self, app_instance):
        self.app = app_instance
        self.graphics_failure = False
        self.minimal_mode = False

    def safe_vertical_loading(self, vertical_class):
        """
        Safely load a vertical demo with error handling
        Returns: vertical instance or fallback display
        """
        if vertical_class is None:
            print(f"[ERROR] Vertical class is None")
            return None

        try:
            print(f"[ERROR_HANDLER] Loading vertical: {vertical_class.__name__}")

            # Try to instantiate the vertical
            vertical_instance = vertical_class(standalone=False)

            # Verify it has required methods
            if not hasattr(vertical_instance, 'run'):
                raise AttributeError(f"{vertical_class.__name__} missing 'run' method")

            print(f"[ERROR_HANDLER] Successfully loaded {vertical_class.__name__}")
            return vertical_instance

        except Exception as e:
            print(f"[ERROR] Failed to load {vertical_class.__name__}: {e}")
            traceback.print_exc()
            return self.create_fallback_vertical(vertical_class.__name__, str(e))

    def create_fallback_vertical(self, vertical_name, error_msg):
        """Create a fallback vertical that displays error"""

        class FallbackVertical:
            def __init__(self):
                self.screen = None
                self.running = True
                self.vertical_name = vertical_name
                self.error_msg = error_msg

            def run(self, duration=30):
                """Display error message"""
                import pygame
                clock = pygame.time.Clock()
                start_time = pygame.time.get_ticks()

                font_large = pygame.font.Font(None, 72)
                font_small = pygame.font.Font(None, 36)

                while self.running:
                    # Check timeout
                    if (pygame.time.get_ticks() - start_time) / 1000 > duration:
                        break

                    # Handle events
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.running = False

                    # Render error screen
                    self.screen.fill((20, 20, 30))

                    # Error title
                    title = font_large.render("Vertical Load Error", True, (255, 100, 100))
                    title_rect = title.get_rect(center=(self.screen.get_width() // 2, 200))
                    self.screen.blit(title, title_rect)

                    # Vertical name
                    name_surf = font_small.render(f"Failed to load: {self.vertical_name}", True, (200, 200, 200))
                    name_rect = name_surf.get_rect(center=(self.screen.get_width() // 2, 300))
                    self.screen.blit(name_surf, name_rect)

                    # Error message (truncate if too long)
                    error_display = self.error_msg[:60] + "..." if len(self.error_msg) > 60 else self.error_msg
                    error_surf = font_small.render(error_display, True, (150, 150, 150))
                    error_rect = error_surf.get_rect(center=(self.screen.get_width() // 2, 350))
                    self.screen.blit(error_surf, error_rect)

                    # Instructions
                    instr = font_small.render("Press ESC to return to menu", True, (100, 200, 255))
                    instr_rect = instr.get_rect(center=(self.screen.get_width() // 2, 450))
                    self.screen.blit(instr, instr_rect)

                    pygame.display.flip()
                    clock.tick(30)

        return FallbackVertical()

    def handle_rendering_error(self, error):
        """Handle rendering errors"""
        print(f"[ERROR] Rendering error: {error}")
        self.graphics_failure = True
        self.enable_minimal_mode()

    def enable_minimal_mode(self):
        """Enable minimal mode with basic graphics only"""
        if self.minimal_mode:
            return

        print("[ERROR_HANDLER] Enabling minimal mode due to graphics failure")
        self.minimal_mode = True

        # Disable advanced graphics features
        if hasattr(self.app, 'use_animations'):
            self.app.use_animations = False
        if hasattr(self.app, 'use_effects'):
            self.app.use_effects = False

    def graceful_degradation(self):
        """Check system state and degrade gracefully if needed"""
        if self.graphics_failure:
            self.enable_minimal_mode()

        # Check memory usage, performance, etc.
        # For now, just placeholder

    def log_error(self, error_type, error_msg, context=""):
        """Log error for debugging"""
        timestamp = pygame.time.get_ticks() / 1000
        print(f"[ERROR] [{timestamp:.2f}s] {error_type}: {error_msg}")
        if context:
            print(f"[ERROR]   Context: {context}")

    def display_error_overlay(self, screen, message):
        """Display a non-blocking error overlay"""
        width, height = screen.get_size()

        # Semi-transparent overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))

        # Error box
        box_width = 500
        box_height = 150
        box_x = (width - box_width) // 2
        box_y = (height - box_height) // 2

        pygame.draw.rect(overlay, (60, 20, 20, 250),
                        (box_x, box_y, box_width, box_height),
                        border_radius=10)
        pygame.draw.rect(overlay, (255, 100, 100),
                        (box_x, box_y, box_width, box_height),
                        3, border_radius=10)

        # Error text
        font = pygame.font.Font(None, 40)
        text_surf = font.render(message, True, (255, 200, 200))
        text_rect = text_surf.get_rect(center=(width // 2, height // 2))
        overlay.blit(text_surf, text_rect)

        screen.blit(overlay, (0, 0))
