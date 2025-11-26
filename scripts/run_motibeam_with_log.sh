#!/bin/bash
#
# MotiBeam OS Startup Wrapper with Logging
# Launches MotiBeam with proper X display configuration for systemd autostart
#

# Configuration
MOTIBEAM_DIR="/home/motibeam/MotiBeam-OS"
LOG_FILE="/home/motibeam/motibeam_boot.log"
VENV_DIR="${MOTIBEAM_DIR}/motibeam-env"
APP_SCRIPT="${MOTIBEAM_DIR}/motibeam_app.py"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Start logging
log "=========================================="
log "MotiBeam OS Startup"
log "=========================================="

# Change to MotiBeam directory
cd "${MOTIBEAM_DIR}" || {
    log "ERROR: Failed to change to ${MOTIBEAM_DIR}"
    exit 1
}

# Set X display environment (critical for pygame to work)
export DISPLAY=:0
export XAUTHORITY=/home/motibeam/.Xauthority

# Set SDL variables for better compatibility
export SDL_VIDEODRIVER=x11
export SDL_AUDIODRIVER=pulse

# Log environment
log "Working directory: ${MOTIBEAM_DIR}"
log "DISPLAY: ${DISPLAY}"
log "XAUTHORITY: ${XAUTHORITY}"
log "User: ${USER}"

# Wait a bit for X server to be fully ready (important for boot autostart)
log "Waiting for X server to be ready..."
for i in {1..10}; do
    if command -v xset &>/dev/null && xset q &>/dev/null 2>&1; then
        log "X server ready after ${i} attempts"
        break
    fi
    sleep 1
done

# Check if virtual environment exists and activate it
if [ -d "${VENV_DIR}" ]; then
    log "Activating virtual environment: ${VENV_DIR}"
    source "${VENV_DIR}/bin/activate" 2>/dev/null || log "Warning: venv activation failed, using system Python"
else
    log "Using system Python (no venv found)"
fi

# Verify app script exists
if [ ! -f "${APP_SCRIPT}" ]; then
    log "ERROR: Application script not found at ${APP_SCRIPT}"
    exit 1
fi

# Launch MotiBeam
log "Launching MotiBeam OS: python3 ${APP_SCRIPT}"
log "=========================================="

# Run the application and log output
python3 "${APP_SCRIPT}" >> "${LOG_FILE}" 2>&1
EXIT_CODE=$?

# Log completion
log "=========================================="
log "MotiBeam OS exited with code: ${EXIT_CODE}"
log "=========================================="

exit ${EXIT_CODE}
