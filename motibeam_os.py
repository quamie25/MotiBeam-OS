#!/usr/bin/env python3
"""
MOTIBEAM OS - Unified Demo Engine
Hostname: motibeamOS | User: motibeam
Six Vertical Ambient Computing Platform
"""

import pygame
import cv2
import numpy as np
import time
import os
from pygame.locals import *

# Initialize Pygame for projection
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Remove FULLSCREEN for testing
pygame.display.set_caption("MotiBeam OS - Ambient Computing")
pygame.mouse.set_visible(False)

# Try to initialize camera (may not work on Mac, but will on Pi)
try:
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    CAMERA_AVAILABLE = True
    print("✅ Camera initialized")
except:
    CAMERA_AVAILABLE = False
    print("⚠️  Camera not available (will work on Pi)")

# Font setup
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Demo States - All Six Verticals
DEMOS = [
    "CLINICAL & WELLNESS",
    "AUTOMOTIVE SAFETY", 
    "MARITIME/AVIATION",
    "ENTERPRISE & INDUSTRIAL", 
    "SECURITY & GOVERNMENT",
    "EDUCATION & LEARNING"
]
current_demo_index = 0

def get_sensor_data():
    """Get camera data for environment sensing"""
    if not CAMERA_AVAILABLE:
        return "Env: Camera Ready on Pi"
    
    ret, frame = camera.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        activity = np.std(gray)
        return f"Env Activity: {activity:.2f}"
    return "Env: Sensing Ready"

def draw_demo_screen(demo_name, instructions, status=""):
    """Draw professional demo interface"""
    screen.fill((0, 0, 30))  # Dark blue background
    
    # Header
    header = pygame.Rect(0, 0, screen.get_width(), 80)
    pygame.draw.rect(screen, (0, 50, 100), header)
    
    title_surf = font_large.render(demo_name, True, (255, 255, 255))
    screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 20))
    
    # Demo content
    y_offset = 120
    for line in instructions:
        instr_surf = font_medium.render(line, True, (200, 230, 255))
        screen.blit(instr_surf, (screen.get_width()//2 - instr_surf.get_width()//2, y_offset))
        y_offset += 50
    
    # Status bar
    if status:
        status_surf = font_small.render(status, True, (100, 255, 100))
        screen.blit(status_surf, (20, screen.get_height() - 40))
    
    # Footer
    footer_text = "SPACE: Next Demo  |  Q: Quit  |  Host: motibeamOS"
    footer_surf = font_small.render(footer_text, True, (150, 200, 255))
    screen.blit(footer_surf, (screen.get_width()//2 - footer_surf.get_width()//2, screen.get_height() - 80))
    
    pygame.display.flip()

# ========== VERTICAL DEMOS ==========

def clinical_demo():
    instructions = [
        "MULTI-MODAL ADHERENCE VERIFICATION",
        "Voice: 'Medication Taken'",
        "Gesture: Nod Head Confirmation", 
        "Projected: ✓ Checkmark + Vital Signs",
        "Adherence Confidence Score: 94%",
        "Clinical Deterioration Index: Stable"
    ]
    status = get_sensor_data()
    draw_demo_screen(DEMOS[0], instructions, status)

def automotive_demo():
    instructions = [
        "EXTERNAL PROJECTION SAFETY",
        "Projecting: << STOP >> & Direction Arrows",
        "V2X: Pedestrian Detected Rear-Left",
        "Cabin Display: Speed Limit 25 MPH", 
        "Safety Zone: ACTIVE",
        "Autonomous Vehicle Ready"
    ]
    draw_demo_screen(DEMOS[1], instructions, "Vehicle Systems: NOMINAL")

def maritime_demo():
    instructions = [
        "EMERGENCY SIGNALING SYSTEM",
        "SOS & Lifeboat Direction Arrows",
        "Universal Safety Symbols Active",
        "Deck: Non-slip Zones Highlighted",
        "Water Detection: Sensors Active",
        "First Responder Coordination"
    ]
    status_text = "STATUS: DRILL MODE | All Systems Operational"  # FIXED LINE
    draw_demo_screen(DEMOS[2], instructions, status_text)

def enterprise_demo():
    instructions = [
        "INDUSTRIAL AUTOMATION & SAFETY",
        "Warehouse: Forklift Hazard Zones",
        "Pick Path: Navigation Arrows on Floor", 
        "Assembly: Torque Spec Overlays",
        "Workforce Training: Step-by-Step",
        "Corporate Wellness Programming"
    ]
    draw_demo_screen(DEMOS[3], instructions, "Efficiency: +15% | Safety: 100%")

def security_demo():
    instructions = [
        "GUARDIAN ALERT SYSTEM",
        "Projecting: 'ALPHA ZONE SECURE'",
        "Personnel: 3 Friendly, 0 Unknown",
        "Evacuation: Green Path Highlighted", 
        "Tactical Overlays: Active",
        "VA/DoD Deployment Ready"
    ]
    draw_demo_screen(DEMOS[4], instructions, "Alert Level: GREEN | All Systems Secure")

def education_demo():
    instructions = [
        "AMBIENT LEARNING PLATFORM",
        "Study-to-Sleep: French Vocabulary",
        "Homework Helper: Step 3/5 Calculus",
        "Presentation: Timer 4:32 Remaining",
        "Classroom Tools: Attendance & Alerts",
        "Smart Dorm: University Ready"
    ]
    draw_demo_screen(DEMOS[5], instructions, "Focus: 87% | Retention: High")

# Demo mapping
DEMO_FUNCTIONS = {
    0: clinical_demo,
    1: automotive_demo,
    2: maritime_demo, 
    3: enterprise_demo,
    4: security_demo,
    5: education_demo
}

# ========== MAIN LOOP ==========

print("\n" + "="*50)
print("🚀 MOTIBEAM OS - SIX VERTICAL DEMO ENGINE")
print("📍 Hostname: motibeamOS | User: motibeam")
print("📊 Verticals: Clinical, Automotive, Maritime, Enterprise, Security, Education")
print("="*50)
print("Press SPACEBAR to cycle through demos")
print("Press Q to quit")
print("="*50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                running = False
            elif event.key == K_SPACE:
                current_demo_index = (current_demo_index + 1) % len(DEMOS)
                print(f"🔄 Switching to: {DEMOS[current_demo_index]}")
    
    # Run current demo
    DEMO_FUNCTIONS[current_demo_index]()
    time.sleep(0.05)

# Cleanup
if CAMERA_AVAILABLE:
    camera.release()
pygame.quit()
print("\n✅ MotiBeam OS Shutdown Complete")
print("🎯 Ready for Pi 5 Deployment: ssh motibeam@motibeamOS.local")
print("📁 GitHub: git@github.com:quamie25/MotiBeam-OS.git")
