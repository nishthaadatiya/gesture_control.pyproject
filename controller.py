import numpy as np
import subprocess
import ctypes
import json
import os


# Load config
_config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(_config_path) as f:
    _cfg = json.load(f)


# --- macOS native brightness via DisplayServices (works on Apple Silicon) ---
_ds_available = False
try:
    _CoreGraphics = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
    )
    _CoreGraphics.CGMainDisplayID.restype = ctypes.c_uint32
    _display_id = _CoreGraphics.CGMainDisplayID()

    _DisplayServices = ctypes.cdll.LoadLibrary(
        "/System/Library/PrivateFrameworks/DisplayServices.framework/DisplayServices"
    )
    _DisplayServices.DisplayServicesSetBrightness.argtypes = [
        ctypes.c_uint32, ctypes.c_float
    ]
    _DisplayServices.DisplayServicesSetBrightness.restype = ctypes.c_int
    _ds_available = True
except OSError:
    _ds_available = False


def pinch_distance(landmarks):
    """Euclidean distance between thumb tip (4) and index tip (8)."""
    x1, y1 = landmarks[4]
    x2, y2 = landmarks[8]
    return float(np.hypot(x2 - x1, y2 - y1))


def set_volume(distance, min_dist=_cfg["min_dist"], max_dist=_cfg["max_dist"]):
    vol_pct = int(np.interp(distance, [min_dist, max_dist], [0, 100]))
    subprocess.run(
        ["osascript", "-e", f"set volume output volume {vol_pct}"],
        capture_output=True
    )
    return vol_pct


def set_brightness(distance, min_dist=_cfg["min_dist"], max_dist=_cfg["max_dist"]):
    brightness = int(np.interp(distance, [min_dist, max_dist], [0, 100]))
    val = brightness / 100.0
    if _ds_available:
        _DisplayServices.DisplayServicesSetBrightness(
            _display_id, ctypes.c_float(val)
        )
    else:
        # Fallback: Homebrew brightness CLI
        subprocess.run(["brightness", f"{val:.2f}"], capture_output=True)
    return brightness

