# MotiBeam OS - Autostart Configuration Guide

This guide provides complete instructions for configuring MotiBeam OS to automatically start on boot using either **systemd** (recommended) or **LXDE autostart** (fallback).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Method 1: Systemd Service (Recommended)](#method-1-systemd-service-recommended)
3. [Method 2: LXDE Autostart (Fallback)](#method-2-lxde-autostart-fallback)
4. [Troubleshooting](#troubleshooting)
5. [Log Files](#log-files)

---

## Prerequisites

Before configuring autostart, ensure:

1. **MotiBeam OS works when run manually:**
   ```bash
   cd ~/MotiBeam-OS
   python3 motibeam_app.py
   ```
   → The application should launch in fullscreen and display properly.

2. **Required packages are installed:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pygame xserver-xorg
   ```

   **Optional but recommended** (for X server connection diagnostics):
   ```bash
   sudo apt-get install -y x11-xserver-utils
   ```

   Note: The startup script will work without `x11-xserver-utils`, but won't be able to verify X server connectivity before launching.

3. **The Pi auto-logs in to the desktop:**
   - Run `sudo raspi-config`
   - Navigate to: **System Options** → **Boot / Auto Login** → **Desktop Autologin**

4. **Create the logs directory:**
   ```bash
   mkdir -p ~/MotiBeam-OS/logs
   ```

---

## Method 1: Systemd Service (Recommended)

### Step 1: Create the systemd service file

Create a new file at `/etc/systemd/system/motibeam.service`:

```bash
sudo nano /etc/systemd/system/motibeam.service
```

Paste the following content:

```ini
[Unit]
Description=MotiBeam OS - Multi-Vertical Ambient Computing Platform
After=graphical.target network-online.target
Wants=graphical.target network-online.target

[Service]
Type=simple
User=motibeam
WorkingDirectory=/home/motibeam/MotiBeam-OS

# Environment variables for X display
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/motibeam/.Xauthority

# SDL settings for better compatibility
Environment=SDL_VIDEODRIVER=x11
Environment=SDL_AUDIODRIVER=pulse

# Ensure clean output in logs
Environment=PYTHONUNBUFFERED=1

# Launch MotiBeam with logging wrapper
ExecStart=/bin/bash /home/motibeam/MotiBeam-OS/scripts/run_motibeam_with_log.sh

# Restart on failure (but not too aggressively)
Restart=on-failure
RestartSec=10

# Give the service time to start
TimeoutStartSec=30

[Install]
WantedBy=graphical.target
```

**Important:** Replace `motibeam` with your actual username if different.

### Step 2: Reload systemd and enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable motibeam
```

### Step 3: Start the service immediately (for testing)

```bash
sudo systemctl start motibeam
```

### Step 4: Check the service status

```bash
sudo systemctl status motibeam --no-pager -l
```

You should see:
```
● motibeam.service - MotiBeam OS - Multi-Vertical Ambient Computing Platform
     Loaded: loaded (/etc/systemd/system/motibeam.service; enabled)
     Active: active (running) since ...
```

### Step 5: Test autostart on reboot

```bash
sudo reboot
```

After reboot, MotiBeam OS should automatically launch in fullscreen.

---

## Method 2: LXDE Autostart (Fallback)

If systemd doesn't work for your setup, use LXDE's autostart feature.

### Step 1: Create autostart directory

```bash
mkdir -p ~/.config/autostart
```

### Step 2: Create the desktop entry

Create `~/.config/autostart/motibeam.desktop`:

```bash
nano ~/.config/autostart/motibeam.desktop
```

Paste the following content:

```ini
[Desktop Entry]
Type=Application
Name=MotiBeam OS
Comment=Multi-Vertical Ambient Computing Platform
Exec=/bin/bash /home/motibeam/MotiBeam-OS/scripts/run_motibeam_with_log.sh
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
```

**Important:** Replace `/home/motibeam` with your actual home directory path.

### Step 3: Make it executable

```bash
chmod +x ~/.config/autostart/motibeam.desktop
```

### Step 4: Test autostart

Log out and log back in, or reboot:

```bash
sudo reboot
```

MotiBeam OS should launch automatically after login.

---

## Troubleshooting

### Service shows "active (running)" but no display

**Possible causes:**

1. **X server not ready when service starts**
   - Solution: The service now waits for `graphical.target` and includes a startup delay
   - Check logs: `journalctl -u motibeam.service -n 100 --no-pager`

2. **Wrong DISPLAY or XAUTHORITY values**
   - Find the correct values:
     ```bash
     echo $DISPLAY
     ls -la ~/.Xauthority
     ```
   - Update the service file with correct values

3. **Permission issues with .Xauthority**
   - Fix permissions:
     ```bash
     chmod 600 ~/.Xauthority
     chown $USER:$USER ~/.Xauthority
     ```

### Check detailed logs

View the MotiBeam boot log:

```bash
cat ~/MotiBeam-OS/logs/motibeam_boot.log
```

View systemd service logs:

```bash
journalctl -u motibeam.service -n 100 --no-pager
```

View all recent logs with error context:

```bash
journalctl -u motibeam.service -b --no-pager
```

### Manual testing with the logging wrapper

Test the logging wrapper directly:

```bash
cd ~/MotiBeam-OS
./scripts/run_motibeam_with_log.sh
```

Check if X connection works:

```bash
export DISPLAY=:0
xset q
```

If `xset q` fails, the X server is not accessible.

### Pygame won't start

If you see `pygame.error: No available video device`:

1. Verify X is running:
   ```bash
   ps aux | grep X
   ```

2. Test pygame separately:
   ```bash
   python3 -c "import pygame; pygame.init(); print('OK')"
   ```

3. Set SDL video driver explicitly:
   ```bash
   export SDL_VIDEODRIVER=x11
   export DISPLAY=:0
   python3 motibeam_app.py
   ```

### Service fails immediately

Check the exit code and error message:

```bash
journalctl -u motibeam.service --no-pager | tail -50
```

Common issues:
- **Python import errors:** Install missing dependencies
- **File not found:** Verify paths in service file are correct
- **Permission denied:** Ensure user has permission to access files

---

## Log Files

MotiBeam OS creates detailed logs for troubleshooting:

### Boot log location

```
~/MotiBeam-OS/logs/motibeam_boot.log
```

This log includes:
- Timestamp of startup
- Environment variables (DISPLAY, USER, etc.)
- X server connection status
- Python and pygame version info
- Application stdout/stderr
- Exit codes and error traces

### Viewing logs in real-time

```bash
tail -f ~/MotiBeam-OS/logs/motibeam_boot.log
```

### Clearing old logs

```bash
rm ~/MotiBeam-OS/logs/motibeam_boot.log
```

The log will be recreated on next startup.

---

## Advanced Configuration

### Delay startup for slower systems

If your Pi needs more time for the X server to start, increase the delay in the wrapper script:

Edit `~/MotiBeam-OS/scripts/run_motibeam_with_log.sh`:

```bash
nano ~/MotiBeam-OS/scripts/run_motibeam_with_log.sh
```

Find the line:
```bash
sleep 5
```

Change to:
```bash
sleep 10
```

### Disable service temporarily

```bash
sudo systemctl stop motibeam
sudo systemctl disable motibeam
```

### Re-enable service

```bash
sudo systemctl enable motibeam
sudo systemctl start motibeam
```

### Running both methods

**Warning:** Do NOT run both systemd and LXDE autostart simultaneously. This will launch two instances of MotiBeam OS.

To use only one method:
- **Systemd only:** Remove `~/.config/autostart/motibeam.desktop`
- **LXDE only:** Run `sudo systemctl disable motibeam`

---

## Quick Reference

### Systemd Commands

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable motibeam

# Start service now
sudo systemctl start motibeam

# Stop service
sudo systemctl stop motibeam

# Restart service
sudo systemctl restart motibeam

# Check status
sudo systemctl status motibeam --no-pager -l

# View logs
journalctl -u motibeam.service -n 100 --no-pager

# Disable autostart
sudo systemctl disable motibeam
```

### File Locations

| File | Purpose |
|------|---------|
| `/etc/systemd/system/motibeam.service` | Systemd service definition |
| `~/.config/autostart/motibeam.desktop` | LXDE autostart entry |
| `~/MotiBeam-OS/scripts/run_motibeam_with_log.sh` | Startup wrapper with logging |
| `~/MotiBeam-OS/logs/motibeam_boot.log` | Application startup log |
| `~/MotiBeam-OS/motibeam_app.py` | Main MotiBeam application |

---

## Support

If you continue to experience issues after following this guide:

1. Capture the boot log:
   ```bash
   cat ~/MotiBeam-OS/logs/motibeam_boot.log
   ```

2. Capture systemd logs:
   ```bash
   journalctl -u motibeam.service -n 60 --no-pager
   ```

3. Check X server status:
   ```bash
   echo $DISPLAY
   xset q
   ps aux | grep X
   ```

4. Verify MotiBeam works manually:
   ```bash
   cd ~/MotiBeam-OS
   python3 motibeam_app.py
   ```

Share these outputs when requesting support.

---

**MotiBeam OS v3.0**
Multi-Vertical Ambient Computing Platform
