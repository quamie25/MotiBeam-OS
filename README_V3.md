# MotiBeamOS v3.0 Upgrade Documentation

## Quick Start - Raspberry Pi Instructions

### Running on Your Pi

```bash
# Navigate to your MotiBeam-OS directory
cd ~/MotiBeam-OS

# Fetch latest changes
git fetch origin

# Checkout the v3 branch
git checkout claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM

# Run MotiBeamOS v3.0
python3 motibeam_v3.py
```

### What You'll Get

**Core v3.0 Features (Always Available):**
- ✅ Settings Panel (press `S`)
- ✅ Ambient & Holiday Scenes (press `B`)
- ✅ Auto HUD Demo (press `H`)

**Optional Vertical Demos:**
- The menu will automatically show only available demos
- If demo files are missing, v3 will still run perfectly
- Optional demos: Clinical, Education, Automotive, Emergency, Industrial, Security

### Keyboard Shortcuts

**Main Menu:**
- `S` → Settings Panel
- `B` → Ambient Scenes
- `H` → Auto HUD Demo
- `1-6` → Vertical demos (if available)
- `ESC` → Exit

---

## Overview

MotiBeamOS v3.0 is a major upgrade introducing three core features:
1. **Settings Panel** - Comprehensive configuration UI
2. **Ambient Background Scenes** - 10 beautiful ambient/holiday scenes
3. **Auto Vertical HUD** - In-car heads-up display demo

**Note:** The application is now self-contained and tolerant of missing optional modules. It will run successfully with just the core v3 features, even if no vertical demos are present.

---

## File Structure

```
MotiBeam-OS/
├── config/
│   └── settings.json              # Persistent settings storage
├── core/
│   └── scene_manager.py           # Scene discovery and management
├── scenes/
│   ├── scene_*.py                 # Existing demo scenes (unchanged)
│   ├── scene_fireplace.py         # NEW: Ambient fireplace
│   ├── scene_aurora.py            # NEW: Aurora borealis
│   ├── scene_rain.py              # NEW: Rainfall
│   ├── scene_waves.py             # NEW: Ocean waves
│   ├── scene_neon_sunset.py       # NEW: Vaporwave sunset
│   ├── scene_snowfall.py          # NEW: Gentle snowfall
│   ├── scene_christmas_tree.py    # NEW: Holiday tree with lights
│   ├── scene_candy_cane_wave.py   # NEW: Candy cane stripes
│   ├── scene_fireplace_snow_overlay.py  # NEW: Cozy fireplace + snow
│   └── scene_holiday_glow.py      # NEW: Pulsing holiday colors
├── settings_panel.py              # NEW: Settings UI module
├── vertical_auto.py               # NEW: Auto HUD demo
├── motibeam_v3.py                 # NEW: v3.0 main application
└── motibeam_app.py                # Original application (preserved)
```

---

## Phase 1: Settings Panel

### Features

**Location:** `settings_panel.py`

**Layout:**
- Left sidebar menu (280px wide)
- Right content area (dynamic controls)

**Menu Sections:**
1. **Display**
   - Brightness: Slider (0-100, default 75)
   - Screen Ratio: Dropdown [Auto, 16:9, 4:3]

2. **Visuals**
   - Theme: Dropdown [Light, Dark]
   - Animation Speed: Slider (0-100, default 50)

3. **Scenes**
   - Active Scene: Dropdown (populated from scene manager)
   - Category Filter: Dropdown [All, Ambient, Holiday]
   - Preview Window: Visual preview of selected scene

4. **Sensors**
   - Presence Detection: Toggle (default OFF)
   - Mic Sensitivity: Slider (0-100, default 60)

5. **Profiles**
   - Active Profile: Dropdown [Smart Home, Auto, Wellness, Delivery]

6. **System**
   - About: Version info (read-only)
   - Reboot: Button (placeholder)
   - Factory Reset: Button (resets to defaults)

