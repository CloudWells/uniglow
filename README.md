# UniGlow

Keyboard backlight control for Uniwill-based laptops (MECHREVO, TUXEDO, XMG,
Schenker and other Tongfang/Uniwill ODM machines) running the
[tuxedo-drivers](https://gitlab.com/tuxedocomputers/development/packages/tuxedo-drivers)
kernel modules. Native GTK4/libadwaita application with English and Russian UI.

## Features

- Power on/off and brightness (hardware levels)
- Single-zone RGB color: preset palette + custom color picker
- Software effects: breathing and rainbow with adjustable speed
  (the EC exposes no hardware effects on Linux)
- Restore saved state on login (optional autostart entry)
- Headless CLI mode: `uniglow --apply`
- No daemon, no root: a bundled udev rule grants group `users` write access
  to the LED sysfs attributes; brightness additionally falls back to
  systemd-logind `SetBrightness`, which needs no extra permissions

## Requirements

- Kernel modules `uniwill_wmi` + `tuxedo_keyboard` (tuxedo-drivers) providing
  `/sys/class/leds/rgb:kbd_backlight` or `/sys/class/leds/white:kbd_backlight`.
  On non-TUXEDO hardware (e.g. MECHREVO) tuxedo-drivers must be built with its
  DMI compatibility check disabled.
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
sudo udevadm trigger --subsystem-match=leds --action=add
```

Make sure your user is a member of group `users` (`id -nG`); if not:
`sudo usermod -aG users $USER` and re-login.

### Build the RPM yourself

```bash
git archive --format=tar.gz --prefix=uniglow-1.1.0/ -o ~/rpmbuild/SOURCES/uniglow-1.1.0.tar.gz HEAD
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

## License

MIT
