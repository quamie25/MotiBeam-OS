#!/usr/bin/env python3
"""
MotiBeam Display Test - Simplified for Pi OS Lite
Press ESC or wait 10 seconds to exit
"""

import pygame
import sys
import os

# Don't force specific video driver - let SDL auto-detect
# Remove the kmsdrm requirement

# Initialize Pygame
pygame.init()

# Display settings for Goodee projector
WIDTH = 1280
HEIGHT = 720

# Try to create display without forcing fullscreen mode first
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MotiBeam Display Test")
except Exception as e:
    print(f"Failed to create display: {e}")
    print("Trying alternate method...")
    # Fallback to smaller resolution
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
start_time = pygame.time.get_ticks()

print(f"Display test running at {WIDTH}x{HEIGHT}")
print("Press ESC to exit, or wait 10 seconds...")

while running:
    # Auto-exit after 10 seconds
    if pygame.time.get_ticks() - start_time > 10000:
        print("10 seconds elapsed, exiting...")
        running = False

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
    title = font_large.render("MotiBeam", True, CYAN)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    # Status
    status = font_medium.render("Display Test Active", True, WHITE)
    status_rect = status.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(status, status_rect)

    # Resolution info
    res_text = font_small.render(f"{WIDTH}x{HEIGHT}", True, GREEN)
    res_rect = res_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(res_text, res_rect)

    # Corner markers
    marker_size = 30
    pygame.draw.circle(screen, CYAN, (marker_size, marker_size), 15)
    pygame.draw.circle(screen, CYAN, (WIDTH - marker_size, marker_size), 15)
    pygame.draw.circle(screen, CYAN, (marker_size, HEIGHT - marker_size), 15)
    pygame.draw.circle(screen, CYAN, (WIDTH - marker_size, HEIGHT - marker_size), 15)

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
pygame.quit()
print("Display test complete.")
