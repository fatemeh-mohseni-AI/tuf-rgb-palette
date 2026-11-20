<p align="center">
  <img src="assets/hero.svg" alt="TUF RGB Palette — a glowing RGB keyboard on a dark background" width="100%" />
</p>

<h3 align="center">Choose your glow. One click, one command. ✨</h3>

<p align="center">
  A tiny, beautiful, offline-friendly RGB color picker for ASUS TUF keyboards on Linux.<br />
  <strong>32 colors · 6 animated effects · Peach favorite 🍑 · Zsh aliases · No firmware saving</strong>
</p>

<p align="center">
  <a href="https://fatemeh-mohseni-ai.github.io/tuf-rgb-palette/"><img alt="Open live palette" src="https://img.shields.io/badge/OPEN_LIVE_PALETTE-00d3b8?style=for-the-badge&labelColor=161a2d" /></a>
  <a href="https://github.com/fatemeh-mohseni-AI/tuf-rgb-palette/blob/main/keyboard-colors.zsh"><img alt="Zsh aliases" src="https://img.shields.io/badge/ZSH_ALIASES-b5a1ff?style=for-the-badge&labelColor=161a2d" /></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/LICENSE-MIT-fc9cda?style=for-the-badge&labelColor=161a2d" /></a>
</p>

<p align="center">
  <a href="https://fatemeh-mohseni-ai.github.io/tuf-rgb-palette/"><strong>🌈 Try the web app</strong></a>
  &nbsp;·&nbsp;
  <a href="#-quick-start"><strong>⚡ Quick start</strong></a>
  &nbsp;·&nbsp;
  <a href="#-color-collection"><strong>🎨 Browse colors</strong></a>
  &nbsp;·&nbsp;
  <a href="#-animated-effects"><strong>✨ Animated effects</strong></a>
</p>

---

## 💡 What is TUF RGB Palette?

A lightweight color palette that turns a colorful swatch into a **ready-to-paste Linux terminal command**. No Armoury Crate, daemon, or extra RGB driver installation is required **when your laptop already exposes the compatible kernel interface**.

Built around an **ASUS TUF Gaming F15 FX507ZM** running **Ubuntu 22.04 with Linux kernel 6.8**. It may work on other ASUS TUF devices with the same `asus-wmi` sysfs interface; those models are not verified here.

> [!IMPORTANT]
> The website **only copies commands to your clipboard**; it cannot directly control your keyboard. Run the copied command on a compatible Linux machine. Every provided command uses the **temporary** setting, not the firmware-save setting.

## 🍑 Creator’s favorite: Peach

**Peach (`#FFB48C`)** is the creator’s favorite color. It is highlighted in the web palette, selected by default, and used for both the Breathing and Heartbeat effects. Type `kb-peach` for a static Peach glow.

## ✨ Highlights

| | Feature | What it does |
|:--:|---|---|
| 🎨 | **32 hand-picked shades** | Warm, green, blue, purple, pink & neutral |
| 🖱️ | **One-click copy** | Click a swatch to copy the full Linux command |
| 🌈 | **Custom color picker** | Choose any HEX color and generate an RGB command |
| 🔎 | **Search & filters** | Find colors by name, group, HEX or alias |
| ⌨️ | **Zsh shortcuts** | Type `kb-peach`, `kb-mint`, `kb-ice` and more |
| ✨ | **Six animated effects** | Warm, Pastel, Rainbow, Sunset, Breathing and Heartbeat |
| 📴 | **Offline by design** | Open `index.html` directly; no packages or build step |
| 💾 | **No firmware save** | RGB changes are requested for the current session only |

## 🚀 Quick start

**Option A — use the website**

### [🌐 Open the interactive palette](https://fatemeh-mohseni-ai.github.io/tuf-rgb-palette/)

Pick a color → click to copy → paste into your terminal. That's it.

**Option B — run it completely offline**

```bash
git clone https://github.com/fatemeh-mohseni-AI/tuf-rgb-palette.git
cd tuf-rgb-palette
xdg-open index.html
```

