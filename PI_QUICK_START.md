# MotiBeamOS v3.0 - Raspberry Pi Quick Start

## Installation on Your Pi

```bash
cd ~/MotiBeam-OS
git fetch origin
git checkout claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM
python3 motibeam_v3.py
```

## What to Expect on First Run

### Console Output
```
============================================================
Starting MotiBeam OS v3.0
Multi-Vertical Ambient Computing Platform
============================================================

Core v3.0 Features:
  ✓ Settings Panel
  ✓ Ambient & Holiday Scenes
  ✓ Auto HUD Demo

Optional vertical demos available: 6/6
============================================================
Note: boot_screen.py not found - skipping boot sequence
Note: Clinical demo not found - will not appear in menu
...
✓ Core v3.0 components initialized successfully
✓ Built menu with [N] available vertical demos
```

### What Works WITHOUT Optional Demos

Even if you see "not found" messages, these **ALWAYS work**:
- ✅ Main menu
- ✅ Settings Panel (press `S`)
- ✅ Ambient Scenes (press `B`)
  - Fireplace, Aurora, Rain, Waves, Neon Sunset
  - Snowfall, Christmas Tree, Candy Cane Wave
  - Fireplace + Snow Window, Holiday Glow
- ✅ Auto HUD Demo (press `H`)

## Main Menu Keyboard Shortcuts

### Core v3 Features (Always Available)
- `S` → Settings Panel
- `B` → Ambient Scenes
- `H` → Auto HUD Demo

### Vertical Demos (If Available)
- `1` → Clinical & Wellness
- `2` → Education/Learning
- `3` → Automotive Safety
- `4` → Emergency Systems
- `5` → Enterprise/Industrial
- `6` → Security/Government
- `A` → Run All (if multiple demos available)

### Navigation
- `UP/DOWN` → Navigate vertical demos
- `ENTER` → Select highlighted item
- `ESC` → Exit application

## Scene Shortcuts (In Ambient Mode)

Once in Ambient Scenes (press `B`), use:
- `Ctrl+1` → Fireplace
- `Ctrl+2` → Aurora
- `Ctrl+3` → Snowfall
- `Ctrl+4` → Christmas Tree Glow
- `Ctrl+5` → Candy Cane Wave
- `Ctrl+6` → Fireplace + Snow Window
- `S` → Settings Panel
- `ESC` or `B` → Return to menu

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
```bash
sudo apt-get update
sudo apt-get install python3-pygame
```

### "ModuleNotFoundError: No module named 'settings_panel'"
- You're on the wrong branch!
- Run: `git checkout claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM`
- Run: `git pull origin`

### No vertical demos showing in menu
- This is **normal** if those files don't exist
- Core v3 features (S/B/H) will still work perfectly
- Check console for "Note: [demo] not found" messages

### Performance is slow
- Edit scene files to reduce particle counts
- Lower animation speed in Settings Panel
- Consider running in windowed mode (edit motibeam_v3.py line 97)

### Screen is too small/large
- Press `S` for Settings
- Go to Display section
- Adjust Screen Ratio (Auto, 16:9, 4:3)

## File Locations

**Core v3 files (required):**
- `motibeam_v3.py` - Main application
- `settings_panel.py` - Settings UI
- `vertical_auto.py` - Auto HUD
- `core/scene_manager.py` - Scene loader
- `scenes/scene_*.py` - Ambient/holiday scenes (10 files)

**Optional files:**
- `scenes/boot_screen.py`
- `scenes/clinical_demo*.py`
- `scenes/education_demo.py`
- `scenes/automotive_demo.py`
- `scenes/emergency_demo.py`
- `scenes/industrial_demo.py`
- `scenes/security_demo.py`

**Generated at runtime:**
- `config/settings.json` - Your settings (auto-created)

## Quick Test

After launching, try this sequence:
1. Press `S` → Settings Panel should open
2. Press `ESC` → Return to menu
3. Press `B` → Ambient scenes should start
4. Wait 3 seconds → Should see fireplace animation
5. Press `S` → Settings should open over the scene
6. Navigate to "Scenes" section
7. Click "Active Scene" dropdown to cycle scenes
8. Press `ESC` → Close settings, scene continues
9. Press `ESC` → Return to menu
10. Press `H` → Auto HUD demo should start
11. Wait 10 seconds → Should see speedometer, navigation, maybe collision alert
12. Press `ESC` → Return to menu
13. Press `ESC` → Exit application

If all that works → **v3.0 is fully functional!** 🎉

## Support

For full documentation, see `README_V3.md` in this directory.

**Branch:** `claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM`

**Version:** 3.0 (Pi-ready build with optional module support)
