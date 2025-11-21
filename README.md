# 🌟 MotiBeam OS

**Advanced Projection-Based Assistive Technology System**

MotiBeam OS is a production-ready ambient computing platform that transforms any surface into an interactive assistive technology interface using projection, voice control, and gesture detection.

## 🎯 Features

### ✅ Core Functionality (All Working)
- **Multi-Demo System**: Three interactive demonstration modes
  - Clinical Medication Tracker with voice/gesture confirmation
  - Interactive Drill Assistant with step-by-step guidance
  - General Interactive Guidance System
- **Professional UI**: Smooth transitions, progress bars, color-coded status indicators
- **Automatic Demo Cycling**: Seamlessly transitions between demos every 10 seconds

### 🎤 Voice Control Integration
- **Speech Recognition**: Real-time voice command processing
- **Medication Tracking**: Say "medication taken" to confirm doses
- **Microphone Status**: Live indicator showing listening state
- **Graceful Fallback**: Continues operation without voice hardware

### 👤 Gesture Detection
- **Face Detection**: OpenCV Haar cascade face tracking
- **Head Nod Recognition**: Detect vertical head movements for confirmation
- **Real-time Feedback**: Visual status indicators for gesture detection
- **Graceful Fallback**: Works without camera hardware

### 📷 Real Sensor Data
- **Live Camera Feed**: Picture-in-picture preview in corner
- **Real-time FPS Counter**: Monitor camera performance
- **Environment Brightness**: Automatic brightness detection
- **Performance Metrics**: Frame rate and system monitoring

### 🎨 Professional UI Enhancements
- **MotiBeam Logo Header**: Branded interface with system info
- **Smooth Transitions**: Animated progress between demos
- **Progress Bars**: Visual feedback for demo timing
- **Color-Coded Status**: Success (green), warning (amber), error (red)
- **Responsive Design**: Optimized for 1280x720 projection

### 🛡️ Error Handling
- **Try/Except Blocks**: All hardware operations protected
- **Graceful Degradation**: Features disable when hardware unavailable
- **Clear Error Messages**: Informative status updates
- **Logging**: Console output for debugging

### 🚀 Deployment Ready
- **One-Command Install**: Automated installation script
- **Systemd Service**: Auto-start on boot
- **Resource Management**: CPU and memory limits
- **Security Hardening**: Protected file system access

## 🖥️ Hardware Requirements

### Confirmed Compatible Hardware
- **Raspberry Pi 5** (4GB or 8GB RAM recommended)
- **GOODEE Pico Projector** (1280x720 resolution)
- **Fifine K669D USB Microphone** (or any USB microphone)
- **Logitech 1080P USB Camera** (or any USB webcam)
- **Raspberry Pi OS 64-bit** (Bookworm or later)

### Minimum Requirements
- **Raspberry Pi 4** or newer
- **Any HD projector** (720p minimum)
- **USB microphone** (optional, for voice control)
- **USB webcam** (optional, for gesture detection)
- **Raspberry Pi OS** or any Debian-based Linux

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/quamie25/MotiBeam-OS.git
cd MotiBeam-OS

# Run the installation script
sudo ./install_pi.sh

# Reboot to apply all settings
sudo reboot
```

The installation script will:
1. ✅ Install all system dependencies
2. ✅ Configure camera, microphone, and display
3. ✅ Create Python virtual environment
4. ✅ Install Python packages
5. ✅ Set up systemd service for auto-start
6. ✅ Configure permissions and access
7. ✅ Run system tests

### Manual Installation

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
    portaudio19-dev libopencv-dev python3-opencv \
    libsdl2-dev v4l-utils alsa-utils

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run MotiBeam OS
python motibeam_os.py
```

## 🎮 Usage

### Automatic Start
MotiBeam OS starts automatically on boot when installed via `install_pi.sh`.

### Manual Control

```bash
# Start the service
sudo systemctl start motibeam

# Stop the service
sudo systemctl stop motibeam

# Check status
sudo systemctl status motibeam

# View logs
sudo journalctl -u motibeam -f
```

### Interactive Controls

| Key | Action |
|-----|--------|
| `SPACE` | Next demo |
| `1` | Medication Tracker demo |
| `2` | Drill Mode demo |
| `3` | Interactive Guide demo |
| `ESC` | Exit application |

### Voice Commands

When voice control is enabled:
- **"Medication taken"** - Confirms medication in Clinical demo
- **"Medicine taken"** - Alternative confirmation phrase

