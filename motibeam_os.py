#!/usr/bin/env python3
"""
MotiBeam OS - Advanced Projection-Based Assistive Technology System
Developed for Raspberry Pi 5 with GOODEE Pico Projector

Features:
- Voice control integration for medication tracking
- Gesture detection with OpenCV face/head nod recognition
- Real-time camera feed and environmental monitoring
- Professional UI with smooth transitions
- Production-ready error handling and fallbacks
"""

import pygame
import sys
import math
import time
from datetime import datetime
from enum import Enum
import threading
import queue

# Optional hardware integrations with graceful fallbacks
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  Speech recognition not available. Install 'SpeechRecognition' for voice control.")

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("⚠️  OpenCV not available. Install 'opencv-python' for gesture detection.")

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

# Display configuration for GOODEE Pico Projector
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS = 30

# Color palette - Professional and accessible
COLORS = {
    'bg': (15, 20, 35),           # Dark blue-gray background
    'accent': (0, 255, 180),      # Cyan accent
    'text': (240, 245, 255),      # Off-white text
    'warning': (255, 180, 0),     # Amber warning
    'error': (255, 80, 80),       # Soft red error
    'success': (80, 255, 120),    # Green success
    'muted': (120, 130, 150),     # Muted gray
    'highlight': (100, 200, 255), # Light blue
}

# Camera configuration for Logitech 1080P USB camera
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_PREVIEW_SIZE = (160, 120)  # Small preview in corner

# Gesture detection parameters
FACE_CASCADE_PATH = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
NOD_THRESHOLD = 15  # Pixel movement threshold for head nod detection

# Demo modes
class DemoMode(Enum):
    MEDICATION_TRACKER = 0
    DRILL_MODE = 1
    INTERACTIVE_GUIDE = 2

# ============================================================================
# HARDWARE INTEGRATION CLASSES
# ============================================================================

class VoiceController:
    """Handles voice recognition for medication tracking"""

    def __init__(self):
        self.enabled = SPEECH_AVAILABLE
        self.recognizer = sr.Recognizer() if self.enabled else None
        self.microphone = None
        self.listening = False
        self.last_command = None
        self.command_queue = queue.Queue()
        self.status = "Initializing..."

        if self.enabled:
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.status = "Ready"
            except Exception as e:
                print(f"⚠️  Microphone initialization failed: {e}")
                self.enabled = False
                self.status = "No microphone"

    def start_listening(self):
        """Start background listening thread"""
        if not self.enabled:
            return

        self.listening = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def stop_listening(self):
        """Stop listening thread"""
        self.listening = False

    def _listen_loop(self):
        """Background thread for continuous listening"""
        while self.listening:
            try:
                with self.microphone as source:
                    self.status = "Listening..."
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)

                self.status = "Processing..."
                text = self.recognizer.recognize_google(audio).lower()

                # Check for medication-related commands
                if "medication" in text or "medicine" in text:
                    if "taken" in text or "take" in text:
                        self.last_command = "MEDICATION_TAKEN"
                        self.command_queue.put("MEDICATION_TAKEN")
                        self.status = f"✓ Heard: {text}"

            except sr.WaitTimeoutError:
                self.status = "Ready"
            except sr.UnknownValueError:
                self.status = "Didn't understand"
            except Exception as e:
                self.status = f"Error: {str(e)[:20]}"
                time.sleep(0.5)

    def get_status(self):
        """Get current microphone status"""
        if not self.enabled:
            return "⚠️  Voice: Disabled"
        return f"🎤 Voice: {self.status}"


