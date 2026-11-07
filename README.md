# UniGlow

Keyboard backlight and laptop control for Uniwill-based laptops (MECHREVO,
TUXEDO, XMG, Schenker and other Tongfang/Uniwill ODM machines) running the
upstream `uniwill-laptop` kernel driver or the
[tuxedo-drivers](https://gitlab.com/tuxedocomputers/development/packages/tuxedo-drivers)
kernel modules. Native GTK4/libadwaita application with English and Russian UI.

## Features

- Power on/off and brightness (hardware levels)
- Single-zone RGB color: preset palette + custom color picker
- Software effects: breathing and rainbow with adjustable speed
  (the EC exposes no hardware effects on Linux)
- Restore saved state on login (optional autostart entry)
- Headless CLI mode: `uniglow --apply`
- Laptop page (`uniwill-laptop` driver only): CPU/GPU temperatures, both fan
  speeds with PWM duty (read-only, polled every 2 s only while the page is on
  screen), battery charging mode (Full 100 % / Balanced / Stationary),
  Fn lock and Super key lock
- No daemon, no root: a bundled udev rule grants group `users` write access
  to the LED, Fn/Super lock and charging-mode sysfs attributes; brightness
  additionally falls back to systemd-logind `SetBrightness`, which needs no
  extra permissions

## Requirements

- One of:
  - the upstream `uniwill-laptop` driver (platform device `INOU0000:00`),
    providing `/sys/class/leds/uniwill:rgb:kbd_backlight`, the `uniwill`
    hwmon chip, `fn_lock`/`super_key_enable` and the battery `charge_types`;
  - tuxedo-drivers (`uniwill_wmi` + `tuxedo_keyboard`) providing
    `/sys/class/leds/rgb:kbd_backlight` or `white:kbd_backlight` (backlight
    page only). On non-TUXEDO hardware (e.g. MECHREVO) tuxedo-drivers must be
    built with its DMI compatibility check disabled.
- GTK 4.10+, libadwaita 1.7+, python3-gobject

## Install

### Fedora / Nobara (RPM)

Grab the RPM from [Releases](https://github.com/CloudWells/uniglow/releases):

```bash
sudo dnf install ./uniglow-*.noarch.rpm
```

### Manual

```bash
sudo install -m755 uniglow /usr/local/bin/
sudo install -m644 data/70-uniglow-kbd-backlight.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger --subsystem-match=leds --action=change
sudo udevadm trigger --subsystem-match=platform --sysname-match='INOU0000:00' --action=change
sudo udevadm trigger --subsystem-match=power_supply --sysname-match=BAT0 --action=change
```

Make sure your user is a member of group `users` (`id -nG`); if not:
`sudo usermod -aG users $USER` and re-login.

### Build the RPM yourself

```bash
git archive --format=tar.gz --prefix=uniglow-1.2.0/ -o ~/rpmbuild/SOURCES/uniglow-1.2.0.tar.gz HEAD
rpmbuild -bb packaging/uniglow.spec
```

## Usage

Launch **UniGlow** from the app grid, or:

```bash
uniglow            # GUI
uniglow --apply    # apply saved state (used by the autostart entry;
                   # stays resident only while an animated mode is active)
```

The UI language follows the system locale; switch it manually from the
hamburger menu (System / English / Русский).

## Changelog

### 1.2.0 — 2026-11-07

- Support the upstream `uniwill-laptop` kernel driver: LED
  `uniwill:rgb:kbd_backlight` is tried first (tuxedo-drivers names kept as a
  fallback); colors are scaled to the driver's per-channel range from
  `multi_max_intensity` (0..50 on uniwill-laptop, which silently clamps larger
  values and washed colors out to white)
- New **Laptop** page: CPU/GPU temperature, main/secondary fan RPM and PWM
  duty, polled every 2 s on a worker thread only while the page is visible;
  battery charging mode (`charge_types`: Standard / Long_Life / Trickle);
  Fn lock; Super key lock. Writes go through a worker thread; the page is
  hidden when the driver exposes none of it
- udev rule covers the new LED name, `fn_lock` and `super_key_enable` on
  `INOU0000:00` and `charge_types`/`charge_type` on `BAT0`; the RPM `%post`
  re-triggers all three subsystems

### 1.1.0 — 2026-08-14

- Asynchronous coalescing EC writer, live keyboard preview, UI polish

### 1.0.0 — 2026-08-14

- Initial release

## License

MIT
