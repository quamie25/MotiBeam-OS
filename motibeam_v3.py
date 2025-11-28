#!/usr/bin/env python3
"""
MotiBeam OS v3.0 - Complete Application
Integrates: Boot Screen, Menu, Demos, Settings Panel, Ambient Scenes, Auto HUD
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, '/home/user/MotiBeam-OS')
sys.path.insert(0, '/home/user/MotiBeam-OS/scenes')
sys.path.insert(0, '/home/user/MotiBeam-OS/core')

import pygame

# Import existing demo scenes
from boot_screen import BootScreen
from clinical_demo_enhanced import ClinicalWellnessEnhanced
from automotive_demo import AutomotiveDemo
from emergency_demo import EmergencyDemo
from industrial_demo import IndustrialDemo
from security_demo import SecurityDemo
from education_demo import EducationDemo

# Import new v3.0 modules
import settings_panel
import scene_manager
import vertical_auto


class MotiBeamV3:
    """MotiBeam OS v3.0 - Full Application"""

    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("MotiBeam OS v3.0")
        pygame.mouse.set_visible(True)  # Show mouse for settings interaction

        self.running = True
        self.clock = pygame.time.Clock()

        # UI State
        self.current_mode = "boot"  # boot, menu, demo, settings, ambient, auto_hud
        self.settings_open = False
        self.ambient_mode = False
        self.auto_hud_mode = False

        # Colors
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'cyan': (0, 255, 180),
            'green': (80, 255, 120),
            'yellow': (255, 255, 100),
            'red': (255, 80, 80),
            'orange': (255, 180, 0),
            'blue': (100, 200, 255),
            'purple': (200, 100, 255),
            'gray': (150, 150, 150),
        }

        # Fonts
        self.font_huge = pygame.font.Font(None, 140)
        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)

        # Initialize v3.0 components
        self._init_v3_components()

    def _init_v3_components(self):
        """Initialize settings panel and scene manager"""
        # Initialize settings panel
        settings_panel.init_settings_panel(self.screen, self.font_medium, self.font_small)

        # Initialize scene manager
        scene_manager.init_scene_manager(self.screen)

        # Connect settings panel to scene manager
        settings_panel.set_scene_manager(scene_manager)

        # Load settings and set initial scene
        settings = settings_panel.get_current_settings()
        active_scene = settings.get("Scenes", {}).get("active_scene", "Fireplace")
        scene_manager.set_active_scene(active_scene)

        # Initialize auto HUD
        vertical_auto.init_auto_vertical(self.screen)

    def show_boot_screen(self):
        """Display boot sequence"""
        boot = BootScreen(standalone=False)
        boot.screen = self.screen
        boot.run(duration=5)

    def show_main_menu(self):
        """Display main menu and return selection"""
        # Menu items
        menu_items = [
            {"key": "1", "name": "Clinical & Wellness", "symbol": "[+]", "color": self.colors['green'],
             "demo": "clinical"},
            {"key": "2", "name": "Education/Learning", "symbol": "[#]", "color": self.colors['purple'],
             "demo": "education"},
            {"key": "3", "name": "Automotive Safety", "symbol": "[>]", "color": self.colors['yellow'],
             "demo": "automotive"},
            {"key": "4", "name": "Emergency Systems", "symbol": "[!]", "color": self.colors['red'],
             "demo": "emergency"},
            {"key": "5", "name": "Enterprise/Industrial", "symbol": "[=]", "color": self.colors['cyan'],
             "demo": "industrial"},
            {"key": "6", "name": "Security/Government", "symbol": "[*]", "color": self.colors['orange'],
             "demo": "security"},
        ]

        selected = None
        menu_running = True
        hover_index = 0

        while menu_running and self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        menu_running = False
                    elif event.key == pygame.K_s:
                        # Open settings
                        selected = "settings"
                        menu_running = False
                    elif event.key == pygame.K_b:
                        # Ambient background scenes
                        selected = "ambient"
                        menu_running = False
                    elif event.key == pygame.K_1:
                        selected = menu_items[0]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_2:
                        selected = menu_items[1]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_3:
                        selected = menu_items[2]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_4:
                        selected = menu_items[3]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_5:
                        selected = menu_items[4]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_6:
                        selected = menu_items[5]["demo"]
                        menu_running = False
                    elif event.key == pygame.K_a:
                        selected = "all"
                        menu_running = False
                    elif event.key == pygame.K_UP:
                        hover_index = (hover_index - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        hover_index = (hover_index + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        selected = menu_items[hover_index]["demo"]
                        menu_running = False

            # Render menu
            self.screen.fill(self.colors['black'])

            # Animated background elements
            import math
            t = pygame.time.get_ticks() / 2000.0
            for i in range(4):
                x = 200 + i * 300
                y = 360 + int(30 * math.sin(t + i * 0.5))
                radius = 150
                pygame.draw.circle(self.screen, (*self.colors['cyan'][:3], 20), (x, y), radius, 2)

            # Logo with glow effect
            glow_pulse = 0.8 + 0.2 * abs(math.sin(t * 2))
            glow_color = tuple(int(c * glow_pulse) for c in self.colors['cyan'])

            logo = self.font_huge.render("MotiBeam OS", True, glow_color)
            logo_rect = logo.get_rect(center=(self.width // 2, 80))
            self.screen.blit(logo, logo_rect)

            # Version
            version = self.font_small.render("v3.0", True, self.colors['gray'])
            version_rect = version.get_rect(center=(self.width // 2 + 200, 100))
            self.screen.blit(version, version_rect)

            # Tagline
            tagline = self.font_small.render("Multi-Vertical Ambient Computing Platform", True, self.colors['white'])
            tagline_rect = tagline.get_rect(center=(self.width // 2, 160))
            self.screen.blit(tagline, tagline_rect)

            # Menu title
            menu_title = self.font_medium.render("SELECT VERTICAL:", True, self.colors['cyan'])
            menu_title_rect = menu_title.get_rect(centerx=self.width // 2, top=210)
            self.screen.blit(menu_title, menu_title_rect)

            # Menu items
            y_pos = 290
            y_spacing = 60

            for i, item in enumerate(menu_items):
                is_hovered = (i == hover_index)

                # Highlight box for hovered item
                if is_hovered:
                    highlight_rect = pygame.Rect(150, y_pos - 8, self.width - 300, 55)
                    pygame.draw.rect(self.screen, item['color'], highlight_rect, 3, border_radius=10)

                # Menu item text with symbol
                text = f"{item['key']}. {item['symbol']} {item['name']}"
                color = item['color'] if is_hovered else self.colors['white']
                text_surf = self.font_medium.render(text, True, color)
                text_rect = text_surf.get_rect(centerx=self.width // 2, top=y_pos)
                self.screen.blit(text_surf, text_rect)

                y_pos += y_spacing

            # Additional options
            all_y = y_pos + 10
            options_text = [
                "A. [ALL] Run All Demos",
                "S. [SET] Settings Panel",
                "B. [BG] Ambient Scenes"
            ]

            for i, opt in enumerate(options_text):
                opt_surf = self.font_small.render(opt, True, self.colors['white'])
                opt_rect = opt_surf.get_rect(center=(self.width // 2, all_y + i * 35))
                self.screen.blit(opt_surf, opt_rect)

            # Footer
            footer_text = "Press 1-6, A, S, B | UP/DOWN + ENTER | ESC to exit"
            footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
            footer_rect = footer_surf.get_rect(center=(self.width // 2, self.height - 30))
            self.screen.blit(footer_surf, footer_rect)

            pygame.display.flip()
            self.clock.tick(30)

        return selected

    def run_demo(self, demo_name):
        """Run selected vertical demo"""
        demo_map = {
            "clinical": ClinicalWellnessEnhanced,
            "education": EducationDemo,
            "automotive": AutomotiveDemo,
            "emergency": EmergencyDemo,
            "industrial": IndustrialDemo,
            "security": SecurityDemo,
        }

        if demo_name in demo_map:
            print(f"Launching {demo_name} demo...")
            demo = demo_map[demo_name](standalone=False)
            demo.screen = self.screen
            demo.run(duration=300)  # 5 minutes max
            print(f"{demo_name} demo completed.")

    def run_all_demos(self):
        """Run all 6 vertical demos in order"""
        demos = ["clinical", "education", "automotive", "emergency", "industrial", "security"]
        for i, demo_name in enumerate(demos):
            if not self.running:
                break
            print(f"Running demo {i + 1}/6: {demo_name}")
            self.run_demo(demo_name)

    def run_settings_mode(self):
        """Run settings panel mode"""
        print("Opening settings panel...")
        settings_running = True

        while settings_running and self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    settings_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                        settings_running = False
                    elif event.key == pygame.K_F11:
                        # Save settings manually
                        settings = settings_panel.get_current_settings()
                        settings_panel.save_settings(settings)
                        print("Settings saved.")

                # Pass event to settings panel
                settings_panel.handle_settings_events(event)

            # Render settings panel
            settings_panel.render_settings_panel(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

        print("Settings panel closed.")

    def run_ambient_mode(self):
        """Run ambient background scenes mode"""
        print("Entering ambient scenes mode...")
        ambient_running = True
        last_time = pygame.time.get_ticks()

        # Get current settings
        settings = settings_panel.get_current_settings()
        demo_mode = settings.get("Demo", {}).get("enabled", False)
        demo_profile = settings.get("Demo", {}).get("demo_profile", "Smart Home")

        # If demo mode + Auto profile, switch to Auto HUD instead
        if demo_mode and demo_profile == "Auto":
            self.run_auto_hud_mode()
            return

        while ambient_running and self.running:
            current_time = pygame.time.get_ticks()
            dt = current_time - last_time
            last_time = current_time

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    ambient_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                        ambient_running = False
                    elif event.key == pygame.K_s:
                        # Open settings from ambient mode
                        self.run_settings_mode()
                    # Scene shortcuts
                    elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Fireplace")
                    elif event.key == pygame.K_2 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Aurora")
                    elif event.key == pygame.K_3 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Snowfall")
                    elif event.key == pygame.K_4 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Christmas Tree Glow")
                    elif event.key == pygame.K_5 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Candy Cane Wave")
                    elif event.key == pygame.K_6 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        scene_manager.set_active_scene("Fireplace + Snow Window")

            # Update and render active scene
            scene_manager.update_active_scene(dt)
            scene_manager.render_active_scene(self.screen)

            # Draw scene name overlay
            scene_name = scene_manager.get_active_scene_name()
            if scene_name:
                overlay_text = self.font_small.render(f"Scene: {scene_name}", True, (200, 200, 200))
                self.screen.blit(overlay_text, (20, 20))

            # Help text
            help_text = self.font_small.render("ESC/B: Exit | S: Settings | Ctrl+1-6: Scene shortcuts",
                                               True, (150, 150, 150))
            self.screen.blit(help_text, (20, self.height - 50))

            pygame.display.flip()
            self.clock.tick(30)

        print("Ambient mode exited.")

    def run_auto_hud_mode(self):
        """Run Auto HUD demo mode"""
        print("Entering Auto HUD mode...")
        auto_running = True
        last_time = pygame.time.get_ticks()

        # Re-initialize auto HUD
        vertical_auto.init_auto_vertical(self.screen)

        while auto_running and self.running:
            current_time = pygame.time.get_ticks()
            dt = current_time - last_time
            last_time = current_time

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    auto_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        auto_running = False

            # Update and render Auto HUD
            vertical_auto.update_auto_vertical(dt)
            vertical_auto.render_auto_vertical(self.screen)

            # Help text
            help_text = self.font_small.render("ESC: Exit Auto HUD Demo", True, (150, 150, 150))
            self.screen.blit(help_text, (20, self.height - 50))

            pygame.display.flip()
            self.clock.tick(30)

        print("Auto HUD mode exited.")

    def run(self):
        """Main application loop"""
        # Show boot screen
        self.show_boot_screen()

        # Main loop
        while self.running:
            # Show menu and get selection
            selection = self.show_main_menu()

            if not self.running:
                break

            # Handle selection
            if selection == "all":
                print("Running all 6 vertical demos...")
                self.run_all_demos()
            elif selection == "settings":
                self.run_settings_mode()
            elif selection == "ambient":
                self.run_ambient_mode()
            elif selection:
                self.run_demo(selection)
            else:
                continue

        # Cleanup
        pygame.quit()
        print("MotiBeam OS v3.0 shutdown complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("Starting MotiBeam OS v3.0")
    print("Multi-Vertical Ambient Computing Platform")
    print("New Features: Settings Panel | Ambient Scenes | Auto HUD")
    print("=" * 60)
    app = MotiBeamV3()
    app.run()
