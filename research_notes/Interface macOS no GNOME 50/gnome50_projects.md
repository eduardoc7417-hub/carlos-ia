# macOS look and feel on GNOME Shell 50: candidate projects (status 2026-10-31)

**How to read the evidence labels.** All data was collected on 2026-10-31. Nothing was run on a GNOME 50 machine, so no entry here is a runtime test.

- **PROVEN (declared):** extensions.gnome.org (EGO) lists shell 50 for that extension. "+repo" means the repo's `metadata.json` also contains 50. This is the strongest evidence collected. It shows declared and listed support, not that the extension works well with the others.
- **CLAIMED:** only the maintainer's repo, README or changelog says so, and EGO does not confirm it. All themes fall here because they have no metadata or listing mechanism.
- **UNVERIFIED:** no evidence for 50 was found.
- **NOT SUPPORTED:** both EGO and the repo stop before 50, or EGO stops before 50 and no repo was checked.

**Data limits.**
- "Last push" is GitHub `pushed_at`, which counts a push to any branch. It is not necessarily a default-branch commit or a release.
- EGO per-version upload dates were not collected.
- "n/c" means not checked. The GitHub API rate limit ran out, so some repos have no license or date.
- Issue-tracker sweeps were done only for WhiteSur and MacTahoe. Extension issue trackers were not reviewed for GNOME 50 bugs.

