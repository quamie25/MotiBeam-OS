#!/usr/bin/env python3
"""
MotiBeamOS v4.0 - Vertical Configuration
SINGLE SOURCE OF TRUTH for vertical demo ordering
"""

# Import vertical demos (with fallback to None if not available)
try:
    from clinical_demo_enhanced import ClinicalWellnessEnhanced
except ImportError:
    try:
        from clinical_demo import ClinicalDemo as ClinicalWellnessEnhanced
    except ImportError:
        ClinicalWellnessEnhanced = None

try:
    from automotive_demo import AutomotiveDemo
except ImportError:
    AutomotiveDemo = None

try:
    from education_demo import EducationDemo
except ImportError:
    EducationDemo = None

try:
    from security_demo import SecurityDemo
except ImportError:
    SecurityDemo = None

try:
    from emergency_demo import EmergencyDemo
except ImportError:
    EmergencyDemo = None

try:
    from industrial_demo import IndustrialDemo
except ImportError:
    IndustrialDemo = None


# SINGLE SOURCE OF TRUTH - Reorder this array to change menu order
# This controls:
# - Main menu display order
# - TAB cycling sequence
# - Demo mode rotation order
VERTICAL_DEMOS = [
    ("1", "Smart Home", None),  # Placeholder for future Smart Home vertical
    ("2", "Auto HUD", AutomotiveDemo),
    ("3", "Wellness", ClinicalWellnessEnhanced),
    ("4", "Education", EducationDemo),
    ("5", "Security", SecurityDemo),
    ("6", "Emergency", EmergencyDemo),
    ("7", "Industrial", IndustrialDemo),
]

# Filter out None entries (unavailable verticals)
VERTICAL_DEMOS = [(k, n, c) for k, n, c in VERTICAL_DEMOS if c is not None]


# Vertical display metadata
VERTICAL_METADATA = {
    "Smart Home": {
        "symbol": "[🏠]",
        "color": (80, 255, 120),  # Green
        "description": "Smart home dashboard and control"
    },
    "Auto HUD": {
        "symbol": "[🚗]",
        "color": (255, 255, 100),  # Yellow
        "description": "Automotive heads-up display"
    },
    "Wellness": {
        "symbol": "[+]",
        "color": (80, 255, 120),  # Green
        "description": "Clinical & wellness monitoring"
    },
    "Education": {
        "symbol": "[#]",
        "color": (200, 100, 255),  # Purple
        "description": "Education and learning platform"
    },
    "Security": {
        "symbol": "[*]",
        "color": (255, 180, 0),  # Orange
        "description": "Security & government systems"
    },
    "Emergency": {
        "symbol": "[!]",
        "color": (255, 80, 80),  # Red
        "description": "Emergency response systems"
    },
    "Industrial": {
        "symbol": "[=]",
        "color": (0, 255, 180),  # Cyan
        "description": "Enterprise & industrial control"
    },
}


def get_available_verticals():
    """Get list of available vertical demos"""
    return VERTICAL_DEMOS


def get_vertical_by_key(key):
    """Get vertical demo by key number"""
    for k, name, cls in VERTICAL_DEMOS:
        if k == key:
            return (k, name, cls)
    return None


def get_vertical_metadata(name):
    """Get metadata for a vertical"""
    return VERTICAL_METADATA.get(name, {
        "symbol": "[?]",
        "color": (150, 150, 150),
        "description": "Unknown vertical"
    })
