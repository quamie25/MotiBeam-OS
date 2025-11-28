#!/usr/bin/env python3
"""
MotiBeamOS v3.0 - Scene Manager
Dynamically discovers and manages ambient/holiday scene modules
"""

import os
import sys
import importlib.util

# Scene discovery constants
SCENES_DIR = "scenes"
SCENE_PREFIX = "scene_"

# Global state
_scenes = {}  # Dict of {scene_name: module}
_active_scene = None
_active_scene_name = None
_screen = None


class SceneInfo:
    """Metadata about a scene"""

    def __init__(self, name, category, module):
        self.name = name
        self.category = category
        self.module = module


def _discover_scenes():
    """Scan scenes directory for scene_*.py files and load their metadata"""
    global _scenes

    _scenes = {}

    if not os.path.exists(SCENES_DIR):
        print(f"Warning: Scenes directory '{SCENES_DIR}' not found")
        return

    for filename in os.listdir(SCENES_DIR):
        if filename.startswith(SCENE_PREFIX) and filename.endswith(".py"):
            scene_file = filename[:-3]  # Remove .py
            module_path = os.path.join(SCENES_DIR, filename)

            try:
                # Import module dynamically
                spec = importlib.util.spec_from_file_location(scene_file, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[scene_file] = module
                spec.loader.exec_module(module)

                # Check if module has required interface
                if hasattr(module, 'SCENE_NAME') and hasattr(module, 'SCENE_CATEGORY'):
                    if hasattr(module, 'init_scene') and hasattr(module, 'update_scene') and hasattr(module,
                                                                                                       'render_scene'):
                        scene_name = module.SCENE_NAME
                        scene_category = module.SCENE_CATEGORY

                        _scenes[scene_name] = SceneInfo(scene_name, scene_category, module)
                        print(f"Loaded scene: {scene_name} ({scene_category})")
                    else:
                        print(
                            f"Warning: {filename} missing required functions (init_scene, update_scene, render_scene)")
                else:
                    print(f"Warning: {filename} missing SCENE_NAME or SCENE_CATEGORY")

            except Exception as e:
                print(f"Error loading scene {filename}: {e}")


def load_all_scenes():
    """Load all available scenes and return metadata list"""
    _discover_scenes()
    return get_scene_list()


def get_scene_list():
    """Return list of (scene_name, category) tuples"""
    return [(info.name, info.category) for info in _scenes.values()]


def set_active_scene(scene_name):
    """Switch to a different scene by name"""
    global _active_scene, _active_scene_name

    if scene_name not in _scenes:
        print(f"Warning: Scene '{scene_name}' not found")
        return False

    try:
        _active_scene_name = scene_name
        _active_scene = _scenes[scene_name].module

        # Initialize the scene
        if _screen and hasattr(_active_scene, 'init_scene'):
            _active_scene.init_scene(_screen)

        print(f"Switched to scene: {scene_name}")
        return True

    except Exception as e:
        print(f"Error switching to scene {scene_name}: {e}")
        _active_scene = None
        _active_scene_name = None
        return False


def get_active_scene_name():
    """Return the name of the currently active scene"""
    return _active_scene_name


def update_active_scene(dt):
    """Update the active scene"""
    if _active_scene and hasattr(_active_scene, 'update_scene'):
        try:
            _active_scene.update_scene(dt)
        except Exception as e:
            print(f"Error updating scene: {e}")


def render_active_scene(screen):
    """Render the active scene"""
    global _screen
    _screen = screen

    if _active_scene and hasattr(_active_scene, 'render_scene'):
        try:
            _active_scene.render_scene(screen)
        except Exception as e:
            print(f"Error rendering scene: {e}")


def init_scene_manager(screen):
    """Initialize scene manager with screen reference"""
    global _screen
    _screen = screen
    load_all_scenes()


# Public API
__all__ = [
    'load_all_scenes',
    'get_scene_list',
    'set_active_scene',
    'get_active_scene_name',
    'update_active_scene',
    'render_active_scene',
    'init_scene_manager'
]
