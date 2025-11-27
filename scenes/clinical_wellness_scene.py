#!/usr/bin/env python3
"""
VERTICAL 1: Clinical & Wellness - Interactive Patient Dashboard
Complete clinical monitoring with medication reminders, breathing exercises, and veteran grounding support
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

from scene_base import MotiBeamScene
import pygame
import math
from datetime import datetime, timedelta

class ClinicalWellnessScene(MotiBeamScene):
    """Interactive Clinical & Wellness Dashboard with medication, breathing, and grounding modes"""

    def __init__(self, standalone=True):
        super().__init__(title="MotiBeam - Clinical & Wellness", standalone=standalone)

        # Medication state
        self.med_mode_active = False
        self.med_next_minutes = 10  # demo countdown in minutes
        self.med_countdown = self.med_next_minutes * 60  # convert to seconds
        self.med_next_time = None
        self.med_alert_pulse = 0

        # Breathing state
        self.breathing_active = False
        self.breath_phase = "INHALE"  # INHALE, HOLD, EXHALE
        self.breath_timer = 0.0
        self.breath_cycle_count = 0
        self.breath_circle_radius = 80
        self.breath_target_radius = 80

        # Grounding state
        self.grounding_active = False
        self.grounding_index = 0
        self.grounding_timer = 0.0
        self.grounding_prompts = [
            "You are safe here.",
            "Name 3 things you can see.",
            "Name 3 things you can hear.",
            "Take one slow, deep breath."
        ]
        self.grounding_prompt_duration = 5.0  # seconds per prompt

        # Sleep prep state
        self.sleep_prep_active = False

        # Stress level tracking
        self.stress_level = "CALM"  # CALM, ELEVATED, GROUNDING ACTIVE

        # HIPAA privacy shield
        self.privacy_shield_active = False

        # Animation state
        self.fade_alpha = 0  # For fade-in effect (0 to 255)
        self.fade_in_complete = False
        self.fade_out = False
        self.animation_time = 0

        # Pulse animations
        self.med_pulse = 0
        self.breathing_pulse = 0
        self.grounding_pulse = 0

        # Activity feed
        self.recent_activities = [
            self._format_activity("Clinical dashboard initialized"),
            self._format_activity("System ready"),
        ]
        self.max_activities = 8

        # Calculate initial medication next time
        self._update_med_next_time()

    def _format_activity(self, message):
        """Format an activity with current timestamp"""
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        return f"{timestamp} - {message}"

    def _add_activity(self, message):
        """Add a new activity to the recent feed"""
        self.recent_activities.insert(0, self._format_activity(message))
        if len(self.recent_activities) > self.max_activities:
            self.recent_activities = self.recent_activities[:self.max_activities]

    def _update_med_next_time(self):
        """Calculate the next medication time based on countdown"""
        if self.med_countdown > 0:
            future_time = datetime.now() + timedelta(seconds=self.med_countdown)
            self.med_next_time = future_time.strftime("%I:%M %p")
        else:
            self.med_next_time = "DOSE DUE NOW"

    def handle_events(self, event):
        """Handle individual pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Start fade-out animation
                self.fade_out = True
                self._add_activity("Dashboard closing...")
            elif event.key == pygame.K_m:
                # Toggle Medication Mode
                if not self.med_mode_active:
                    self.med_mode_active = True
                    self.med_countdown = self.med_next_minutes * 60
                    self._update_med_next_time()
                    self._add_activity("Medication reminder started (10 min demo)")
                else:
                    self.med_mode_active = False
                    self._add_activity("Medication reminder stopped")
                self.med_pulse = 1.0
            elif event.key == pygame.K_b:
                # Toggle Breathing Session
                if not self.breathing_active:
                    self.breathing_active = True
                    self.breath_phase = "INHALE"
                    self.breath_timer = 0.0
                    self.breath_cycle_count = 0
                    self._add_activity("Breathing session started")
                else:
                    self.breathing_active = False
                    self.breath_phase = "INHALE"
                    self._add_activity(f"Breathing session ended ({self.breath_cycle_count} cycles)")
                self.breathing_pulse = 1.0
            elif event.key == pygame.K_s:
                # Toggle Grounding Mode
                if not self.grounding_active:
                    self.grounding_active = True
                    self.grounding_timer = 0.0
                    self.grounding_index = 0
                    self.stress_level = "GROUNDING ACTIVE"
                    self._add_activity("Grounding mode activated")
                else:
                    self.grounding_active = False
                    self.stress_level = "CALM"
                    self._add_activity("Grounding mode ended")
                self.grounding_pulse = 1.0
            elif event.key == pygame.K_h:
                # Toggle HIPAA Privacy Shield
                self.privacy_shield_active = not self.privacy_shield_active
                if self.privacy_shield_active:
                    self._add_activity("Privacy shield enabled")
                else:
                    self._add_activity("Privacy shield disabled")

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
        self.grounding_pulse = max(0, self.grounding_pulse - dt * 2.5)

        # Update medication countdown
        if self.med_mode_active:
            self.med_countdown -= dt
            if self.med_countdown <= 0:
                # Medication time reached
                self.med_countdown = 0
                self._add_activity("⚠ Dose time reached - please take medication")
                self.med_alert_pulse = 1.0
                # Reset countdown for continuous demo
                self.med_countdown = self.med_next_minutes * 60
            self._update_med_next_time()

        # Decay medication alert pulse
        self.med_alert_pulse = max(0, self.med_alert_pulse - dt * 3)

        # Update breathing exercise
        if self.breathing_active:
            self.breath_timer += dt

            if self.breath_phase == "INHALE":
                # Inhale for 4 seconds
                self.breath_target_radius = 150
                if self.breath_timer >= 4.0:
                    self.breath_phase = "HOLD"
                    self.breath_timer = 0.0
            elif self.breath_phase == "HOLD":
                # Hold for 4 seconds
                self.breath_target_radius = 150
                if self.breath_timer >= 4.0:
                    self.breath_phase = "EXHALE"
                    self.breath_timer = 0.0
            elif self.breath_phase == "EXHALE":
                # Exhale for 4 seconds
                self.breath_target_radius = 80
                if self.breath_timer >= 4.0:
                    self.breath_phase = "INHALE"
                    self.breath_timer = 0.0
                    self.breath_cycle_count += 1

            # Smooth interpolation towards target radius
            radius_diff = self.breath_target_radius - self.breath_circle_radius
            self.breath_circle_radius += radius_diff * dt * 3.0

        # Update grounding mode
        if self.grounding_active:
            self.grounding_timer += dt
            # Cycle through prompts
            if self.grounding_timer >= self.grounding_prompt_duration:
                self.grounding_timer = 0.0
                self.grounding_index = (self.grounding_index + 1) % len(self.grounding_prompts)

    def draw(self):
        """Render the scene"""
        self.screen.fill(self.colors['black'])

        # Header
        title_surf = self.font_large.render("CLINICAL & WELLNESS", True, self.colors['green'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=20)
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_small.render("Medication • Breathing • Grounding", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=self.width//2, top=110)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Current time display
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%A, %B %d")

        time_surf = self.font_medium.render(current_time, True, self.colors['cyan'])
        time_rect = time_surf.get_rect(centerx=self.width//2, top=150)
        self.screen.blit(time_surf, time_rect)

        date_surf = self.font_small.render(current_date, True, self.colors['gray'])
        date_rect = date_surf.get_rect(centerx=self.width//2, top=205)
        self.screen.blit(date_surf, date_rect)

        # Left panel: Health Status
        status_x = 50
        status_y = 260
        status_width = 480

        self._draw_health_status_panel(status_x, status_y, status_width)

        # Center panel: Active Mode Visualization
        center_x = 570
        center_y = 260
        center_width = 280
        center_height = 400

        self._draw_center_visualization(center_x, center_y, center_width, center_height)

        # Right panel: Clinical Activity
        activity_x = 890
        activity_y = 260
        activity_width = 340

        self._draw_activity_panel(activity_x, activity_y, activity_width)

        # Footer with controls
        footer_text = "M=Medication | B=Breathing | S=Grounding | H=Privacy | ESC=Exit"
        footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height-15)
        self.screen.blit(footer_surf, footer_rect)

        # Corner markers
        self.draw_corner_markers(self.colors['green'])

        # HIPAA Privacy Shield overlay
        if self.privacy_shield_active:
            self._draw_privacy_shield()

        # Apply fade effect
        if self.fade_alpha < 255:
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.set_alpha(255 - int(self.fade_alpha))
            fade_surface.fill(self.colors['black'])
            self.screen.blit(fade_surface, (0, 0))

    def _draw_health_status_panel(self, x, y, width):
        """Draw the left panel with health status items"""
        # Section header
        header_surf = self.font_medium.render("HEALTH STATUS", True, self.colors['green'])
        self.screen.blit(header_surf, (x + 10, y))

        # Underline
        line_y = y + 50
        pygame.draw.line(self.screen, self.colors['green'], (x, line_y), (x + width, line_y), 2)

        # Status items
        item_y = y + 70
        item_height = 70

        # 1. Next Medication
        med_time_display = self.med_next_time if self.med_mode_active else "None scheduled"
        self._draw_status_item(
            x, item_y, width, item_height,
            "🕒 Next Medication",
            med_time_display,
            self.colors['yellow'] if self.med_mode_active else self.colors['gray'],
            self.med_pulse
        )

        # 2. Medication Mode
        item_y += item_height + 5
        if self.med_mode_active:
            med_status = "REMINDER ACTIVE"
            med_color = self.colors['yellow']
        else:
            med_status = "IDLE"
            med_color = self.colors['gray']

        self._draw_status_item(
            x, item_y, width, item_height,
            "💊 Medication Mode",
            med_status,
            med_color,
            self.med_pulse
        )

        # 3. Sleep Prep
        item_y += item_height + 5
        sleep_status = "RUNNING" if self.sleep_prep_active else "OFF"
        sleep_color = self.colors['blue'] if self.sleep_prep_active else self.colors['gray']

        self._draw_status_item(
            x, item_y, width, item_height,
            "🌙 Sleep Prep",
            sleep_status,
            sleep_color,
            0
        )

        # 4. Stress Level
        item_y += item_height + 5
        if self.stress_level == "GROUNDING ACTIVE":
            stress_color = self.colors['purple']
        elif self.stress_level == "ELEVATED":
            stress_color = self.colors['orange']
        else:
            stress_color = self.colors['green']

        self._draw_status_item(
            x, item_y, width, item_height,
            "🧠 Stress Level",
            self.stress_level,
            stress_color,
            self.grounding_pulse
        )

    def _draw_status_item(self, x, y, width, height, label, value, color, pulse):
        """Draw an individual status item"""
        # Border with pulse effect
        border_width = 2
        border_color = color

        if pulse > 0:
            border_width = int(2 + pulse * 4)
            pulse_brightness = int(155 + 100 * pulse)
            border_color = (pulse_brightness, pulse_brightness, pulse_brightness)

        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (20, 20, 20), item_rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, item_rect, border_width, border_radius=8)

        # Label
        label_surf = self.font_small.render(label, True, self.colors['white'])
        self.screen.blit(label_surf, (x + 15, y + 12))

        # Value
        value_surf = self.font_medium.render(value, True, color)
        value_rect = value_surf.get_rect(right=x + width - 15, centery=y + height // 2)
        self.screen.blit(value_surf, value_rect)

    def _draw_center_visualization(self, x, y, width, height):
        """Draw the center panel with active mode visualization"""
        # Background panel
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (15, 15, 20), panel_rect, border_radius=10)

        # Determine which visualization to show
        if self.med_mode_active and self.med_countdown <= 60:
            # Medication alert (when less than 1 minute remaining)
            self._draw_medication_alert(x, y, width, height)
        elif self.breathing_active:
            # Breathing visualization
            self._draw_breathing_circle(x, y, width, height)
        elif self.grounding_active:
            # Grounding prompts
            self._draw_grounding_prompts(x, y, width, height)
        else:
            # Default idle state
            self._draw_idle_state(x, y, width, height)

        # Border
        border_color = self.colors['green']
        if self.breathing_active:
            border_color = self.colors['blue']
        elif self.grounding_active:
            border_color = self.colors['purple']
        elif self.med_mode_active:
            border_color = self.colors['yellow']

        pygame.draw.rect(self.screen, border_color, panel_rect, 2, border_radius=10)

    def _draw_medication_alert(self, x, y, width, height):
        """Draw medication countdown alert"""
        # Title
        title_surf = self.font_medium.render("MEDICATION ALERT", True, self.colors['yellow'])
        title_rect = title_surf.get_rect(centerx=x + width//2, top=y + 30)
        self.screen.blit(title_surf, title_rect)

        # Countdown display
        minutes = int(self.med_countdown // 60)
        seconds = int(self.med_countdown % 60)
        countdown_text = f"{minutes:02d}:{seconds:02d}"

        countdown_surf = self.font_huge.render(countdown_text, True, self.colors['yellow'])
        countdown_rect = countdown_surf.get_rect(centerx=x + width//2, centery=y + height//2 - 20)
        self.screen.blit(countdown_surf, countdown_rect)

        # Next dose text
        next_text = f"Next dose: {self.med_next_time}"
        next_surf = self.font_small.render(next_text, True, self.colors['white'])
        next_rect = next_surf.get_rect(centerx=x + width//2, top=countdown_rect.bottom + 30)
        self.screen.blit(next_surf, next_rect)

        # Progress bar
        bar_width = width - 40
        bar_height = 20
        bar_x = x + 20
        bar_y = y + height - 60

        # Background bar
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (40, 40, 40), bar_rect, border_radius=10)

        # Progress fill
        progress = (self.med_next_minutes * 60 - self.med_countdown) / (self.med_next_minutes * 60)
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            pygame.draw.rect(self.screen, self.colors['yellow'], fill_rect, border_radius=10)

        # Border
        pygame.draw.rect(self.screen, self.colors['yellow'], bar_rect, 2, border_radius=10)

    def _draw_breathing_circle(self, x, y, width, height):
        """Draw animated breathing circle"""
        # Title
        title_surf = self.font_medium.render("GUIDED BREATHING", True, self.colors['blue'])
        title_rect = title_surf.get_rect(centerx=x + width//2, top=y + 20)
        self.screen.blit(title_surf, title_rect)

        # Phase instruction
        phase_text = self.breath_phase
        instr_surf = self.font_large.render(phase_text, True, self.colors['blue'])
        instr_rect = instr_surf.get_rect(centerx=x + width//2, top=y + 60)
        self.screen.blit(instr_surf, instr_rect)

        # Animated breathing circle
        center_x = x + width // 2
        center_y = y + height // 2 + 20

        # Draw outer guide circle
        pygame.draw.circle(self.screen, self.colors['blue'], (center_x, center_y), 120, 2)

        # Draw animated inner circle with glow
        radius = int(self.breath_circle_radius)

        # Glow effect
        for i in range(3):
            glow_radius = radius + (3 - i) * 12
            glow_alpha = 25 * (3 - i)
            glow_surf = pygame.Surface((glow_radius * 2 + 20, glow_radius * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.colors['blue'], glow_alpha),
                             (glow_radius + 10, glow_radius + 10), glow_radius)
            self.screen.blit(glow_surf, (center_x - glow_radius - 10, center_y - glow_radius - 10))

        # Main circle
        pygame.draw.circle(self.screen, self.colors['blue'], (center_x, center_y), radius)

        # Timer display
        timer_text = f"{self.breath_timer:.1f}s"
        timer_surf = self.font_small.render(timer_text, True, self.colors['white'])
        timer_rect = timer_surf.get_rect(centerx=center_x, centery=center_y)
        self.screen.blit(timer_surf, timer_rect)

        # Cycle count at bottom
        cycles_text = f"Cycles: {self.breath_cycle_count}"
        cycles_surf = self.font_small.render(cycles_text, True, self.colors['blue'])
        cycles_rect = cycles_surf.get_rect(centerx=x + width//2, bottom=y + height - 20)
        self.screen.blit(cycles_surf, cycles_rect)

    def _draw_grounding_prompts(self, x, y, width, height):
        """Draw grounding mode with calming prompts"""
        # Title
        title_surf = self.font_medium.render("GROUNDING MODE", True, self.colors['purple'])
        title_rect = title_surf.get_rect(centerx=x + width//2, top=y + 20)
        self.screen.blit(title_surf, title_rect)

        # Subtitle
        subtitle_surf = self.font_small.render("Veteran Support", True, self.colors['white'])
        subtitle_rect = subtitle_surf.get_rect(centerx=x + width//2, top=y + 60)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Pulsing ring visualization
        center_x = x + width // 2
        center_y = y + height // 2 - 20

        # Draw pulsing rings
        pulse = abs(math.sin(self.animation_time * 1.5))
        for i in range(4):
            ring_radius = 50 + i * 25 + int(pulse * 10)
            ring_alpha = int(180 - i * 35)
            ring_surf = pygame.Surface((ring_radius * 2 + 10, ring_radius * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(ring_surf, (*self.colors['purple'], ring_alpha),
                             (ring_radius + 5, ring_radius + 5), ring_radius, 3)
            self.screen.blit(ring_surf, (center_x - ring_radius - 5, center_y - ring_radius - 5))

        # Current prompt (word-wrapped if needed)
        current_prompt = self.grounding_prompts[self.grounding_index]

        # Word wrap the prompt to fit width
        words = current_prompt.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.font_medium.render(test_line, True, self.colors['white'])
            if test_surf.get_width() <= width - 40:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Draw wrapped lines
        prompt_y = y + height - 100
        for line in lines:
            line_surf = self.font_medium.render(line, True, self.colors['white'])
            line_rect = line_surf.get_rect(centerx=x + width//2, centery=prompt_y)
            self.screen.blit(line_surf, line_rect)
            prompt_y += 40

    def _draw_idle_state(self, x, y, width, height):
        """Draw idle state when no mode is active"""
        # Title
        title_surf = self.font_medium.render("READY", True, self.colors['gray'])
        title_rect = title_surf.get_rect(centerx=x + width//2, centery=y + height//2 - 40)
        self.screen.blit(title_surf, title_rect)

        # Instructions
        instr_lines = [
            "Press M for Medication",
            "Press B for Breathing",
            "Press S for Grounding"
        ]

        instr_y = y + height//2 + 20
        for line in instr_lines:
            line_surf = self.font_small.render(line, True, self.colors['white'])
            line_rect = line_surf.get_rect(centerx=x + width//2, top=instr_y)
            self.screen.blit(line_surf, line_rect)
            instr_y += 35

    def _draw_activity_panel(self, x, y, width):
        """Draw the clinical activity feed"""
        # Header
        header_surf = self.font_medium.render("CLINICAL ACTIVITY", True, self.colors['cyan'])
        self.screen.blit(header_surf, (x + 10, y))

        # Underline
        line_y = y + 50
        pygame.draw.line(self.screen, self.colors['cyan'], (x, line_y), (x + width, line_y), 2)

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
            if activity_surf.get_width() > width - 20:
                # Truncate text
                truncated = activity[:40] + "..."
                activity_surf = self.font_small.render(truncated, True, text_color)

            self.screen.blit(activity_surf, (x + 10, activity_y))

            # Separator line
            if i < len(self.recent_activities) - 1 and i < 7:
                sep_y = activity_y + 35
                sep_color = tuple(int(c * age_factor * 0.3) for c in self.colors['white'])
                pygame.draw.line(self.screen, sep_color, (x + 5, sep_y), (x + width - 5, sep_y), 1)

            activity_y += activity_height

    def _draw_privacy_shield(self):
        """Draw HIPAA privacy shield overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Darken sensitive areas (medication times, specific values)
        # Draw translucent black rectangles over sensitive data areas

        # Health status panel area
        status_overlay = pygame.Rect(50, 330, 480, 280)
        pygame.draw.rect(overlay, (0, 0, 0, 180), status_overlay, border_radius=8)

        # Activity feed specific entries
        activity_overlay = pygame.Rect(890, 330, 340, 330)
        pygame.draw.rect(overlay, (0, 0, 0, 180), activity_overlay, border_radius=8)

        self.screen.blit(overlay, (0, 0))

        # Privacy shield indicator
        shield_text = "🔒 PRIVACY SHIELD ACTIVE"
        shield_surf = self.font_medium.render(shield_text, True, self.colors['yellow'])
        shield_rect = shield_surf.get_rect(centerx=self.width//2, top=self.height - 50)

        # Background for shield text
        bg_rect = pygame.Rect(shield_rect.x - 10, shield_rect.y - 5,
                             shield_rect.width + 20, shield_rect.height + 10)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.colors['yellow'], bg_rect, 2, border_radius=5)

        self.screen.blit(shield_surf, shield_rect)

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
    demo = ClinicalWellnessScene(standalone=True)
    demo.run(duration=300)  # Run for 5 minutes when standalone
