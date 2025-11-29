#!/bin/bash
# MotiBeamOS v4.0 Launcher
# Automatically sets DISPLAY for SSH sessions
# Enhanced with global commands, cinematic display, and robust error handling

# Set display if not already set
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "Set DISPLAY=:0 for pygame"
fi

# Run MotiBeamOS v4.0
cd ~/MotiBeam-OS
python3 motibeam_v3.py
