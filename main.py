"""XIAO ESP32-S3 demo — blinks SOS in Morse code on the built-in LED (GPIO 21).

Also prints the pattern to serial so it works headless.
Uses a one-shot Timer chain so the REPL stays responsive between flashes.

If the LED appears inverted (on when it should be off), set ACTIVE_LOW = False.
"""
from machine import Pin, Timer

LED_PIN = 21
ACTIVE_LOW = True   # XIAO ESP32-S3 user LED is active-low (LOW = on)
DOT_MS = 150        # base timing unit in ms

led = Pin(LED_PIN, Pin.OUT, value=1 if ACTIVE_LOW else 0)  # start off


def _on():
    led.value(0 if ACTIVE_LOW else 1)


def _off():
    led.value(1 if ACTIVE_LOW else 0)


# SOS sequence: (led_on, duration_ms, serial_char)
# Morse timing: dot=1, dash=3, element-gap=1, letter-gap=3, word-gap=7
_SEQ = [
    # S: ...
    (1, DOT_MS,   '.'), (0, DOT_MS, ''),
    (1, DOT_MS,   '.'), (0, DOT_MS, ''),
    (1, DOT_MS,   '.'), (0, 3*DOT_MS, ' '),
    # O: ---
    (1, 3*DOT_MS, '-'), (0, DOT_MS, ''),
    (1, 3*DOT_MS, '-'), (0, DOT_MS, ''),
    (1, 3*DOT_MS, '-'), (0, 3*DOT_MS, ' '),
    # S: ...
    (1, DOT_MS,   '.'), (0, DOT_MS, ''),
    (1, DOT_MS,   '.'), (0, DOT_MS, ''),
    (1, DOT_MS,   '.'), (0, 7*DOT_MS, '\n'),  # word gap before repeat
]

_idx = 0
_timer = Timer(0)


def _step(t):
    global _idx
    on, duration, ch = _SEQ[_idx % len(_SEQ)]
    _on() if on else _off()
    if ch:
        print(ch, end='' if ch != '\n' else '\n')
    _idx += 1
    _timer.init(mode=Timer.ONE_SHOT, period=duration, callback=_step)


_step(None)
print("SOS started  (... --- ...)")
