#!/usr/bin/env python3
"""
PATENT MAPPING (Internal Design Note):
- Aligns with filed MotiBeam patents for:
  - Universal Ambient Projection System (multi-vertical architecture)
  - Cross-environment projection capabilities (Claims 11-13, 20, 23-24)
Relevant claims: 1, 11, 12, 13, 20, 23, 24.
This is an architectural implementation, not a legal opinion.

PatentVerticalConfig - Phase 1 Vertical Ordering Configuration
SINGLE SOURCE OF TRUTH for patent-aligned vertical demo ordering.
"""

# Import vertical demos (with graceful fallback to None if not available)
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


# PATENT-ALIGNED VERTICAL CONFIGURATION
# This is the SINGLE SOURCE OF TRUTH controlling:
# - Main menu display order (Patent Claim 1: ambient_os interface)
# - TAB cycling sequence (Patent Claim 24: seamless transitions)
# - Demo mode rotation order (Patent Claim 20: multi-environment)
# - Cross-vertical integration (Patent Claims 11-13)
PATENT_VERTICALS = [
    ("1", "Smart Home", None),  # Placeholder - future smart home dashboard
    ("2", "Auto HUD", AutomotiveDemo),
    ("3", "Wellness", ClinicalWellnessEnhanced),
    ("4", "Education", EducationDemo),
    ("5", "Security", SecurityDemo),
    ("6", "Emergency", EmergencyDemo),
    ("7", "Industrial", IndustrialDemo),
]

# Filter out None entries (unavailable verticals)
# Maintains graceful degradation principle
PATENT_VERTICALS = [(k, n, c) for k, n, c in PATENT_VERTICALS if c is not None]


# Vertical display metadata (patent-aligned)
# Each vertical represents a distinct "environment" per Claims 11-13
PATENT_VERTICAL_METADATA = {
    "Smart Home": {
        "symbol": "[🏠]",
        "color": (80, 255, 120),  # Green
        "description": "Smart home dashboard and ambient control",
        "patent_environment": "residential",  # Patent Claim 11
    },
    "Auto HUD": {
        "symbol": "[🚗]",
        "color": (255, 255, 100),  # Yellow
        "description": "Automotive heads-up display projection",
        "patent_environment": "automotive",  # Patent Claim 12
    },
    "Wellness": {
        "symbol": "[+]",
        "color": (80, 255, 120),  # Green
        "description": "Clinical & wellness monitoring projection",
        "patent_environment": "clinical",  # Patent Claims 14-17
    },
    "Education": {
        "symbol": "[#]",
        "color": (200, 100, 255),  # Purple
        "description": "Education and learning platform",
        "patent_environment": "educational",  # Patent Claim 13
    },
    "Security": {
        "symbol": "[*]",
        "color": (255, 180, 0),  # Orange
        "description": "Security & government systems projection",
        "patent_environment": "security",  # Patent Claim 11
    },
    "Emergency": {
        "symbol": "[!]",
        "color": (255, 80, 80),  # Red
        "description": "Emergency response and SOS systems",
        "patent_environment": "emergency",  # Patent Claims 18-19
    },
    "Industrial": {
        "symbol": "[=]",
        "color": (0, 255, 180),  # Cyan
        "description": "Enterprise & industrial process control",
        "patent_environment": "industrial",  # Patent Claim 13
    },
}


def get_patent_verticals():
    """
    Get list of available patent-aligned vertical demos

    Returns:
        list: Tuples of (key, name, class) for each vertical

    Phase 1: Return configured verticals
    Phase 2: Dynamic vertical loading based on hardware/permissions
    """
    return PATENT_VERTICALS


def get_vertical_by_patent_key(key):
    """
    Get vertical demo by patent configuration key

    Args:
        key: str - Numeric key (e.g., "1", "2", "3")

    Returns:
        tuple or None: (key, name, class) if found

    Used by patent input manager for direct vertical access
    """
    for k, name, cls in PATENT_VERTICALS:
        if k == key:
            return (k, name, cls)
    return None


def get_patent_vertical_metadata(name):
    """
    Get patent-aligned metadata for a vertical

    Args:
        name: str - Vertical name (e.g., "Wellness", "Auto HUD")

    Returns:
        dict: Metadata including symbol, color, description, environment

    Includes patent environment classification per Claims 11-17
    """
    return PATENT_VERTICAL_METADATA.get(name, {
        "symbol": "[?]",
        "color": (150, 150, 150),
        "description": "Unknown vertical",
        "patent_environment": "general",
    })


def get_next_vertical(current_name):
    """
    Get next vertical in patent cycling order

    Args:
        current_name: str - Current vertical name

    Returns:
        tuple or None: (key, name, class) of next vertical

    Used by patent input manager for TAB cycling (Claim 24)
    Phase 1: Simple sequential cycling
    Phase 2: Smart cycling based on context/user preferences
    """
    if not PATENT_VERTICALS:
        return None

    # Find current vertical index
    current_index = -1
    for i, (k, name, cls) in enumerate(PATENT_VERTICALS):
        if name == current_name:
            current_index = i
            break

    # If not found or at end, cycle to first
    if current_index == -1 or current_index >= len(PATENT_VERTICALS) - 1:
        return PATENT_VERTICALS[0]
    else:
        return PATENT_VERTICALS[current_index + 1]


def get_vertical_environment_type(vertical_name):
    """
    Get patent environment classification for a vertical

    Args:
        vertical_name: str - Name of vertical

    Returns:
        str: Environment type (residential, automotive, clinical, etc.)

    Maps to patent Claims 11-17 environment classifications
    """
    metadata = get_patent_vertical_metadata(vertical_name)
    return metadata.get("patent_environment", "general")


def validate_vertical_configuration():
    """
    Validate patent vertical configuration

    Returns:
        tuple: (is_valid: bool, issues: list)

    Phase 1: Basic validation
    Phase 2: Deep validation including class compatibility
    """
    issues = []

    # Check for duplicate keys
    keys = [k for k, n, c in PATENT_VERTICALS]
    if len(keys) != len(set(keys)):
        issues.append("Duplicate keys found in PATENT_VERTICALS")

    # Check for duplicate names
    names = [n for k, n, c in PATENT_VERTICALS]
    if len(names) != len(set(names)):
        issues.append("Duplicate names found in PATENT_VERTICALS")

    # Check that all verticals have metadata
    for k, name, cls in PATENT_VERTICALS:
        if name not in PATENT_VERTICAL_METADATA:
            issues.append(f"Missing metadata for vertical: {name}")

    is_valid = len(issues) == 0
    return (is_valid, issues)


# Validate configuration on module load
_is_valid, _issues = validate_vertical_configuration()
if not _is_valid:
    print("[PatentVerticalConfig] WARNING: Configuration issues detected:")
    for issue in _issues:
        print(f"  - {issue}")
else:
    print(f"[PatentVerticalConfig] ✓ Configuration valid ({len(PATENT_VERTICALS)} verticals)")
