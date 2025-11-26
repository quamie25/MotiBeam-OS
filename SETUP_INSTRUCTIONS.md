# MotiBeam OS - Final Setup Instructions

## Quick Setup (Do this on your Pi)

### Step 1: Get the Latest Code

Your Pi still has old scene files. Pull the latest branch:

```bash
cd ~/MotiBeam-OS

# Backup any local changes (optional)
git stash

# Get the absolute latest code
git fetch origin claude/fix-motibeam-autostart-01EYvCc5T4Bu3Ufi7or8wuZr
git reset --hard origin/claude/fix-motibeam-autostart-01EYvCc5T4Bu3Ufi7or8wuZr
```

### Step 2: Verify Files Are Updated

```bash
# Should show "from scene_base import MotiBeamScene" on line 9 (NOT "from .scene_base")
head -20 scenes/education_demo.py

# Should exist
ls -la scenes/__init__.py

# Should exist and be updated
ls -la scripts/run_motibeam_with_log.sh
```

### Step 3: Update the Systemd Service File

```bash
sudo nano /etc/systemd/system/motibeam.service
```

**Replace the entire contents** with this:

```ini
[Unit]
Description=MotiBeam OS - Multi-Vertical Ambient Computing Platform
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
User=motibeam
Group=motibeam
WorkingDirectory=/home/motibeam/MotiBeam-OS

# Launch MotiBeam with logging wrapper
ExecStart=/home/motibeam/MotiBeam-OS/scripts/run_motibeam_with_log.sh

# Restart on failure
Restart=on-failure
RestartSec=10

# Give service time to start
TimeoutStartSec=30

[Install]
WantedBy=graphical.target
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

### Step 4: Make Sure Script is Executable

```bash
chmod +x ~/MotiBeam-OS/scripts/run_motibeam_with_log.sh
```

### Step 5: Test Manually First (IMPORTANT!)

Before relying on systemd, test that the app works with DISPLAY set:

```bash
cd ~/MotiBeam-OS
export DISPLAY=:0
export XAUTHORITY=/home/motibeam/.Xauthority
python3 motibeam_app.py
```

**Expected result:** MotiBeam launches fullscreen on your projector. Press ESC to exit.

**If it doesn't work:** Check that:
- You're on the Pi desktop (not SSH only)
- The projector is connected and on
- The scene files are updated (no more `from .scene_base`)

### Step 6: Enable and Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable motibeam
sudo systemctl restart motibeam
```

### Step 7: Check Service Status

```bash
sudo systemctl status motibeam --no-pager -l
```

You should see:
- `Active: active (running)`
- Main PID should be `bash` with a child `python3` process
- MotiBeam should appear on your projector!

### Step 8: Check the Logs

```bash
tail -f /home/motibeam/motibeam_boot.log
```

You should see:
- "MotiBeam OS Startup"
- "DISPLAY: :0"
- "X server ready after X attempts"
- "Launching MotiBeam OS"
- MotiBeam startup messages

Press Ctrl+C to exit the log view.

### Step 9: Final Reboot Test

```bash
sudo reboot
```

After reboot:
- Pi should boot to desktop (briefly)
- MotiBeam should automatically launch fullscreen
- No login prompt needed (if you have auto-login enabled)

---

## Troubleshooting

### If MotiBeam doesn't appear after reboot:

1. **Check the service status:**
   ```bash
   sudo systemctl status motibeam --no-pager -l
   ```

2. **Check the boot log:**
   ```bash
   cat /home/motibeam/motibeam_boot.log
   ```

3. **Check for DISPLAY errors:**
   ```bash
   grep "DISPLAY" /home/motibeam/motibeam_boot.log
   grep "ERROR" /home/motibeam/motibeam_boot.log
   ```

4. **Verify X server is running:**
   ```bash
   ps aux | grep X
   echo $DISPLAY
   ```

### If you see "Import error" or "no module named":

Your scene files are still old! Repeat Step 1 with `git reset --hard`.

### If service keeps restarting:

```bash
journalctl -u motibeam.service -n 100 --no-pager
```

Look for Python errors or import failures.

### If it works manually but not via systemd:

The service might be starting too early. Try increasing the wait time in the wrapper script:

```bash
nano ~/MotiBeam-OS/scripts/run_motibeam_with_log.sh
```

Change line with `for i in {1..10}` to `for i in {1..20}` for a longer wait.

---

## What Changed in This Fix

1. **Simplified wrapper script:**
   - Explicitly sets `DISPLAY=:0` and `XAUTHORITY`
   - Waits up to 10 seconds for X server to be ready
   - Simpler logging (writes to `/home/motibeam/motibeam_boot.log`)
   - Actually launches the Python app!

2. **Updated service file:**
   - Runs as `User=motibeam` (not root)
   - Only depends on `graphical.target` (removed network dependency)
   - Environment variables set in script, not service file
   - Cleaner configuration

3. **Fixed scene imports:**
   - Added `scenes/__init__.py` to make it a proper Python package
   - All scene files use correct `from scene_base import MotiBeamScene`
   - No more relative import errors

---

## After It's Working

Once MotiBeam boots automatically, you can:

**Stop the service:**
```bash
sudo systemctl stop motibeam
```

**Disable autostart:**
```bash
sudo systemctl disable motibeam
```

**Re-enable autostart:**
```bash
sudo systemctl enable motibeam
sudo systemctl start motibeam
```

**View live logs:**
```bash
tail -f /home/motibeam/motibeam_boot.log
```

---

**MotiBeam OS should now boot automatically in fullscreen!**
