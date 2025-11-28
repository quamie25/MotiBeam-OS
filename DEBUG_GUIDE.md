# Debug Logging Added - Main Menu Troubleshooting

## What Was Added

I've added comprehensive debug logging to help diagnose why the main menu isn't appearing on screen.

## Changes Made

### File: `motibeam_v3.py`

**Debug messages added:**

1. **Main `run()` method:**
   - `[DEBUG] Entering main run() loop` - When run() starts
   - `[DEBUG] Boot screen complete, entering main loop` - After boot screen
   - `[DEBUG] Main loop iteration, self.running = X` - Each main loop iteration
   - `[DEBUG] Menu returned selection: X, self.running = Y` - After menu returns
   - `[DEBUG] self.running is False, breaking main loop` - If exiting

2. **`show_main_menu()` method:**
   - `[DEBUG] Entering show_main_menu()` - When menu function starts
   - `[DEBUG] self.running = X` - Current running state
   - `[DEBUG] Starting main menu loop...` - Before entering render loop
   - `[DEBUG] Menu loop frame N` - Every 30 frames (once per second)
   - `[DEBUG] Key pressed: X (unicode: 'Y')` - Every keypress
   - `[DEBUG] S pressed -> Open Settings Panel` - S key action
   - `[DEBUG] B pressed -> Enter Ambient Scenes` - B key action
   - `[DEBUG] H pressed -> Enter Auto HUD Demo` - H key action
   - `[DEBUG] ESC pressed -> Exit application` - ESC key action
   - `[DEBUG] QUIT event received` - Window close event
   - `[DEBUG] Exiting main menu, selected = X` - When leaving menu

## How to Run with Debug

```bash
cd ~/MotiBeam-OS
git fetch origin
git pull origin claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM
python3 motibeam_v3.py
```

## What to Look For

### Expected Console Output (Success Case)

```
============================================================
Starting MotiBeam OS v3.0
...
✓ Core v3.0 components initialized successfully
✓ Built menu with 6 available vertical demos
Starting BootScreen...
5 seconds elapsed, exiting...
Scene complete.
Boot sequence complete, entering main menu...

[DEBUG] Entering main run() loop
[DEBUG] Boot screen complete, entering main loop
[DEBUG] Main loop iteration, self.running = True
[DEBUG] Entering show_main_menu()
[DEBUG] self.running = True
[DEBUG] Starting main menu loop...
[DEBUG] Menu loop frame 1
[DEBUG] Menu loop frame 31
[DEBUG] Menu loop frame 61
... (continues every second)
```

**At this point, you should see the main menu on screen!**

When you press a key:
```
[DEBUG] Key pressed: 115 (unicode: 's')
[DEBUG] S pressed -> Open Settings Panel
[DEBUG] Exiting main menu, selected = settings
[DEBUG] Menu returned selection: settings, self.running = True
Opening settings panel...
```

### Diagnostic Scenarios

#### Scenario 1: Menu loop never starts
```
Boot sequence complete, entering main menu...
[DEBUG] Entering main run() loop
[DEBUG] Boot screen complete, entering main loop
[DEBUG] Main loop iteration, self.running = True
[DEBUG] Entering show_main_menu()
[DEBUG] self.running = False
```
**Problem:** `self.running` is False when entering menu
**Likely cause:** Something is setting running to False

#### Scenario 2: Menu loop starts but exits immediately
```
[DEBUG] Starting main menu loop...
[DEBUG] Menu loop frame 1
[DEBUG] Exiting main menu, selected = None
```
**Problem:** Loop runs once then exits
**Likely cause:** `menu_running` or `self.running` becomes False

#### Scenario 3: Menu loop runs but no keypresses detected
```
[DEBUG] Menu loop frame 1
[DEBUG] Menu loop frame 31
[DEBUG] Menu loop frame 61
... (no key press messages when you press keys)
```
**Problem:** Keyboard input not reaching the app
**Possible causes:**
- Another window has focus
- Pygame input not working
- SSH/remote session issue

#### Scenario 4: Keypresses detected but nothing happens
```
[DEBUG] Menu loop frame 31
[DEBUG] Key pressed: 115 (unicode: 's')
... (no "S pressed" message)
```
**Problem:** Key code not matching expected value
**Solution:** Check what key code is actually being sent

## Testing Steps

1. **Run the app:**
   ```bash
   python3 motibeam_v3.py
   ```

2. **Wait for boot screen to complete** (5 seconds)

3. **Check console for:**
   - `[DEBUG] Starting main menu loop...`
   - `[DEBUG] Menu loop frame 1` (and continuing)

4. **Check screen for:**
   - Large "MotiBeam OS v3.0" logo
   - "CORE FEATURES:" section
   - S/B/H options listed
   - "VERTICAL DEMOS:" section (if available)

5. **Press S key:**
   - Console should show: `[DEBUG] Key pressed: 115 (unicode: 's')`
   - Console should show: `[DEBUG] S pressed -> Open Settings Panel`
   - Settings panel should appear on screen

6. **Press ESC to exit:**
   - Console should show: `[DEBUG] ESC pressed -> Exit application`
   - App should exit cleanly

## Common Issues & Solutions

### Issue: No `[DEBUG] Entering main run() loop` message
**Cause:** `run()` method not being called
**Fix:** Check if there's an exception in `__init__`

### Issue: No `[DEBUG] Starting main menu loop...` message
**Cause:** `show_main_menu()` not being called or exiting early
**Fix:** Check the main loop condition

### Issue: Frame messages stop after a few iterations
**Cause:** Loop is exiting unexpectedly
**Fix:** Check for events that might set `running = False`

### Issue: No key press messages when pressing keys
**Cause:** Window doesn't have focus or keyboard not working
**Fix:**
- Click on the window to give it focus
- Try running in windowed mode instead of fullscreen
- Check if running over SSH (may not have display access)

### Issue: Wrong key codes
**Cause:** Keyboard layout or pygame key mapping issue
**Fix:** Note what key code is actually received and update code

## Next Steps

After you run this on your Pi, please share:

1. **Complete console output** - Especially all `[DEBUG]` lines
2. **What you see on screen** - Blank? Menu? Something else?
3. **What happens when you press keys** - Any debug messages?

This will tell us exactly where the problem is and how to fix it.

## Removing Debug Output (Later)

Once we've identified and fixed the issue, we can:

1. Remove or comment out all lines starting with `print("[DEBUG]"`
2. Or keep them but add a `DEBUG = False` flag at the top
3. Or redirect them to a log file instead of console

For now, leave them in - they're helpful for troubleshooting!

---

**Branch:** `claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM`
**Commit:** d1fa3a6 "Add comprehensive debug logging for main menu troubleshooting"
