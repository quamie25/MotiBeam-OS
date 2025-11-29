#!/usr/bin/env python3
"""
MotiBeamOS v4.0 - Display Manager
Handles display setup, projector detection, and cinematic mode
"""

import pygame
import os


class DisplayManager:
    """Manages display setup and projector configuration"""

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.screen = None
        self.cursor_visible = True
        self.is_fullscreen = False

        # Check environment variables
        self.debug_windowed = os.environ.get('MOTIBEAM_WINDOWED', '0') == '1'
        self.force_fullscreen = os.environ.get('MOTIBEAM_FULLSCREEN', '0') == '1'

    def setup_display(self):
        """Setup display with optimal settings"""
        pygame.init()

        # Determine if we should use fullscreen
        use_fullscreen = self.force_fullscreen or (not self.debug_windowed and self.should_use_fullscreen())

        if use_fullscreen:
            print("[DISPLAY] Enabling cinematic fullscreen mode")
            self.enable_cinematic_mode()
        else:
            print("[DISPLAY] Using windowed mode (800x600)")
            self.width = 800
            self.height = 600
            self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("MotiBeam OS v4.0")

        # Check display driver
        driver = pygame.display.get_driver()
        print(f"[DISPLAY] Driver: {driver}, Resolution: {self.width}x{self.height}")

        if driver == "offscreen":
            print("⚠️  WARNING: Using offscreen driver - set DISPLAY=:0 if on Pi")

        return self.screen

    def should_use_fullscreen(self):
        """Determine if fullscreen should be used"""
        # Check if projector is connected or if we're on a Pi with display
        display_driver = pygame.display.get_driver()
        return display_driver != "offscreen"

    def enable_cinematic_mode(self):
        """Enable true fullscreen - no borders, no title bar"""
        try:
            # Get display info
            display_info = pygame.display.Info()
            self.width = display_info.current_w
            self.height = display_info.current_h

            print(f"[DISPLAY] Native resolution: {self.width}x{self.height}")

            # Try NOFRAME first for borderless fullscreen
            try:
                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                print("[DISPLAY] Cinematic mode: NOFRAME")
            except:
                # Fallback to regular fullscreen
                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                print("[DISPLAY] Cinematic mode: FULLSCREEN")

            self.is_fullscreen = True
            self.auto_center_calibration()

        except Exception as e:
            print(f"[DISPLAY] Cinematic mode failed: {e}")
            # Fallback to standard fullscreen
            self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
            self.is_fullscreen = True

    def auto_center_calibration(self):
        """Auto-detect and center for projector"""
        # Projector-specific calibration can be added here
        if self.is_projector_connected():
            print("[DISPLAY] Projector detected, using optimal settings")
            self.use_projector_resolution()

    def is_projector_connected(self):
        """Check if projector is connected"""
        # This is a placeholder - actual detection would require platform-specific code
        # For now, assume projector if resolution is standard projection size
        return self.width >= 1280 and self.height >= 720

    def use_projector_resolution(self):
        """Optimize for projector display"""
        # Projectors typically prefer these resolutions
        common_projector_res = [
            (1920, 1080),  # Full HD
            (1280, 720),   # HD
            (1024, 768),   # XGA
        ]

        # Find best match
        current_res = (self.width, self.height)
        if current_res not in common_projector_res:
            print(f"[DISPLAY] Non-standard resolution: {current_res}")

    def update_cursor_visibility(self, input_manager):
        """Update cursor visibility based on inactivity"""
        should_hide = input_manager.should_hide_cursor()

        if should_hide and self.cursor_visible:
            pygame.mouse.set_visible(False)
            self.cursor_visible = False
            print("[DISPLAY] Cursor hidden (3s inactivity)")
        elif not should_hide and not self.cursor_visible:
            pygame.mouse.set_visible(True)
            self.cursor_visible = True

    def hide_cursor_after_delay(self, input_manager):
        """Check and hide cursor if inactive"""
        self.update_cursor_visibility(input_manager)

    def get_screen(self):
        """Get the screen surface"""
        return self.screen

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.is_fullscreen:
            self.width = 800
            self.height = 600
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.is_fullscreen = False
            print("[DISPLAY] Switched to windowed mode")
        else:
            self.enable_cinematic_mode()
            print("[DISPLAY] Switched to fullscreen mode")
