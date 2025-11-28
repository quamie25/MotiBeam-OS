#!/usr/bin/env python3
"""
MotiBeamOS v3.0 - Settings Panel
Provides a comprehensive settings UI with left menu and dynamic content area
"""

import pygame
import json
import os

# Settings file path
SETTINGS_FILE = "config/settings.json"

# Panel layout constants
MENU_WIDTH = 280
PANEL_PADDING = 20
CONTROL_HEIGHT = 50
CONTROL_SPACING = 15

# Colors
COLOR_BG = (20, 20, 25)
COLOR_MENU_BG = (30, 30, 35)
COLOR_MENU_HOVER = (50, 50, 60)
COLOR_MENU_ACTIVE = (0, 180, 140)
COLOR_TEXT = (220, 220, 220)
COLOR_TEXT_DIM = (140, 140, 140)
COLOR_CONTROL_BG = (40, 40, 45)
COLOR_CONTROL_ACTIVE = (0, 200, 160)
COLOR_SLIDER_BG = (60, 60, 70)
COLOR_SLIDER_FILL = (0, 200, 160)
COLOR_BUTTON = (70, 70, 80)
COLOR_BUTTON_HOVER = (90, 90, 100)
COLOR_BUTTON_DANGER = (200, 60, 60)

# Global state
_settings = {}
_current_menu = "Display"
_menu_items = ["Display", "Visuals", "Scenes", "Sensors", "Profiles", "System", "Demo Mode"]
_hover_menu = None
_hover_control = None
_dragging_slider = None
_scene_manager = None  # Will be set externally
_screen_width = 1280
_screen_height = 720
_font_medium = None
_font_small = None
_settings_dirty = False  # Track if settings need saving


def load_settings():
    """Load settings from JSON file"""
    global _settings

    default_settings = {
        "Display": {
            "brightness": 75,
            "screen_ratio": "Auto"
        },
        "Visuals": {
            "theme": "Dark",
            "animation_speed": 50
        },
        "Scenes": {
            "active_scene": "Fireplace",
            "category_filter": "All"
        },
        "Sensors": {
            "presence_detection": False,
            "mic_sensitivity": 60
        },
        "Profiles": {
            "active_profile": "Smart Home"
        },
        "System": {
            "version": "MotiBeamOS v3.0"
        },
        "Demo": {
            "enabled": False,
            "demo_profile": "Smart Home"
        }
    }

    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                _settings = json.load(f)
        else:
            _settings = default_settings
            save_settings(_settings)
    except Exception as e:
        print(f"Error loading settings: {e}")
        _settings = default_settings

    return _settings


def save_settings(settings):
    """Save settings to JSON file"""
    global _settings, _settings_dirty
    _settings = settings
    _settings_dirty = False

    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")


def get_current_settings():
    """Return current settings dictionary"""
    return _settings


def set_scene_manager(manager):
    """Set the scene manager reference for scene integration"""
    global _scene_manager
    _scene_manager = manager


def init_settings_panel(screen, font_medium=None, font_small=None):
    """Initialize settings panel (optional - auto-inits on first render)"""
    global _screen_width, _screen_height, _font_medium, _font_small
    _screen_width = screen.get_width()
    _screen_height = screen.get_height()
    _font_medium = font_medium or pygame.font.Font(None, 48)
    _font_small = font_small or pygame.font.Font(None, 36)
    load_settings()


def _draw_text(screen, text, pos, font, color=COLOR_TEXT, align="left"):
    """Helper to draw text"""
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()

    if align == "center":
        rect.center = pos
    elif align == "right":
        rect.right = pos[0]
        rect.top = pos[1]
    else:
        rect.topleft = pos

    screen.blit(surf, rect)
    return rect