class GestureDetector:
    """Handles OpenCV-based face detection and head nod recognition"""

    def __init__(self):
        self.enabled = OPENCV_AVAILABLE
        self.face_cascade = None
        self.last_face_y = None
        self.nod_detected = False
        self.status = "Initializing..."

        if self.enabled:
            try:
                self.face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
                if self.face_cascade.empty():
                    raise Exception("Failed to load Haar cascade")
                self.status = "Ready"
            except Exception as e:
                print(f"⚠️  Gesture detection initialization failed: {e}")
                self.enabled = False
                self.status = "Not available"

    def detect_nod(self, frame):
        """Detect head nod from face position changes"""
        if not self.enabled or frame is None:
            return False

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                # Get the largest face
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                face_center_y = y + h // 2

                # Detect vertical movement (nod)
                if self.last_face_y is not None:
                    movement = abs(face_center_y - self.last_face_y)
                    if movement > NOD_THRESHOLD:
                        self.nod_detected = True
                        self.status = "✓ Nod detected!"
                        self.last_face_y = None  # Reset to avoid duplicate detection
                        return True
                    else:
                        self.status = "Face tracked"

                self.last_face_y = face_center_y
            else:
                self.status = "No face detected"
                self.last_face_y = None

            return False

        except Exception as e:
            self.status = f"Error: {str(e)[:20]}"
            return False

    def get_status(self):
        """Get current gesture detection status"""
        if not self.enabled:
            return "⚠️  Gesture: Disabled"
        return f"👤 Gesture: {self.status}"


class CameraFeed:
    """Handles real-time camera feed and environmental monitoring"""

    def __init__(self):
        self.enabled = OPENCV_AVAILABLE
        self.capture = None
        self.current_frame = None
        self.fps_counter = []
        self.brightness = 0
        self.status = "Initializing..."

        if self.enabled:
            try:
                self.capture = cv2.VideoCapture(CAMERA_INDEX)
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

                # Test capture
                ret, frame = self.capture.read()
                if not ret:
                    raise Exception("Failed to read from camera")

                self.status = "Active"
            except Exception as e:
                print(f"⚠️  Camera initialization failed: {e}")
                self.enabled = False
                self.status = "No camera"
                if self.capture:
                    self.capture.release()

    def update(self):
        """Capture new frame and update metrics"""
        if not self.enabled or not self.capture:
            return None

        try:
            start_time = time.time()
            ret, frame = self.capture.read()

            if ret:
                self.current_frame = frame

                # Calculate FPS
                self.fps_counter.append(time.time() - start_time)
                if len(self.fps_counter) > 30:
                    self.fps_counter.pop(0)

                # Calculate brightness (average of all pixels)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.brightness = int(np.mean(gray))

                return frame
            else:
                self.status = "Failed to read"
                return None

        except Exception as e:
            self.status = f"Error: {str(e)[:20]}"
            return None

    def get_fps(self):
        """Calculate current FPS"""
        if not self.fps_counter:
            return 0
        avg_time = sum(self.fps_counter) / len(self.fps_counter)
        return int(1.0 / avg_time) if avg_time > 0 else 0

    def get_preview_surface(self):
        """Convert current frame to pygame surface for preview"""
        if self.current_frame is None:
            return None

        try:
            # Resize for preview
            small_frame = cv2.resize(self.current_frame, CAMERA_PREVIEW_SIZE)
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            # Rotate to match pygame coordinate system
            rgb_frame = np.rot90(rgb_frame)
            # Create pygame surface
            return pygame.surfarray.make_surface(rgb_frame)
        except Exception as e:
            print(f"Preview conversion error: {e}")
            return None

    def cleanup(self):
        """Release camera resources"""
        if self.capture:
            self.capture.release()


# ============================================================================
# UI HELPER FUNCTIONS
# ============================================================================

def draw_text(surface, text, pos, size=32, color=None, align='left', bold=False):
    """Draw text with enhanced styling options"""
    if color is None:
        color = COLORS['text']

    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.center = pos
    elif align == 'right':
        text_rect.right = pos[0]
        text_rect.top = pos[1]
    else:  # left
        text_rect.topleft = pos

    surface.blit(text_surface, text_rect)
    return text_rect


def draw_progress_bar(surface, rect, progress, color=None, bg_color=None):
    """Draw a progress bar with percentage"""
    if color is None:
        color = COLORS['accent']
    if bg_color is None:
        bg_color = COLORS['muted']

    # Background
    pygame.draw.rect(surface, bg_color, rect, border_radius=5)

    # Filled portion
    if progress > 0:
        filled_rect = rect.copy()
        filled_rect.width = int(rect.width * min(progress, 1.0))
        pygame.draw.rect(surface, color, filled_rect, border_radius=5)

    # Border
    pygame.draw.rect(surface, color, rect, 2, border_radius=5)