**Platform context.**
- Ubuntu 26.04 LTS ships GNOME 50, and Yaru moved closer to upstream GNOME styling — [Ubuntu release notes](https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/).
- Mutter 50 alpha removed the X11 backend and Shell removed its X11 code. XWayland remains for X11 apps — [Phoronix](https://www.phoronix.com/news/GNOME-Mutter-Shell-50-Alpha).
- GNOME's [release notes for 50](https://release.gnome.org/50/) say nothing on extensions or themes.
- GNOME 51 already exists in the wild: an [issue reporter](https://github.com/vinceliuice/WhiteSur-gtk-theme/issues/1440) runs Shell 51.1 with gtk4 4.24.1 and libadwaita 1.10.0, and many extensions below already list 51.

## GTK/Shell themes and libadwaita handling

### Takeaway
WhiteSur and MacTahoe are the only serious maintained macOS-style themes found, and GNOME 50 support for both is CLAIMED, not proven. Both style libadwaita apps only by overwriting per-user `~/.config/gtk-4.0`, so neither has a clean system-wide route for a distro. The recommended pick is **WhiteSur** because its GNOME 50 fixes are explicit and the one GNOME 50 issue reviewed was attributed by its reporter to another component (a limited search, not a full tracker sweep). **MacTahoe** is the fallback, or the pick if the Tahoe look matters more than polish.

### Cited Findings

| Project | Role | License | Last push / latest release | Activity | GNOME 50 status and evidence |
|---|---|---|---|---|---|
| [WhiteSur-gtk-theme](https://github.com/vinceliuice/WhiteSur-gtk-theme) | **Pick** | MIT | 2026-09-11 / 2026-09-10 | 9.4k stars, 555 open issues, monthly releases | **CLAIMED.** Changelog has ["Gnome50 compat" #1420 (2026-08-08) and "fix nautilus gnome 50 issues" #1408 (2026-07-07)](https://github.com/vinceliuice/WhiteSur-gtk-theme/releases) |
| [MacTahoe-gtk-theme](https://github.com/vinceliuice/MacTahoe-gtk-theme) | **Fallback** | MIT | 2026-09-28 / 2026-09-10 | 1.7k stars, 102 open issues, monthly releases | **CLAIMED.** ["Fixed GNOME 50 issues" in release 2026-05-24](https://github.com/vinceliuice/MacTahoe-gtk-theme/releases), but [4 GNOME 50 / 26.04 issues appear open](https://github.com/vinceliuice/MacTahoe-gtk-theme/issues?q=gnome+50) |
| [GNOME-macOS-Tahoe (kayozxo)](https://github.com/kayozxo/GNOME-macOS-Tahoe) | Reference only | No license detected by GitHub | 2026-08-22 | 1.1k stars | **UNVERIFIED.** [Page lists no GNOME versions](https://github.com/kayozxo/GNOME-macOS-Tahoe). Do not ship without a license |
| [adw-gtk3](https://github.com/lassekongo83/adw-gtk3) | Non-macOS, non-invasive alternative for GTK3 apps | LGPL-2.1 | 2026-05-07 | 2k stars | **UNVERIFIED** for 50 |

**Installer behavior (read from source)**
- For any shell version 48 or later, both installers map to `GNOME_VERSION="48-0"`, so GNOME 50 receives the 48 code path. There is no 50-specific branch in the version detection — [WhiteSur lib-core.sh](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/libs/lib-core.sh); [MacTahoe lib-core.sh](https://raw.githubusercontent.com/vinceliuice/MacTahoe-gtk-theme/main/libs/lib-core.sh).
- Both installers have an `-l/--libadwaita` flag that installs into the gtk-4.0 config and refuse to run it under sudo ("Do not run '--libadwaita' option with sudo!") — [WhiteSur install.sh](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/install.sh); [MacTahoe install.sh](https://raw.githubusercontent.com/vinceliuice/MacTahoe-gtk-theme/main/install.sh).
- MacTahoe also offers a blur variant of the libadwaita install (`./install.sh -b -l`) — [MacTahoe README](https://raw.githubusercontent.com/vinceliuice/MacTahoe-gtk-theme/main/README.md).

**The libadwaita method and its limits**
- The READMEs state that libadwaita does not support custom themes and the method overwrites the gtk-4.0 config. All GTK4 apps get one fixed theme with no dark-mode switching, and changing theme means overwriting again. The section is titled "not perfect" — [WhiteSur README](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/README.md).
- A GNOME developer described `~/.config/gtk-4.0/gtk.css` and `GTK_THEME` as working but said none of it is officially supported — [alatiera blog, 2021](https://blogs.gnome.org/alatiera/2021/09/18/the-truth-they-are-not-telling-you-about-themes/); [GNOME Discourse](https://discourse.gnome.org/t/why-and-how-libadwaita-prevents-theming/17079).
- A Discourse reply says `GTK_THEME` is a debugging tool and that libadwaita might start unsetting it. Whether that shipped was not verified — [GNOME Discourse](https://discourse.gnome.org/t/why-gtk-theme-env-breaks-adwaita-applications/16016).
- Flatpak needs `flatpak override --filesystem=xdg-config/gtk-3.0` and `xdg-config/gtk-4.0`. The theme-connect option `-F` builds a GTK3 runtime theme only — [WhiteSur README](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/README.md); [lib-flatpak.sh](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/libs/lib-flatpak.sh).

**Known GNOME 50 and 51 field reports**
- MacTahoe, open: [#93 Files top bar on GNOME 50, #96 square corner shades, #97 Nautilus shadow mismatch, #148 GDM on Ubuntu 26.04](https://github.com/vinceliuice/MacTahoe-gtk-theme/issues?q=gnome+50). Status was read from a search listing page, and these may have been partly addressed by later commits.
- WhiteSur [#1399](https://github.com/vinceliuice/WhiteSur-gtk-theme/issues/1399) (white line on the panel, Ubuntu 26.04 / GNOME 50): the reporter later attributed it to Ubuntu's Desktop Icons NG, not the theme. There is no maintainer reply.
- WhiteSur [#1440](https://github.com/vinceliuice/WhiteSur-gtk-theme/issues/1440) (GNOME 51.1 only): severe stutter and closure assertion errors with User Themes. The root cause is unidentified and the theme link is only the reporter's suspicion. It does not apply to 50 as reported, but it is a risk signal for later upgrades.

### Inferences
- A distro can package the GTK3 and Shell parts into `/usr/share/themes`, since the installer has a root path. The libadwaita part has no system-wide equivalent in these installers. The realistic options are `/etc/skel` for new users only, or a first-login user service that copies files into `~/.config/gtk-4.0`. Either one must own and version those files, and it may clobber user CSS.
- Because the override is fixed to one variant, automatic light/dark switching needs a custom swap mechanism. MacTahoe's recent "gnome-theme-switcher app" ([release notes](https://github.com/vinceliuice/MacTahoe-gtk-theme/releases)) may be relevant, but it was not inspected.
- The least invasive design is to treat libadwaita CSS as a separate, optional, tested layer per GTK/libadwaita version, because the mechanism is unsupported and can break on any update.

### Gaps
- No source specific to GTK 4.22 or libadwaita 1.9 behavior or CSS changes was found, so the libadwaita override on 1.9 is UNVERIFIED beyond the fixes noted above.
- The [Shell theme's dependency on User Themes](https://extensions.gnome.org/extension/19/user-themes/) (listed for 48–51) is known, but no one has documented a distro packaging of these themes on 26.04.
- Whether WhiteSur has unreported 50 problems was not assessed. A search found few reports, which does not show absence of bugs.

## Icons and cursors (licenses, Apple-derived artwork)

### Takeaway
Themes and cursors are maintained and GPL-3.0, but GPL labels do not resolve Apple-artwork or trademark risk. The repository contents could not be audited. For a distributable OS, treat any asset set that copies macOS icons or the Apple logo as a legal review item before shipping.

### Cited Findings

| Project | Role | License (repo declared) | Last push | GNOME 50 relevance | Apple-related evidence |
|---|---|---|---|---|---|
| [WhiteSur-icon-theme](https://github.com/vinceliuice/WhiteSur-icon-theme) | **Pick** (subject to legal review) | GPL-3.0 | 2026-09-10 | Icon themes are toolkit-level. No 50-specific evidence: UNVERIFIED | [README installer option](https://raw.githubusercontent.com/vinceliuice/WhiteSur-icon-theme/master/README.md) "Replace Apple logo with KDE Plasma logo", so an Apple logo ships by default |
| [MacTahoe-icon-theme](https://github.com/vinceliuice/MacTahoe-icon-theme) | Fallback | GPL-3.0 | 2026-09-10 | UNVERIFIED | README search found no license or Apple statement. Audit needed |
| [WhiteSur-cursors](https://github.com/vinceliuice/WhiteSur-cursors) | **Pick (cursor)** | GPL-3.0 | 2025-04-05 (stale but simple) | UNVERIFIED | ["Inspired by macOS and based on capitaine-cursors"](https://raw.githubusercontent.com/vinceliuice/WhiteSur-cursors/master/README.md) |
| [apple_cursor](https://github.com/ful1e5/apple_cursor) | Fallback | GPL-3.0 | 2024-09-28 | UNVERIFIED | Name uses "Apple" and it ships [macOS variants](https://raw.githubusercontent.com/ful1e5/apple_cursor/main/README.md). SVGs are in the repo. Provenance not stated in the lines read |
| [McMojave-cursors](https://github.com/vinceliuice/McMojave-cursors) | Not recommended | GPL-3.0 | 2021-02-24 | UNVERIFIED | Stale |

- The WhiteSur and MacTahoe GTK installers also expose an `apple` icon option for the panel Activities icon among other logos — [WhiteSur README](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/README.md).
- Search results gave the GPL-3.0 listing and a description of the WhiteSur icons as recreating the Big Sur look, but no legal analysis — [SourceForge mirror](https://sourceforge.net/projects/whitesur-icon-theme.mirror/). A third-party RPM package exists — [Alcance Libre](https://joel-lenovo.alcancelibre.org/aldos/1.4/updates/x86_64/repoview/whitesur-icon-theme.html).

### Inferences
- A GPL file on a repo only licenses what the author could license. It does not grant rights to Apple's trademarks or to any copied Apple icon designs. This is an inference, not legal advice.
- A safer distro baseline is to replace the Apple logo with the distro's own logo in every asset. Prefer "inspired by" sets, and have the app icons reviewed individually for close copies.

### Gaps
- The file-tree audit for Apple-named assets failed because the GitHub API was rate-limited (403). Which icon files derive from Apple artwork remains **unknown**.
- No Debian or Fedora packaging review or legal position on these themes was found.

## Dock extensions

### Takeaway
**Dash to Dock** is the most robust dock on GNOME 50 but its schema has no magnification. **Dash2Dock Animated** is the proven-listed option with real magnification and built-in blur, at the cost of a smaller project with an AI-assisted maintenance model. For an honest macOS look use Dash2Dock Animated. For stability use Dash to Dock with Blur my Shell and optionally a bounce layer.

### Cited Findings

| Extension | Role | License | Last push | Activity | GNOME 50 | Magnification | Blur | Autohide |
|---|---|---|---|---|---|---|---|---|
| [Dash2Dock Animated](https://extensions.gnome.org/extension/4994/dash2dock-lite/) ([repo](https://github.com/icedman/dash2dock-lite)) | **Pick for macOS feel** | GPL-3.0 | 2026-10-15 | 355 stars, 166 open | **PROVEN +repo** (EGO to 50, repo metadata 45–50, no 51 yet) | Yes: `animation-magnify` key in [schema](https://raw.githubusercontent.com/icedman/dash2dock-lite/main/schemas/org.gnome.shell.extensions.dash2dock-lite.gschema.xml) | Yes: `blur-background` key | Yes: `autohide-dash` key |
| [Dash to Dock](https://extensions.gnome.org/extension/307/dash-to-dock/) ([repo](https://github.com/micheleg/dash-to-dock)) | **Fallback / stable base** | GPL-2.0 | 2026-10-08 | 4.4k stars, 836 open | **PROVEN +repo** (EGO to 51, metadata 45–51) | No key: [schema](https://raw.githubusercontent.com/micheleg/dash-to-dock/master/schemas/org.gnome.shell.extensions.dash-to-dock.gschema.xml) has 0 "magnif" matches | Via [Blur my Shell](https://github.com/aunetx/blur-my-shell) | Yes: autohide and intellihide keys |
| [WACK Cupertino Dock Lite](https://extensions.gnome.org/extension/10108/wack-cupertino-dock-lite/) | Add-on to Dash to Dock | n/c | n/c | n/c | PROVEN (EGO 46–50) | Description covers bounce animations and theming; magnification not confirmed | n/c | Relies on Dash to Dock |
| [MacOS Dock](https://extensions.gnome.org/extension/10719/macos-dock/) | Watch | n/c | n/c | n/c | PROVEN (EGO 45–50) | [Self-described](https://github.com/vinnytherobot/MacOSDock) | n/c | n/c |
| [Docka](https://extensions.gnome.org/extension/10270/docka/) / [Native Dock](https://extensions.gnome.org/extension/11144/native-dock/) | Minimal alternatives | n/c | n/c | n/c | PROVEN (46–50 / 50–51) | Not claimed | n/c | Docka: yes, per description |
| [Dash to Panel](https://extensions.gnome.org/extension/1160/dash-to-panel/) | Not macOS-like | n/c | n/c | n/c | PROVEN (48–51) | n/a | n/a | n/a |
| [Dock from Dash](https://extensions.gnome.org/extension/4703/dock-from-dash/) | Avoid | n/c | n/c | n/c | **NOT SUPPORTED** (EGO to 49) | n/a | n/a | n/a |

- Dash2Dock's README says maintenance and version updates are "now primarily assisted by AI" and that EGO reviewer policies mean updates may no longer reach EGO and will come primarily through the repo. It also lists GNOME 50 support — [README](https://raw.githubusercontent.com/icedman/dash2dock-lite/main/README.md).
- Blur my Shell's README lists static or dynamic blur for Dash to Dock — [repo](https://www.GitHub.com/aunetx/blur-my-shell).
- A third-party summary says Ubuntu 26.04's Ubuntu Dock is fully opaque — [knightli](https://knightli.com/en/2026/04/26/ubuntu-26-04-lts-release-notes/).

### Inferences
- A distro should expect to vendor Dash2Dock from tagged repo releases rather than rely on EGO, and pin versions.
- The AI-assisted maintenance note is a governance signal to weigh, not proof of poor quality.
- Ubuntu Dock is a Dash to Dock derivative on Ubuntu, so a replacement dock should be enabled only with Ubuntu Dock removed or disabled. Conflict behavior between them on 26.04 was not tested.

### Gaps
- No GNOME 50 issue review was done for either dock.
- Magnification smoothness, multi-monitor behavior and CPU cost are unmeasured.
- Support for Dash to Dock with Blur my Shell on GNOME 50 together is unverified. Search returned nothing on 50 specifically.

## Blur, rounded windows, window animations, left-side buttons

### Takeaway
All key pieces have listed GNOME 50 support and none found is Mutter-patched. Rounded Window Corners Reborn is the weakest link for upgrade continuity, because its main branch metadata lists only 50 and its last push is from July. Left-side buttons are a plain gsetting.

### Cited Findings

| Category | Project | Role | License | Last push | Activity | GNOME 50 |
|---|---|---|---|---|---|---|
| Blur | [Blur my Shell](https://extensions.gnome.org/extension/3193/blur-my-shell/) ([repo](https://github.com/aunetx/blur-my-shell)) | **Pick** | GPL-3.0 | 2026-10-31 | 2.4k stars, 49 open, very active | **PROVEN +repo** (EGO to 51, metadata 46–51) |
| Blur | Dash2Dock's own blur | Fallback (dock only) | GPL-3.0 | 2026-10-15 | see above | PROVEN +repo |
| Rounded | [Rounded Window Corners Reborn](https://extensions.gnome.org/extension/7048/rounded-window-corners-reborn/) ([repo](https://github.com/flexagoon/rounded-window-corners)) | **Pick** | GPL-3.0 | 2026-07-20 | 430 stars, 45 open | **PROVEN +repo** (EGO 47–50, [metadata](https://raw.githubusercontent.com/flexagoon/rounded-window-corners/main/resources/metadata.json) `["50"]`) |
| Rounded | [Rounded Windows](https://extensions.gnome.org/extension/9668/rounded-window-corners/) ([repo](https://github.com/Nathanaelrc/rounded-windows)) | Fallback | n/c | n/c | n/c | PROVEN (EGO 45–50) |
| Animation | [Compiz alike magic lamp](https://extensions.gnome.org/extension/3740/compiz-alike-magic-lamp-effect/) ([repo](https://github.com/hermes83/compiz-alike-magic-lamp-effect)) | **Pick** (genie-style minimize) | GPL-3.0 | 2026-10-09 | 149 stars, 10 open | **PROVEN +repo** (EGO to 51) |
| Animation | [Compiz windows effect](https://extensions.gnome.org/extension/3210/compiz-windows-effect/) | Optional wobble | n/c | n/c | n/c | PROVEN (EGO 48–51) |
| Animation | [Burn My Windows](https://extensions.gnome.org/extension/4679/burn-my-windows/) ([repo](https://github.com/Schneegans/Burn-My-Windows)) | Fallback | GPL-3.0 | 2026-10-31 | 3.1k stars, 33 open | **PROVEN +repo** (metadata 45–51) |

- Left buttons: the [`button-layout` schema](https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas/-/raw/master/schemas/org.gnome.desktop.wm.preferences.gschema.xml.in) is a string where a colon separates left and right. So `gsettings set org.gnome.desktop.wm.preferences button-layout 'close,minimize,maximize:'` places buttons left. It is a standard key and needs no patch.
- Dash2Dock's README lists compatibility with a [different fork of the magic lamp effect](https://github.com/PR3SIDENT/gnome-shell-extension-compiz-alike-magic-lamp-effect) than hermes83's — [README](https://raw.githubusercontent.com/icedman/dash2dock-lite/main/README.md).
- Earlier Blur my Shell documentation warned of blur bugs and that it could not do rounded blur on some surfaces. That text comes from a [fork README](https://github.com/Schneegans/blur-my-shell) and may be stale.

### Inferences
- No candidate in this section was found to require Mutter patches. This comes from their distribution as extensions, not from a code audit.
- Rounded corners on client-side-decorated windows may double up with theme corners. MacTahoe's open [#96](https://github.com/vinceliuice/MacTahoe-gtk-theme/issues?q=gnome+50) on corner shades suggests corners are a sensitive area worth testing together.
- Ubuntu's LTS stays at GNOME 50, so RWC's lack of 51 only matters if the distro moves past 50.

### Gaps
- Whether libadwaita 1.9 honors `button-layout` in every headerbar type was not confirmed from a source.
- Whether the macOS traffic-light button styling depends on the theme override for libadwaita apps is expected but was not separately tested.
- Burn My Windows and the magic lamp's interaction when both are enabled is unknown.

## Top bar and global menu on Wayland

### Takeaway
A true system-wide macOS menu bar is **not possible** on GNOME 50 Wayland. Real menus appear only for apps that export them, and the rest are shortcut-driven approximations. The practical pick is logo menu plus app name in the panel. Treat Orbit Global Menu as an optional experiment.

### Cited Findings

| Function | Project | Role | License | Last push | GNOME 50 |
|---|---|---|---|---|---|
| Apple-like menu | [Logo Menu](https://extensions.gnome.org/extension/4451/logo-menu/) ([repo](https://github.com/Aryan20/Logomenu)) | **Pick** | GPL-2.0 | 2026-09-27 | **PROVEN +repo** (metadata 49–51) |
| Apple-like menu | [Kiwi Menu](https://extensions.gnome.org/extension/8697/kiwi-menu/) ([repo](https://github.com/kem-a/kiwi-menu)) | Fallback, more macOS-specific | n/c | n/c | PROVEN (EGO 45–51) |
| App name | [Window Title Pro Topbar](https://extensions.gnome.org/extension/10319/window-title-pro/) ([repo](https://github.com/eprahemi/window-title-pro-topbar)) | **Pick** | n/c | n/c | PROVEN (EGO 45–51) |
| App name | [App Name Indicator](https://extensions.gnome.org/extension/8667/app-name-indicator/) ([repo](https://github.com/devlocalhost/appnameindicator/)) | Fallback | n/c | n/c | PROVEN (EGO 49–50) |
| Panel layout | [Top Bar Organizer](https://extensions.gnome.org/extension/4356/top-bar-organizer/) | **Pick** | n/c | n/c | PROVEN (EGO 47–50) |
| Panel layout | [Just Perfection](https://extensions.gnome.org/extension/3843/just-perfection/) | Companion | n/c | n/c | PROVEN (EGO 48–51) |
| Tray | [AppIndicator support](https://extensions.gnome.org/extension/615/appindicator-support/) ([repo](https://github.com/ubuntu/gnome-shell-extension-appindicator)) | **Pick** | GPL-2.0 | 2026-10-05 | **PROVEN +repo** (includes 50, 51) |
| Global menu | [Orbit Global Menu](https://github.com/Unmade760/orbit-global-menu) | Experimental | GPL-3.0 | 2026-10-31 | **CLAIMED** (README: Shell 48–51) |
| Global menu | [Global Menu for GNOME](https://extensions.gnome.org/extension/10288/global-menu-for-gnome/) ([repo](https://github.com/ShiroOSL/global-menu-for-gnome)) | Fallback | n/c | n/c | PROVEN (EGO 45–50) |
| Do not use | [App menu is back](https://extensions.gnome.org/extension/6433/app-menu-is-back/), [Window title is back](https://extensions.gnome.org/extension/6310/window-title-is-back/) | Avoid | GPL-3.0 / none detected | 2026-08-26 / 2025-11-10 | **NOT SUPPORTED**: EGO to 49, [metadata](https://raw.githubusercontent.com/fthx/appmenu-is-back/main/metadata.json) `["49"]` |
| Conflict | [Unite](https://extensions.gnome.org/extension/1287/unite/) ([repo](https://github.com/hardpixel/unite-shell)) | Avoid unless vendored | GPL-3.0 | 2026-09-03 | **CLAIMED**: repo metadata 45–50, but EGO stops at 44 |
| Do not use | [Open Bar](https://extensions.gnome.org/extension/6580/open-bar/) | Avoid | n/c | n/c | **NOT SUPPORTED** on EGO (to 49) |

**What the global menu can really do**
- Orbit's README says GNOME has no global menu and most apps no longer export one. It uses three tiers: real D-Bus menus through a companion daemon, built-in menus for 290 apps that send keyboard shortcuts to the window, and generic window and session actions for everything else — [Orbit README](https://raw.githubusercontent.com/Unmade760/orbit-global-menu/main/README.md).
- Orbit's optional daemon package pulls `appmenu-gtk3-module`, loaded into GTK3 apps, and has Ubuntu 26.04 build instructions — [Orbit README](https://raw.githubusercontent.com/Unmade760/orbit-global-menu/main/README.md).
- An independent writeup says the shortcut-based menu is not always identical to the app's own menu, and cites a smaller app count (about 171) from its date — [UbuntuHandbook, Oct 2026](https://ubuntuhandbook.org/index.php/2026/10/this-extension-adds-global-menu-to-ubuntu-26-04-top-bar/).
- Older background argues GTK no longer supports generic loadable modules, so GTK4 menu export depends on the app developer's choice. The source is an old issue on an archived project and is background only — [Gnome-Global-AppMenu #116](https://gitlab.com/lestcape/Gnome-Global-AppMenu/-/issues/116).
- **Conflict:** UbuntuHandbook describes Global Menu for GNOME as showing one fixed menu rather than updating per app, while its [EGO description](https://extensions.gnome.org/extension/10288/global-menu-for-gnome/) says "contextual" menus for the focused app. Neither was tested.

### Inferences
- Do not market a macOS-style global menu as a feature. Sending shortcuts simulates menus and may not reflect state (checkmarks, disabled items).
- Orbit is a small project (96 stars, first press coverage found is from October 2026) and should not be a default in an LTS-based distro without testing. Its global `appmenu-gtk3-module` also alters GTK3 app behavior for everything, which is more invasive than the extension alone.

### Gaps
- GTK4 and libadwaita global export status in 2026 could not be confirmed from a current primary source.
- Orbit's EGO listing status was not checked.
- Open Bar's use in the kayozxo recipe suggests that recipe may not transfer to 50 unchanged; it was not tested.

## Launchpad, Control Center, Spotlight, Mission Control, hot corners, GDM, Plymouth

### Takeaway
No true Launchpad or Control Center clone with GNOME 50 evidence was found, so the native overview and quick settings plus small tweaks are the sensible answer. Spotlight-like launchers do exist with listing evidence. Mission Control maps well onto the overview. GDM theming is a fragile `gresource` modification on Ubuntu, with a documented 26.04 failure. Plymouth candidates are stale, so build your own.

### Cited Findings

| Function | Project | Role | License | Last push | GNOME 50 |
|---|---|---|---|---|---|
| Launchpad | Native overview app grid + [App Grid Wizard](https://extensions.gnome.org/extension/7867/app-grid-wizard/) ([repo](https://github.com/MahdiMirzadeh/app-grid-wizard)) | **Pick** (folders by category) | n/c | n/c | PROVEN (EGO 45–50) |
| Launchpad | [Alphabetical App Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/), [App Grid Tuner](https://extensions.gnome.org/extension/8745/app-grid-tuner/), [App Grid Button In Top Panel](https://extensions.gnome.org/extension/8584/app-grid-button-in-top-panel/), [Show Apps Hot Corner](https://extensions.gnome.org/extension/10356/show-apps-hot-corner/) | Companions | n/c | n/c | PROVEN (shell-50 EGO query); purpose inferred from names |
| Launchpad / overview | [V-Shell](https://extensions.gnome.org/extension/5177/vertical-workspaces/) ([repo](https://github.com/G-dH/vertical-workspaces)) | Fallback; heavy | GPL-3.0 | 2026-10-30 | **PROVEN +repo** (metadata 45–51) |
| Control Center | Native quick settings + [Compact Quick Settings](https://extensions.gnome.org/extension/5527/compact-quick-settings/) + [Quick Settings Audio Panel](https://extensions.gnome.org/extension/5940/quick-settings-audio-panel/) | **Pick** | n/c | n/c | PROVEN (both list 50) |
| Control Center | [Quick Settings Tweaks](https://extensions.gnome.org/extension/5446/quick-settings-tweaker/) ([repo](https://github.com/qwreey/quick-settings-tweaks)) | Avoid | GPL-3.0 | 2026-02-03 | **NOT SUPPORTED**: EGO to 48, metadata 48–49 |
| Spotlight | [Spotlight](https://extensions.gnome.org/extension/10666/spotlight/) ([repo](https://github.com/itsnin/spotlight)) | **Pick** (young) | n/c | n/c | PROVEN (EGO 45–51) |
| Spotlight | [Lightning GNOME Launcher](https://extensions.gnome.org/extension/9817/lightning-gnome-launcher-extension/) ([repo](https://gitlab.com/rimal.avimanyu/lightning-gnome-launcher-extension)) | Fallback | n/c | n/c | PROVEN (EGO 48–50) |
| Spotlight | [Search Light](https://extensions.gnome.org/extension/5489/search-light/) ([repo](https://github.com/icedman/search-light)) | Watch | GPL-3.0 | 2026-05-09 | **CLAIMED**: repo metadata lists 48–50, EGO stops at 49 |
| Spotlight | Native overview search | Baseline | n/a | n/a | Part of GNOME Shell |
| Mission Control | Native overview | **Pick** | n/a | n/a | Part of GNOME Shell |
| Mission Control | [Coverflow Alt-Tab](https://extensions.gnome.org/extension/97/coverflow-alt-tab/) | Optional | n/c | n/c | PROVEN (EGO to 50) |
| Hot corners | [CHC-E](https://extensions.gnome.org/extension/4167/custom-hot-corners-extended/) ([repo](https://github.com/G-dH/custom-hot-corners-extended)) | **Pick** for macOS-style active corners | GPL-3.0 | 2026-10-21 | **PROVEN +repo** (see note on 51) |
| Hot corners | [Hot Edge](https://extensions.gnome.org/extension/4222/hot-edge/) | Fallback | n/c | n/c | PROVEN (EGO to 51) |
| GDM | Theme `tweaks.sh -g` (WhiteSur/MacTahoe) | **Pick with workaround, as packaged asset** | MIT | as above | **CLAIMED with reported failure on 26.04** |
| GDM | [gdm-settings](https://github.com/gdm-settings/gdm-settings) | Fallback (GUI) | AGPL (exact version truncated in API output) | 2026-10-27 | **UNVERIFIED** on 50 |
| Lock screen | [Lockscreen Extension](https://extensions.gnome.org/extension/7472/lockscreen-extension/), [WACK Sonoma Lockscreen](https://extensions.gnome.org/extension/9713/wack-sonoma-lockscreen/) | Optional | n/c | n/c | PROVEN (EGO to 50) |
| Plymouth | [darwin-plymouth](https://github.com/libredeb/darwin-plymouth) | Not recommended (stale, Apple logo) | GPL-3.0 | 2023-03-22 | **UNVERIFIED** |
| Plymouth | Custom own-brand theme | **Recommendation** | yours | n/a | n/a |

- CHC-E: EGO lists 48–51, while the repo's metadata shows 45–50 on the branch read. Both include 50 — [EGO](https://extensions.gnome.org/extension/4167/custom-hot-corners-extended/); [metadata](https://raw.githubusercontent.com/G-dH/custom-hot-corners-extended/main/metadata.json).
- A dedicated Launchpad clone for GNOME was not found. An [XFCE plugin thread](https://reddit.zackpollard.pro/r/xfce/comments/1m5hefx/i_created_a_fullscreen_macosstyle_launchpad) was the closest search result. An EGO search for "launchpad" returned unrelated launchers on shell 50.
- Hot corners: `org.gnome.desktop.interface enable-hot-corners` defaults to true and maps the top-left corner to the overview — [schema](https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas/-/raw/master/schemas/org.gnome.desktop.interface.gschema.xml.in).
- **GDM on 26.04:** [MacTahoe #148](https://github.com/vinceliuice/MacTahoe-gtk-theme/issues/148) (Ubuntu 26.04.1, GDM 50.1) reports that `tweaks.sh -g` patches the Yaru gresource, while the active `gdm-theme.gresource` alternative resolves to `/usr/share/gnome-shell/gnome-shell-theme.gresource`. So nothing changes on screen. The reporter's confirmed workaround is `sudo update-alternatives --set gdm-theme.gresource /usr/share/gnome-shell/theme/Yaru/gnome-shell-theme.gresource`. No maintainer reply yet.
- Plymouth: macOS-style themes exist, with [reports that a LUKS password box can sit behind the Apple logo](https://store.kde.org/p/1009320) on darwin-plymouth. A [Fedora thread](https://discussion.fedoraproject.org/t/adding-apple-logo-to-fedora-boot-splash-screen/176979) suggests a custom theme over BGRT tricks. Installation uses `plymouth-set-default-theme ... -R` and initramfs rebuilds — [KDE Store listing](https://store.kde.org/p/2214975).
- A third-party summary says 26.04 has a new boot spinner — [knightli](https://knightli.com/en/2026/04/26/ubuntu-26-04-lts-release-notes/).

### Inferences
- Shipping the GDM theme as a distro package that installs its own gresource and registers it through `update-alternatives` is cleaner than running `tweaks.sh`. It would avoid patching Yaru's file in place and surviving-upgrade problems, but this design is untested.
- Disable the top-left hot corner or remap it deliberately, since macOS has no default active corner there.
- V-Shell is powerful but large, and it overlaps with the overview. It is a fallback rather than a default for this reason.

### Gaps
- `Spotlight` and `Lightning` quality and maintenance are unassessed beyond listing evidence.
- gdm-settings' README grep found no explicit version statement; its compatibility with 50 needs testing.
- No current maintained macOS-style Plymouth theme with 26.04 evidence was found.

## Existing distros and shipping system-wide

### Takeaway
Zorin OS is the most instructive precedent: it stays on an LTS GNOME and curates extensions behind its own layout tool. For Carlos-OS, install extensions under `/usr/share/gnome-shell/extensions`, enable them through a dconf system database, and pin tested versions. The macOS-theme projects themselves are user-install recipes, not distro packaging.

### Cited Findings
- Zorin OS 18 is based on Ubuntu 24.04 and GNOME 46, heavily modified with extensions, and sponsors Dash-to-Panel — [The Register](https://www.theregister.com/2025/09/24/zorin_os_18_beta/).
- Zorin 18.1 ships 27 separate extensions — [The Register](https://www.theregister.com/2026/04/21/zorin_os_181_released/).
- Zorin Appearance switches layouts with one click, and some layouts are Pro-only. Tiling Shell is preinstalled — [UbuntuHandbook](https://ubuntuhandbook.org/index.php/2025/10/zorin-os-18-officially-released-based-on-ubuntu-24-04-lts/); [OMG! Ubuntu](https://www.omgubuntu.co.uk/2025/10/zorin-os-18-released-with-new-look-new-apps-more/amp).
- Pop!_OS 24.04 moved to the in-house Rust COSMIC desktop rather than GNOME with extensions, and replaced GNOME apps with its own — [The Register](https://www.theregister.com/2024/09/12/pop_os_2404_cosmic_desktop/); [The Register](https://www.theregister.com/2025/09/30/pop_os_2404_beta_released/).
- Reviewers compare COSMIC's layout to elementary's Pantheon, which is not GNOME-based code — [The Register](https://www.theregister.com/2025/09/30/pop_os_2404_beta_released/).
- [GNOME-macOS-Tahoe](https://github.com/kayozxo/GNOME-macOS-Tahoe) bundles Open Bar, Blur my Shell, Dash to Dock, Gnome 4x UI Improvements, Space Bar, Tiling Shell, User Themes, Vitals and Ulauncher. Open Bar is listed only to 49 on EGO (see above).
- Machine-wide extensions: install to `/usr/share/gnome-shell/extensions`, create `/etc/dconf/profile/user` with `user-db:user` and `system-db:local`, add `/etc/dconf/db/local.d/00-extensions` with `[org/gnome/shell] enabled-extensions=[...]`, and run `dconf update`. New extensions are disabled by default, changes apply at new logins, and existing users with their own enabled extensions are unaffected — [GNOME System Administration Guide](https://help.gnome.org/admin/system-admin-guide/stable/extensions-enable.html.en).
- That guide links a separate "Lock down enabled extensions" page for preventing user changes — [GNOME System Administration Guide](https://help.gnome.org/admin/system-admin-guide/stable/extensions-enable.html.en).
- EGO's `shell-version` declarations differ by project: [RWC metadata](https://raw.githubusercontent.com/flexagoon/rounded-window-corners/main/resources/metadata.json) lists only 50, while [Blur my Shell](https://raw.githubusercontent.com/aunetx/blur-my-shell/master/metadata.json) spans 46–51.

**Proposed baseline for Ubuntu 26.04 (all extension picks evidenced above)**
- Theme: WhiteSur (Shell and GTK3 system-wide; libadwaita layer optional and per-user)
- Dock: Dash2Dock Animated (Dash to Dock + Blur my Shell as fallback)
- Effects: Blur my Shell, Rounded Window Corners Reborn, magic lamp
- Panel: Logo Menu, Window Title Pro, Top Bar Organizer, AppIndicator, User Themes
- Launch: native grid + App Grid Wizard; native overview + Spotlight
- Global menu: not by default

### Inferences
- **Lesson from Zorin:** freezing GNOME and curating extensions behind a single settings tool limits breakage. For Carlos-OS, staying on 26.04's GNOME 50 and pinning extensions would give similar stability.
- **Lesson from Pop!_OS:** fully controlling the desktop look eventually led one distro to replace GNOME Shell. Carlos-OS should keep this in mind if macOS fidelity becomes a priority. It is expensive and off-target for now.
- Package each extension as a `.deb` to pin versions and to avoid user-update drift. Validate on each GNOME point release.
- Add a CI smoke test that boots a Wayland session, enables the extension set, and checks the journal for extension errors. This creates the runtime proof that this research cannot.

### Gaps
- **Not sourced, recalled from prior knowledge, so verify:** Ubuntu's session mode files under `/usr/share/gnome-shell/modes/`, `*.gschema.override` defaults such as `10_ubuntu-settings`, and `disable-extension-version-validation` / `disable-user-extensions`. These are the likely mechanics to study on a live 26.04 image, including how Ubuntu's own session enables its extensions.
- No source was found on elementary OS 8's current design or packaging, or on any maintained GNOME-based macOS-clone distro on GNOME 50.
- Zorin's packaging internals (how extension defaults are set) were not found in sources read.
- Interaction of the whole baseline set on one GNOME 50 session is **unproven**. Each item was evidenced separately, so a runtime test on 26.04 is required before committing.