The page uses plain HTML, CSS and JavaScript; no external images, scripts, fonts, trackers or network requests are needed to use the color picker. If a browser blocks automatic copying from a local `file://` page, the app provides a manual copy fallback.

### 🐚 Optional: install the Zsh shortcuts

Clone the repository **inside your home directory**, then add its helper script to Zsh:

```zsh
cd "$HOME"
git clone https://github.com/fatemeh-mohseni-AI/tuf-rgb-palette.git
echo 'source "$HOME/tuf-rgb-palette/keyboard-colors.zsh"' >> ~/.zshrc
source ~/.zshrc
```

Now use any of the aliases:

```zsh
kb-peach       # creator’s favorite 🍑
kb-mint        # fresh teal-green
kb-purple      # violet glow
kb-ice         # icy blue
kb-rose        # rosy pink
kb-warmwhite   # warm white
kb-off         # request static black (0, 0, 0)
```

Or pick any custom RGB combination (0–255 per channel):

```zsh
kbd_rgb 0 211 184
```

> Already cloned elsewhere? Edit the `source` path in `~/.zshrc` to point to your actual copy of `keyboard-colors.zsh`. Add the line only once.

## ✨ Animated effects

Six **single-zone** animations run locally through Python 3's standard library (no Python packages to install). Each frame updates the **whole keyboard to one color**; this hardware cannot draw per-key shapes.

| Effect | Mood | Command (after loading Zsh aliases) |
|---|---|---|
| ☀️ **Warm Tones** | Peach → coral → amber → honey → rose | `kb-fx-warm` |
| 🫧 **Soft Pastels** | Blush → lavender → powder blue → mint → buttercream | `kb-fx-pastel` |
| 🌈 **Rainbow** | A full spectrum of smoothly changing colors | `kb-fx-rainbow` |
| 🌇 **Sunset** | Golden peach → coral → pink → violet | `kb-fx-sunset` |
| 🍑 **Peach Breathing** | Peach softly brightens and dims | `kb-fx-breathing` |
| 💓 **Peach Heartbeat** | Two short pulses followed by a pause | `kb-fx-heartbeat` |

### Run an animation

From **inside the cloned repository**, choose an effect:

```bash
sudo python3 scripts/rgb_effects.py warm
sudo python3 scripts/rgb_effects.py pastel
sudo python3 scripts/rgb_effects.py rainbow
```

Or, if you sourced `keyboard-colors.zsh`, use the convenient Zsh aliases:

```zsh
kb-fx-warm
kb-fx-pastel
kb-fx-rainbow
kb-fx-sunset
kb-fx-breathing
kb-fx-heartbeat
```

**Stop with `Ctrl+C`**. The last color stays in place until changed or reset by the system. This does not modify firmware settings, does not start automatically, and makes no background service.

Try running an effect for a limited number of loops:

```bash
sudo python3 scripts/rgb_effects.py pastel --cycles 2
```

Tune update speed (larger interval = slower and fewer hardware writes):

```bash
sudo python3 scripts/rgb_effects.py rainbow --interval 0.5
```

Make Heartbeat pulse in a different color (defaults to Peach):

```bash
sudo python3 scripts/rgb_effects.py heartbeat --color '#FFB48C'
```

Preview the exact write commands without `sudo` or an ASUS laptop:

```bash
python3 scripts/rgb_effects.py warm --dry-run --cycles 1
```

> [!NOTE]
> The website's Effects cards copy the command, **not** the animation itself. You must clone the repository to run Python effects on your laptop. If your keyboard updates slowly or appears to skip frames, try `--interval 0.5` or higher. Avoid running multiple effects at once; they would compete for the same sysfs device.

## 🎨 Color collection

Here are a few favorites from the **32 built-in presets**:

