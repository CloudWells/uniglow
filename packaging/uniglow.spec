Name:           uniglow
Version:        1.1.0
Release:        1%{?dist}
Summary:        Keyboard backlight control for Uniwill laptops (GTK4)
Summary(ru):    Управление подсветкой клавиатуры ноутбуков Uniwill (GTK4)
License:        MIT
URL:            https://github.com/CloudWells/uniglow
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       systemd-udev

%description
Native GTK4/libadwaita application to control the keyboard backlight of
Uniwill-based laptops (MECHREVO, TUXEDO, XMG, Schenker...) driven by the
tuxedo-drivers kernel modules: on/off, brightness, single-zone RGB color,
software breathing/rainbow effects, state restore on login. English and
Russian UI. Ships a udev rule granting group "users" write access to the
LED sysfs attributes.

%description -l ru
Нативное GTK4/libadwaita-приложение для управления подсветкой клавиатуры
ноутбуков на шасси Uniwill (MECHREVO, TUXEDO, XMG, Schenker...) с модулями
ядра tuxedo-drivers: вкл/выкл, яркость, цвет RGB, программные эффекты
«дыхание» и «радуга», восстановление состояния при входе. Интерфейс на
английском и русском.

%prep
%autosetup

%install
install -Dpm 0755 uniglow %{buildroot}%{_bindir}/uniglow
install -Dpm 0644 data/io.github.cloudwells.uniglow.desktop \
    %{buildroot}%{_datadir}/applications/io.github.cloudwells.uniglow.desktop
install -Dpm 0644 data/io.github.cloudwells.uniglow.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.cloudwells.uniglow.svg
install -Dpm 0644 data/70-uniglow-kbd-backlight.rules \
    %{buildroot}%{_udevrulesdir}/70-uniglow-kbd-backlight.rules

%post
udevadm control --reload 2>/dev/null || :
udevadm trigger --subsystem-match=leds --action=add 2>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/uniglow
%{_datadir}/applications/io.github.cloudwells.uniglow.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.cloudwells.uniglow.svg
%{_udevrulesdir}/70-uniglow-kbd-backlight.rules

%changelog
* Fri Aug 14 2026 CloudWells <151101453+CloudWells@users.noreply.github.com> - 1.1.0-1
- Move all EC writes to a coalescing worker thread: the Uniwill EC takes
  ~450 ms per LED write and v1.0.0 wrote from the GTK main loop, freezing
  the UI. Handlers are now instant; only the newest state is written.
- Live keyboard preview canvas with glow (instant feedback, animates effects)
- Brightness as segmented buttons instead of a slider; preset selection ring;
  speed row hidden for static mode; debounced config saves

* Fri Aug 14 2026 CloudWells <151101453+CloudWells@users.noreply.github.com> - 1.0.0-1
- Initial release: on/off, brightness, RGB color with presets, breathing and
  rainbow software effects, EN/RU UI, login state restore, udev rule
