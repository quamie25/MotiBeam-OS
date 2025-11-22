#!/usr/bin/env python3
"""
MotiBeam Scene Base Class
Foundation for all vertical demo scenes
"""

import pygame
import sys
from datetime import datetime

class MotiBeamScene:
    """Base class for MotiBeam demo scenes"""
    
    def __init__(self, width=1280, height=720, title="MotiBeam Demo", fullscreen=True, standalone=True):
        if standalone:
            pygame.init()
        
        self.width = width
        self.height = height
        self.standalone = standalone
        
        # Create screen only if standalone
        if standalone:
            if fullscreen:
                try:
                    self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                except:
                    print("Fullscreen failed, using windowed mode")
                    self.screen = pygame.display.set_mode((width, height))
            else:
                self.screen = pygame.display.set_mode((width, height))
            
            pygame.display.set_caption(title)
            pygame.mouse.set_visible(False)
        else:
            # Screen will be assigned by parent app
            self.screen = None
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.start_time = pygame.time.get_ticks()
        
        # Common colors
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'cyan': (0, 255, 180),
            'green': (80, 255, 120),
            'blue': (100, 200, 255),
            'orange': (255, 180, 0),
            'red': (255, 80, 80),
            'yellow': (255, 255, 100),
            'purple': (200, 100, 255),
            'gray': (150, 150, 150),
        }
        
        # Common fonts
        self.font_huge = pygame.font.Font(None, 140)
        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def draw_header(self, title, subtitle=""):
        """Draw scene header"""
        # Title
        title_surf = self.font_large.render(title, True, self.colors['cyan'])
        title_rect = title_surf.get_rect(centerx=self.width//2, top=50)
        self.screen.blit(title_surf, title_rect)
        
        # Subtitle
        if subtitle:
            sub_surf = self.font_small.render(subtitle, True, self.colors['white'])
            sub_rect = sub_surf.get_rect(centerx=self.width//2, top=170)
            self.screen.blit(sub_surf, sub_rect)
            
    def draw_footer(self, text="Press ESC to exit"):
        """Draw scene footer"""
        footer_surf = self.font_small.render(text, True, self.colors['gray'])
        footer_rect = footer_surf.get_rect(centerx=self.width//2, bottom=self.height-30)
        self.screen.blit(footer_surf, footer_rect)
        
    def draw_corner_markers(self, color=None):
        """Draw corner markers to verify display bounds"""
        if color is None:
            color = self.colors['cyan']
        marker_size = 30
        pygame.draw.circle(self.screen, color, (marker_size, marker_size), 15)
        pygame.draw.circle(self.screen, color, (self.width - marker_size, marker_size), 15)
        pygame.draw.circle(self.screen, color, (marker_size, self.height - marker_size), 15)
        pygame.draw.circle(self.screen, color, (self.width - marker_size, self.height - marker_size), 15)
        
    def update(self):
        """Override in subclass"""
        pass
        
    def render(self):
        """Override in subclass"""
        self.screen.fill(self.colors['black'])
        
    def run(self, duration=30):
        """Main loop - runs for specified duration (seconds)"""
        print(f"Starting {self.__class__.__name__}...")
        
        while self.running:
            # Auto-exit after duration
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed > duration:
                print(f"{duration} seconds elapsed, exiting...")
                self.running = False
                
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(30)
        
        # Only quit pygame if standalone
        if self.standalone:
            pygame.quit()
        print("Scene complete.")
