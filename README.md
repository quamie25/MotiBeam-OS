# 🌟 MotiBeam OS

**Multi-Vertical Ambient Computing Platform**

MotiBeam OS transforms any wall into an interactive ambient computing surface using projection technology. With 7 specialized verticals, it serves clinical care, education, smart home control, and more—all with a "wall looks alive" design that makes content float naturally without the TV-in-a-box look.

## 🎯 What is MotiBeam OS?

MotiBeam OS is a projection-based platform designed for:
- **Veterans with memory decline** - Visual medication tracking and reminders
- **K-12 Education** - Interactive learning with ambient sleep mode
- **Smart Homes** - Family dashboard and home control
- **Healthcare** - Medication compliance and health monitoring
- **Automotive** - Vehicle maintenance assistance
- **Emergency Response** - Step-by-step emergency procedures
- **Industrial** - Work safety and procedural guidance
- **Security** - Real-time monitoring and alerts

## ✨ Key Features

### 🎓 Education Vertical (Fully Implemented)
**Perfect for 5th grade learning**
- **Math Word Problems** - Step-by-step problem solving with hints
- **Vocabulary Builder** - Word definitions and learning
- **Sleep Mode** - Ambient learning with fading content
  - Pure black background (wall looks alive, not like TV)
  - ASCII symbols (no emoji rendering issues)
  - Proper text wrapping (no cutoff)
  - Smooth fade in/out animations
- **Controls**: Press 1 (Math), 2 (Vocab), 3 (Sleep), ESC (Exit)

### 🏠 Smart Home Vertical (Fully Implemented)
**Compete with Ring, Nest, Alexa, Apple Home**
- **Family Dashboard** - Home status overview
- **Doorbell Monitor** - Front door camera view
- **Package Tracker** - Delivery notifications
- **Smart Controls** - Lights, thermostat, door, garage
- **Family Messages** - Message board for the family
- **Interactive Controls**: L (Lights), D (Door), G (Garage), +/- (Temp)

### 🏥 Clinical, Automotive, Emergency, Industrial, Security
**Coming Soon** - Placeholder screens ready for development

### 🎨 "Wall Looks Alive" Design
- **Pure Black Background** - Content floats on wall naturally
- **No TV Box Look** - Minimal background, maximum impact
- **Fullscreen Projection** - Immersive experience
- **Smooth Transitions** - Professional animations

### ⌨️ Universal ESC Handling
- **ESC from any vertical** → Returns to main menu
- **ESC from main menu** → Clean exit (no freeze)
- **No stuck screens** → Reliable navigation throughout

## 🖥️ Hardware Setup

### Confirmed Working Configuration
- **Raspberry Pi 5** (4GB or 8GB)
- **GOODEE Pico Projector** (1280x720)
- **Logitech 1080P USB Camera** (optional)
- **Fifine K669D USB Microphone** (optional)
- **Raspberry Pi OS 64-bit** (Bookworm)

### Display Resolution
- **1280x720** (720p) - Optimized for projectors
- **Pure Black Background** - Saves projector bulb life
- **Fullscreen Mode** - Automatic on launch

## 📦 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/quamie25/MotiBeam-OS.git
cd MotiBeam-OS

# Create virtual environment
python3 -m venv motibeam-env
source motibeam-env/bin/activate

# Install dependencies
pip install pygame