def _draw_toggle(screen, rect, value, hovered=False):
    """Draw a toggle switch"""
    # Background
    bg_color = COLOR_CONTROL_ACTIVE if value else COLOR_CONTROL_BG
    if hovered and not value:
        bg_color = COLOR_SLIDER_BG
    pygame.draw.rect(screen, bg_color, rect, border_radius=rect.height // 2)

    # Knob
    knob_radius = rect.height // 2 - 4
    knob_x = rect.right - knob_radius - 6 if value else rect.left + knob_radius + 6
    knob_y = rect.centery
    pygame.draw.circle(screen, COLOR_TEXT, (knob_x, knob_y), knob_radius)


def _draw_slider(screen, rect, value, min_val=0, max_val=100, hovered=False, dragging=False):
    """Draw a slider control"""
    # Background track
    track_rect = pygame.Rect(rect.x, rect.centery - 4, rect.width, 8)
    pygame.draw.rect(screen, COLOR_SLIDER_BG, track_rect, border_radius=4)

    # Fill track
    fill_width = int((value - min_val) / (max_val - min_val) * rect.width)
    fill_rect = pygame.Rect(rect.x, rect.centery - 4, fill_width, 8)
    pygame.draw.rect(screen, COLOR_SLIDER_FILL, fill_rect, border_radius=4)

    # Knob
    knob_x = rect.x + fill_width
    knob_y = rect.centery
    knob_radius = 12 if hovered or dragging else 10
    pygame.draw.circle(screen, COLOR_CONTROL_ACTIVE if dragging else COLOR_TEXT, (knob_x, knob_y), knob_radius)

    # Value label
    value_text = f"{int(value)}"
    _draw_text(screen, value_text, (rect.right + 10, rect.centery - 12), _font_small, COLOR_TEXT_DIM)


def _draw_dropdown(screen, rect, value, options, hovered=False):
    """Draw a dropdown control"""
    # Background
    bg_color = COLOR_BUTTON_HOVER if hovered else COLOR_CONTROL_BG
    pygame.draw.rect(screen, bg_color, rect, border_radius=5)

    # Selected value
    _draw_text(screen, value, (rect.x + 15, rect.y + 10), _font_small, COLOR_TEXT)

    # Dropdown arrow
    arrow_x = rect.right - 30
    arrow_y = rect.centery
    points = [
        (arrow_x, arrow_y - 5),
        (arrow_x + 10, arrow_y - 5),
        (arrow_x + 5, arrow_y + 5)
    ]
    pygame.draw.polygon(screen, COLOR_TEXT_DIM, points)


def _draw_button(screen, rect, text, hovered=False, danger=False):
    """Draw a button"""
    if danger:
        bg_color = COLOR_BUTTON_DANGER if hovered else (150, 50, 50)
    else:
        bg_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON

    pygame.draw.rect(screen, bg_color, rect, border_radius=5)
    _draw_text(screen, text, (rect.centerx, rect.centery - 12), _font_small, COLOR_TEXT, align="center")


def _draw_preview_window(screen, rect):
    """Draw a scene preview window"""
    pygame.draw.rect(screen, COLOR_CONTROL_BG, rect, border_radius=5)

    # If scene manager is available, try to get a preview
    if _scene_manager:
        # For now, just show the active scene name
        scene_name = _settings.get("Scenes", {}).get("active_scene", "None")
        _draw_text(screen, f"Preview: {scene_name}",
                  (rect.centerx, rect.centery - 12), _font_small, COLOR_TEXT_DIM, align="center")
    else:
        _draw_text(screen, "Preview",
                  (rect.centerx, rect.centery - 12), _font_small, COLOR_TEXT_DIM, align="center")


def _get_scene_list():
    """Get list of available scenes from scene manager"""
    if _scene_manager:
        return _scene_manager.get_scene_list()
    return ["Fireplace", "Aurora", "Rain", "Waves", "Snowfall"]


def _get_scene_categories():
    """Get list of scene categories"""
    if _scene_manager:
        scenes = _scene_manager.get_scene_list()
        categories = set(["All"])
        for scene_name, category in scenes:
            categories.add(category)
        return sorted(list(categories))
    return ["All", "Ambient", "Holiday"]


def _render_display_settings(screen, content_x, content_y, content_width):
    """Render Display settings section"""
    global _hover_control, _dragging_slider

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Display Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Brightness slider
    _draw_text(screen, "Brightness", (content_x, y), _font_small)
    y += 40
    slider_rect = pygame.Rect(content_x, y, content_width - 100, 30)
    hovered = slider_rect.collidepoint(mouse_pos)
    dragging = _dragging_slider == "brightness"
    _draw_slider(screen, slider_rect, _settings["Display"]["brightness"], 0, 100, hovered, dragging)
    if hovered:
        _hover_control = ("slider", "brightness", slider_rect)
    y += 60

    # Screen Ratio dropdown
    _draw_text(screen, "Screen Ratio", (content_x, y), _font_small)
    y += 40
    dropdown_rect = pygame.Rect(content_x, y, 250, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    _draw_dropdown(screen, dropdown_rect, _settings["Display"]["screen_ratio"],
                   ["Auto", "16:9", "4:3"], hovered)
    if hovered:
        _hover_control = ("dropdown", "screen_ratio", dropdown_rect, ["Auto", "16:9", "4:3"])


def _render_visuals_settings(screen, content_x, content_y, content_width):
    """Render Visuals settings section"""
    global _hover_control, _dragging_slider

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Visual Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Theme dropdown
    _draw_text(screen, "Theme", (content_x, y), _font_small)
    y += 40
    dropdown_rect = pygame.Rect(content_x, y, 250, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    _draw_dropdown(screen, dropdown_rect, _settings["Visuals"]["theme"],
                   ["Light", "Dark"], hovered)
    if hovered:
        _hover_control = ("dropdown", "theme", dropdown_rect, ["Light", "Dark"])
    y += 70

    # Animation Speed slider
    _draw_text(screen, "Animation Speed", (content_x, y), _font_small)
    y += 40
    slider_rect = pygame.Rect(content_x, y, content_width - 100, 30)
    hovered = slider_rect.collidepoint(mouse_pos)
    dragging = _dragging_slider == "animation_speed"
    _draw_slider(screen, slider_rect, _settings["Visuals"]["animation_speed"], 0, 100, hovered, dragging)
    if hovered:
        _hover_control = ("slider", "animation_speed", slider_rect)


def _render_scenes_settings(screen, content_x, content_y, content_width):
    """Render Scenes settings section"""
    global _hover_control

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Scene Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Category Filter dropdown
    _draw_text(screen, "Category Filter", (content_x, y), _font_small)
    y += 40
    categories = _get_scene_categories()
    dropdown_rect = pygame.Rect(content_x, y, 250, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    _draw_dropdown(screen, dropdown_rect, _settings["Scenes"]["category_filter"],
                   categories, hovered)
    if hovered:
        _hover_control = ("dropdown", "category_filter", dropdown_rect, categories)
    y += 70

    # Active Scene dropdown
    _draw_text(screen, "Active Scene", (content_x, y), _font_small)
    y += 40
    scenes = _get_scene_list()
    scene_names = [name for name, cat in scenes]
    # Filter by category if not "All"
    if _settings["Scenes"]["category_filter"] != "All":
        scene_names = [name for name, cat in scenes if cat == _settings["Scenes"]["category_filter"]]

    dropdown_rect = pygame.Rect(content_x, y, 350, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    current_scene = _settings["Scenes"]["active_scene"]
    if current_scene not in scene_names and scene_names:
        current_scene = scene_names[0]
        _settings["Scenes"]["active_scene"] = current_scene
    _draw_dropdown(screen, dropdown_rect, current_scene, scene_names, hovered)
    if hovered:
        _hover_control = ("dropdown", "active_scene", dropdown_rect, scene_names)
    y += 70

    # Preview Window
    _draw_text(screen, "Preview", (content_x, y), _font_small)
    y += 40
    preview_rect = pygame.Rect(content_x, y, content_width - 50, 200)
    _draw_preview_window(screen, preview_rect)


def _render_sensors_settings(screen, content_x, content_y, content_width):
    """Render Sensors settings section"""
    global _hover_control, _dragging_slider

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Sensor Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Presence Detection toggle
    _draw_text(screen, "Presence Detection", (content_x, y), _font_small)
    toggle_rect = pygame.Rect(content_x + 400, y, 100, 40)
    hovered = toggle_rect.collidepoint(mouse_pos)
    _draw_toggle(screen, toggle_rect, _settings["Sensors"]["presence_detection"], hovered)
    if hovered:
        _hover_control = ("toggle", "presence_detection", toggle_rect)
    y += 70

    # Mic Sensitivity slider
    _draw_text(screen, "Mic Sensitivity", (content_x, y), _font_small)
    y += 40
    slider_rect = pygame.Rect(content_x, y, content_width - 100, 30)
    hovered = slider_rect.collidepoint(mouse_pos)
    dragging = _dragging_slider == "mic_sensitivity"
    _draw_slider(screen, slider_rect, _settings["Sensors"]["mic_sensitivity"], 0, 100, hovered, dragging)
    if hovered:
        _hover_control = ("slider", "mic_sensitivity", slider_rect)


def _render_profiles_settings(screen, content_x, content_y, content_width):
    """Render Profiles settings section"""
    global _hover_control

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Profile Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Active Profile dropdown
    _draw_text(screen, "Active Profile", (content_x, y), _font_small)
    y += 40
    profiles = ["Smart Home", "Auto", "Wellness", "Delivery"]
    dropdown_rect = pygame.Rect(content_x, y, 300, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    _draw_dropdown(screen, dropdown_rect, _settings["Profiles"]["active_profile"],
                   profiles, hovered)
    if hovered:
        _hover_control = ("dropdown", "active_profile", dropdown_rect, profiles)
    y += 70

    # Info text
    _draw_text(screen, "Profile behavior will be implemented in future updates.",
              (content_x, y), _font_small, COLOR_TEXT_DIM)


def _render_system_settings(screen, content_x, content_y, content_width):
    """Render System settings section"""
    global _hover_control

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "System Settings", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # About (read-only)
    _draw_text(screen, "About", (content_x, y), _font_small)
    y += 40
    version_text = _settings["System"]["version"]
    _draw_text(screen, version_text, (content_x, y), _font_small, COLOR_TEXT_DIM)
    y += 70

    # Reboot button
    reboot_rect = pygame.Rect(content_x, y, 200, CONTROL_HEIGHT)
    hovered = reboot_rect.collidepoint(mouse_pos)
    _draw_button(screen, reboot_rect, "Reboot", hovered)
    if hovered:
        _hover_control = ("button", "reboot", reboot_rect)
    y += 70

    # Factory Reset button (danger)
    reset_rect = pygame.Rect(content_x, y, 250, CONTROL_HEIGHT)
    hovered = reset_rect.collidepoint(mouse_pos)
    _draw_button(screen, reset_rect, "Factory Reset", hovered, danger=True)
    if hovered:
        _hover_control = ("button", "factory_reset", reset_rect)


def _render_demo_settings(screen, content_x, content_y, content_width):
    """Render Demo Mode settings section"""
    global _hover_control

    y = content_y
    mouse_pos = pygame.mouse.get_pos()

    # Title
    _draw_text(screen, "Demo Mode", (content_x, y), _font_medium, COLOR_CONTROL_ACTIVE)
    y += 70

    # Enable Demo Mode toggle
    _draw_text(screen, "Enable Demo Mode", (content_x, y), _font_small)
    toggle_rect = pygame.Rect(content_x + 400, y, 100, 40)
    hovered = toggle_rect.collidepoint(mouse_pos)
    _draw_toggle(screen, toggle_rect, _settings["Demo"]["enabled"], hovered)
    if hovered:
        _hover_control = ("toggle", "demo_enabled", toggle_rect)
    y += 70

    # Demo Profile dropdown
    _draw_text(screen, "Demo Profile", (content_x, y), _font_small)
    y += 40
    profiles = ["Smart Home", "Auto", "Wellness", "Delivery"]
    dropdown_rect = pygame.Rect(content_x, y, 300, CONTROL_HEIGHT)
    hovered = dropdown_rect.collidepoint(mouse_pos)
    _draw_dropdown(screen, dropdown_rect, _settings["Demo"]["demo_profile"],
                   profiles, hovered)
    if hovered:
        _hover_control = ("dropdown", "demo_profile", dropdown_rect, profiles)


def render_settings_panel(screen):
    """Render the complete settings panel"""
    global _hover_control, _hover_menu, _font_medium, _font_small

    # Auto-initialize if needed
    if _font_medium is None:
        init_settings_panel(screen)

    # Reset hover states
    _hover_control = None
    _hover_menu = None

    mouse_pos = pygame.mouse.get_pos()

    # Background
    screen.fill(COLOR_BG)

    # Left menu panel
    menu_rect = pygame.Rect(0, 0, MENU_WIDTH, _screen_height)
    pygame.draw.rect(screen, COLOR_MENU_BG, menu_rect)

    # Menu title
    _draw_text(screen, "SETTINGS", (PANEL_PADDING, PANEL_PADDING), _font_medium, COLOR_CONTROL_ACTIVE)

    # Menu items
    y = 100
    for i, item in enumerate(_menu_items):
        item_rect = pygame.Rect(PANEL_PADDING, y, MENU_WIDTH - 2 * PANEL_PADDING, CONTROL_HEIGHT)

        is_active = (_current_menu == item)
        is_hovered = item_rect.collidepoint(mouse_pos)

        if is_hovered:
            _hover_menu = item

        # Draw item background
        if is_active:
            pygame.draw.rect(screen, COLOR_MENU_ACTIVE, item_rect, border_radius=5)
        elif is_hovered:
            pygame.draw.rect(screen, COLOR_MENU_HOVER, item_rect, border_radius=5)

        # Draw item text
        text_color = COLOR_TEXT if (is_active or is_hovered) else COLOR_TEXT_DIM
        _draw_text(screen, item, (item_rect.x + 15, item_rect.y + 12), _font_small, text_color)

        y += CONTROL_HEIGHT + CONTROL_SPACING

    # Vertical separator
    pygame.draw.line(screen, COLOR_CONTROL_ACTIVE, (MENU_WIDTH, 0), (MENU_WIDTH, _screen_height), 2)

    # Content area
    content_x = MENU_WIDTH + PANEL_PADDING * 2
    content_y = PANEL_PADDING * 2
    content_width = _screen_width - MENU_WIDTH - PANEL_PADDING * 4

    # Render current menu section
    if _current_menu == "Display":
        _render_display_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "Visuals":
        _render_visuals_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "Scenes":
        _render_scenes_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "Sensors":
        _render_sensors_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "Profiles":
        _render_profiles_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "System":
        _render_system_settings(screen, content_x, content_y, content_width)
    elif _current_menu == "Demo Mode":
        _render_demo_settings(screen, content_x, content_y, content_width)

    # Footer hint
    hint_text = "Press 'S' or 'ESC' to exit settings"
    _draw_text(screen, hint_text, (_screen_width // 2, _screen_height - 30),
              _font_small, COLOR_TEXT_DIM, align="center")


def handle_settings_events(event):
    """Handle events for settings panel"""
    global _current_menu, _dragging_slider, _settings, _settings_dirty

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left click
            # Check if clicking on menu item
            if _hover_menu:
                _current_menu = _hover_menu

            # Check if clicking on control
            if _hover_control:
                control_type = _hover_control[0]
                control_id = _hover_control[1]

                if control_type == "toggle":
                    # Toggle the value
                    if control_id == "presence_detection":
                        _settings["Sensors"]["presence_detection"] = not _settings["Sensors"]["presence_detection"]
                    elif control_id == "demo_enabled":
                        _settings["Demo"]["enabled"] = not _settings["Demo"]["enabled"]
                    _settings_dirty = True

                elif control_type == "slider":
                    _dragging_slider = control_id

                elif control_type == "dropdown":
                    # Cycle through options
                    options = _hover_control[3]

                    if control_id == "screen_ratio":
                        current = _settings["Display"]["screen_ratio"]
                        idx = (options.index(current) + 1) % len(options)
                        _settings["Display"]["screen_ratio"] = options[idx]
                    elif control_id == "theme":
                        current = _settings["Visuals"]["theme"]
                        idx = (options.index(current) + 1) % len(options)
                        _settings["Visuals"]["theme"] = options[idx]
                    elif control_id == "category_filter":
                        current = _settings["Scenes"]["category_filter"]
                        idx = (options.index(current) + 1) % len(options)
                        _settings["Scenes"]["category_filter"] = options[idx]
                    elif control_id == "active_scene":
                        current = _settings["Scenes"]["active_scene"]
                        if current in options:
                            idx = (options.index(current) + 1) % len(options)
                        else:
                            idx = 0
                        _settings["Scenes"]["active_scene"] = options[idx]
                        # Update scene manager
                        if _scene_manager:
                            _scene_manager.set_active_scene(options[idx])
                    elif control_id == "active_profile":
                        current = _settings["Profiles"]["active_profile"]
                        idx = (options.index(current) + 1) % len(options)
                        _settings["Profiles"]["active_profile"] = options[idx]
                    elif control_id == "demo_profile":
                        current = _settings["Demo"]["demo_profile"]
                        idx = (options.index(current) + 1) % len(options)
                        _settings["Demo"]["demo_profile"] = options[idx]

                    _settings_dirty = True

                elif control_type == "button":
                    if control_id == "reboot":
                        print("REBOOT: System reboot requested (placeholder)")
                    elif control_id == "factory_reset":
                        print("FACTORY RESET: Resetting to defaults...")
                        load_settings()  # This loads defaults if file doesn't exist
                        _settings_dirty = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            if _dragging_slider:
                _settings_dirty = True
            _dragging_slider = None

    elif event.type == pygame.MOUSEMOTION:
        if _dragging_slider:
            # Update slider value based on mouse position
            slider_rect = _hover_control[2]
            mouse_x = event.pos[0]

            # Calculate value from mouse position
            value = ((mouse_x - slider_rect.x) / slider_rect.width) * 100
            value = max(0, min(100, value))

            if _dragging_slider == "brightness":
                _settings["Display"]["brightness"] = int(value)
            elif _dragging_slider == "animation_speed":
                _settings["Visuals"]["animation_speed"] = int(value)
            elif _dragging_slider == "mic_sensitivity":
                _settings["Sensors"]["mic_sensitivity"] = int(value)

    # Auto-save on any change
    if _settings_dirty:
        save_settings(_settings)


# Public API summary
__all__ = [
    'load_settings',
    'save_settings',
    'get_current_settings',
    'set_scene_manager',
    'init_settings_panel',
    'render_settings_panel',
    'handle_settings_events'
]