| Shade | HEX | Zsh command | Mood |
|---|---|---|---|
| 🍑 **Peach ★** | `#FFB48C` | `kb-peach` | **Creator’s favorite** |
| 🟢 Mint | `#00D3B8` | `kb-mint` | Cool & fresh |
| 🟣 Purple | `#A032FF` | `kb-purple` | Dreamy |
| 🔵 Sky | `#50A0FF` | `kb-sky` | Soft blue |
| 🩵 Ice | `#A0DCFF` | `kb-ice` | Frosted |
| 🩷 Rose | `#FF4682` | `kb-rose` | Warm pink |
| 🟠 Amber | `#FFBF00` | `kb-amber` | Golden hour |
| 🟢 Emerald | `#00C878` | `kb-emerald` | Bright green |
| ⚪ Warm White | `#FFE0B9` | `kb-warmwhite` | Cozy desk |

<details>
<summary><strong>See all 32 Zsh aliases</strong></summary>

| Family | Aliases |
|---|---|
| 🔴 **Warm** | `kb-red` · `kb-crimson` · `kb-coral` · `kb-orange` · `kb-amber` · `kb-gold` · `kb-yellow` |
| 🟢 **Green** | `kb-lime` · `kb-green` · `kb-emerald` · `kb-mint` · `kb-teal` · `kb-turquoise` |
| 🔵 **Blue** | `kb-cyan` · `kb-ice` · `kb-sky` · `kb-blue` · `kb-royal` · `kb-navy` |
| 🟣 **Purple** | `kb-lavender` · `kb-purple` · `kb-violet` · `kb-magenta` · `kb-fuchsia` |
| 🩷 **Pink** | `kb-pink` · `kb-hotpink` · `kb-rose` · `kb-peach` |
| ⚪ **Neutral** | `kb-white` · `kb-warmwhite` · `kb-cream` · `kb-off` |

</details>

Actual LED colors may look different from a monitor swatch. `kb-off` sends RGB (0, 0, 0); the visual result depends on the keyboard firmware.

## 🛠️ How it works

If your laptop has the supported interface, the website generates a command like this:

```bash
# Mint / static RGB / temporary (not stored in firmware)
printf '0 0 0 211 184 0\n' | sudo tee /sys/class/leds/asus::kbd_backlight/kbd_rgb_mode
```

The six values are `command mode red green blue speed`:

| Part | Value | Purpose |
|---|---|---|
| Command | `0` | Apply temporarily; don't ask firmware to save |
| Mode | `0` | Static color |
| RGB | `0 211 184` | Red, green and blue (0–255) |
| Speed | `0` | Not relevant for static mode |

The color may reset after restarting, sleeping, or changing power states, depending on your hardware. Animated effects use repeated writes to the same temporary interface; they are software-controlled and stop when the Python process exits. `sudo` may prompt for your password when writing to the sysfs interface.

### ✅ Check compatibility

```bash
uname -r
ls /sys/class/leds/asus::kbd_backlight/kbd_rgb_mode
```

If that path is missing, this project won't work as-is: it does **not** install or modify kernel drivers. Do not substitute unverified sysfs paths or arbitrary values.

## 📁 Project structure

```text
tuf-rgb-palette/
├── assets/
│   └── hero.svg            # README banner
├── index.html              # Offline-friendly interactive palette
├── keyboard-colors.zsh     # 32 colors + 6 effect shortcuts
├── scripts/
│   └── rgb_effects.py      # Temporary, single-zone RGB effects
├── tests/
│   └── test_rgb_effects.py # Hardware-free Python tests
├── README.md               # This guide
└── LICENSE                 # MIT
```

## 🧪 Tests

Run the built-in tests without any ASUS hardware or administrator permissions:

```bash
python3 -m unittest discover -s tests -v
```

These tests check RGB ranges, command format (temporary mode only), animation frames and dry-run behavior.

## 🤝 Contributing

Have another compatible ASUS model, a favorite RGB shade, or a UI improvement? Issues and pull requests are welcome. If you add or edit presets, please keep the colors in `index.html` and `keyboard-colors.zsh` in sync.

## 📄 License

[MIT](LICENSE) · Built with 💜 for Linux & colorful keyboards.

<p align="center"><a href="https://fatemeh-mohseni-ai.github.io/tuf-rgb-palette/"><strong>🌈 Open the palette and find your glow</strong></a></p>
