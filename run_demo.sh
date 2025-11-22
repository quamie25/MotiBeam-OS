#!/bin/bash
# MotiBeam Demo Launcher - Handles X server and display

# Start X server if not running
if ! pgrep -x "Xorg" > /dev/null; then
    echo "Starting X server..."
    startx &
    sleep 3
fi

# Set display
export DISPLAY=:0

# Activate virtual environment
source ~/motibeam-env/bin/activate

# Hide cursor
unclutter -idle 0 &

# Run the demo
python3 "$@"

# Cleanup
killall unclutter 2>/dev/null
