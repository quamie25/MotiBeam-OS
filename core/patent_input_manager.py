#!/usr/bin/env python3
"""
PATENT MAPPING (Internal Design Note):
- Aligns with filed MotiBeam patents for:
  - Universal Ambient Projection System (Claim 24: seamless transitions)
  - Cross-vertical control and navigation
Relevant claims: 20, 23, 24.
This is an architectural implementation, not a legal opinion.

PatentProtectedInputManager - Phase 1 Global Input Handler
Provides universal input commands that work across all verticals.
"""

import pygame
import time


class PatentProtectedInputManager:
    """
    Global Input Manager (Patent Claim 24: Seamless Transitions)

    Provides universal keyboard commands that work from ANY vertical:
    - ESC: Return to main menu (seamless transition)
    - SPACE: Quick context settings overlay
    - TAB: Cycle through verticals in configured order
    - M: Toggle universal master menu

    Phase 1: Core command handling with cursor management
    Phase 2: Gesture recognition, voice commands, wearable input
    """

    def __init__(self, os_ref):
        """
        Initialize patent-protected input manager

        Args:
            os_ref: Reference to main MotiBeamOS instance
        """
        self.os_ref = os_ref  # Reference to main OS for state control

        # Quick settings overlay state
        self.quick_settings_open = False

        # Master menu state
        self.master_menu_open = False

        # Cursor auto-hide tracking
        self.last_mouse_movement = time.time()
        self.cursor_visible = True
        self.cursor_hide_delay = 3.0  # seconds

        print("[PatentInputManager] Initialized (patent-aligned)")

    def handle_global_commands(self, event):
        """
        Handle global keyboard commands that work everywhere

        Args:
            event: pygame.event.Event - Input event to process

        Returns:
            bool: True if event was handled (stop further processing)

        Phase 1: Handle ESC/SPACE/TAB/M keys
        Phase 2: Add gesture, voice, and wearable inputs
        """
        # Track mouse movement for cursor auto-hide
        if event.type == pygame.MOUSEMOTION:
            self.last_mouse_movement = time.time()
            if not self.cursor_visible:
                pygame.mouse.set_visible(True)
                self.cursor_visible = True
            return False  # Don't block mouse movement events

        # Only handle keyboard events for global commands
        if event.type != pygame.KEYDOWN:
            return False

        # ESC: Return to main menu (Claim 24: seamless transitions)
        if event.key == pygame.K_ESCAPE:
            # If quick settings or master menu is open, close them first
            if self.quick_settings_open:
                self.quick_settings_open = False
                return True
            elif self.master_menu_open:
                self.master_menu_open = False
                return True
            else:
                # Return to main menu from any vertical
                self.return_to_main_menu()
                return True

        # SPACE: Toggle quick settings overlay
        elif event.key == pygame.K_SPACE:
            self.toggle_quick_settings()
            return True

        # TAB: Cycle to next vertical
        elif event.key == pygame.K_TAB:
            self.cycle_verticals()
            return True

        # M: Toggle master menu
        elif event.key == pygame.K_m:
            self.toggle_master_menu()
            return True

        # Command not handled
        return False

    def return_to_main_menu(self):
        """
        Return to main menu from current vertical (Claim 24: seamless transitions)

        Phase 1: Set flags to exit current mode
        Phase 2: Smooth transition animations
        """
        print("[PatentInputManager] Return to main menu requested")

        # TODO Phase 2: Fade-out transition animation
        # TODO Phase 2: Save current vertical state for resume

        # Signal to OS to exit current mode
        if hasattr(self.os_ref, 'current_mode'):
            print(f"[PatentInputManager] Exiting mode: {self.os_ref.current_mode}")

        # Close any overlays first
        self.quick_settings_open = False
        self.master_menu_open = False

        # Note: Actual menu return is handled by the event loop in motibeam_v3.py
        # This method just sets the intent

    def toggle_quick_settings(self):
        """
        Toggle quick context settings overlay (SPACE key)

        Phase 1: Simple overlay with global commands
        Phase 2: Context-aware settings based on active vertical
        """
        self.quick_settings_open = not self.quick_settings_open

        if self.quick_settings_open:
            print("[PatentInputManager] Quick settings opened")
            # Close master menu if it's open
            self.master_menu_open = False
        else:
            print("[PatentInputManager] Quick settings closed")

        # TODO Phase 2: Show vertical-specific quick settings
        # TODO Phase 2: Recently used settings
        # TODO Phase 2: User favorites

    def cycle_verticals(self):
        """
        Cycle to next vertical in configured order (TAB key)

        Phase 1: Log intent (actual cycling done by OS)
        Phase 2: Smooth vertical transitions with state preservation
        """
        print("[PatentInputManager] Cycle to next vertical requested")

        # TODO Phase 2: Determine next vertical from patent_vertical_config
        # TODO Phase 2: Cross-fade transition between verticals
        # TODO Phase 2: Preserve state for return to previous vertical

        # Note: Actual cycling logic in motibeam_v3.py
        # This sets the intent via flag or callback

    def toggle_master_menu(self):
        """
        Toggle universal master menu overlay (M key)

        Phase 1: Simple menu overlay
        Phase 2: Full system control panel
        """
        self.master_menu_open = not self.master_menu_open

        if self.master_menu_open:
            print("[PatentInputManager] Master menu opened")
            # Close quick settings if it's open
            self.quick_settings_open = False
        else:
            print("[PatentInputManager] Master menu closed")

        # TODO Phase 2: System settings access
        # TODO Phase 2: User profile management
        # TODO Phase 2: Device pairing controls
        # TODO Phase 2: Projection calibration

    def render_quick_settings(self, screen):
        """
        Render quick settings overlay if open

        Args:
            screen: pygame.Surface - Surface to draw on

        Phase 1: Simple text overlay
        Phase 2: Rich UI with interactive controls
        """
        if not self.quick_settings_open:
            return

        # Get screen dimensions
        width, height = screen.get_size()

        # Semi-transparent overlay background
        overlay = pygame.Surface((400, 300))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))

        # Border
        pygame.draw.rect(overlay, (0, 255, 180), overlay.get_rect(), 3, border_radius=10)

        # Title
        font_title = pygame.font.Font(None, 48)
        title = font_title.render("Quick Menu", True, (0, 255, 180))
        overlay.blit(title, (overlay.get_width() // 2 - title.get_width() // 2, 20))

        # Menu options
        font_option = pygame.font.Font(None, 32)
        options = [
            "ESC - Return to Menu",
            "SPACE - Close This Menu",
            "TAB - Next Vertical",
            "M - Master Menu",
            "S - Full Settings",
        ]

        y_pos = 80
        for option in options:
            text = font_option.render(option, True, (200, 200, 200))
            overlay.blit(text, (30, y_pos))
            y_pos += 40

        # Center overlay on screen
        screen.blit(overlay, (width // 2 - 200, height // 2 - 150))

    def render_master_menu(self, screen):
        """
        Render master menu overlay if open

        Args:
            screen: pygame.Surface - Surface to draw on

        Phase 1: Placeholder - similar to quick settings
        Phase 2: Full system control interface
        """
        if not self.master_menu_open:
            return

        # Get screen dimensions
        width, height = screen.get_size()

        # Larger overlay for master menu
        overlay = pygame.Surface((500, 400))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))

        # Border
        pygame.draw.rect(overlay, (255, 180, 0), overlay.get_rect(), 3, border_radius=10)

        # Title
        font_title = pygame.font.Font(None, 48)
        title = font_title.render("Master Menu", True, (255, 180, 0))
        overlay.blit(title, (overlay.get_width() // 2 - title.get_width() // 2, 20))

        # Menu sections
        font_section = pygame.font.Font(None, 28)
        sections = [
            "System Settings",
            "User Profiles",
            "Device Pairing",
            "Projection Calibration",
            "Wearable Integration",
            "Sensor Configuration",
            "",
            "Press M or ESC to close",
        ]

        y_pos = 80
        for section in sections:
            if section:
                text = font_section.render(section, True, (200, 200, 200))
                overlay.blit(text, (40, y_pos))
            y_pos += 35

        # Center overlay on screen
        screen.blit(overlay, (width // 2 - 250, height // 2 - 200))

        # TODO Phase 2: Interactive menu items
        # TODO Phase 2: Sub-menus for each section
        # TODO Phase 2: Live status indicators

    def should_hide_cursor(self):
        """
        Check if cursor should be hidden due to inactivity

        Returns:
            bool: True if cursor should be hidden

        Phase 1: Time-based auto-hide
        Phase 2: Context-aware cursor visibility
        """
        time_since_movement = time.time() - self.last_mouse_movement
        return time_since_movement > self.cursor_hide_delay

    def reset_cursor_timer(self):
        """
        Reset cursor auto-hide timer (call when user interacts)

        Phase 1: Reset timer only
        Phase 2: Learn user interaction patterns
        """
        self.last_mouse_movement = time.time()
        if not self.cursor_visible:
            pygame.mouse.set_visible(True)
            self.cursor_visible = True
