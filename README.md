# 🎨 TUF RGB Palette

**Pick a color. Copy a command. Change your ASUS TUF keyboard glow on Linux.**

A lightweight, self-contained, offline-friendly color palette for ASUS TUF laptops exposing the Linux `asus-wmi` keyboard RGB sysfs interface. Includes **32 curated colors**, a **custom HEX picker**, and ready-to-source **Zsh aliases**.

> **Designed around:** ASUS TUF Gaming F15 FX507ZM, Ubuntu 22.04, kernel 6.8. Other devices might work if they expose the same sysfs interface. This repository does not install drivers or guarantee compatibility with other models.

## ✨ Features

- 🌈 Click any color swatch to copy its **full terminal command**.
- 🎨 Pick any custom HEX color and automatically generate RGB values.
- 🔎 Search and filter shades by name, category, HEX code, or alias.
- ⌨️ Copy a short `kb-*` alias after installing the Zsh helpers.
- 📴 Works offline; `index.html` requires **no build, dependencies, or external assets**.
- 🔒 No analytics or network requests required for the color picker.
- 💾 **Temporary changes by default** — does *not* write a persistent firmware color.

## 🚀 Use the color picker

Download or clone the repository, then open `index.html` in a browser. Click any swatch and paste the copied command into a Linux terminal. The browser copies the command; **it does not directly control your keyboard**.

```bash
git clone https://github.com/fatemeh-mohseni-AI/tuf-rgb-palette.git
cd tuf-rgb-palette
xdg-open index.html
```

Some browsers restrict the Clipboard API when opening a `file://` URL. The app also tries a local-browser fallback and, if copying is unavailable, displays selectable text for manual copy.

### Example terminal command

```bash
# Mint: temporary static RGB (0, 211, 184)
printf '0 0 0 211 184 0\n' | sudo tee /sys/class/leds/asus::kbd_backlight/kbd_rgb_mode
```

For the interface format, six values mean `command mode red green blue speed`:

| Value | Example | Meaning |
| --- | --- | --- |
| `command` | `0` | Apply temporarily (`1` asks firmware to save; **not used here**) |
| `mode` | `0` | Static color |
| `red`, `green`, `blue` | `0 211 184` | RGB color channels, each 0–255 |
| `speed` | `0` | Ignored for static color |

The command uses `sudo tee` to write to sysfs. Linux may prompt for your administrator password. Depending on your laptop firmware, temporary colors may reset at reboot or after power-state changes.

## 🐚 Optional: Zsh aliases

Source the helper file in your current Zsh session:

```zsh
source /absolute/path/to/tuf-rgb-palette/keyboard-colors.zsh
kb-mint
kb-purple
kb-ice
kb-warmwhite
```

To load aliases automatically in new Zsh terminals, add one `source` line to your `~/.zshrc` (replace the path with the actual location):

```zsh
source "$HOME/path/to/tuf-rgb-palette/keyboard-colors.zsh"
```

To set any custom RGB color without an alias:

```zsh
kbd_rgb 0 211 184
```

The helper validates values and checks that the kernel interface exists before attempting the write.

## 🎨 Included aliases

| Family | Aliases |
| --- | --- |
| Warm | `kb-red`, `kb-crimson`, `kb-coral`, `kb-orange`, `kb-amber`, `kb-gold`, `kb-yellow` |
| Green | `kb-lime`, `kb-green`, `kb-emerald`, `kb-mint`, `kb-teal`, `kb-turquoise` |
| Blue | `kb-cyan`, `kb-ice`, `kb-sky`, `kb-blue`, `kb-royal`, `kb-navy` |
| Purple | `kb-lavender`, `kb-purple`, `kb-violet`, `kb-magenta`, `kb-fuchsia` |
| Pink | `kb-pink`, `kb-hotpink`, `kb-rose`, `kb-peach` |
| Neutral | `kb-white`, `kb-warmwhite`, `kb-cream`, `kb-off` |

> `kb-off` requests static RGB `(0,0,0)`. Whether that looks fully off varies with hardware.

## ✅ Compatibility check

```bash
uname -r
ls /sys/class/leds/asus::kbd_backlight/kbd_rgb_mode
```

If the path is missing, this approach will not work as-is. Avoid writing arbitrary values to other sysfs device paths.

## 🌐 Publish on GitHub Pages

For a public repository, open **Settings → Pages**, choose **Deploy from a branch**, then select `main` and `/ (root)`. GitHub will publish the static `index.html` at:

`https://fatemeh-mohseni-ai.github.io/tuf-rgb-palette/`

That address will work **after** GitHub Pages is enabled and its deployment completes. Locally opening `index.html` continues to work without GitHub Pages or internet access.

## 🔧 Tech

Vanilla HTML, CSS and JavaScript — no bundler, packages, server, external images or web fonts. Source is simple enough to modify. The colors in `index.html` and `keyboard-colors.zsh` should be kept in sync when extending the palette.

## License

MIT — see [LICENSE](LICENSE).