7. **Demo Mode**
   - Enable Demo Mode: Toggle
   - Demo Profile: Dropdown [Smart Home, Auto, Wellness, Delivery]

### Controls

**Supported Control Types:**
- Toggle (on/off switch)
- Dropdown (click to cycle options)
- Slider (drag to adjust, shows value)
- Button (clickable actions)
- Read-only text
- Preview window

### Storage

**File:** `config/settings.json`

**Auto-save:** Settings automatically save on any change

**API Functions:**
```python
load_settings()                    # Load from JSON
save_settings(settings)            # Save to JSON
get_current_settings()             # Get current dict
set_scene_manager(manager)         # Connect to scene manager
init_settings_panel(screen, font)  # Initialize (optional)
render_settings_panel(screen)      # Render UI
handle_settings_events(event)      # Process events
```

### Access

**From Menu:** Press `S` or select "Settings Panel"
**From Ambient Mode:** Press `S`
**Exit:** Press `S` or `ESC`

---

## Phase 2: Ambient Background Scenes

### Scene Manager

**Location:** `core/scene_manager.py`

**Features:**
- Automatic scene discovery (scans `scenes/` for `scene_*.py`)
- Dynamic loading of scene modules
- Safe error handling
- Scene switching with initialization

**Scene Interface:**

Each scene must define:
```python
SCENE_NAME = "Human Readable Name"
SCENE_CATEGORY = "Ambient"  # or "Holiday", etc.

def init_scene(screen):
    # Initialize scene state

def update_scene(dt):
    # Update animation (dt in milliseconds)

def render_scene(screen):
    # Render to screen
```

**API Functions:**
```python
init_scene_manager(screen)         # Initialize with screen
load_all_scenes()                  # Discover and load scenes
get_scene_list()                   # Returns [(name, category), ...]
set_active_scene(name)             # Switch to scene
get_active_scene_name()            # Get current scene name
update_active_scene(dt)            # Update current scene
render_active_scene(screen)        # Render current scene
```

### Ambient Scenes (Non-Holiday)

#### 1. Fireplace
**File:** `scene_fireplace.py`
**Category:** Ambient
**Description:** Warm orange gradient with animated flickering flames and glowing embers
**Features:**
- Layered flame particles (red → yellow → white core)
- Floating embers with drift
- Smooth particle lifecycle

#### 2. Aurora
**File:** `scene_aurora.py`
**Category:** Ambient
**Description:** Dark sky with moving aurora borealis bands
**Features:**
- Multiple wavy colored bands
- Twinkling stars
- Smooth sine-wave motion
- Green, blue, purple, cyan colors

#### 3. Rain
**File:** `scene_rain.py`
**Category:** Ambient
**Description:** Bluish background with falling raindrops and splash effects
**Features:**
- Vertical raindrop streaks
- Varying speeds and sizes
- Splash animations on impact
- Subtle fog/mist overlay

#### 4. Waves
**File:** `scene_waves.py`
**Category:** Ambient
**Description:** Horizontal ocean wave lines with sine motion
**Features:**
- 3 wave layers with different speeds
- Foam effects on crests
- Blue gradient ocean background
- Parallax depth effect

#### 5. Neon Sunset
**File:** `scene_neon_sunset.py`
**Category:** Ambient
**Description:** Vaporwave/retro sunset with perspective grid
**Features:**
- Purple/pink/orange gradient sky
- Glowing sun with layers
- Perspective grid floor
- Horizontal scanlines
- Slow drift animation

#### 6. Snowfall
**File:** `scene_snowfall.py`
**Category:** Holiday (can be Ambient)
**Description:** Gentle snowfall with parallax effect
**Features:**
- 200+ snowflakes with varying sizes
- Parallax: larger flakes fall faster
- Gentle horizontal drift
- Sparkle highlights on larger flakes

### Holiday Scenes Pack

