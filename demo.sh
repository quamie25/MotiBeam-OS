#!/bin/bash
###############################################################################
# MotiBeam Weekend Demos - Master Launcher
# Usage: ./demo.sh [vertical] [duration]
# Example: ./demo.sh clinical 60
###############################################################################

# Activate virtual environment
source ~/motibeam-env/bin/activate

# Change to MotiBeam-OS directory
cd ~/MotiBeam-OS

# Default duration (seconds)
DURATION=30

# Parse arguments
VERTICAL=$1
if [ -n "$2" ]; then
    DURATION=$2
fi

# Function to run a demo
run_demo() {
    echo "========================================="
    echo "🎬 MotiBeam Demo: $1"
    echo "========================================="
    python3 scenes/$2 "$DURATION"
}

# Run specific vertical or all
case "$VERTICAL" in
    clinical|1)
        run_demo "Clinical & Wellness" "clinical_demo.py"
        ;;
    automotive|2)
        run_demo "Automotive Safety" "automotive_demo.py"
        ;;
    emergency|3)
        run_demo "Emergency/Maritime/Aviation" "emergency_demo.py"
        ;;
    industrial|4)
        run_demo "Enterprise/Industrial" "industrial_demo.py"
        ;;
    security|5)
        run_demo "Security/Government" "security_demo.py"
        ;;
    education|6)
        run_demo "Education/Learning" "education_demo.py"
        ;;
    all|*)
        echo "🎬 Running ALL 6 Vertical Demos ($DURATION seconds each)"
        echo "========================================="
        run_demo "Clinical & Wellness" "clinical_demo.py"
        run_demo "Automotive Safety" "automotive_demo.py"
        run_demo "Emergency/Maritime/Aviation" "emergency_demo.py"
        run_demo "Enterprise/Industrial" "industrial_demo.py"
        run_demo "Security/Government" "security_demo.py"
        run_demo "Education/Learning" "education_demo.py"
        echo "========================================="
        echo "✅ All demos complete!"
        ;;
esac
