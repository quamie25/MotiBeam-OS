# Display Issues - "offscreen" Driver Fix

## 🎯 The Problem

Your console shows:
```
[DEBUG] Display driver: offscreen
```

This means pygame is running in **headless/offscreen mode**:
- ❌ No visible window
- ❌ No display output
- ❌ No keyboard/mouse input
- ✅ Code runs but everything is "virtual"

---

## 🔍 Why This Happens

**You're likely:**
1. SSH'd into the Pi without X11 forwarding
2. Running in a terminal without DISPLAY set
3. No X server is running
4. Display not accessible to your user

---

## ✅ Solutions (Try in Order)

### Solution 1: Run Directly on Pi Desktop (BEST)

**If your Pi has a monitor connected:**

1. Go to the physical Raspberry Pi
2. Make sure desktop is running (Pixel/LXDE)
3. Open terminal **on the Pi desktop**
4. Run:
```bash
cd ~/MotiBeam-OS
python3 motibeam_v3.py
```

**Expected output:**
```
[DEBUG] Display driver: x11
```
✅ Window appears!
✅ Keyboard works!

---

### Solution 2: Export DISPLAY Variable

**If using SSH but Pi has a display:**

```bash
# Tell pygame to use the main display
export DISPLAY=:0

# Now run
cd ~/MotiBeam-OS
python3 motibeam_v3.py
```

**Check if it worked:**
- Console should show `[DEBUG] Display driver: x11`
- Window should appear on Pi's monitor

---

### Solution 3: SSH with X11 Forwarding

**If SSH from Mac/Linux with X server:**

```bash
# On your computer (not on Pi):
ssh -X motibeam@motibeamOS

# Or if that doesn't work:
ssh -Y motibeam@motibeamOS

# Then on Pi:
cd ~/MotiBeam-OS
python3 motibeam_v3.py
```

**Window will appear on YOUR computer, not the Pi!**

**Requirements:**
- Mac: Install XQuartz
- Linux: X11 already installed
- Windows: Install VcXsrv or Xming

---

### Solution 4: Virtual Framebuffer (Headless)

**For truly headless operation (testing/automation):**

```bash
# Install virtual framebuffer
sudo apt-get update
sudo apt-get install xvfb

# Run with virtual display
xvfb-run python3 motibeam_v3.py
```

**Note:** Still no visible window, but driver will be "x11" instead of "offscreen"

---

## 🧪 Diagnostic Commands

### Check if X server is running:
```bash
echo $DISPLAY
# Should show: :0 or :0.0
# If empty, X might not be running
```

### Check display driver manually:
```bash
python3 -c "import pygame; pygame.init(); print(pygame.display.get_driver())"
```

Expected results:
- ✅ `x11` - Display is working!
- ❌ `offscreen` - No display available

### List available drivers:
```bash
python3 -c "import pygame; print(pygame.display.get_driver())"
```

### Check if desktop is running:
```bash
ps aux | grep -i "X\|wayland"
```

If you see Xorg or X11 process → Desktop is running

---

## 📋 Step-by-Step: Desktop Terminal Method

**This is the EASIEST way:**

1. **On the Pi (physically or via VNC):**
   - Click the Raspberry Pi menu
   - Accessories → Terminal
   - You'll see a terminal window

2. **In that terminal:**
```bash
cd ~/MotiBeam-OS
python3 motibeam_v3.py
```

3. **Expected:**
   - Console shows: `[DEBUG] Display driver: x11`
   - Pygame window appears
   - You can click and type in it

---

## 🎮 Expected Working Output

```
pygame 2.6.1 (SDL 2.32.4, Python 3.13.5)
...
[DEBUG] Creating WINDOWED display (800x600)
[DEBUG] Screen created: 800x600
[DEBUG] Display driver: x11          ← THIS IS WHAT YOU WANT!
...
[DEBUG] Starting main menu loop...
[DEBUG] Menu loop frame 1
```

Then press `S`:
```
[DEBUG] Key pressed: 115 (unicode: 's')
[DEBUG] S pressed -> Open Settings Panel
```

---

## ❌ Current Broken Output

```
[DEBUG] Display driver: offscreen    ← THE PROBLEM
...
[DEBUG] Menu loop frame 1
[DEBUG] Menu loop frame 31
... (loops forever, no input)
```

---

## 🔧 Quick Fixes Summary

| Situation | Solution | Command |
|-----------|----------|---------|
| Pi with monitor | Run from desktop terminal | Open terminal on Pi |
| SSH with display | Export DISPLAY | `export DISPLAY=:0` |
| SSH from Mac/Linux | X11 forwarding | `ssh -X user@host` |
| Headless testing | Virtual framebuffer | `xvfb-run python3 ...` |

---

## 🎯 What To Do Now

1. **Determine your situation:**
   - Do you have a monitor connected to the Pi?
   - Are you SSH'd in?
   - Do you need a GUI or just testing?

2. **Choose the right solution above**

3. **Run the updated code:**
```bash
cd ~/MotiBeam-OS
git pull origin claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM
python3 motibeam_v3.py
```

4. **Look for the warning:**
   - If you see the ⚠️ warning, you're still in offscreen mode
   - Follow the solutions printed in the warning

5. **Success = No warning + x11 driver:**
```
[DEBUG] Display driver: x11
```

---

## 📞 Still Not Working?

**Share this info:**
1. How are you connecting? (physical Pi, SSH, VNC, etc.)
2. Output of: `echo $DISPLAY`
3. Output of: `ps aux | grep X`
4. Full console output from motibeam_v3.py

---

**Branch:** `claude/motibeamos-v3-upgrade-01RZdhsAnZcKJT5itvLLR7xM`

**Commit:** 3b8d0ef - "Add detection and warning for offscreen display driver"

---

## 🎉 Once You Get "x11" Driver

The app will work perfectly:
- ✅ Window visible
- ✅ Keyboard input works
- ✅ Mouse works
- ✅ All features accessible (S/B/H)

Just get that display driver from "offscreen" to "x11"! 🚀