#### 7. Christmas Tree Glow
**File:** `scene_christmas_tree.py`
**Category:** Holiday
**Description:** Stylized tree with pulsing ornaments and twinkling lights
**Features:**
- Layered triangular tree structure
- Colorful ornaments with glow effects
- Multi-colored twinkling light strings
- Glowing star on top
- Dark night background

#### 8. Candy Cane Wave
**File:** `scene_candy_cane_wave.py`
**Category:** Holiday
**Description:** Red and white diagonal stripes with wave motion
**Features:**
- Scrolling candy cane stripes
- Sine wave distortion
- Sparkle effects
- Bright, festive colors

#### 9. Fireplace + Snow Window
**File:** `scene_fireplace_snow_overlay.py`
**Category:** Holiday
**Description:** Combines fireplace (bottom) with snowy window view (top)
**Features:**
- Split screen: window above, fireplace below
- Window frame with panes
- Snowfall outside window
- Warm fireplace glow
- "Cozy inside, snow outside" atmosphere

#### 10. Holiday Glow
**File:** `scene_holiday_glow.py`
**Category:** Holiday
**Description:** Soft pulsing gradients in festive colors
**Features:**
- Multiple glowing orbs (red, green, gold)
- Very slow, gentle pulsing
- Floating particles
- Ideal for low-motion ambient display
- Color cycling overlay

### Scene Integration

**Settings Panel Integration:**
- Active Scene dropdown populated from scene manager
- Category Filter: [All, Ambient, Holiday]
- Changing scene immediately switches display
- Scene selection saved to `settings.json`

**Keyboard Shortcuts:**

From main menu:
- `B` → Enter Ambient Scenes mode

In Ambient Mode:
- `Ctrl+1` → Fireplace
- `Ctrl+2` → Aurora
- `Ctrl+3` → Snowfall
- `Ctrl+4` → Christmas Tree Glow
- `Ctrl+5` → Candy Cane Wave
- `Ctrl+6` → Fireplace + Snow Window
- `S` → Open Settings
- `ESC` or `B` → Exit to menu

---

## Phase 3: Auto Vertical (HUD Demo)

### Overview

**Location:** `vertical_auto.py`

**Purpose:** Simulates an in-car heads-up display for automotive licensing demos

**Activation:**
- Enable "Demo Mode" in Settings
- Set "Demo Profile" to "Auto"
- Enter Ambient Scenes mode

**Alternative:** Direct keyboard shortcut `Ctrl+A` (when implemented in main loop)

### Features

#### 1. Speedometer
- Digital numeric speed readout (e.g., "32 mph")
- Circular arc that fills with speed (0-60 mph range)
- Smooth acceleration/deceleration animation

#### 2. Turn-by-Turn Navigation
- Text banner with instructions
  - "Turn right in 500 ft"
  - "Turn right in 300 ft"
  - "Turn right NOW"
  - "Continue straight"
  - etc.
- Directional arrow indicator (left/right)
- Distance countdown
- Semi-transparent background panel

#### 3. Collision Alert
- Full-screen red border flash
- Large "BRAKE!" text
- Pulsing animation (no seizure-inducing strobe)
- Triggers during timeline events

#### 4. Night Drive Mode
- Neon blue/cyan HUD elements
- Dark night sky background with stars
- "NIGHT DRIVE" indicator
- High contrast for visibility

### Simulated Drive Timeline

**Duration:** ~30 seconds looping

**Timeline Events:**
```
0s:   Speed → 35 mph, Turn instruction
3s:   Update turn distance
5s:   Slow to 25 mph (approaching turn)
7.5s: "Turn right NOW"
8.5s: Speed up to 40 mph
12s:  Speed → 45 mph
14s:  COLLISION ALERT triggered
15s:  Emergency brake → 20 mph
16s:  Alert cleared
17s:  Resume → 35 mph
19s:  New turn instruction (left)
...
```

### API Functions

