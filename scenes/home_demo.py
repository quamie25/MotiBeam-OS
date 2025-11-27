#!/usr/bin/env python3
"""
VERTICAL 7: Smart Home / Family Dashboard Demo
Complete home automation control panel with family widgets and activity tracking
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime

class HomeDashboardScene(MotiBeamScene):
    """Smart Home Dashboard with automation controls and family widgets"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Smart Home Dashboard", standalone=standalone)

        # Device states
        self.lights_on = True
        self.door_locked = True
        self.garage_open = False
        self.thermostat_mode = "OFF"  # OFF, HEAT, COOL
        self.thermostat_temp = 72
        self.camera_active = True

        # Animation state
        self.fade_alpha = 0  # For fade-in effect (starts at 0, goes to 255)
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Control toggle animations (pulse effects)
        self.light_pulse = 0
        self.lock_pulse = 0
        self.garage_pulse = 0
        self.thermo_pulse = 0
        self.camera_pulse = 0
        self.camera_blink = 0

        # Recent activity feed
        self.recent_activities = [
            self._format_activity("System initialized"),
            self._format_activity("Dashboard started"),
        ]
        self.max_activities = 8

    def _format_activity(self, message):
        """Format an activity with current timestamp"""
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        return f"{timestamp} - {message}"

    def _add_activity(self, message):
        """Add a new activity to the recent feed"""
        self.recent_activities.insert(0, self._format_activity(message))
        # Keep only the most recent activities
        if len(self.recent_activities) > self.max_activities:
            self.recent_activities = self.recent_activities[:self.max_activities]

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Start fade-out animation
                self.fade_out = True
                self._add_activity("Dashboard closing...")
            elif event.key == pygame.K_l:
                # Toggle lights
                self.lights_on = not self.lights_on
                self.light_pulse = 1.0
                status = "ON" if self.lights_on else "OFF"
                self._add_activity(f"Lights turned {status}")
            elif event.key == pygame.K_d:
                # Toggle door lock
                self.door_locked = not self.door_locked
                self.lock_pulse = 1.0
                status = "LOCKED" if self.door_locked else "UNLOCKED"
                self._add_activity(f"Front door {status}")
            elif event.key == pygame.K_g:
                # Toggle garage
                self.garage_open = not self.garage_open
                self.garage_pulse = 1.0
                status = "OPENED" if self.garage_open else "CLOSED"
                self._add_activity(f"Garage door {status}")
            elif event.key == pygame.K_t:
                # Cycle thermostat mode and adjust temperature
                modes = ["OFF", "HEAT", "COOL"]
                current_idx = modes.index(self.thermostat_mode)
                self.thermostat_mode = modes[(current_idx + 1) % len(modes)]

                # Adjust target temperature based on mode
                if self.thermostat_mode == "HEAT":
                    self.thermostat_temp = 72
                elif self.thermostat_mode == "COOL":
                    self.thermostat_temp = 68
                else:
                    self.thermostat_temp = 70

                self.thermo_pulse = 1.0
                self._add_activity(f"Thermostat set to {self.thermostat_mode} ({self.thermostat_temp}°F)")
            elif event.key == pygame.K_c:
                # Toggle camera
                self.camera_active = not self.camera_active
                self.camera_pulse = 1.0
                status = "ACTIVATED" if self.camera_active else "DEACTIVATED"
                self._add_activity(f"Security camera {status}")

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

        # Decay pulse animations
        self.light_pulse = max(0, self.light_pulse - dt * 2.5)
        self.lock_pulse = max(0, self.lock_pulse - dt * 2.5)
        self.garage_pulse = max(0, self.garage_pulse - dt * 2.5)
        self.thermo_pulse = max(0, self.thermo_pulse - dt * 2.5)
        self.camera_pulse = max(0, self.camera_pulse - dt * 2.5)

        # Camera blink animation
        self.camera_blink += dt * 3
        if self.camera_blink > 2 * math.pi:
            self.camera_blink = 0

    def draw(self):
        """Render the scene"""
        self.screen.fill(self.colors['black'])

        # Header
        title_surf = self.font_large.render("SMART HOME", True, self.colors['cyan'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=20)
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_small.render("Family Dashboard & Automation", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=self.width//2, top=110)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Current time and date display
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%A, %B %d")

        time_surf = self.font_medium.render(current_time, True, self.colors['green'])
        time_rect = time_surf.get_rect(centerx=self.width//2, top=150)
        self.screen.blit(time_surf, time_rect)

        date_surf = self.font_small.render(current_date, True, self.colors['gray'])
        date_rect = date_surf.get_rect(centerx=self.width//2, top=205)
        self.screen.blit(date_surf, date_rect)

        # Left section: HOME STATUS controls
        status_x = 50
        status_y = 270
        status_width = 550

        self._draw_status_header(status_x, status_y, "HOME STATUS")

        # Status items with enhanced animations
        item_y = status_y + 60
        item_height = 65

        # Lights status
        self._draw_status_item(
            status_x, item_y, status_width, item_height,
            "💡 Lights",
            "ON" if self.lights_on else "OFF",
            self.colors['yellow'] if self.lights_on else self.colors['gray'],
            self.light_pulse,
            glow=self.lights_on
        )

        # Door Lock status
        item_y += item_height
        self._draw_status_item(
            status_x, item_y, status_width, item_height,
            "🔒 Front Door",
            "LOCKED" if self.door_locked else "UNLOCKED",
            self.colors['green'] if self.door_locked else self.colors['red'],
            self.lock_pulse,
            alert=not self.door_locked
        )

        # Garage status
        item_y += item_height
        self._draw_status_item(
            status_x, item_y, status_width, item_height,
            "🚗 Garage Door",
            "CLOSED" if not self.garage_open else "OPEN",
            self.colors['green'] if not self.garage_open else self.colors['orange'],
            self.garage_pulse,
            arrow=self.garage_open
        )

        # Thermostat status
        item_y += item_height
        thermo_color = self.colors['orange'] if self.thermostat_mode == "HEAT" else \
                       self.colors['blue'] if self.thermostat_mode == "COOL" else \
                       self.colors['gray']
        thermo_status = f"{self.thermostat_mode} - {self.thermostat_temp}°F" if self.thermostat_mode != "OFF" else "OFF"
        self._draw_status_item(
            status_x, item_y, status_width, item_height,
            "🌡️ Thermostat",
            thermo_status,
            thermo_color,
            self.thermo_pulse,
            temp_mode=self.thermostat_mode
        )

        # Camera status
        item_y += item_height
        self._draw_status_item(
            status_x, item_y, status_width, item_height,
            "📹 Security Camera",
            "ACTIVE" if self.camera_active else "INACTIVE",
            self.colors['cyan'] if self.camera_active else self.colors['gray'],
            self.camera_pulse,
            recording=self.camera_active
        )

        # Right section: RECENT ACTIVITY
        activity_x = 650
        activity_y = 270
        activity_width = 580

        self._draw_activity_panel(activity_x, activity_y, activity_width)

        # Footer with controls
        footer_text = "L=Lights | D=Door | G=Garage | T=Thermo | C=Camera | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height-15)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(self.colors['cyan'])

        # Apply fade effect (for fade-in and fade-out)
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(255 - int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])
            self.screen.blit(fade_surface, (0, 0))

    def _draw_status_header(self, x, y, title):
        """Draw section header"""
        title_surf = self.font_medium.render(title, True, self.colors['cyan'])
        self.screen.blit(title_surf, (x + 10, y))

        # Underline
        line_y = y + 50
        pygame.draw.line(self.screen, self.colors['cyan'], (x, line_y), (x + 550, line_y), 2)

    def _draw_status_item(self, x, y, width, height, label, status, color, pulse,
                         glow=False, alert=False, arrow=False, temp_mode=None, recording=False):
        """Draw an individual status item with various animation effects"""

        # Background glow effect for lights
        if glow and pulse > 0.1:
            glow_intensity = int(30 + 50 * pulse)
            glow_color = (*color[:3], glow_intensity) if len(color) == 3 else color
            glow_rect = pygame.Rect(x - 5, y - 5, width + 10, height + 10)
            glow_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.colors['yellow'], glow_intensity), glow_surf.get_rect(), border_radius=12)
            self.screen.blit(glow_surf, (x - 5, y - 5))

        # Main background with pulse border
        border_width = 2
        border_color = self.colors['white']

        if pulse > 0:
            border_width = int(2 + pulse * 4)
            pulse_brightness = int(155 + 100 * pulse)
            border_color = (pulse_brightness, pulse_brightness, pulse_brightness)

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, item_rect, border_width, border_radius=10)

        # Label
        label_surf = self.font_small.render(label, True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Status with color and effects
        status_color = color
        if alert and pulse > 0:
            # Pulsing alert color for unlocked door
            pulse_factor = abs(math.sin(self.animation_time * 3))
            status_color = tuple(int(c * (0.7 + 0.3 * pulse_factor)) for c in color)

        status_surf = self.font_medium.render(status, True, status_color)
        status_rect = status_surf.get_rect(right=x + width - 15, centery=y + height // 2)
        self.screen.blit(status_surf, status_rect)

        # Special animations
        # Arrow for garage
        if arrow:
            arrow_x = x + width - 180
            arrow_y = y + height // 2
            # Animated up arrow
            arrow_offset = int(5 * abs(math.sin(self.animation_time * 2)))
            arrow_points = [
                (arrow_x, arrow_y - 8 - arrow_offset),
                (arrow_x - 8, arrow_y + 2 - arrow_offset),
                (arrow_x + 8, arrow_y + 2 - arrow_offset)
            ]
            pygame.draw.polygon(self.screen, self.colors['orange'], arrow_points)

        # Temperature color indicator for thermostat
        if temp_mode == "HEAT":
            # Draw warm color bar
            bar_x = x + width - 200
            bar_y = y + height - 15
            pygame.draw.rect(self.screen, self.colors['orange'], (bar_x, bar_y, 80, 8), border_radius=4)
        elif temp_mode == "COOL":
            # Draw cool color bar
            bar_x = x + width - 200
            bar_y = y + height - 15
            pygame.draw.rect(self.screen, self.colors['blue'], (bar_x, bar_y, 80, 8), border_radius=4)

        # Recording indicator for camera
        if recording:
            # Blinking red dot
            blink_alpha = int(128 + 127 * abs(math.sin(self.camera_blink)))
            dot_x = x + width - 180
            dot_y = y + height // 2
            dot_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(dot_surf, (*self.colors['red'], blink_alpha), (10, 10), 8)
            self.screen.blit(dot_surf, (dot_x - 10, dot_y - 10))

            # "REC" text
            rec_surf = self.font_small.render("REC", True, self.colors['red'])
            rec_surf.set_alpha(blink_alpha)
            self.screen.blit(rec_surf, (dot_x + 15, dot_y - 12))

    def _draw_activity_panel(self, x, y, width):
        """Draw the recent activity feed"""
        # Header
        self._draw_status_header(x, y, "RECENT ACTIVITY")

        # Activity list
        activity_y = y + 70
        activity_height = 48

        for i, activity in enumerate(self.recent_activities[:8]):
            # Fade older activities
            age_factor = 1.0 - (i * 0.08)
            text_color = tuple(int(c * age_factor) for c in self.colors['white'])

            # Activity text with word wrapping if needed
            activity_surf = self.font_small.render(activity, True, text_color)

            # Truncate if too long
            if activity_surf.get_width() > width - 40:
                # Truncate and add ellipsis
                truncated = activity[:50] + "..."
                activity_surf = self.font_small.render(truncated, True, text_color)

            self.screen.blit(activity_surf, (x + 20, activity_y))

            # Separator line
            if i < len(self.recent_activities) - 1 and i < 7:
                line_y = activity_y + 35
                line_color = tuple(int(c * age_factor * 0.3) for c in self.colors['white'])
                pygame.draw.line(self.screen, line_color, (x + 10, line_y), (x + width - 10, line_y), 1)

            activity_y += activity_height

    def run(self, duration=300):
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
    demo = HomeDashboardScene(standalone=True)
    demo.run(duration=300)  # Run for 5 minutes when standalone
