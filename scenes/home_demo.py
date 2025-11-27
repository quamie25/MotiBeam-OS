#!/usr/bin/env python3
"""
VERTICAL 7: Smart Home / Family Dashboard Demo
Complete home automation control panel with family widgets
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime

class HomeDemo(MotiBeamScene):
    """Smart Home Dashboard with automation controls and family widgets"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Smart Home Dashboard", standalone=standalone)

        # Device states
        self.lights_on = True
        self.door_locked = True
        self.thermostat_mode = "HEAT"  # HEAT, COOL, OFF
        self.camera_active = True

        # Animation state
        self.fade_alpha = 0  # For fade-in effect
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Widget data
        self.weather_temp = 72
        self.weather_condition = "Partly Cloudy"
        self.calendar_events = [
            "Team Meeting - 2:00 PM",
            "Grocery Shopping - 5:30 PM"
        ]

        # Control toggle animations
        self.light_pulse = 0
        self.lock_pulse = 0
        self.thermo_pulse = 0
        self.camera_pulse = 0

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Start fade-out animation
                self.fade_out = True
            elif event.key == pygame.K_l:
                # Toggle lights
                self.lights_on = not self.lights_on
                self.light_pulse = 1.0
            elif event.key == pygame.K_d:
                # Toggle door lock
                self.door_locked = not self.door_locked
                self.lock_pulse = 1.0
            elif event.key == pygame.K_t:
                # Cycle thermostat mode
                modes = ["HEAT", "COOL", "OFF"]
                current_idx = modes.index(self.thermostat_mode)
                self.thermostat_mode = modes[(current_idx + 1) % len(modes)]
                self.thermo_pulse = 1.0
            elif event.key == pygame.K_c:
                # Toggle camera
                self.camera_active = not self.camera_active
                self.camera_pulse = 1.0

    def update(self, dt):
        """Update scene state with delta time"""
        # Update animation time
        self.animation_time += dt

        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_alpha = min(255, self.fade_alpha + (255 * dt / 1.0))  # 1 second fade-in
            if self.fade_alpha >= 255:
                self.fade_in_complete = True

        # Fade-out animation
        if self.fade_out:
            self.fade_alpha = max(0, self.fade_alpha - (255 * dt / 0.5))  # 0.5 second fade-out
            if self.fade_alpha <= 0:
                self.running = False

        # Decay pulse animations
        self.light_pulse = max(0, self.light_pulse - dt * 2)
        self.lock_pulse = max(0, self.lock_pulse - dt * 2)
        self.thermo_pulse = max(0, self.thermo_pulse - dt * 2)
        self.camera_pulse = max(0, self.camera_pulse - dt * 2)

    def draw(self):
        """Render the scene"""
        self.screen.fill(self.colors['black'])

        # Create a surface for fade effect
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])

        # Header
        title_surf = self.font_large.render("SMART HOME", True, self.colors['cyan'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=30)
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_small.render("Family Dashboard & Automation", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=self.width//2, top=130)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Current time display
        current_time = datetime.now().strftime("%I:%M %p")
        time_surf = self.font_medium.render(current_time, True, self.colors['green'])
        time_rect = time_surf.get_rect(centerx=self.width//2, top=180)
        self.screen.blit(time_surf, time_rect)

        # Layout: 2x2 grid for controls + sidebar for widgets
        control_width = 280
        control_height = 180
        grid_x_start = 80
        grid_y_start = 280
        grid_spacing_x = 320
        grid_spacing_y = 220

        # Control 1: Lights (top-left)
        self._draw_control_panel(
            grid_x_start,
            grid_y_start,
            control_width,
            control_height,
            "LIGHTS",
            "ON" if self.lights_on else "OFF",
            self.colors['yellow'] if self.lights_on else self.colors['gray'],
            "L",
            self.light_pulse
        )

        # Control 2: Door Lock (top-right)
        self._draw_control_panel(
            grid_x_start + grid_spacing_x,
            grid_y_start,
            control_width,
            control_height,
            "DOOR LOCK",
            "LOCKED" if self.door_locked else "UNLOCKED",
            self.colors['green'] if self.door_locked else self.colors['red'],
            "D",
            self.lock_pulse
        )

        # Control 3: Thermostat (bottom-left)
        thermo_color = self.colors['orange'] if self.thermostat_mode == "HEAT" else \
                       self.colors['blue'] if self.thermostat_mode == "COOL" else \
                       self.colors['gray']
        self._draw_control_panel(
            grid_x_start,
            grid_y_start + grid_spacing_y,
            control_width,
            control_height,
            "THERMOSTAT",
            self.thermostat_mode,
            thermo_color,
            "T",
            self.thermo_pulse
        )

        # Control 4: Security Camera (bottom-right)
        self._draw_control_panel(
            grid_x_start + grid_spacing_x,
            grid_y_start + grid_spacing_y,
            control_width,
            control_height,
            "CAMERA",
            "ACTIVE" if self.camera_active else "INACTIVE",
            self.colors['cyan'] if self.camera_active else self.colors['gray'],
            "C",
            self.camera_pulse
        )

        # Right sidebar for family widgets
        sidebar_x = 720
        sidebar_y = 280
        widget_width = 480

        # Weather widget
        self._draw_weather_widget(sidebar_x, sidebar_y, widget_width)

        # Calendar widget
        self._draw_calendar_widget(sidebar_x, sidebar_y + 200, widget_width)

        # Security status widget
        self._draw_security_widget(sidebar_x, sidebar_y + 380, widget_width)

        # Footer with controls
        footer_text = "L=Lights | D=Door | T=Thermo | C=Camera | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height-20)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(self.colors['cyan'])

        # Apply fade effect
        if self.fade_alpha < 255:
            self.screen.blit(fade_surface, (0, 0))

    def _draw_control_panel(self, x, y, width, height, label, status, color, key, pulse):
        """Draw a control panel with label, status, and animation"""
        # Background box with pulse effect
        border_width = 3
        if pulse > 0:
            pulse_color = tuple(min(255, int(c + (255 - c) * pulse)) for c in color)
            border_width = int(3 + pulse * 5)
        else:
            pulse_color = color

        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, pulse_color, panel_rect, border_width, border_radius=10)

        # Label
        label_surf = self.font_small.render(label, True, self.colors['white'])
        label_rect = label_surf.get_rect(centerx=x + width//2, top=y + 20)
        self.screen.blit(label_surf, label_rect)

        # Status with color
        status_surf = self.font_medium.render(status, True, color)
        status_rect = status_surf.get_rect(center=(x + width//2, y + height//2 + 10))
        self.screen.blit(status_surf, status_rect)

        # Key hint
        key_hint = f"[{key}]"
        key_surf = self.font_small.render(key_hint, True, self.colors['gray'])
        key_rect = key_surf.get_rect(centerx=x + width//2, bottom=y + height - 15)
        self.screen.blit(key_surf, key_rect)

        # Status indicator dot with animation
        dot_radius = 8
        if pulse > 0:
            dot_radius = int(8 + pulse * 4)
        pygame.draw.circle(self.screen, color, (x + width - 30, y + 30), dot_radius)

    def _draw_weather_widget(self, x, y, width):
        """Draw weather information widget"""
        # Border
        widget_rect = pygame.Rect(x, y, width, 150)
        pygame.draw.rect(self.screen, self.colors['blue'], widget_rect, 2, border_radius=8)

        # Title
        title_surf = self.font_small.render("WEATHER", True, self.colors['blue'])
        title_rect = title_surf.get_rect(left=x + 20, top=y + 15)
        self.screen.blit(title_surf, title_rect)

        # Temperature with animation
        temp_glow = 0.8 + 0.2 * abs(math.sin(self.animation_time))
        temp_color = tuple(int(c * temp_glow) for c in self.colors['orange'])
        temp_text = f"{self.weather_temp}°F"
        temp_surf = self.font_large.render(temp_text, True, temp_color)
        temp_rect = temp_surf.get_rect(left=x + 30, centery=y + 85)
        self.screen.blit(temp_surf, temp_rect)

        # Condition
        cond_surf = self.font_small.render(self.weather_condition, True, self.colors['white'])
        cond_rect = cond_surf.get_rect(right=x + width - 30, centery=y + 75)
        self.screen.blit(cond_surf, cond_rect)

    def _draw_calendar_widget(self, x, y, width):
        """Draw calendar/events widget"""
        # Border
        widget_rect = pygame.Rect(x, y, width, 150)
        pygame.draw.rect(self.screen, self.colors['purple'], widget_rect, 2, border_radius=8)

        # Title
        title_surf = self.font_small.render("TODAY'S SCHEDULE", True, self.colors['purple'])
        title_rect = title_surf.get_rect(left=x + 20, top=y + 15)
        self.screen.blit(title_surf, title_rect)

        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        date_surf = self.font_small.render(current_date, True, self.colors['white'])
        date_rect = date_surf.get_rect(left=x + 20, top=y + 50)
        self.screen.blit(date_surf, date_rect)

        # Events
        event_y = y + 85
        for i, event in enumerate(self.calendar_events[:2]):  # Show max 2 events
            # Bullet point with pulse
            pulse = abs(math.sin(self.animation_time + i * 0.5))
            bullet_color = tuple(int(100 + 155 * pulse) for _ in range(3))
            pygame.draw.circle(self.screen, bullet_color, (x + 30, event_y + 10), 5)

            # Event text
            event_surf = self.font_small.render(event, True, self.colors['white'])
            event_rect = event_surf.get_rect(left=x + 50, top=event_y)
            self.screen.blit(event_surf, event_rect)
            event_y += 35

    def _draw_security_widget(self, x, y, width):
        """Draw security status widget"""
        # Border with color based on security status
        security_color = self.colors['green'] if self.door_locked and self.camera_active else self.colors['orange']
        widget_rect = pygame.Rect(x, y, width, 100)
        pygame.draw.rect(self.screen, security_color, widget_rect, 2, border_radius=8)

        # Title
        title_surf = self.font_small.render("SECURITY STATUS", True, security_color)
        title_rect = title_surf.get_rect(left=x + 20, top=y + 15)
        self.screen.blit(title_surf, title_rect)

        # Status text
        if self.door_locked and self.camera_active:
            status_text = "ALL SYSTEMS SECURE"
            status_color = self.colors['green']
        elif self.door_locked or self.camera_active:
            status_text = "PARTIAL SECURITY"
            status_color = self.colors['orange']
        else:
            status_text = "SECURITY DISABLED"
            status_color = self.colors['red']

        # Animated status with pulse
        pulse = abs(math.sin(self.animation_time * 2))
        pulse_alpha = int(180 + 75 * pulse)
        status_surf = self.font_medium.render(status_text, True, status_color)
        status_surf.set_alpha(pulse_alpha)
        status_rect = status_surf.get_rect(centerx=x + width//2, centery=y + 65)
        self.screen.blit(status_surf, status_rect)

    def run(self, duration=300):
        """Custom run loop with proper event and dt handling"""
        print(f"Starting {self.__class__.__name__}...")
        last_time = pygame.time.get_ticks()

        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time

            # Auto-exit after duration
            elapsed = (current_time - self.start_time) / 1000
            if elapsed > duration:
                print(f"{duration} seconds elapsed, exiting...")
                self.running = False

            # Handle events with individual event passing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_events(event)

            # Update with delta time
            self.update(dt)

            # Draw (using draw instead of render)
            self.draw()

            # Flip display and tick clock
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS for smooth animations

        # Only quit pygame if standalone
        if self.standalone:
            pygame.quit()
        print("Scene complete.")

if __name__ == "__main__":
    demo = HomeDemo(standalone=True)
    demo.run(duration=300)  # Run for 5 minutes when standalone