```python
init_auto_vertical(screen)         # Initialize HUD
update_auto_vertical(dt)           # Update state (dt in ms)
render_auto_vertical(screen)       # Render HUD
```

### Controls

- `ESC` → Exit Auto HUD mode

---

## Main Application (motibeam_v3.py)

### Launch

```bash
python3 motibeam_v3.py
```

### Boot Sequence

1. Boot screen (5 seconds)
2. Main menu

### Main Menu Options

**Vertical Demos (Original):**
- `1` → Clinical & Wellness
- `2` → Education/Learning
- `3` → Automotive Safety
- `4` → Emergency Systems
- `5` → Enterprise/Industrial
- `6` → Security/Government
- `A` → Run All Demos

**New v3.0 Features:**
- `S` → Settings Panel
- `B` → Ambient Background Scenes

**Navigation:**
- `UP/DOWN` arrows → Navigate menu
- `ENTER` → Select highlighted item
- `ESC` → Exit application

### Modes

1. **Demo Mode:** Runs existing vertical demos (unchanged)
2. **Settings Mode:** Full settings panel UI
3. **Ambient Mode:** Display ambient/holiday scenes
4. **Auto HUD Mode:** Automotive HUD demo (triggered by Demo Mode settings)

---

## Code Style & Architecture

### Design Principles

✅ **Modular:** Each component is self-contained
✅ **Clean:** Clear function names, well-commented
✅ **Maintainable:** Simple architecture, no "God files"
✅ **Efficient:** Optimized for Raspberry Pi-level hardware
✅ **Pygame-only:** No external dependencies

### Scene Convention

- Scene files: `scene_*.py`
- Function-based interface (not classes)
- Required: `SCENE_NAME`, `SCENE_CATEGORY`, `init_scene()`, `update_scene()`, `render_scene()`
- Delta time: milliseconds (consistent across all scenes)

### Settings Convention

- JSON storage in `config/settings.json`
- Auto-save on any change
- Dictionary structure mirroring menu sections
- Defaults provided if file missing

### Color Palette

**HUD Elements:**
- Primary: Cyan (0, 220, 255)
- Secondary: Light blue (100, 180, 255)
- Warning: Yellow (255, 200, 0)
- Danger: Red (255, 60, 60)

**Ambient Scenes:**
- Use warm/cool gradients
- Avoid harsh whites in dark room contexts
- Smooth color transitions

---

## Testing

### Quick Test Checklist

- [ ] Boot screen displays correctly
- [ ] Main menu navigation works (UP/DOWN, number keys)
- [ ] All 6 vertical demos launch and exit cleanly
- [ ] Settings panel opens (press `S`)
- [ ] Settings controls work (toggle, dropdown, slider)
- [ ] Settings save/load from JSON
- [ ] Ambient scenes mode opens (press `B`)
- [ ] All 10 scenes load and render without errors
- [ ] Scene switching works (via settings or shortcuts)
- [ ] Auto HUD activates when Demo Mode enabled + Auto profile
- [ ] Auto HUD timeline plays through correctly
- [ ] Can return to menu from all modes

### Debug Output

The application prints status messages:
```
Loaded scene: Fireplace (Ambient)
Loaded scene: Aurora (Ambient)
...
Switched to scene: Fireplace
Opening settings panel...
Settings saved.
Entering ambient scenes mode...
```

---

## Keyboard Reference Card

### Main Menu
| Key | Action |
|-----|--------|
| `1-6` | Select vertical demo |
| `A` | Run all demos |
| `S` | Open settings |
| `B` | Enter ambient scenes |
| `UP/DOWN` | Navigate menu |
| `ENTER` | Select item |
| `ESC` | Exit application |

### Ambient Mode
| Key | Action |
|-----|--------|
| `Ctrl+1` | Fireplace scene |
| `Ctrl+2` | Aurora scene |
| `Ctrl+3` | Snowfall scene |
| `Ctrl+4` | Christmas Tree scene |
| `Ctrl+5` | Candy Cane Wave scene |
| `Ctrl+6` | Fireplace + Snow scene |
| `S` | Open settings |
| `B` or `ESC` | Exit to menu |

