# UniGlow

Keyboard backlight control for Uniwill-based laptops (MECHREVO, TUXEDO, XMG,
Schenker and other Tongfang/Uniwill ODM machines) running the
[tuxedo-drivers](https://gitlab.com/tuxedocomputers/development/packages/tuxedo-drivers)
kernel modules. Native GTK4/libadwaita app, English/Russian UI.

**Features**

- On/off, brightness (hardware levels), single-zone RGB color with presets
- Software effects: breathing, rainbow (the EC has no hardware effects on Linux)
- Restore state on login (optional autostart), `uniglow --apply` CLI
- No daemon, no root: ships a udev rule granting group `users` write access
  to the LED; brightness additionally falls back to systemd-logind

**Requirements**

- Kernel modules `uniwill_wmi` + `tuxedo_keyboard` loaded
  (device `/sys/class/leds/rgb:kbd_backlight` or `white:kbd_backlight`)
- GTK 4.10+, libadwaita 1.7+, python3-gobject

**Install (Fedora/Nobara)**

```bash
sudo dnf install uniglow-*.rpm       # from Releases
```

or manually:

```bash
sudo install -m755 uniglow /usr/local/bin/
sudo install -m644 data/70-uniglow-kbd-backlight.rules /etc/udev/rules.d/
sudo udevadm control --reload && sudo udevadm trigger --subsystem-match=leds --action=add
```

Make sure your user is in group `users` (`id -nG`), otherwise
`sudo usermod -aG users $USER` and re-login.

---

# UniGlow (по-русски)

Управление подсветкой клавиатуры для ноутбуков на шасси Uniwill (MECHREVO,
TUXEDO, XMG, Schenker и другие), работающих на модулях ядра tuxedo-drivers.
Нативное приложение GTK4/libadwaita, интерфейс на английском и русском.

**Возможности**

- Вкл/выкл, яркость (аппаратные уровни), цвет RGB одной зоной, пресеты
- Программные эффекты: дыхание, радуга (аппаратных режимов у EC в Linux нет)
- Восстановление состояния при входе (автостарт), CLI-режим `uniglow --apply`
- Без демона и без root: в комплекте udev-правило, дающее группе `users`
  запись в LED; яркость дополнительно умеет ходить через systemd-logind

**Требования**: загруженные модули `uniwill_wmi` + `tuxedo_keyboard`
(устройство `/sys/class/leds/rgb:kbd_backlight` или `white:kbd_backlight`),
GTK 4.10+, libadwaita 1.7+, python3-gobject.

Установка — RPM из Releases либо вручную (см. команды выше). Пользователь
должен состоять в группе `users`.

## License

MIT
