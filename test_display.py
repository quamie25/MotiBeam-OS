#!/usr/bin/env python3
"""
MotiBeam Display Test - Verify full-screen 1280x720 projection
Press ESC to exit
"""

import pygame
import sys
import os

# Force display to HDMI (projector)
os.environ['SDL_VIDEODRIVER'] = 'kmsdrm'

# Initialize Pygame
pygame.init()

# Display settings for Goodee projector
WIDTH = 1280
HEIGHT = 720

# Create full-screen display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("MotiBeam Display Test")
pygame.mouse.set_visible(False)  # Hide cursor

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 180)
GREEN = (80, 255, 120)

# Font
font_large = pygame.font.Font(None, 120)
font_medium = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 40)

# Main loop
clock = pygame.time.Clock()
running = True

print("Display test running. Press ESC to exit.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw test pattern
    # Title
    title = font_large.render("MotiBeam OS", True, CYAN)
    title_rect = title.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title, title_rect)

    # Status
    status = font_medium.render("Display Test - Full Screen Active", True, WHITE)
    status_rect = status.get_rect(center=(WIDTH // 2, 300))
    screen.blit(status, status_rect)

    # Resolution info
    res_text = font_small.render(f"Resolution: {WIDTH}x{HEIGHT}", True, GREEN)
    res_rect = res_text.get_rect(center=(WIDTH // 2, 400))
    screen.blit(res_text, res_rect)

    # Instructions
    inst = font_small.render("Press ESC to exit", True, WHITE)
    inst_rect = inst.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    screen.blit(inst, inst_rect)

    # Corner markers (to verify no overscan/box)
    marker_size = 50
    pygame.draw.circle(screen, CYAN, (marker_size, marker_size), 20)  # Top-left
    pygame.draw.circle(screen, CYAN, (WIDTH - marker_size, marker_size), 20)  # Top-right
    pygame.draw.circle(screen, CYAN, (marker_size, HEIGHT - marker_size), 20)  # Bottom-left
    pygame.draw.circle(screen, CYAN, (WIDTH - marker_size, HEIGHT - marker_size), 20)  # Bottom-right

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
pygame.quit()
print("Display test complete.")