### Settings Panel
| Key | Action |
|-----|--------|
| `Mouse` | Click controls |
| `Drag` | Adjust sliders |
| `S` or `ESC` | Close settings |

### Auto HUD Mode
| Key | Action |
|-----|--------|
| `ESC` | Exit to menu |

---

## Migration from v2.x

**No breaking changes** - All existing functionality preserved:
- Original demo scenes unchanged
- `motibeam_app.py` still works as before
- New features are additive

**To use v3.0:**
```bash
python3 motibeam_v3.py   # New v3.0 app with all features
```

**To use v2.x:**
```bash
python3 motibeam_app.py  # Original app (still works)
```

---

## Future Enhancements

Potential additions for v3.1+:
- Profile-specific behaviors (Smart Home, Wellness, Delivery modes)
- Scene playlist/rotation
- Sensor integration (actual presence detection, mic input)
- More ambient scenes (forest, space, underwater, etc.)
- Custom scene creator tool
- Web-based settings interface
- Multi-display support

---

## Optional Modules

MotiBeamOS v3.0 is designed to be resilient and will run successfully even if optional modules are missing.

### Required Modules (Core v3)

These **must** be present for v3 to run:
- `settings_panel.py`
- `core/scene_manager.py`
- `vertical_auto.py`
- Scene files: `scenes/scene_*.py` (10 ambient/holiday scenes)

### Optional Modules (Vertical Demos)

These are **optional** and can be added later:
- `scenes/boot_screen.py` - Boot sequence (fallback: simple splash)
- `scenes/clinical_demo.py` or `scenes/clinical_demo_enhanced.py`
- `scenes/education_demo.py`
- `scenes/automotive_demo.py`
- `scenes/emergency_demo.py`
- `scenes/industrial_demo.py`
- `scenes/security_demo.py`

**Behavior:**
- If optional modules are missing, v3 will print a note and continue
- Menu will only show available demos
- Core v3 features (Settings, Scenes, Auto HUD) always work

---

## Troubleshooting

**Issue:** ModuleNotFoundError for core modules
- Ensure you're on the correct branch: `claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM`
- Run `git pull origin` to get latest changes
- Verify these files exist: `settings_panel.py`, `core/scene_manager.py`, `vertical_auto.py`

**Issue:** Scenes not loading
- Check that `scenes/scene_*.py` files exist (fireplace, aurora, rain, etc.)
- Look for error messages in console
- Verify scene modules have required interface (SCENE_NAME, SCENE_CATEGORY, init/update/render)

**Issue:** Settings not saving
- Check `config/` directory exists and is writable
- Verify `settings.json` is valid JSON
- File will be auto-created with defaults if missing

**Issue:** Performance issues
- Reduce number of particles in scenes (edit scene files)
- Lower animation speed in Settings Panel
- Check system resources (Raspberry Pi may need optimization)

**Issue:** Auto HUD not activating
- Verify Demo Mode is enabled in Settings Panel
- Check Demo Profile is set to "Auto"
- Or press `H` from main menu for direct access

**Issue:** Optional demos not showing
- This is normal if those files don't exist in your branch
- Check console output for "Note: [demo] not found" messages
- Core v3 features will still work perfectly

---

## Credits

**MotiBeamOS v3.0**
- Multi-Vertical Ambient Computing Platform
- Developed with Pygame
- Optimized for Raspberry Pi and projection displays

**Components:**
- Phase 1: Settings Panel
- Phase 2: Ambient Scenes (6 ambient + 4 holiday)
- Phase 3: Auto Vertical HUD

**License:** See LICENSE file

---

## Contact & Support

For issues, feature requests, or contributions, please refer to the project repository.

**Version:** 3.0
**Release Date:** 2025-11-28
