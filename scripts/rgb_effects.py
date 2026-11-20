#!/usr/bin/env python3
"""Temporary single-zone RGB animations for compatible ASUS TUF keyboards.

Uses the Linux asus-wmi kbd_rgb_mode sysfs interface. Does not save to firmware.
Requires Python 3.10+ and root privileges for actual hardware writes.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time
from pathlib import Path
from typing import Iterator

RGB = tuple[int, int, int]
RGB_PATH = Path("/sys/class/leds/asus::kbd_backlight/kbd_rgb_mode")

PEACH: RGB = (255, 180, 140)  # #FFB48C — the creator's favorite 🍑
PALETTES: dict[str, tuple[RGB, ...]] = {
    "warm": (
        PEACH,
        (255, 145, 104),  # soft coral
        (255, 175, 80),   # amber
        (255, 212, 139),  # honey
        (255, 116, 126),  # sunset rose
    ),
    "pastel": (
        PEACH,
        (255, 201, 218),  # blush pink
        (206, 189, 255),  # lavender
        (176, 222, 255),  # powder blue
        (173, 238, 215),  # mint
        (255, 237, 186),  # buttercream
    ),
    "rainbow": (
        (255, 45, 78),    # red
        (255, 133, 32),   # orange
        (255, 220, 51),   # yellow
        (45, 225, 96),    # green
        (38, 222, 228),   # cyan
        (67, 117, 255),   # blue
        (166, 85, 255),   # violet
        (250, 93, 201),   # pink
    ),
    "sunset": (
        (255, 190, 111),  # golden peach
        (255, 127, 88),   # coral
        (255, 90, 139),   # pink
        (180, 95, 218),   # violet
        (255, 157, 138),  # soft peach
    ),
}

EFFECTS = ("warm", "pastel", "rainbow", "sunset", "breathing", "heartbeat")


def rgb_command(color: RGB) -> str:
    """Write command=0, mode=0, RGB, speed=0; never persist in firmware."""
    if len(color) != 3 or any(not isinstance(c, int) or c < 0 or c > 255 for c in color):
        raise ValueError("Each RGB channel must be an integer from 0 to 255.")
    return f"0 0 {color[0]} {color[1]} {color[2]} 0\n"


def parse_hex(value: str) -> RGB:
    value = value.lstrip("#")
    if len(value) != 6 or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise argparse.ArgumentTypeError("Use a six-digit color such as #FFB48C")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def lerp(a: RGB, b: RGB, fraction: float) -> RGB:
    return tuple(round(x + (y - x) * fraction) for x, y in zip(a, b))  # type: ignore[return-value]


def palette_frames(name: str, steps: int = 10) -> Iterator[RGB]:
    colors = PALETTES[name]
    for i, left in enumerate(colors):
        right = colors[(i + 1) % len(colors)]
        for step in range(steps):
            yield lerp(left, right, step / steps)


def scale_color(color: RGB, brightness: float) -> RGB:
    return tuple(round(c * brightness) for c in color)  # type: ignore[return-value]


def breathing_frames(color: RGB, steps: int = 32) -> Iterator[RGB]:
    """Ease between 18% and 100% light; a smooth full-keyboard pulse."""
    for step in range(steps):
        phase = 2 * math.pi * step / steps
        level = 0.18 + 0.82 * (1 - math.cos(phase)) / 2
        yield scale_color(color, level)


def heartbeat_frames(color: RGB) -> Iterator[RGB]:
    """Two quick flashes, then a rest (whole keyboard, not a drawn heart)."""
    for level in (0.16, 0.45, 1.0, 0.36, 0.16,
                  0.55, 1.0, 0.40, 0.16, 0.16,
                  0.16, 0.16, 0.16, 0.16, 0.16, 0.16):
        yield scale_color(color, level)


def frames_for(name: str, base: RGB) -> Iterator[RGB]:
    if name in PALETTES:
        return palette_frames(name)
    if name == "breathing":
        return breathing_frames(base)
    if name == "heartbeat":
        return heartbeat_frames(base)
    raise ValueError(f"Unknown effect: {name}")


def write_color(color: RGB) -> None:
    # Sysfs attributes are reopened for each write, as required by many drivers.
    with RGB_PATH.open("w", encoding="ascii") as control:
        control.write(rgb_command(color))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Animate ASUS TUF single-zone RGB without saving to firmware.",
        epilog="Examples: sudo python3 scripts/rgb_effects.py pastel | "
               "python3 scripts/rgb_effects.py rainbow --dry-run --cycles 1",
    )
    parser.add_argument("effect", nargs="?", choices=EFFECTS,
                        help="Animation to play")
    parser.add_argument("--list", action="store_true", help="List available effects")
    parser.add_argument("--interval", type=float, default=0.25,
                        help="Seconds between updates (0.15–5.0; default 0.25)")
    parser.add_argument("--cycles", type=int, default=0,
                        help="Number of loops, 0 = until Ctrl+C (default)")
    parser.add_argument("--color", type=parse_hex, default=PEACH, metavar="HEX",
                        help="Pulse base color for breathing/heartbeat (default #FFB48C)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print commands without writing to hardware or waiting")
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(EFFECTS))
        return 0
    if args.effect is None:
        parser.error("Choose an effect, or use --list.")
    if not math.isfinite(args.interval) or not 0.15 <= args.interval <= 5:
        parser.error("--interval must be between 0.15 and 5 seconds.")
    if args.cycles < 0:
        parser.error("--cycles must be zero or a positive integer.")
    if args.effect in PALETTES and args.color != PEACH:
        parser.error("--color is only supported for breathing and heartbeat.")
    if not args.dry_run:
        if not RGB_PATH.exists():
            print(f"RGB controller not found: {RGB_PATH}", file=sys.stderr)
            return 1
        if os.geteuid() != 0:
            print("Hardware control needs root: use sudo python3 scripts/rgb_effects.py "
                  f"{args.effect}", file=sys.stderr)
            return 1

    cycles = args.cycles or (1 if args.dry_run else None)
    count = 0
    try:
        print(f"Playing {args.effect} (Ctrl+C to stop)." if not args.dry_run
              else f"Preview: {args.effect}", file=sys.stderr)
        while cycles is None or count < cycles:
            for color in frames_for(args.effect, args.color):
                if args.dry_run:
                    print(rgb_command(color), end="")
                else:
                    write_color(color)
                    time.sleep(args.interval)
            count += 1
    except KeyboardInterrupt:
        print("\nEffect stopped; last color remains until changed/reset.",
              file=sys.stderr)
        return 0
    except OSError as exc:
        print(f"Failed to write RGB controller: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