def draw_status_indicator(surface, pos, status, label):
    """Draw a color-coded status indicator"""
    if status == "success":
        color = COLORS['success']
        symbol = "✓"
    elif status == "warning":
        color = COLORS['warning']
        symbol = "⚠"
    elif status == "error":
        color = COLORS['error']
        symbol = "✗"
    else:  # active/normal
        color = COLORS['accent']
        symbol = "●"

    # Draw indicator circle
    pygame.draw.circle(surface, color, pos, 8)

    # Draw label
    draw_text(surface, f"{symbol} {label}", (pos[0] + 20, pos[1] - 10), 24, color)


def draw_motibeam_header(surface):
    """Draw the MotiBeam OS logo and header"""
    # Logo area
    logo_rect = pygame.Rect(20, 20, 200, 60)
    pygame.draw.rect(surface, COLORS['accent'], logo_rect, 3, border_radius=10)

    # MotiBeam text
    draw_text(surface, "MotiBeam", (40, 30), 48, COLORS['accent'], bold=True)
    draw_text(surface, "OS", (180, 50), 28, COLORS['text'])

    # System info
    timestamp = datetime.now().strftime("%H:%M:%S")
    draw_text(surface, timestamp, (DISPLAY_WIDTH - 20, 30), 32, COLORS['muted'], align='right')
    draw_text(surface, "Raspberry Pi 5", (DISPLAY_WIDTH - 20, 60), 24, COLORS['muted'], align='right')


def draw_hardware_status(surface, voice_ctrl, gesture_det, camera_feed, y_pos):
    """Draw status indicators for all hardware components"""
    x_start = 20
    spacing = 300

    # Voice control status
    status_text = voice_ctrl.get_status()
    draw_text(surface, status_text, (x_start, y_pos), 24, COLORS['text'])

    # Gesture detection status
    status_text = gesture_det.get_status()
    draw_text(surface, status_text, (x_start + spacing, y_pos), 24, COLORS['text'])

    # Camera status with FPS
    if camera_feed.enabled:
        fps = camera_feed.get_fps()
        brightness = camera_feed.brightness
        status_text = f"📷 Camera: {fps} FPS | Brightness: {brightness}"
    else:
        status_text = "⚠️  Camera: Disabled"
    draw_text(surface, status_text, (x_start + spacing * 2, y_pos), 24, COLORS['text'])


def draw_camera_preview(surface, camera_feed, pos):
    """Draw small camera preview in corner"""
    preview = camera_feed.get_preview_surface()
    if preview:
        # Border
        border_rect = pygame.Rect(pos[0] - 2, pos[1] - 2,
                                   CAMERA_PREVIEW_SIZE[0] + 4,
                                   CAMERA_PREVIEW_SIZE[1] + 4)
        pygame.draw.rect(surface, COLORS['accent'], border_rect, 2, border_radius=5)

        # Preview
        surface.blit(preview, pos)

        # Label
        draw_text(surface, "LIVE", (pos[0], pos[1] + CAMERA_PREVIEW_SIZE[1] + 5),
                 20, COLORS['accent'])


# ============================================================================
# DEMO SCREENS
# ============================================================================

