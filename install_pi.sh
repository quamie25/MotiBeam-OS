#!/bin/bash
###############################################################################
# MotiBeam OS - Raspberry Pi Installation Script
#
# This script installs and configures MotiBeam OS on Raspberry Pi 5
# Hardware: GOODEE Pico Projector, Fifine K669D Mic, Logitech Camera
#
# Usage: sudo ./install_pi.sh
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/home/motibeam/motibeam-os"
SERVICE_NAME="motibeam"
PYTHON_VERSION="3.11"

###############################################################################
# Helper Functions
###############################################################################

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║              🌟 MotiBeam OS Installer 🌟                  ║"
    echo "║           Raspberry Pi 5 Setup Script                    ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

check_pi_model() {
    if ! grep -q "Raspberry Pi 5" /proc/cpuinfo; then
        print_warning "This script is optimized for Raspberry Pi 5"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_info "Raspberry Pi 5 detected ✓"
    fi
}

###############################################################################
# Installation Steps
###############################################################################

install_system_dependencies() {
    print_step "Installing system dependencies..."

    apt-get update
    apt-get upgrade -y

    # Core dependencies
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        git \
        portaudio19-dev \
        libportaudio2 \
        libasound2-dev \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libfreetype6-dev \
        libopencv-dev \
        python3-opencv \
        v4l-utils \
        alsa-utils \
        pulseaudio

    # OpenCV Haar Cascades
    if [ ! -f /usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml ]; then
        print_warning "Haar cascades not found, installing..."
        apt-get install -y opencv-data
    fi

    print_info "System dependencies installed ✓"
}

setup_camera() {
    print_step "Configuring Logitech 1080P USB Camera..."

    # Load camera modules
    modprobe bcm2835-v4l2

    # Add to boot
    if ! grep -q "bcm2835-v4l2" /etc/modules; then
        echo "bcm2835-v4l2" >> /etc/modules
    fi

    # Test camera
    if v4l2-ctl --list-devices | grep -q "Logitech"; then
        print_info "Logitech camera detected ✓"
    else
        print_warning "Logitech camera not detected. Please check connection."
    fi

    # Set camera permissions
    usermod -a -G video motibeam || true

    print_info "Camera configuration complete ✓"
}

setup_audio() {
    print_step "Configuring Fifine K669D Microphone..."

    # Set up ALSA
    cat > /etc/asound.conf << 'EOF'
# MotiBeam OS Audio Configuration
pcm.!default {
    type asym
    playback.pcm "dmix"
    capture.pcm "dsnoop"
}

pcm.dmix {
    type dmix
    ipc_key 1024
    slave {
        pcm "hw:0,0"
        period_time 0
        period_size 1024
        buffer_size 4096
        rate 44100
    }
    bindings {
        0 0
        1 1
    }
}

pcm.dsnoop {
    type dsnoop
    ipc_key 1025
    slave {
        pcm "hw:1,0"
        period_time 0
        period_size 1024
        buffer_size 4096
        rate 44100
    }
    bindings {
        0 0
        1 1
    }
}
EOF

    # Add user to audio group
    usermod -a -G audio motibeam || true

    # Test microphone
    if arecord -l | grep -q "Fifine\|USB"; then
        print_info "USB microphone detected ✓"
    else
        print_warning "USB microphone not detected. Please check connection."
    fi

    print_info "Audio configuration complete ✓"
}

setup_display() {
    print_step "Configuring GOODEE Pico Projector (1280x720)..."

    # Set display resolution in config.txt
    if ! grep -q "hdmi_mode=85" /boot/config.txt; then
        cat >> /boot/config.txt << 'EOF'

# MotiBeam OS Display Configuration
# GOODEE Pico Projector - 1280x720
hdmi_group=2
hdmi_mode=85
hdmi_drive=2
EOF
    fi

    print_info "Display configuration complete ✓"
    print_warning "Reboot required for display settings to take effect"
}

create_virtual_environment() {
    print_step "Creating Python virtual environment..."

    # Create installation directory
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"

    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip setuptools wheel

    print_info "Virtual environment created ✓"
}

install_python_dependencies() {
    print_step "Installing Python dependencies..."

    cd "$INSTALL_DIR"
    source venv/bin/activate

    # Copy requirements.txt if it exists
    if [ -f "$OLDPWD/requirements.txt" ]; then
        cp "$OLDPWD/requirements.txt" .
    else
        print_error "requirements.txt not found!"
        exit 1
    fi

    # Install dependencies
    pip install -r requirements.txt

    print_info "Python dependencies installed ✓"
}