### Gesture Controls

When gesture detection is enabled:
- **Head Nod** - Confirms actions (vertical head movement)

## 🏗️ Architecture

### Project Structure

```
MotiBeam-OS/
├── motibeam_os.py       # Main application
├── requirements.txt     # Python dependencies
├── install_pi.sh        # Installation script
├── motibeam.service     # Systemd service file
├── README.md            # This file
├── LICENSE              # License information
└── .gitignore           # Git ignore rules
```

### Code Organization

```python
# Hardware Integration Classes
VoiceController()      # Speech recognition
GestureDetector()      # Face/gesture detection
CameraFeed()          # Real-time camera feed

# UI Helper Functions
draw_text()           # Enhanced text rendering
draw_progress_bar()   # Progress indicators
draw_status_indicator() # Color-coded status
draw_motibeam_header() # Logo and branding

# Demo Screens
draw_medication_tracker_demo()
draw_drill_mode_demo()
draw_interactive_guide_demo()

# Main Application
MotiBeamOS()          # Application controller
```

## 🔧 Configuration

### Display Settings

Edit `/boot/config.txt` for custom display resolution:

```ini
# For GOODEE Pico Projector (1280x720)
hdmi_group=2
hdmi_mode=85
hdmi_drive=2
```

### Audio Settings

Edit `/etc/asound.conf` for custom audio configuration:

```
# Default microphone and speaker settings
pcm.!default {
    type asym
    playback.pcm "dmix"
    capture.pcm "dsnoop"
}
```

### Camera Settings

Test camera with:
```bash
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --all
```

## 🧪 Testing

### Test Individual Components

```python
# Test voice recognition
python3 -c "import speech_recognition as sr; print('Voice: OK')"

# Test OpenCV
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"

# Test camera
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera:', cap.isOpened())"

# Test pygame
python3 -c "import pygame; pygame.init(); print('Pygame: OK')"
```

### System Diagnostics

```bash
# Check camera
v4l2-ctl --list-devices

# Check microphone
arecord -l

# Check display
fbset

# Check services
systemctl status motibeam
```

## 🐛 Troubleshooting

### Camera Not Detected

```bash
# Check camera connection
lsusb | grep -i camera

# Test camera
v4l2-ctl --list-devices

# Add user to video group
sudo usermod -a -G video $USER
```

### Microphone Not Working

```bash
# List audio devices
arecord -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Add user to audio group
sudo usermod -a -G audio $USER
```

### Display Issues

```bash
# Check HDMI status
tvservice -s

# Test display modes
tvservice -m CEA
tvservice -m DMT
```

### Service Won't Start

```bash
# Check service logs
sudo journalctl -u motibeam -n 50

# Check permissions
ls -la /home/motibeam/motibeam-os/

# Test manual run
cd /home/motibeam/motibeam-os
source venv/bin/activate
python motibeam_os.py
```

## 📚 Dependencies

### System Packages
- Python 3.11+
- SDL2 (graphics)
- PortAudio (audio)
- OpenCV (computer vision)
- V4L2 (video for Linux)
- ALSA (audio)

### Python Packages
- **pygame 2.5.2** - Graphics and display
- **opencv-python 4.8.1** - Computer vision
- **numpy 1.24.3** - Array operations
- **SpeechRecognition 3.10.0** - Voice recognition
- **PyAudio 0.2.14** - Audio interface

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/quamie25/MotiBeam-OS.git
cd MotiBeam-OS

# Create development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in development mode
python motibeam_os.py
```

## 📄 License

This project is licensed under the terms included in the LICENSE file.

## 🙏 Acknowledgments

- OpenCV team for computer vision libraries
- Pygame community for graphics framework
- CMU Sphinx team for speech recognition
- Raspberry Pi Foundation

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: https://github.com/quamie25/MotiBeam-OS/issues
- **Documentation**: This README

## 🗺️ Roadmap

### Current Version (v2.0)
- ✅ Voice control integration
- ✅ Gesture detection
- ✅ Real-time camera feed
- ✅ Professional UI
- ✅ Production deployment

### Future Enhancements
- 🔄 Multi-language support
- 🔄 Custom demo builder
- 🔄 Remote configuration
- 🔄 Cloud sync for settings
- 🔄 Advanced gesture recognition (MediaPipe)
- 🔄 AI-powered assistance

---

**Made with ❤️ for accessible technology**
