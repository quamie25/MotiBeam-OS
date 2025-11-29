#!/bin/bash
# MotiBeamOS v3.0 Launcher
# Automatically sets DISPLAY for SSH sessions

# Set display if not already set
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "Set DISPLAY=:0 for pygame"
fi

# Run MotiBeamOS
cd ~/MotiBeam-OS
python3 motibeam_v3.py
