#!/bin/bash
#
# MotiBeam OS Startup Wrapper with Logging
# This script wraps the MotiBeam application to provide detailed logging
# for debugging systemd autostart issues.
#

# Configuration
MOTIBEAM_DIR="/home/motibeam/MotiBeam-OS"
LOG_DIR="${MOTIBEAM_DIR}/logs"
LOG_FILE="${LOG_DIR}/motibeam_boot.log"
VENV_DIR="${MOTIBEAM_DIR}/motibeam-env"
APP_SCRIPT="${MOTIBEAM_DIR}/motibeam_app.py"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Function to log with timestamp (uses basic shell redirects, no tee required)
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg"
    echo "$msg" >> "${LOG_FILE}"
}

# Start logging
log "=========================================="
log "MotiBeam OS Startup Initiated"
log "=========================================="

# Log environment
log "USER: ${USER}"
log "HOME: ${HOME}"
log "DISPLAY: ${DISPLAY}"
log "XAUTHORITY: ${XAUTHORITY}"
log "PWD: $(pwd)"
log "PATH: ${PATH}"

# Check if X server is accessible (only if xset is available)
log "Checking X server connection..."
if command -v xset &>/dev/null; then
    if xset q &>/dev/null; then
        log "✓ X server connection successful"
    else
        log "✗ WARNING: Cannot connect to X server!"
        log "  This may cause pygame to fail. Waiting 5 seconds..."
        sleep 5
        if xset q &>/dev/null; then
            log "✓ X server connection successful after delay"
        else
            log "✗ ERROR: Still cannot connect to X server"
        fi
    fi
else
    log "⚠ xset not found (install x11-xserver-utils to enable X server checks)"
    log "  Attempting to continue anyway..."
fi

# Change to MotiBeam directory
log "Changing to directory: ${MOTIBEAM_DIR}"
cd "${MOTIBEAM_DIR}" || {
    log "✗ ERROR: Failed to change to ${MOTIBEAM_DIR}"
    exit 1
}

# Check if virtual environment exists and activate it
if [ -d "${VENV_DIR}" ]; then
    log "Virtual environment found at: ${VENV_DIR}"
    log "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate" || {
        log "✗ WARNING: Failed to activate virtual environment, continuing anyway..."
    }
    log "✓ Virtual environment activated (or using system Python)"
else
    log "No virtual environment found at ${VENV_DIR}, using system Python"
fi

# Log Python information
log "Python version: $(python3 --version 2>&1)"
log "Python executable: $(which python3)"

# Check if pygame is available
log "Checking pygame availability..."
PYGAME_CHECK=$(python3 -c "import pygame; print('pygame version:', pygame.version.ver)" 2>&1)
if [ $? -eq 0 ]; then
    log "$PYGAME_CHECK"
    log "✓ pygame is available"
else
    log "$PYGAME_CHECK"
    log "✗ ERROR: pygame import failed!"
fi

# Check if application script exists
if [ ! -f "${APP_SCRIPT}" ]; then
    log "✗ ERROR: Application script not found at ${APP_SCRIPT}"
    exit 1
fi
log "✓ Application script found"

# Set SDL environment variables for better compatibility
export SDL_VIDEODRIVER=x11
export SDL_AUDIODRIVER=pulse
log "SDL_VIDEODRIVER: ${SDL_VIDEODRIVER}"
log "SDL_AUDIODRIVER: ${SDL_AUDIODRIVER}"

# Launch MotiBeam
log "----------------------------------------"
log "Launching MotiBeam OS..."
log "Command: python3 ${APP_SCRIPT}"
log "----------------------------------------"

# Run the application and capture exit code
# Redirect both stdout and stderr to log file while still showing on console
python3 "${APP_SCRIPT}" 2>&1 | while IFS= read -r line; do
    echo "$line"
    echo "$line" >> "${LOG_FILE}"
done

# Capture the exit code from python3 (not from the while loop)
EXIT_CODE=${PIPESTATUS[0]}

# Log completion
log "----------------------------------------"
log "MotiBeam OS exited with code: ${EXIT_CODE}"
log "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
log "=========================================="

# Exit with the same code as the application
exit ${EXIT_CODE}
