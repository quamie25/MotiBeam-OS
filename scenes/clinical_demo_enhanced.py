#!/usr/bin/env python3
"""
VERTICAL 1: Clinical & Wellness - Interactive Dashboard
Complete clinical monitoring with medication reminders, breathing exercises, and stress management
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime, timedelta

class ClinicalWellnessEnhanced(MotiBeamScene):
    """Interactive Clinical & Wellness Dashboard with real-time monitoring"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Clinical & Wellness", standalone=standalone)

        # Medication reminder state
        self.medication_enabled = True
        self.medication_countdown = 300  # 5 minutes in seconds
        self.medication_name = "Morning Vitamins"
        self.medication_overdue = False

        # Breathing exercise state
        self.breathing_active = False
        self.breathing_phase = "idle"  # idle, inhale, hold, exhale
        self.breathing_timer = 0
        self.breathing_cycle_count = 0
        self.breathing_circle_radius = 80
        self.breathing_target_radius = 80

        # Stress grounding mode state
        self.stress_mode_active = False
        self.stress_timer = 0
        self.stress_wave_offset = 0
        self.stress_session_duration = 0

        # Animation state
        self.fade_alpha = 0  # For fade-in effect
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Pulse animations
        self.med_pulse = 0
        self.breathing_pulse = 0
        self.stress_pulse = 0

        # Vital signs (simulated)
        self.heart_rate = 72
        self.heart_rate_pulse = 0

        # Activity feed
        self.recent_activities = [
            self._format_activity("Clinical dashboard initialized"),
            self._format_activity("System ready"),
        ]
        self.max_activities = 8

    def _format_activity(self, message):
        """Format an activity with current timestamp"""
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        return f"{timestamp} - {message}"

    def _add_activity(self, message):
        """Add a new activity to the recent feed"""
        self.recent_activities.insert(0, self._format_activity(message))
        if len(self.recent_activities) > self.max_activities:
            self.recent_activities = self.recent_activities[:self.max_activities]

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Start fade-out animation
                self.fade_out = True
                self._add_activity("Dashboard closing...")
            elif event.key == pygame.K_m:
                # Toggle/reset medication reminder
                if self.medication_overdue:
                    # Mark as taken
                    self.medication_overdue = False
                    self.medication_countdown = 300  # Reset to 5 minutes
                    self._add_activity(f"✓ {self.medication_name} marked as taken")
                else:
                    # Test reminder (set to 10 seconds)
                    self.medication_countdown = 10
                    self._add_activity("Medication reminder set to 10 seconds (test mode)")
                self.med_pulse = 1.0
            elif event.key == pygame.K_b:
                # Toggle breathing exercise
                if not self.breathing_active:
                    self.breathing_active = True
                    self.breathing_phase = "inhale"
                    self.breathing_timer = 0
                    self.breathing_cycle_count = 0
                    self._add_activity("Started guided breathing exercise")
                else:
                    self.breathing_active = False
                    self.breathing_phase = "idle"
                    self._add_activity(f"Breathing exercise completed ({self.breathing_cycle_count} cycles)")
                self.breathing_pulse = 1.0
            elif event.key == pygame.K_s:
                # Toggle stress grounding mode
                if not self.stress_mode_active:
                    self.stress_mode_active = True
                    self.stress_timer = 0
                    self.stress_session_duration = 0
                    self._add_activity("Started stress grounding session")
                else:
                    self.stress_mode_active = False
                    duration = int(self.stress_session_duration)
                    self._add_activity(f"Stress session completed ({duration}s)")
                self.stress_pulse = 1.0

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
        self.med_pulse = max(0, self.med_pulse - dt * 2.5)
        self.breathing_pulse = max(0, self.breathing_pulse - dt * 2.5)
        self.stress_pulse = max(0, self.stress_pulse - dt * 2.5)

        # Update medication countdown
        if self.medication_enabled and not self.medication_overdue:
            self.medication_countdown -= dt
            if self.medication_countdown <= 0:
                self.medication_countdown = 0
                self.medication_overdue = True
                self._add_activity(f"⚠ MEDICATION REMINDER: {self.medication_name} is due!")

        # Update breathing exercise
        if self.breathing_active:
            self.breathing_timer += dt

            if self.breathing_phase == "inhale":
                # Inhale for 4 seconds
                self.breathing_target_radius = 150
                if self.breathing_timer >= 4.0:
                    self.breathing_phase = "hold_in"
                    self.breathing_timer = 0
            elif self.breathing_phase == "hold_in":
                # Hold for 2 seconds
                self.breathing_target_radius = 150
                if self.breathing_timer >= 2.0:
                    self.breathing_phase = "exhale"
                    self.breathing_timer = 0
            elif self.breathing_phase == "exhale":
                # Exhale for 6 seconds
                self.breathing_target_radius = 80
                if self.breathing_timer >= 6.0:
                    self.breathing_phase = "hold_out"
                    self.breathing_timer = 0
            elif self.breathing_phase == "hold_out":
                # Hold for 2 seconds
                self.breathing_target_radius = 80
                if self.breathing_timer >= 2.0:
                    self.breathing_phase = "inhale"
                    self.breathing_timer = 0
                    self.breathing_cycle_count += 1

            # Smooth interpolation towards target radius
            radius_diff = self.breathing_target_radius - self.breathing_circle_radius
            self.breathing_circle_radius += radius_diff * dt * 2.5

        # Update stress grounding mode
        if self.stress_mode_active:
            self.stress_timer += dt
            self.stress_session_duration += dt
            self.stress_wave_offset += dt * 1.5

        # Heart rate pulse animation
        self.heart_rate_pulse = abs(math.sin(self.animation_time * 3))

    def draw(self):
        """Render the scene"""
        self.screen.fill(self.colors['black'])

        # Header
        title_surf = self.font_large.render("CLINICAL & WELLNESS", True, self.colors['green'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=20)
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_small.render("Patient Monitoring & Wellness Management", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=self.width//2, top=110)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Current time display
        current_time = datetime.now().strftime("%I:%M %p")
        time_surf = self.font_medium.render(current_time, True, self.colors['cyan'])
        time_rect = time_surf.get_rect(centerx=self.width//2, top=150)
        self.screen.blit(time_surf, time_rect)

        # Left panel: Clinical Status
        status_x = 50
        status_y = 240
        status_width = 550

        self._draw_status_header(status_x, status_y, "CLINICAL STATUS")

        # Status items
        item_y = status_y + 60
        item_height = 75

        # Vital Signs (Heart Rate)
        self._draw_vital_signs(status_x, item_y, status_width, item_height)

        # Medication Reminder
        item_y += item_height + 10
        self._draw_medication_status(status_x, item_y, status_width, item_height)

        # Breathing Exercise Status
        item_y += item_height + 10
        self._draw_breathing_status(status_x, item_y, status_width, item_height)

        # Stress Grounding Status
        item_y += item_height + 10
        self._draw_stress_status(status_x, item_y, status_width, item_height)

        # Center/Right: Active Mode Visualization or Activity Feed
        viz_x = 650
        viz_y = 240
        viz_width = 580

        if self.breathing_active:
            # Show breathing visualization
            self._draw_breathing_visualization(viz_x, viz_y, viz_width, 450)
        elif self.stress_mode_active:
            # Show stress grounding visualization
            self._draw_stress_visualization(viz_x, viz_y, viz_width, 450)
        else:
            # Show activity feed
            self._draw_activity_panel(viz_x, viz_y, viz_width)

        # Footer with controls
        footer_text = "M=Medication | B=Breathing | S=Stress Mode | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height-15)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(self.colors['green'])

        # Apply fade effect
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(255 - int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])
            self.screen.blit(fade_surface, (0, 0))

    def _draw_status_header(self, x, y, title):
        """Draw section header"""
        title_surf = self.font_medium.render(title, True, self.colors['green'])
        self.screen.blit(title_surf, (x + 10, y))

        # Underline
        line_y = y + 50
        pygame.draw.line(self.screen, self.colors['green'], (x, line_y), (x + 550, line_y), 2)

    def _draw_vital_signs(self, x, y, width, height):
        """Draw vital signs (heart rate)"""
        border_color = self.colors['green']

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, item_rect, 2, border_radius=10)

        # Label with heart icon
        label_surf = self.font_small.render("❤️  Heart Rate", True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Heart rate value with pulse animation
        pulse_scale = 1.0 + (self.heart_rate_pulse * 0.15)
        hr_font = pygame.font.Font(None, int(60 * pulse_scale))
        hr_text = f"{self.heart_rate} bpm"
        hr_color = tuple(int(c * (0.85 + 0.15 * self.heart_rate_pulse)) for c in self.colors['green'])
        hr_surf = hr_font.render(hr_text, True, hr_color)
        hr_rect = hr_surf.get_rect(right=x + width - 15, centery=y + height // 2)
        self.screen.blit(hr_surf, hr_rect)

        # Status indicator
        status_surf = self.font_small.render("NORMAL", True, self.colors['green'])
        self.screen.blit(status_surf, (x + 15, y + height - 25))

    def _draw_medication_status(self, x, y, width, height):
        """Draw medication reminder status"""
        # Determine color based on state
        if self.medication_overdue:
            color = self.colors['red']
            status_text = "OVERDUE!"
            blink = abs(math.sin(self.animation_time * 4))
            border_width = int(2 + blink * 4)
        else:
            color = self.colors['yellow']
            status_text = "SCHEDULED"
            border_width = 2

        # Apply pulse effect
        if self.med_pulse > 0:
            border_width = int(2 + self.med_pulse * 4)
            pulse_brightness = int(155 + 100 * self.med_pulse)
            border_color = (pulse_brightness, pulse_brightness, pulse_brightness)
        else:
            border_color = color

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, item_rect, border_width, border_radius=10)

        # Label
        label_surf = self.font_small.render("💊 Medication Reminder", True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Countdown or overdue message
        if self.medication_overdue:
            msg_surf = self.font_medium.render(status_text, True, self.colors['red'])
            msg_surf.set_alpha(int(128 + 127 * blink))
            msg_rect = msg_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(msg_surf, msg_rect)
        else:
            # Convert countdown to mm:ss
            minutes = int(self.medication_countdown // 60)
            seconds = int(self.medication_countdown % 60)
            countdown_text = f"{minutes:02d}:{seconds:02d}"
            countdown_surf = self.font_medium.render(countdown_text, True, color)
            countdown_rect = countdown_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(countdown_surf, countdown_rect)

        # Medication name
        name_surf = self.font_small.render(self.medication_name, True, self.colors['gray'])
        self.screen.blit(name_surf, (x + 15, y + height - 25))

        # Key hint
        hint_surf = self.font_small.render("[M]", True, self.colors['gray'])
        hint_rect = hint_surf.get_rect(right=x + width - 15, bottom=y + height - 12)
        self.screen.blit(hint_surf, hint_rect)

    def _draw_breathing_status(self, x, y, width, height):
        """Draw breathing exercise status"""
        color = self.colors['blue']

        # Apply pulse effect
        border_width = 2
        border_color = color
        if self.breathing_pulse > 0:
            border_width = int(2 + self.breathing_pulse * 4)
            pulse_brightness = int(155 + 100 * self.breathing_pulse)
            border_color = (pulse_brightness, pulse_brightness, pulse_brightness)

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, item_rect, border_width, border_radius=10)

        # Label
        label_surf = self.font_small.render("🌬️  Breathing Exercise", True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Status
        if self.breathing_active:
            phase_text = self.breathing_phase.upper().replace("_", " ")
            status_surf = self.font_medium.render(phase_text, True, color)
            status_rect = status_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(status_surf, status_rect)

            # Cycle count
            cycles_surf = self.font_small.render(f"{self.breathing_cycle_count} cycles", True, self.colors['gray'])
            self.screen.blit(cycles_surf, (x + 15, y + height - 25))
        else:
            status_surf = self.font_medium.render("READY", True, self.colors['gray'])
            status_rect = status_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(status_surf, status_rect)

        # Key hint
        hint_surf = self.font_small.render("[B]", True, self.colors['gray'])
        hint_rect = hint_surf.get_rect(right=x + width - 15, bottom=y + height - 12)
        self.screen.blit(hint_surf, hint_rect)

    def _draw_stress_status(self, x, y, width, height):
        """Draw stress grounding mode status"""
        color = self.colors['purple']

        # Apply pulse effect
        border_width = 2
        border_color = color
        if self.stress_pulse > 0:
            border_width = int(2 + self.stress_pulse * 4)
            pulse_brightness = int(155 + 100 * self.stress_pulse)
            border_color = (pulse_brightness, pulse_brightness, pulse_brightness)

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, item_rect, border_width, border_radius=10)

        # Label
        label_surf = self.font_small.render("🧘 Stress Grounding", True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Status
        if self.stress_mode_active:
            duration = int(self.stress_session_duration)
            status_text = f"{duration}s"
            status_surf = self.font_medium.render(status_text, True, color)
            status_rect = status_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(status_surf, status_rect)

            # Active indicator
            active_surf = self.font_small.render("ACTIVE", True, color)
            self.screen.blit(active_surf, (x + 15, y + height - 25))
        else:
            status_surf = self.font_medium.render("READY", True, self.colors['gray'])
            status_rect = status_surf.get_rect(right=x + width - 15, centery=y + height // 2)
            self.screen.blit(status_surf, status_rect)

        # Key hint
        hint_surf = self.font_small.render("[S]", True, self.colors['gray'])
        hint_rect = hint_surf.get_rect(right=x + width - 15, bottom=y + height - 12)
        self.screen.blit(hint_surf, hint_rect)

    def _draw_breathing_visualization(self, x, y, width, height):
        """Draw animated breathing circle visualization"""
        # Background panel
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (15, 15, 30), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['blue'], panel_rect, 2, border_radius=10)

        # Title
        title_surf = self.font_medium.render("GUIDED BREATHING", True, self.colors['blue'])
        title_rect = title_surf.get_rect(centerx=x + width//2, top=y + 20)
        self.screen.blit(title_surf, title_rect)

        # Phase instruction
        phase_instructions = {
            "inhale": "Breathe In...",
            "hold_in": "Hold...",
            "exhale": "Breathe Out...",
            "hold_out": "Hold..."
        }
        instruction = phase_instructions.get(self.breathing_phase, "Ready")
        instr_surf = self.font_medium.render(instruction, True, self.colors['white'])
        instr_rect = instr_surf.get_rect(centerx=x + width//2, top=y + 70)
        self.screen.blit(instr_surf, instr_rect)

        # Animated breathing circle
        center_x = x + width // 2
        center_y = y + height // 2 + 20

        # Draw outer guide circle
        pygame.draw.circle(self.screen, self.colors['blue'], (center_x, center_y), 150, 2)

        # Draw animated inner circle with glow
        radius = int(self.breathing_circle_radius)

        # Glow effect
        for i in range(3):
            glow_radius = radius + (3 - i) * 15
            glow_alpha = 30 * (3 - i)
            glow_surf = pygame.Surface((glow_radius * 2 + 20, glow_radius * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.colors['blue'], glow_alpha),
                             (glow_radius + 10, glow_radius + 10), glow_radius)
            self.screen.blit(glow_surf, (center_x - glow_radius - 10, center_y - glow_radius - 10))

        # Main circle
        pygame.draw.circle(self.screen, self.colors['blue'], (center_x, center_y), radius)

        # Timer display
        timer_text = f"{self.breathing_timer:.1f}s"
        timer_surf = self.font_small.render(timer_text, True, self.colors['white'])
        timer_rect = timer_surf.get_rect(centerx=center_x, centery=center_y)
        self.screen.blit(timer_surf, timer_rect)

        # Cycle count at bottom
        cycles_text = f"Completed Cycles: {self.breathing_cycle_count}"
        cycles_surf = self.font_small.render(cycles_text, True, self.colors['blue'])
        cycles_rect = cycles_surf.get_rect(centerx=x + width//2, bottom=y + height - 20)
        self.screen.blit(cycles_surf, cycles_rect)

    def _draw_stress_visualization(self, x, y, width, height):
        """Draw stress grounding wave visualization"""
        # Background panel
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (30, 15, 30), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['purple'], panel_rect, 2, border_radius=10)

        # Title
        title_surf = self.font_medium.render("STRESS GROUNDING", True, self.colors['purple'])
        title_rect = title_surf.get_rect(centerx=x + width//2, top=y + 20)
        self.screen.blit(title_surf, title_rect)

        # Instruction
        instr_surf = self.font_small.render("Focus on the waves... Breathe slowly...", True, self.colors['white'])
        instr_rect = instr_surf.get_rect(centerx=x + width//2, top=y + 70)
        self.screen.blit(instr_surf, instr_rect)

        # Draw calming wave patterns
        center_x = x + width // 2
        center_y = y + height // 2 + 20

        # Multiple wave layers
        for wave_index in range(5):
            wave_radius = 60 + wave_index * 40
            num_points = 60
            points = []

            for i in range(num_points + 1):
                angle = (i / num_points) * 2 * math.pi
                wave_amplitude = 15 * math.sin(self.stress_wave_offset + wave_index * 0.5)
                radius = wave_radius + wave_amplitude * math.sin(angle * 3 + self.stress_wave_offset)

                px = center_x + int(radius * math.cos(angle))
                py = center_y + int(radius * math.sin(angle))
                points.append((px, py))

            # Draw wave with fading alpha
            alpha = int(255 - wave_index * 40)
            wave_color = (*self.colors['purple'], alpha)

            if len(points) > 2:
                wave_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.lines(wave_surf, wave_color, False,
                                [(p[0] - x, p[1] - y) for p in points], 3)
                self.screen.blit(wave_surf, (x, y))

        # Duration display
        duration = int(self.stress_session_duration)
        duration_text = f"Session Time: {duration}s"
        duration_surf = self.font_medium.render(duration_text, True, self.colors['purple'])
        duration_rect = duration_surf.get_rect(centerx=x + width//2, bottom=y + height - 30)
        self.screen.blit(duration_surf, duration_rect)

        # Grounding prompts
        prompts = [
            "Name 5 things you can see",
            "Name 4 things you can touch",
            "Name 3 things you can hear"
        ]
        prompt_index = int(self.stress_timer) % len(prompts)
        prompt_surf = self.font_small.render(prompts[prompt_index], True, self.colors['white'])
        prompt_rect = prompt_surf.get_rect(centerx=x + width//2, bottom=y + height - 60)
        self.screen.blit(prompt_surf, prompt_rect)

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

            # Activity text
            activity_surf = self.font_small.render(activity, True, text_color)

            # Truncate if too long
            if activity_surf.get_width() > width - 40:
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
    demo = ClinicalWellnessEnhanced(standalone=True)
    demo.run(duration=300)  # Run for 5 minutes when standalone