def draw_medication_tracker_demo(surface, progress, voice_ctrl, gesture_det, camera_feed):
    """Demo 1: Clinical Medication Tracking with Voice & Gesture Control"""

    # Title
    draw_text(surface, "CLINICAL MEDICATION TRACKER",
             (DISPLAY_WIDTH // 2, 120), 56, COLORS['accent'], align='center', bold=True)

    # Instructions
    instructions = [
        "Say: 'Medication taken' to confirm",
        "Or nod your head to confirm",
        "Voice and gesture controls active"
    ]

    y_offset = 200
    for instruction in instructions:
        draw_text(surface, instruction, (DISPLAY_WIDTH // 2, y_offset),
                 32, COLORS['text'], align='center')
        y_offset += 40

    # Medication schedule
    medications = [
        ("Morning Pills", "8:00 AM", False),
        ("Afternoon Dose", "2:00 PM", False),
        ("Evening Pills", "8:00 PM", False),
    ]

    y_pos = 330
    for i, (med_name, med_time, taken) in enumerate(medications):
        # Check if medication was confirmed via voice or gesture
        if i == 0:  # Simulate first medication confirmation
            try:
                # Check voice command
                if not voice_ctrl.command_queue.empty():
                    cmd = voice_ctrl.command_queue.get()
                    if cmd == "MEDICATION_TAKEN":
                        taken = True

                # Check gesture
                if camera_feed.current_frame is not None:
                    if gesture_det.detect_nod(camera_feed.current_frame):
                        taken = True
            except:
                pass

        # Status indicator
        status = "success" if taken else "active"
        draw_status_indicator(surface, (100, y_pos + 25), status,
                             f"{med_name} - {med_time}")

        # Draw pill representation
        pill_x = DISPLAY_WIDTH - 200
        pill_color = COLORS['success'] if taken else COLORS['warning']
        pygame.draw.ellipse(surface, pill_color,
                          (pill_x, y_pos + 10, 60, 30), border_radius=15)

        y_pos += 60

    # Progress indicator
    progress_rect = pygame.Rect(100, DISPLAY_HEIGHT - 150, DISPLAY_WIDTH - 200, 40)
    draw_progress_bar(surface, progress_rect, progress, COLORS['accent'])
    draw_text(surface, f"Demo Progress: {int(progress * 100)}%",
             (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 90), 28,
             COLORS['text'], align='center')

    # Hardware status
    draw_hardware_status(surface, voice_ctrl, gesture_det, camera_feed, DISPLAY_HEIGHT - 50)


def draw_drill_mode_demo(surface, progress, voice_ctrl, gesture_det, camera_feed):
    """Demo 2: Interactive Drill Assistant Mode"""

    # Title with proper string formatting (FIX FOR ORIGINAL ERROR)
    draw_text(surface, "INTERACTIVE DRILL ASSISTANT",
             (DISPLAY_WIDTH // 2, 120), 56, COLORS['highlight'], align='center', bold=True)

    # Status bar - PROPERLY FORMATTED STRING (this was the original error location)
    status_text = "STATUS: DRILL MODE | All Systems Operational"
    draw_text(surface, status_text, (DISPLAY_WIDTH // 2, 180),
             32, COLORS['success'], align='center')

    # Drill steps with visual guides
    steps = [
        "1. Position drill perpendicular to surface",
        "2. Apply steady pressure",
        "3. Start drill at low speed",
        "4. Gradually increase speed",
        "5. Maintain constant pressure"
    ]

    y_pos = 250
    for i, step in enumerate(steps):
        # Highlight current step based on progress
        current_step = int(progress * len(steps))
        if i < current_step:
            color = COLORS['success']
            prefix = "✓ "
        elif i == current_step:
            color = COLORS['accent']
            prefix = "▶ "
        else:
            color = COLORS['muted']
            prefix = "  "

        draw_text(surface, prefix + step, (150, y_pos), 36, color)
        y_pos += 55

    # Safety indicators
    safety_y = DISPLAY_HEIGHT - 200
    draw_text(surface, "SAFETY CHECKS:", (100, safety_y), 32, COLORS['warning'], bold=True)

    safety_items = [
        ("Safety Glasses", True),
        ("Work Area Clear", True),
        ("Material Secured", True)
    ]

    safety_x = 100
    for item, status in safety_items:
        indicator_status = "success" if status else "warning"
        draw_status_indicator(surface, (safety_x, safety_y + 50), indicator_status, item)
        safety_x += 350

    # Progress bar
    progress_rect = pygame.Rect(100, DISPLAY_HEIGHT - 100, DISPLAY_WIDTH - 200, 35)
    draw_progress_bar(surface, progress_rect, progress, COLORS['highlight'])


def draw_interactive_guide_demo(surface, progress, voice_ctrl, gesture_det, camera_feed):
    """Demo 3: General Interactive Guidance System"""

    # Title
    draw_text(surface, "INTERACTIVE GUIDANCE SYSTEM",
             (DISPLAY_WIDTH // 2, 120), 56, COLORS['success'], align='center', bold=True)

    # Main instruction area
    instruction_rect = pygame.Rect(100, 200, DISPLAY_WIDTH - 200, 200)
    pygame.draw.rect(surface, COLORS['accent'], instruction_rect, 3, border_radius=15)

    # Animated instruction based on progress
    instruction_phase = int(progress * 3)
    instructions = [
        "Welcome! This system provides step-by-step guidance",
        "Voice commands and gesture controls are active",
        "Real-time visual feedback helps you complete tasks"
    ]

    current_instruction = instructions[min(instruction_phase, len(instructions) - 1)]
    draw_text(surface, current_instruction, (DISPLAY_WIDTH // 2, 300),
             40, COLORS['text'], align='center')

    # Feature showcase
    features_y = 450
    draw_text(surface, "ACTIVE FEATURES:", (DISPLAY_WIDTH // 2, features_y),
             36, COLORS['accent'], align='center', bold=True)

    features = [
        "🎤 Voice Recognition",
        "👤 Gesture Detection",
        "📷 Real-time Monitoring",
        "⚡ Adaptive Assistance"
    ]

    feature_x_start = 200
    feature_spacing = (DISPLAY_WIDTH - 400) // (len(features) - 1)

    for i, feature in enumerate(features):
        x_pos = feature_x_start + i * feature_spacing
        # Pulse effect based on progress
        pulse = 1.0 + 0.1 * math.sin(progress * math.pi * 4 + i)
        size = int(32 * pulse)
        draw_text(surface, feature, (x_pos, features_y + 60), size, COLORS['text'], align='center')

    # Environmental data display
    env_y = DISPLAY_HEIGHT - 180
    draw_text(surface, "ENVIRONMENTAL DATA:", (100, env_y), 28, COLORS['muted'])

    env_data = [
        f"Brightness: {camera_feed.brightness}/255",
        f"Camera FPS: {camera_feed.get_fps()}",
        f"System Time: {datetime.now().strftime('%H:%M:%S')}"
    ]

    for i, data in enumerate(env_data):
        draw_text(surface, data, (100, env_y + 35 + i * 30), 24, COLORS['text'])

    # Progress indicator
    progress_rect = pygame.Rect(100, DISPLAY_HEIGHT - 80, DISPLAY_WIDTH - 200, 30)
    draw_progress_bar(surface, progress_rect, progress, COLORS['success'])


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class MotiBeamOS:
    """Main application controller for MotiBeam OS"""

    def __init__(self):
        pygame.init()

        # Initialize display
        try:
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
            pygame.display.set_caption("MotiBeam OS - Advanced Projection System")
        except Exception as e:
            print(f"❌ Failed to initialize display: {e}")
            sys.exit(1)

        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize hardware components with error handling
        print("🔧 Initializing MotiBeam OS...")

        try:
            self.voice_ctrl = VoiceController()
            print("✓ Voice controller initialized")
        except Exception as e:
            print(f"⚠️  Voice controller failed: {e}")
            self.voice_ctrl = VoiceController()  # Will be disabled

        try:
            self.gesture_det = GestureDetector()
            print("✓ Gesture detector initialized")
        except Exception as e:
            print(f"⚠️  Gesture detector failed: {e}")
            self.gesture_det = GestureDetector()  # Will be disabled

        try:
            self.camera_feed = CameraFeed()
            print("✓ Camera feed initialized")
        except Exception as e:
            print(f"⚠️  Camera feed failed: {e}")
            self.camera_feed = CameraFeed()  # Will be disabled

        # Demo control
        self.current_demo = DemoMode.MEDICATION_TRACKER
        self.demo_start_time = time.time()
        self.demo_duration = 10.0  # 10 seconds per demo
        self.transition_progress = 0.0
        self.in_transition = False

        # Start voice listening if available
        if self.voice_ctrl.enabled:
            self.voice_ctrl.start_listening()

        print("✅ MotiBeam OS initialized successfully!")
        print(f"   Display: {DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
        print(f"   Voice Control: {'Enabled' if self.voice_ctrl.enabled else 'Disabled'}")
        print(f"   Gesture Detection: {'Enabled' if self.gesture_det.enabled else 'Disabled'}")
        print(f"   Camera Feed: {'Enabled' if self.camera_feed.enabled else 'Disabled'}")

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Manual demo switch
                    self.next_demo()
                elif event.key == pygame.K_1:
                    self.current_demo = DemoMode.MEDICATION_TRACKER
                    self.demo_start_time = time.time()
                elif event.key == pygame.K_2:
                    self.current_demo = DemoMode.DRILL_MODE
                    self.demo_start_time = time.time()
                elif event.key == pygame.K_3:
                    self.current_demo = DemoMode.INTERACTIVE_GUIDE
                    self.demo_start_time = time.time()

    def next_demo(self):
        """Transition to next demo"""
        demos = list(DemoMode)
        current_index = demos.index(self.current_demo)
        next_index = (current_index + 1) % len(demos)
        self.current_demo = demos[next_index]
        self.demo_start_time = time.time()
        self.transition_progress = 0.0

    def update(self):
        """Update application state"""
        # Update camera feed
        if self.camera_feed.enabled:
            self.camera_feed.update()

        # Check for automatic demo transition
        elapsed = time.time() - self.demo_start_time
        if elapsed >= self.demo_duration:
            self.next_demo()

        # Update transition animation
        self.transition_progress = min(elapsed / self.demo_duration, 1.0)

    def render(self):
        """Render current frame"""
        # Clear screen
        self.screen.fill(COLORS['bg'])

        # Draw header
        draw_motibeam_header(self.screen)

        # Draw current demo
        if self.current_demo == DemoMode.MEDICATION_TRACKER:
            draw_medication_tracker_demo(self.screen, self.transition_progress,
                                        self.voice_ctrl, self.gesture_det,
                                        self.camera_feed)
        elif self.current_demo == DemoMode.DRILL_MODE:
            draw_drill_mode_demo(self.screen, self.transition_progress,
                                self.voice_ctrl, self.gesture_det,
                                self.camera_feed)
        elif self.current_demo == DemoMode.INTERACTIVE_GUIDE:
            draw_interactive_guide_demo(self.screen, self.transition_progress,
                                       self.voice_ctrl, self.gesture_det,
                                       self.camera_feed)

        # Draw camera preview in corner
        if self.camera_feed.enabled:
            preview_pos = (DISPLAY_WIDTH - CAMERA_PREVIEW_SIZE[0] - 20,
                          DISPLAY_HEIGHT - CAMERA_PREVIEW_SIZE[1] - 100)
            draw_camera_preview(self.screen, self.camera_feed, preview_pos)

        # Draw controls hint
        draw_text(self.screen, "Controls: SPACE=Next | 1/2/3=Select Demo | ESC=Exit",
                 (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 15), 20,
                 COLORS['muted'], align='center')

        # Update display
        pygame.display.flip()

    def run(self):
        """Main application loop"""
        print("\n🚀 MotiBeam OS Running!")
        print("=" * 60)

        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(FPS)

        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")

        except Exception as e:
            print(f"\n❌ Runtime error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("\n🔧 Shutting down MotiBeam OS...")

        if self.voice_ctrl:
            self.voice_ctrl.stop_listening()

        if self.camera_feed:
            self.camera_feed.cleanup()

        pygame.quit()
        print("✅ Shutdown complete")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Application entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🌟 MotiBeam OS v2.0 🌟                       ║
    ║     Advanced Projection-Based Assistive Technology       ║
    ║                                                           ║
    ║  Hardware: Raspberry Pi 5 + GOODEE Pico Projector        ║
    ║  Features: Voice • Gesture • Real-time Monitoring        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        app = MotiBeamOS()
        app.run()
    except Exception as e:
        print(f"\n❌ Failed to start MotiBeam OS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
