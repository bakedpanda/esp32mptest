"""XIAO ESP32-S3 demo — cycles RGB colors on the built-in NeoPixel (GPIO 48).

Prints the current color to serial on each tick so it works headless too.
Uses machine.Timer so the REPL and WebREPL stay responsive.
"""
from machine import Pin, Timer
import neopixel

# XIAO ESP32-S3 built-in RGB LED is a single NeoPixel on GPIO 48
_np = neopixel.NeoPixel(Pin(48), 1)

# Colors to cycle through (R, G, B) — kept dim to avoid blinding
_COLORS = [
    (32, 0, 0),   # red
    (0, 32, 0),   # green
    (0, 0, 32),   # blue
    (16, 16, 0),  # yellow
    (0, 16, 16),  # cyan
    (16, 0, 16),  # magenta
    (0, 0, 0),    # off
]
_NAMES = ["red", "green", "blue", "yellow", "cyan", "magenta", "off"]
_idx = 0


def _tick(t):
    global _idx
    color = _COLORS[_idx % len(_COLORS)]
    name = _NAMES[_idx % len(_NAMES)]
    _np[0] = color
    _np.write()
    print(f"LED: {name} {color}")
    _idx += 1


_timer = Timer(0)
_timer.init(period=750, mode=Timer.PERIODIC, callback=_tick)
print("XIAO ESP32-S3 LED demo started")
