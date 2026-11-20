# ASUS TUF RGB Palette — temporary keyboard color commands
# Load once with: source /path/to/keyboard-colors.zsh
# Or add this line to ~/.zshrc (replace with the real path):
# source "$HOME/path/to/tuf-rgb-palette/keyboard-colors.zsh"
# All commands use cmd=0 (apply temporarily, do NOT save to firmware).
# Requires the kernel-provided asus-wmi kbd_rgb_mode interface.

kbd_rgb() {
  if (( $# != 3 )); then
    print -u2 'Usage: kbd_rgb RED GREEN BLUE (0–255)'
    return 2
  fi

  local channel
  for channel in "$@"; do
    if [[ ! "$channel" =~ '^[0-9]{1,3}$' ]] || (( channel > 255 )); then
      print -u2 'RGB channels must be whole numbers from 0 to 255.'
      return 2
    fi
  done

  local rgb_file='/sys/class/leds/asus::kbd_backlight/kbd_rgb_mode'
  if [[ ! -e "$rgb_file" ]]; then
    print -u2 "ASUS RGB interface not found: $rgb_file"
    return 1
  fi

  printf '0 0 %d %d %d 0\n' "$1" "$2" "$3" | sudo tee "$rgb_file" >/dev/null
}

# Copy-and-paste friendly color aliases

# WARM
alias kb-red='kbd_rgb 255 0 0'
alias kb-crimson='kbd_rgb 220 20 60'
alias kb-coral='kbd_rgb 255 100 80'
alias kb-orange='kbd_rgb 255 130 0'
alias kb-amber='kbd_rgb 255 191 0'
alias kb-gold='kbd_rgb 255 180 0'
alias kb-yellow='kbd_rgb 255 255 0'

# GREEN
alias kb-lime='kbd_rgb 170 255 0'
alias kb-green='kbd_rgb 0 255 0'
alias kb-emerald='kbd_rgb 0 200 120'
alias kb-mint='kbd_rgb 0 211 184'
alias kb-teal='kbd_rgb 0 128 128'
alias kb-turquoise='kbd_rgb 48 213 200'

# BLUE
alias kb-cyan='kbd_rgb 0 255 255'
alias kb-ice='kbd_rgb 160 220 255'
alias kb-sky='kbd_rgb 80 160 255'
alias kb-blue='kbd_rgb 0 80 255'
alias kb-royal='kbd_rgb 65 105 225'
alias kb-navy='kbd_rgb 0 0 128'

# PURPLE
alias kb-lavender='kbd_rgb 180 130 255'
alias kb-purple='kbd_rgb 160 50 255'
alias kb-violet='kbd_rgb 128 0 255'
alias kb-magenta='kbd_rgb 255 0 255'
alias kb-fuchsia='kbd_rgb 255 0 170'

# PINK
alias kb-pink='kbd_rgb 255 100 180'
alias kb-hotpink='kbd_rgb 255 20 147'
alias kb-rose='kbd_rgb 255 70 130'
alias kb-peach='kbd_rgb 255 180 140'

# NEUTRAL
alias kb-white='kbd_rgb 255 255 255'
alias kb-warmwhite='kbd_rgb 255 224 185'
alias kb-cream='kbd_rgb 255 243 208'
alias kb-off='kbd_rgb 0 0 0'

# Example: kb-mint
# Any custom color: kbd_rgb 0 211 184
# 'kb-off' sets static RGB to 0,0,0; hardware may handle darkness differently.