# Run MotiBeam OS
python3 motibeam_app.py
```

### First Run

1. **Boot Screen** appears with MotiBeam logo and progress bar (2 seconds)
2. **Main Menu** shows all 7 verticals
3. Press **6** for Education or **7** for Smart Home
4. Press **ESC** to navigate back or exit

## 🎮 Controls & Navigation

### Main Menu
| Key | Vertical |
|-----|----------|
| `1` | Clinical Care |
| `2` | Automotive |
| `3` | Emergency Response |
| `4` | Industrial |
| `5` | Security |
| `6` | **Education** (Active) |
| `7` | **Smart Home** (Active) |
| `ESC` | Exit MotiBeam OS |

### Education Vertical
| Key | Action |
|-----|--------|
| `1` | Math Word Problems |
| `2` | Vocabulary Builder |
| `3` | Sleep Mode (Ambient Learning) |
| `SPACE` | Show Answer (Math mode) |
| `N` | Next Problem (Math mode) |
| `ESC` | Return to Main Menu |

### Smart Home Vertical
| Key | Action |
|-----|--------|
| `1` | Family Dashboard |
| `2` | Doorbell Monitor |
| `3` | Package Tracker |
| `4` | Smart Home Controls |
| `5` | Family Messages |
| `L` | Toggle Lights (in Controls) |
| `D` | Lock/Unlock Door (in Controls) |
| `G` | Open/Close Garage (in Controls) |
| `+/-` | Adjust Thermostat (in Controls) |
| `ESC` | Return to Main Menu |

## 🏗️ Project Structure

```
MotiBeam-OS/
├── motibeam_app.py           # Main unified application (START HERE)
├── education_demo.py         # Education vertical (standalone/integrated)
├── home_demo.py              # Smart home vertical (standalone/integrated)
├── motibeam_os.py            # Original 3-demo system (legacy)
├── requirements.txt          # Python dependencies
├── install_pi.sh             # Installation script
├── motibeam.service          # Systemd service file
├── README.md                 # This file
└── LICENSE                   # License information
```

### Running Individual Demos

Each vertical can run standalone for testing:

```bash
# Education demo (standalone)
python3 education_demo.py

# Smart home demo (standalone)
python3 home_demo.py

# Unified app (all verticals)
python3 motibeam_app.py
```

## 🎓 Education Vertical - Detailed Guide

### Sleep Mode Features

**Perfect for ambient learning while your child sleeps**

- **Content Types**:
  - Vocabulary words with definitions
  - Math facts (division, multiplication, fractions)
  - Science concepts
  - Historical facts

- **Display Pattern**:
  1. Fade in (1 second)
  2. Hold at full brightness (2 seconds)
  3. Fade out (1 second)
  4. Next item

- **Pure Black Background**:
  - No blue glow or TV look
  - Wall appears alive with floating content
  - Low light output for peaceful sleep

### Math Word Problems

**5th Grade Level Examples**:
- Division word problems
- Area and perimeter calculations
- Fraction addition
- Multi-step problem solving

**Features**:
- Full text wrapping (no cutoff)
- Hint system
- Show/hide answers
- Multiple problems

### Vocabulary Builder

**Age-Appropriate Words**:
- Science terms (Photosynthesis, Evaporation, Habitat)
- Social studies (Democracy, Community)
- Academic vocabulary

**Features**:
- Clear definitions
- Proper text wrapping
- Easy-to-read formatting

## 🏠 Smart Home Vertical - Detailed Guide

### Family Dashboard

- Current time and date
- Home status overview
- Recent activity log
- Quick status for all devices

### Smart Controls

**Controllable Devices**:
- **Lights** - On/Off toggle
- **Thermostat** - Temperature adjustment (60-85°F)
- **Front Door** - Lock/Unlock status
- **Garage** - Open/Closed status

### Package Tracker

- Delivery status
- Expected arrival times
- Multiple package tracking
- Color-coded status (Delivered=Green, Transit=Yellow)

### Family Messages

- Message board for family
- Sender and timestamp
- Important reminders
- Quick communication

## 🔧 Technical Details

### Architecture

```python
# Main Application (motibeam_app.py)
class MotiBeamOS:
    - Boot screen with animation
    - Main menu navigation
    - Vertical launcher
    - Shared screen management
    - Proper cleanup on exit

# Education Demo (education_demo.py)
class EducationDemo:
    - Math, Vocab, Sleep modes
    - Text wrapping engine
    - Fade animations
    - Event handling

# Home Demo (home_demo.py)
class HomeDemo:
    - 5 sub-features
    - Interactive controls
    - State management
    - Real-time updates
