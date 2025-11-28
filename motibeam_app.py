#!/usr/bin/env python3
"""
MotiBeam OS - Master Application v3.0
Professional boot sequence + menu system + 7 vertical demos
"""

import sys
sys.path.insert(0, '/home/motibeam/MotiBeam-OS/scenes')

import pygame

# Import all scenes
from boot_screen import BootScreen
from clinical_wellness_scene import ClinicalWellnessScene
from automotive_demo import AutomotiveDemo
from emergency_demo import EmergencyDemo
from industrial_demo import IndustrialDemo
from security_demo import SecurityDemo
from education_demo import EducationDemo
from home_demo import HomeDashboardScene

class MotiBeamApp:
    """Main MotiBeam OS Application"""
    
    def __init__(self):
        pygame.init()

        # Create a fullscreen window that uses the current desktop resolution
        pygame.display.set_caption("MotiBeam OS")

        # First create fullscreen with (0, 0) so SDL uses the desktop size
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Read back the actual size from pygame
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        print(f"[MotiBeam] Using resolution {self.width}x{self.height}")

        pygame.mouse.set_visible(False)
        
        self.running = True
        
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
        
    def show_boot_screen(self):
        """Display boot sequence"""
        boot = BootScreen(standalone=False)
        boot.screen = self.screen
        boot.run(duration=5)
        
    def show_main_menu(self):
        """Display main menu and return selection"""
        clock = pygame.time.Clock()
        
        # Menu items - 7 vertical demos
        menu_items = [
            {"key": "1", "name": "Clinical & Wellness", "symbol": "[+]", "color": self.colors['green'], "demo": "clinical"},
            {"key": "2", "name": "Education/Learning", "symbol": "[#]", "color": self.colors['purple'], "demo": "education"},
            {"key": "3", "name": "Automotive Safety", "symbol": "[>]", "color": self.colors['yellow'], "demo": "automotive"},
            {"key": "4", "name": "Emergency Systems", "symbol": "[!]", "color": self.colors['red'], "demo": "emergency"},
            {"key": "5", "name": "Enterprise/Industrial", "symbol": "[=]", "color": self.colors['cyan'], "demo": "industrial"},
            {"key": "6", "name": "Security/Government", "symbol": "[*]", "color": self.colors['orange'], "demo": "security"},
            {"key": "7", "name": "Smart Home Dashboard", "symbol": "[◊]", "color": self.colors['blue'], "demo": "home"},
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
                    elif event.key == pygame.K_7:
                        selected = menu_items[6]["demo"]
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
            logo_rect = logo.get_rect(center=(self.width//2, 100))  # Moved up from 120
            self.screen.blit(logo, logo_rect)
            
            # Tagline
            tagline = self.font_small.render("Multi-Vertical Ambient Computing Platform", True, self.colors['white'])
            tagline_rect = tagline.get_rect(center=(self.width//2, 180))  # Moved up from 200
            self.screen.blit(tagline, tagline_rect)
            
            # Menu title
            menu_title = self.font_medium.render("SELECT VERTICAL:", True, self.colors['cyan'])
            menu_title_rect = menu_title.get_rect(centerx=self.width//2, top=230)  # Moved up from 270
            self.screen.blit(menu_title, menu_title_rect)
            
            # Menu items with symbols - TIGHTER SPACING to fit all 7
            y_pos = 295  # Starting position for 7 items
            y_spacing = 52  # Spacing to fit all 7 items
            
            for i, item in enumerate(menu_items):
                is_hovered = (i == hover_index)
                
                # Highlight box for hovered item
                if is_hovered:
                    highlight_rect = pygame.Rect(150, y_pos - 8, self.width - 300, 55)
                    pygame.draw.rect(self.screen, item['color'], highlight_rect, 3, border_radius=10)
                
                # Menu item text with ASCII symbol
                text = f"{item['key']}. {item['symbol']} {item['name']}"
                color = item['color'] if is_hovered else self.colors['white']
                text_surf = self.font_medium.render(text, True, color)
                text_rect = text_surf.get_rect(centerx=self.width//2, top=y_pos)
                self.screen.blit(text_surf, text_rect)
                
                y_pos += y_spacing
            
            # "Run All" option - positioned below all 7 items
            all_y = y_pos + 10
            all_text = "A. [ALL] Run All Demos"
            all_surf = self.font_small.render(all_text, True, self.colors['white'])
            all_rect = all_surf.get_rect(center=(self.width//2, all_y))
            self.screen.blit(all_surf, all_rect)

            # Footer
            footer_text = "Press 1-7 or UP/DOWN + ENTER | A for all | ESC to exit"
            footer_surf = self.font_small.render(footer_text, True, self.colors['gray'])
            footer_rect = footer_surf.get_rect(center=(self.width//2, self.height - 30))
            self.screen.blit(footer_surf, footer_rect)
            
            # Corner markers
            corner_size = 30
            pygame.draw.circle(self.screen, self.colors['cyan'], (corner_size, corner_size), 15)
            pygame.draw.circle(self.screen, self.colors['cyan'], (self.width - corner_size, corner_size), 15)
            pygame.draw.circle(self.screen, self.colors['cyan'], (corner_size, self.height - corner_size), 15)
            pygame.draw.circle(self.screen, self.colors['cyan'], (self.width - corner_size, self.height - corner_size), 15)
            
            pygame.display.flip()
            clock.tick(30)
        
        return selected
    
    def run_demo(self, demo_name):
        """Run selected demo"""
        demo_map = {
            "clinical": ClinicalWellnessScene,
            "education": EducationDemo,
            "automotive": AutomotiveDemo,
            "emergency": EmergencyDemo,
            "industrial": IndustrialDemo,
            "security": SecurityDemo,
            "home": HomeDashboardScene,
        }
        
        if demo_name in demo_map:
            print(f"Launching {demo_name} demo...")
            demo = demo_map[demo_name](standalone=False)
            demo.screen = self.screen
            demo.run(duration=300)  # 5 minutes max
            print(f"{demo_name} demo completed.")
    
    def run_all_demos(self):
        """Run all 7 demos in preferred order"""
        demos = ["clinical", "education", "automotive", "emergency", "industrial", "security", "home"]
        for i, demo_name in enumerate(demos):
            if not self.running:
                break
            print(f"Running demo {i+1}/7: {demo_name}")
            self.run_demo(demo_name)
    
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
            
            # Run selected demo(s)
            if selection == "all":
                print("Running all 7 vertical demos in preferred order...")
                self.run_all_demos()
            elif selection:
                self.run_demo(selection)
            else:
                continue
        
        # Cleanup
        pygame.quit()
        print("MotiBeam OS shutdown complete.")

if __name__ == "__main__":
    print("=" * 60)
    print("Starting MotiBeam OS v3.0")
    print("Multi-Vertical Ambient Computing Platform")
    print("=" * 60)
    app = MotiBeamApp()
    app.run()