install_motibeam_app() {
    print_step "Installing MotiBeam OS application..."

    cd "$INSTALL_DIR"

    # Copy application files
    if [ -f "$OLDPWD/motibeam_os.py" ]; then
        cp "$OLDPWD/motibeam_os.py" .
        chmod +x motibeam_os.py
    else
        print_error "motibeam_os.py not found!"
        exit 1
    fi

    # Set ownership
    chown -R motibeam:motibeam "$INSTALL_DIR"

    print_info "MotiBeam OS application installed ✓"
}

install_systemd_service() {
    print_step "Installing systemd service..."

    # Copy service file
    if [ -f "$OLDPWD/motibeam.service" ]; then
        cp "$OLDPWD/motibeam.service" /etc/systemd/system/
    else
        # Create service file if it doesn't exist
        cat > /etc/systemd/system/motibeam.service << EOF
[Unit]
Description=MotiBeam OS - Advanced Projection System
After=network.target sound.target

[Service]
Type=simple
User=motibeam
WorkingDirectory=$INSTALL_DIR
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/motibeam/.Xauthority"
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/motibeam_os.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical.target
EOF
    fi

    # Reload systemd
    systemctl daemon-reload

    print_info "Systemd service installed ✓"
}

configure_autostart() {
    print_step "Configuring auto-start..."

    # Enable service
    systemctl enable motibeam.service

    # Create desktop autostart entry
    mkdir -p /home/motibeam/.config/autostart
    cat > /home/motibeam/.config/autostart/motibeam.desktop << EOF
[Desktop Entry]
Type=Application
Name=MotiBeam OS
Exec=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/motibeam_os.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

    chown -R motibeam:motibeam /home/motibeam/.config

    print_info "Auto-start configured ✓"
}

run_system_tests() {
    print_step "Running system tests..."

    cd "$INSTALL_DIR"
    source venv/bin/activate

    # Test Python imports
    python3 << 'PYTEST'
import sys
try:
    import pygame
    print("✓ Pygame imported successfully")
except ImportError as e:
    print(f"✗ Pygame import failed: {e}")
    sys.exit(1)

try:
    import cv2
    print("✓ OpenCV imported successfully")
except ImportError as e:
    print(f"✗ OpenCV import failed: {e}")
    sys.exit(1)

try:
    import speech_recognition
    print("✓ SpeechRecognition imported successfully")
except ImportError as e:
    print(f"⚠ SpeechRecognition import failed: {e}")

print("\n✓ Core dependencies test passed!")
PYTEST

    print_info "System tests complete ✓"
}

print_completion_message() {
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║          ✅ MotiBeam OS Installation Complete! ✅         ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "${BLUE}Installation Summary:${NC}"
    echo "  📁 Installation directory: $INSTALL_DIR"
    echo "  🐍 Python environment: $INSTALL_DIR/venv"
    echo "  🎮 Application: $INSTALL_DIR/motibeam_os.py"
    echo "  ⚙️  Service: /etc/systemd/system/motibeam.service"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Reboot the system: sudo reboot"
    echo "  2. MotiBeam OS will start automatically on boot"
    echo ""
    echo -e "${BLUE}Manual Control:${NC}"
    echo "  • Start:   sudo systemctl start motibeam"
    echo "  • Stop:    sudo systemctl stop motibeam"
    echo "  • Status:  sudo systemctl status motibeam"
    echo "  • Logs:    sudo journalctl -u motibeam -f"
    echo ""
    echo -e "${BLUE}Manual Run:${NC}"
    echo "  cd $INSTALL_DIR"
    echo "  source venv/bin/activate"
    echo "  python motibeam_os.py"
    echo ""
    echo -e "${YELLOW}Note: Display settings require a reboot to take effect${NC}"
    echo ""
}

###############################################################################
# Main Installation Flow
###############################################################################

main() {
    print_header

    # Preflight checks
    check_root
    check_pi_model

    # Installation steps
    install_system_dependencies
    setup_camera
    setup_audio
    setup_display
    create_virtual_environment
    install_python_dependencies
    install_motibeam_app
    install_systemd_service
    configure_autostart
    run_system_tests

    # Completion
    print_completion_message

    # Prompt for reboot
    echo -e "${YELLOW}"
    read -p "Reboot now to apply all settings? (y/N) " -n 1 -r
    echo -e "${NC}"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Rebooting in 5 seconds..."
        sleep 5
        reboot
    fi
}

# Run main installation
main