```

### Design Principles

1. **Pure Black Background** - Wall looks alive, not like TV
2. **Fullscreen Always** - Immersive projection experience
3. **Proper ESC Handling** - No frozen screens
4. **Text Wrapping** - Content never cuts off
5. **ASCII Over Emoji** - Reliable rendering
6. **Standalone & Integrated** - Each vertical works alone or together

## 🐛 Troubleshooting

### ESC Key Freezes
**Fixed in current version** - ESC now properly clears screen before exit

### Emoji Shows as Boxes
**Fixed in current version** - Using ASCII symbols like [VOCAB], [DIV], [MULT]

### Questions Cut Off
**Fixed in current version** - Proper text wrapping implemented

### Blue Background Looks Like TV
**Fixed in current version** - Pure black background (0, 0, 0)

### Not Fullscreen
**Fixed in current version** - pygame.FULLSCREEN flag enabled

## 📚 Dependencies

### Required
- **Python 3.11+**
- **pygame 2.6+** - Graphics and display

### Optional
- **opencv-python** - Camera feed (future features)
- **SpeechRecognition** - Voice control (future features)
- **PyAudio** - Audio interface (future features)

### Install Minimal Setup
```bash
pip install pygame
```

### Install Full Setup
```bash
pip install pygame opencv-python SpeechRecognition PyAudio numpy
```

## 🚀 Deployment

### Auto-Start on Boot

```bash
# Copy service file
sudo cp motibeam.service /etc/systemd/system/

# Enable service
sudo systemctl enable motibeam

# Start service
sudo systemctl start motibeam

# Check status
sudo systemctl status motibeam
```

### Manual Start

```bash
# Activate environment
source motibeam-env/bin/activate

# Run application
python3 motibeam_app.py
```

## 🗺️ Roadmap

### Current Version (v3.0)
- ✅ Unified multi-vertical platform
- ✅ Education vertical (5th grade learning)
- ✅ Smart home vertical (family control)
- ✅ Pure black background design
- ✅ Proper ESC handling throughout
- ✅ Text wrapping and ASCII symbols
- ✅ Fullscreen projection mode

### Next Updates
- 🔄 Clinical care vertical (medication tracking)
- 🔄 Automotive vertical (maintenance assistance)
- 🔄 Emergency response vertical
- 🔄 Industrial vertical (safety procedures)
- 🔄 Security vertical (monitoring)
- 🔄 Voice control integration
- 🔄 Camera/gesture detection

### Future Enhancements
- 🔄 Cloud sync for content
- 🔄 Multi-user profiles
- 🔄 Content customization
- 🔄 Mobile app control
- 🔄 AI-powered learning adaptation

## 👨‍👩‍👧‍👦 Use Cases

### For Veterans with Memory Decline
- Visual medication reminders
- Step-by-step task guidance
- Clear, simple interfaces
- Ambient information display

### For K-12 Students
- Interactive homework help
- Sleep learning mode
- Vocabulary building
- Math practice

### For Families
- Shared calendar and messages
- Home automation control
- Package tracking
- Doorbell monitoring

## 💡 Philosophy

**"Make the wall look alive, not like a TV"**

MotiBeam OS uses pure black backgrounds so content appears to float on the wall naturally. No blue glow, no rectangles, no TV-in-a-box look. Just information appearing and disappearing as needed, making your wall an ambient, living surface.

## 📞 Support

- **GitHub Issues**: https://github.com/quamie25/MotiBeam-OS/issues
- **Documentation**: This README
- **Quick Reference**: See controls section above

## 📄 License

This project is licensed under the terms included in the LICENSE file.

## 🙏 Acknowledgments

Built for veterans, students, and families who need ambient computing that feels natural and accessible.

Special thanks to:
- Pygame community
- Raspberry Pi Foundation
- Open source contributors

---

**Made with ❤️ for accessible ambient computing**

**Current Status**: Education & Smart Home verticals fully operational • Pure black "wall looks alive" design • Ready for 5th grade learning 🎓
