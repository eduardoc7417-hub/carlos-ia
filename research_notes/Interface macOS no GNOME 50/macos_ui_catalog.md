# macOS UI Catalog: macOS 27 "Golden Gate" (current as of 2026-10-31)

Value labels used throughout:
- **[OFFICIAL]**: Apple HIG, Apple Support or a WWDC session.
- **[THIRD-PARTY]**: measured or reported outside Apple. Reliability is stated where it is weak.
- **[DERIVED]**: my arithmetic from a sourced value, such as RGB to hex.
- **[UNVERIFIED MEMORY]**: recollection not confirmed by any source this session. Appears only under Gaps. Do not treat it as fact.
- **not documented**: no source found.

Method caveats:
- Apple pages were read through an automated extraction step, not as raw text, so spot-check critical values against the live page.
- HIG values were read from Apple's JSON data endpoints for the HIG pages. These do not state which macOS version each value targets, and some may predate macOS 27.
- Several third-party claims come from search-result excerpts of pages I did not open. These are marked "excerpt".

## Which macOS is newest, and what changed from the previous release?

### Takeaway
The newest release is **macOS 27 "Golden Gate", latest version 27.2 (released 2026-10-26)**. The previous release is macOS 26 Tahoe. Golden Gate keeps Liquid Glass but partly walks Tahoe back: less transparency by default, a user translucency slider, one fixed window radius, edge-to-edge sidebars with colored icons, more legible toolbars, and far fewer menu icons.

### Cited Findings
**Release facts**
- Announced at WWDC on 2026-06-08. Released 2026-09-14 as 27.0 (build 26A428), then 27.0.1 on 09-28 (26A434) and 27.2 on 10-26 (26B123) — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate). The release date is also given by [MacRumors](https://www.macrumors.com/2026/09/10/macos-27-golden-gate-release-date/).
- Apple Support's Mac User Guide pages resolve to macOS 27 — [Apple Support](https://support.apple.com/guide/mac-help/change-dock-settings-mchlp1119/mac).
- Intel Macs are no longer supported — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate).

**Changes from Tahoe to Golden Gate**
| Area | Change | Source |
|---|---|---|
| Liquid Glass | Translucency slider in System Settings > Appearance, from clear to a more opaque, tinted version | [MacRumors](https://www.macrumors.com/roundup/macos-27/) |
| Liquid Glass | Opacity changed to diffuse complex backgrounds better; darkened edge and brighter specular highlights for layer separation | [MacRumors](https://www.macrumors.com/roundup/macos-27/) |
| Liquid Glass | One reviewer says the slider's range is too narrow to be worthwhile (excerpt) | [Tom's Guide](https://www.tomsguide.com/computing/macos/macos-golden-gate-review) or [AppleInsider](https://appleinsider.com/articles/26/06/12/macos-golden-gate-beta-review-its-nothing-without-siri-ai); the excerpt did not make clear which |
| Glass interaction | New: glass "subtly bounces when clicked", for use on controls only | [WWDC26 session 289, official](https://developer.apple.com/videos/play/wwdc2026/289/) |
| Window corners | Fixed radius across apps and system windows, including apps not updated for the new system | [9to5Mac](https://9to5mac.com/2026/06/08/apple-announces-macos-golden-gate-27/) |
| Active window | Shadow, sidebar and opacity changes make the active window easier to identify | [MacRumors](https://www.macrumors.com/roundup/macos-27/) |
| Sidebars | Edge-to-edge, no longer floating, darker background, colored icons | [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/) |
| Toolbars | More shading and legibility; Photos has a solid bar again | [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/) |
| Menus | Icons only on some common actions; menu bar items no longer show icons by default | [MacRumors](https://www.macrumors.com/roundup/macos-27/); [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Context menus | Start with a darker "Ask Siri" item above the rest (observed in public beta) | [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/) |
| Traffic lights | Redesigned in an Aqua-like Liquid Glass style | [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Cursor | Mouseover cursor returns to a glove icon, new design | [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Dock | Background processes appear in context menus | [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Control Center | Consistent closing animation | [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Animations | Many changed; buttons animate more like iOS and iPadOS | [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate) |
| Icons | More glass layers; squircle requirement remains; icons that extend past the squircle still get a gray backplate | [MacRumors](https://www.macrumors.com/roundup/macos-27/); [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/) |
| Spotlight and Siri | Merged "Search or Ask" interface; Siri is a small pill-shaped window that expands | [MacRumors](https://www.macrumors.com/roundup/macos-27/); [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/) |
| Wallpapers | Golden Gate Sunset and Night plus an abstract option; animate on unlock; usable as screen savers | [MacRumors](https://www.macrumors.com/roundup/macos-27/) |

### Inferences
- For a look-alike, target Golden Gate's values and treat Tahoe's as historical. The biggest visual differences are the sidebar and the window radius.
- Six Colors observed a public beta. Treat its details as beta-era unless another source confirms them for the release.

### Gaps
- Apple's own "what's new" page and the macOS 27 release notes were not read.
- A search digest says 27.2 "overhauls the brightness and volume sliders". I did not trace this to an opened source, so it is unconfirmed.

## Dock

### Takeaway
All behavior options are officially documented, but Apple publishes no Dock pixel values. Sizes, magnification range, reflections and timing are not documented by Apple.

### Cited Findings
**[OFFICIAL] settings, in Desktop & Dock** — [Apple Support, macOS 27](https://support.apple.com/guide/mac-help/change-dock-settings-mchlp1119/mac)
- Size slider and Magnification slider.
- Position on screen: left, bottom or right.
- Minimized windows animation. Minimize windows into application icon.
- Automatically hide and show the Dock. Hidden until the pointer reaches the screen edge.
- Animate opening applications (bounce).
- Show indicators for open applications: a small dot below the icon.
- Show suggested and recent apps in Dock, at one end of the Dock.
- Title bar double-click action: Fill, Zoom, Minimize or No Action.

**[THIRD-PARTY] preference keys (excerpt; the exact source of each claim was not separated)** — [mac.install.guide](https://mac.install.guide/mac-setup/dock); [macOS Defaults notes](https://melastmohican.github.io/posts/macos-defaults/index.html); [gist](https://gist.github.com/Softsapiens/d82bef8d0abcb4683357)
- `tilesize` is an integer. One source calls 64 the default.
- `magnification` is a boolean, with `largesize` as an integer.
- `mineffect` accepts `genie`, `scale` or `suck`, with genie listed as default.
- `autohide-delay` is a float in seconds.
- `autohide-time-modifier`: one source lists 0.5 as default; 0 removes the animation.

**[OFFICIAL] context menu**
- Background processes now appear in Dock context menus in Golden Gate — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate). This is secondary sourcing, so the [OFFICIAL] heading does not extend to it.

### Inferences
- The default `tilesize` claim is low confidence, because it is one community source and its target version is unclear.

### Gaps
- Size range in points: not documented. The commonly quoted 16 to 128 range could not be confirmed in this session.
- Dock corner radius, background opacity, blur and icon gap: not documented, no reliable measurement found.
- Default auto-hide delay: no confirmed value.
- [UNVERIFIED MEMORY] Separators divide pinned apps from the recent, Stacks and Trash side. Stacks show as Fan, Grid or List. Dock menus include Options (Keep in Dock, Open at Login, Show in Finder), Show All Windows, Hide and Quit. None of this was checked for version 27.

## Menu Bar

### Takeaway
Official height is **24 pt**, but third-party reports differ and notched Macs behave differently. Order is officially defined. Translucency in Golden Gate has no numeric source.

### Cited Findings
**Height**
- [OFFICIAL] "The menu bar's height is 24 pt", given in the menu bar extra guidance — [HIG Menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar).
- [THIRD-PARTY, weak] One forum user measured Sequoia 25 px and Tahoe 31 px, with no display or scaling stated. Another says their notched M1 MacBook Pro "always" had 31 px — [MacRumors Forums](https://forums.macrumors.com/threads/yet-another-stupid-thing-about-tahoe-new-ui-the-menu-bar-is-taller-for-no-reason.2465392/). These do not state whether the numbers are points or device pixels.
- [THIRD-PARTY] A utility reports a 32 pt notch height, not a menu bar height, on one unspecified Mac (excerpt) — [no_notch](https://github.com/box-kr/no_notch).

**[OFFICIAL] left-side layout** — [HIG Menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)
- Apple menu is always first and cannot be changed by apps.
- Then: *AppName*, File, Edit, Format, View, app-specific menus, Window, Help.
- App name should be 16 characters or fewer in About, Hide and Quit items.
- Option-key alternates: Quit > Quit and Keep Windows; Close > Close All; Close Tab > Close Other Tabs; Duplicate > Save As; Minimize > Minimize All; Zoom > Zoom All; Bring All to Front > Arrange in Front.

**[OFFICIAL] right-side layout**
- Menu bar extras sit opposite the app menus and may be hidden by the system to make room for app menus. They should display a menu rather than a popover — [HIG Menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar).
- Control Center icon sits in the top-right area. Privacy indicators sit to its right: orange microphone, green camera, purple system audio, arrow for location; only one indicator appears at a time — [Apple Support](https://support.apple.com/guide/mac-help/use-control-center-mchl50f94f8f/mac).
- The menu bar typically hides in full screen until the pointer reaches the top edge — [HIG Menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar).

**Golden Gate**
- Spotlight was removed from the menu bar in beta 3, replaced by Siri for waitlisted users — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate).
- "Light" overflow management for items behind the notch; changes broke third-party menu bar utilities (beta) — [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/).

### Inferences
- Use 24 pt as the design baseline on non-notched displays and confirm on real hardware. Forum values of 25 and 31 cannot be reconciled without scale data.

### Gaps
- Translucency values, clock format and clock placement: no source found this session.
- [UNVERIFIED MEMORY] Tahoe's menu bar is transparent by default with a "Show menu bar background" option. The clock is the far-right item. Whether either holds in Golden Gate was not checked.

## Control Center, Notification Center, Widgets, Spotlight, Apps, Mission Control, Spaces, Stage Manager

### Takeaway
Apple documents behavior and arrangement but no geometry or material values for any of these surfaces. Everything numeric here must come from measuring a real Mac.

### Cited Findings
**Control Center [OFFICIAL]** — [Apple Support](https://support.apple.com/guide/mac-help/use-control-center-mchl50f94f8f/mac)
- Opens from a menu bar icon. Groups controls such as Wi-Fi, Focus, Sound and Now Playing.
- Controls are toggles, sliders or arrows that expand to more options.
- The top may show which apps are using the microphone, location, camera or system audio.
- Edit Controls: drag to add, remove or rearrange, filter by sidebar category, Control-click to resize, Done to finish.
- Items can be dragged to the menu bar.

**Spotlight**
- Command-Space opens it instantly; "Ask Siri" appears after a few seconds' wait for questions (beta) — [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/).
- Rebuilt around "Search or Ask" with a microphone option — [MacRumors](https://www.macrumors.com/roundup/macos-27/).
- Visual Intelligence: Command-Shift-Space or Command-Shift-6 — [MacRumors](https://www.macrumors.com/roundup/macos-27/).

**Apps, replacing Launchpad (introduced in Tahoe; excerpts)**
- Launchpad was retired and Apps sits where it was in the Dock — [Macworld](https://www.macworld.com/article/2830963/macos-tahoe-apps-replaces-launchpad.html).
- No custom pages or folders, with a search box on top (excerpts, Tahoe-era) — [Macworld](https://www.macworld.com/article/2830963/macos-tahoe-apps-replaces-launchpad.html); [Yahoo](https://tech.yahoo.com/ai/apple-intelligence/articles/forget-haters-macos-tahoe-feature-100000841.html).
- Command-1 in Spotlight opens the applications grid — [MacMost](https://macmost.com/how-to-use-the-new-spotlight-applications-launcher.html).
- Thumb-and-three-finger pinch opens it — [iGeeksBlog](https://www.igeeksblog.com/launchpad-alternatives-for-mac/).

**Mission Control and Spaces [OFFICIAL]** — [Apple Support](https://support.apple.com/guide/mac-help/view-open-windows-spaces-mission-control-mh35798/mac)
- Shows open windows in a single layer. Spaces bar along the top edge holds thumbnails of full-screen apps, Split View apps and desktop spaces.
- Enter or leave: Mission Control key, Control-Up Arrow, three-finger swipe up/down, Magic Mouse two-finger double-tap, or drag a window to the top edge.
- App windows: Control-Down Arrow, or three/four-finger swipe down if App Exposé is on.
- Show desktop: Command-Mission Control, or spread thumb and three fingers.
- Golden Gate restores window positions, Spaces and screen assignments when switching displays — [MacRumors](https://www.macrumors.com/roundup/macos-27/).

**Stage Manager [OFFICIAL]** — [Apple Support](https://support.apple.com/guide/mac-help/use-stage-manager-mchl534ba392/mac)
- Recent apps on the left, current window in the center; windows can be moved, resized and overlapped.
- Drag an app to the center to group it; drag back to ungroup.
- Toggle in Desktop & Dock or Control Center.
- Options: Show Items, Show Desktop, Show recent apps (off means reveal at left edge), Show windows from an application (All at Once or One at a Time).

### Inferences
- GNOME's Activities overview maps conceptually to Mission Control, but that mapping is my own judgment, not a sourced comparison.

### Gaps
- **Notification Center and widgets were not researched successfully**: no sizes, radii or layout confirmed. Consult Apple Support's Notification Center and widgets guides directly.
- Sizes, radii and blur for all these panels: not documented.
- [UNVERIFIED MEMORY] Notification Center opens from the clock at the top-right; widgets come in small, medium, large and extra large and can sit on the desktop. Spaces switch with Control-Left/Right Arrow or a three-finger horizontal swipe, depending on trackpad settings. Tahoe Spotlight added quick actions and quick keys.

## Windows

### Takeaway
Best current radius value is **20 for Golden Gate (Tahoe 26, pre-Tahoe 10)**, from a forum-reported override, not Apple. Button geometry of 12 px diameter and 8 px gap, with the classic hex set, comes from one third-party library of unknown version and predates the Aqua-like redesign.

### Cited Findings
**Corner radius**
- [THIRD-PARTY, weak] "26 is used for Tahoe, 10 was pre-Tahoe. 20 is used for Golden Gate", via undocumented `defaults write -g NSConvolutionOverride1 -float <n>` — [MacRumors Forums](https://forums.macrumors.com/threads/want-the-bigger-window-corner-radius-back-come-inside.2484898/). Units are not stated and it was not independently measured.
- [THIRD-PARTY] Tahoe had inconsistent corners; a tool's maker claims four different radii across Apple's apps, though the tool has a commercial interest — [Liquid Radius](https://liquidradius-site.pages.dev/).
- [OFFICIAL] The radius is **not given** by Apple. API: `NSViewCornerConfiguration.uniformCorners(radius: .containerConcentric(minimumCornerRadius))`; the closer a view is to the corner, the closer its radius should match — [WWDC26 session 289](https://developer.apple.com/videos/play/wwdc2026/289/).

**Traffic lights**
- [OFFICIAL] Close, minimize and zoom are colored in the key window and gray in main-not-key and inactive windows. Inactive windows also lose vibrancy — [HIG Windows](https://developer.apple.com/design/human-interface-guidelines/windows).
- [THIRD-PARTY] Implementation values from a Rust UI library, macOS version not stated. Diameter 12 px, gap 8 px, horizontal padding 12 px, total width 76 px, hit radius 7 px, hover transition 100 ms, hover scale 1.0, inactive `#80808080` — [uzor](https://docs.rs/crate/uzor/1.0.20/source/src/macos/themes/traffic_lights.rs).

| Button | Normal | Hover | Pressed | Glyph |
|---|---|---|---|---|
| Close | #FF5F57 | #FF6F67 | #E0443E | #4C0002 |
| Minimize | #FEBC2E | #FFCC4D | #DFA52A | #995700 |
| Maximize | #28C840 | #39D956 | #1DAD36 | #006500 |

  Same source: border `#00000020` in light mode, `#00000000` in dark mode.
- **Conflict on the Golden Gate look.**
  - Final release: "Aqua-like Liquid Glass style" — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate).
  - Beta 6: "lightly outlined, nearly colorless circles" — [Bryan's Blog](https://bryans.blog/macos-golden-gate-beta-6-just-gave-the-macs-traffic-lights-a-major-redesign/).
  - Beta 6: Aqua-style with subtle top and bottom edge shadows, like glass drops (excerpts) — [iThinkDiff](https://www.ithinkdiff.com/macos-golden-gate-beta-6-wallpapers-traffic-light-buttons/); [9to5Mac](https://9to5mac.com/2026/08/17/macos-27-golden-gate-beta-6-features-redesigned-traffic-light-window-controls/).
- Title bar and button metrics changed with the macOS 26 SDK; numbers were not retrieved — [Zed commit](https://git.secluded.site/zed/commit/95ae388c0ce8ae4a0b8d149ace3ecba1ea417491).

**Anatomy and toolbars [OFFICIAL]**
- Frame with controls and optional toolbar, body area, and rare bottom bar. Finder's status bar is the cited example, showing item count, selection and disk space — [HIG Windows](https://developer.apple.com/design/human-interface-guidelines/windows).
- Sidebars reach the window edge, content flows behind them, and selection uses a semi-bold style. Bordered toolbar items over the sidebar adopt Liquid Glass. Automatic scroll edge effect becomes hard-edge with free-floating title text — [WWDC26 session 289](https://developer.apple.com/videos/play/wwdc2026/289/).

**Tiling [OFFICIAL, macOS 27]** — [Apple Support](https://support.apple.com/guide/mac-help/tile-mac-windows-mchl9674d0b0/mac)
- Entry points: hover the green button, Window > Move & Resize, Window > Full Screen Tile.
- Fn-Control + F Fill, C Center, R Return to Previous Size, arrows for halves.
- Fn-Control-Shift + arrows: Left & Right, Right & Left, Top & Bottom, Bottom & Top.
- Fn-Control-Option-Shift + arrows: Left, Right, Top or Bottom & Quarters.
- Quarters and single corners have no shortcut.

**Shadows**
- Golden Gate changes shadows to make the active window clearer, with no values given — [MacRumors](https://www.macrumors.com/roundup/macos-27/).

### Inferences
- The classic hex set is a reasonable base color for a Golden Gate look-alike, but it needs a glass treatment (edge shading and highlight) added and tuned by eye against a screenshot.
- Use 20 pt as a provisional radius and verify by overlaying a Golden Gate screenshot.

### Gaps
- Official button size, spacing and final Golden Gate colors: not documented. A shipping-build screenshot is needed.
- Hover glyph shapes: no source. [UNVERIFIED MEMORY] Close is ×, minimize is −, zoom is two diagonal arrows; glyphs appear when the pointer is over the button group.
- Shadow offset, blur and opacity, active or inactive: not documented, no measurement found.
- Sidebar widths, toolbar heights and the drag-tiling zones: not documented in sources read.

## Materials, Appearance and Color

### Takeaway
Apple documents Liquid Glass variants, the 35% dimming rule and the system color table, but no blur radius, refraction or opacity value. System colors below are the most reliable numbers in this catalog.

### Cited Findings
**Liquid Glass [OFFICIAL]** — [HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- Regular: blurs and adjusts luminosity of background; used by most system components, including alerts, sidebars and popovers.
- Clear: highly translucent; only over visually rich backgrounds.
- Clear dimming: add a **35% opacity dark layer** over bright content; not needed over dark content.
- Scroll edge effects blur and reduce the opacity of background content.
- Glass has no inherent color and takes color from the content behind it. Small elements like toolbars can switch between light and dark according to underlying content — [HIG Color](https://developer.apple.com/design/human-interface-guidelines/color).
- Trackpad interaction produces a more subdued response than direct touch — [HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion).

**Vibrancy and standard materials [OFFICIAL]** — [HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- macOS provides several purpose-specific materials and vibrant versions of all system colors. Blending modes: behind window and within window.
- Thicker is more opaque with better contrast; thinner retains background context.
- Inactive windows have no vibrancy — [HIG Windows](https://developer.apple.com/design/human-interface-guidelines/windows).

**Accent colors [OFFICIAL]**
- App accent applies only when General > Accent color is multicolor; otherwise the user's choice replaces it, except fixed-color sidebar icons — [HIG Color](https://developer.apple.com/design/human-interface-guidelines/color).

**System colors.** RGB is [OFFICIAL] from image alt text, and Apple warns values may vary by release; hex is [DERIVED] — [HIG Color](https://developer.apple.com/design/human-interface-guidelines/color). The page shows one cross-platform table; I did not confirm whether a macOS-only table differs.

| Name | Light | Dark | Increased contrast light | Increased contrast dark |
|---|---|---|---|---|
| Red | #FF383C | #FF4245 | #E9152D | #FF6165 |
| Orange | #FF8D28 | #FF9230 | #C55300 | #FFA056 |
| Yellow | #FFCC00 | #FFD600 | #A16A00 | #FEDF43 |
| Green | #34C759 | #30D158 | #008932 | #4AD968 |
| Mint | #00C8B3 | #00DAC3 | #008575 | #54DFCB |
| Teal | #00C3D0 | #00D2E0 | #008198 | #3BDDEC |
| Cyan | #00C0E8 | #3CD3FE | #007EAE | #6DD9FF |
| Blue | #0088FF | #0091FF | #1E6EF4 | #5CB8FF |
| Indigo | #6155F5 | #6D7CFF | #564ADE | #A7AAFF |
| Purple | #CB30E0 | #DB34F2 | #B02FC2 | #EA8DFF |
| Pink | #FF2D55 | #FF375F | #E7124D | #FF8AC4 |
| Brown | #AC7F5E | #B78A66 | #956D51 | #DBA679 |

**Grays, iOS and iPadOS only (labeled that way by Apple; not macOS values)** — [HIG Color](https://developer.apple.com/design/human-interface-guidelines/color)

| Name | Light | Dark |
|---|---|---|
| systemGray | #8E8E93 | #8E8E93 |
| systemGray2 | #AEAEB2 | #636366 |
| systemGray3 | #C7C7CC | #48484A |
| systemGray4 | #D1D1D6 | #3A3A3C |
| systemGray5 | #E5E5EA | #2C2C2E |
| systemGray6 | #F2F2F7 | #1C1C1E |

**Semantic NSColor roles [OFFICIAL names, no values]** — [HIG Color](https://developer.apple.com/design/human-interface-guidelines/color)
- `labelColor`, `secondaryLabelColor`, `tertiaryLabelColor`, `quaternaryLabelColor`, `separatorColor`, `windowBackgroundColor`, `controlAccentColor`, `selectedContentBackgroundColor`, `textBackgroundColor`, `keyboardFocusIndicatorColor`, `linkColor`, `underPageBackgroundColor`, `unemphasizedSelectedContentBackgroundColor`, among others.

### Inferences
- A look-alike should tokenize by these semantic names, since Apple warns against choosing materials by apparent color.
- Any blur value chosen in GNOME will be a tuned estimate, not a macOS spec.

### Gaps
- Blur radius, saturation, refraction, glass opacity, slider range: not documented.
- Actual RGB values of macOS semantic colors, window backgrounds, and the accent color swatches: not documented in sources read.
- WWDC25 Liquid Glass sessions were not read in full.

## Typography and Icons

### Takeaway
The macOS text-style table is officially documented: **SF Pro, default 13 pt, minimum 10 pt, no Dynamic Type**. Icons are 1024 × 1024 px layered artwork masked by the system; Apple's grid numbers live in templates I did not read.

### Cited Findings
**[OFFICIAL] macOS text styles** — [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

| Style | Weight | Size (pt) | Line height (pt) | Emphasized weight |
|---|---|---|---|---|
| Large Title | Regular | 26 | 32 | Bold |
| Title 1 | Regular | 22 | 26 | Bold |
| Title 2 | Regular | 17 | 22 | Bold |
| Title 3 | Regular | 15 | 20 | Semibold |
| Headline | Bold | 13 | 16 | Heavy |
| Body | Regular | 13 | 16 | Semibold |
| Callout | Regular | 12 | 15 | Semibold |
| Subheadline | Regular | 11 | 14 | Semibold |
| Footnote | Regular | 10 | 13 | Semibold |
| Caption 1 | Regular | 10 | 13 | Medium |
| Caption 2 | Medium | 10 | 13 | Semibold |

- Point size is based on 144 ppi for @2x. Prefer Regular, Medium, Semibold or Bold; avoid Ultralight, Thin and Light — [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography).
- The system adjusts tracking dynamically at every point size — [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography).

**[OFFICIAL] SF Pro tracking, selected rows (1/1000 em)** — [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

| Size | 10 | 11 | 12 | 13 | 15 | 17 | 20 | 22 | 26 | 28 | 34 | 48 | 80+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tracking | +12 | +6 | 0 | -6 | -16 | -26 | -23 | -12 | +8 | +14 | +12 | +8 | 0 |

The extraction reported the macOS table matching this one in visible rows, but was not a full comparison.

**[OFFICIAL] App icons** — [HIG App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- Layout 1024 × 1024 px, square, unmasked layers. The system applies a rounded-rectangle mask with corners matched to system elements.
- Background layer plus one or more foreground layers, built in Icon Composer. Prefer SVG or PDF; PNG for mesh gradients and raster art.
- Appearances: default, dark, clear light, clear dark, tinted light, tinted dark.
- Color spaces: sRGB, Gray Gamma 2.2, Display P3.
- Do not add your own specular highlights, shadows, bevels, blurs or glows. The system supplies these.
- Golden Gate icon edges are more pronounced (excerpt) — [Tom's Guide](https://www.tomsguide.com/computing/macos/macos-golden-gate-review).

### Inferences
- SF Pro licensing may restrict use on non-Apple systems. Check Apple's license before bundling it. I did not read that license.

### Gaps
- Icon grid numbers and corner radius: not documented in the HIG text; see templates at [Apple Design Resources](https://developer.apple.com/design/resources/), not read.
- [UNVERIFIED MEMORY] Older macOS icon templates used an inset body of about 824 × 824 on the 1024 canvas with roughly 22% corners. This may not apply to the new layered system.
- Sizes for menu, toolbar and sidebar symbols: not retrieved.

## Animations, Motion, Gestures and Shortcuts

### Takeaway
Apple publishes **no durations or spring values for macOS system animations**. Only qualitative rules, gestures and shortcuts are official, and the one hover timing found is third-party.

### Cited Findings
- [OFFICIAL] Motion guidance is qualitative: purposeful, optional, brief, cancellable, and following the gesture. Avoid motion on frequent interactions — [HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion).
- [OFFICIAL] Glass bounce on click exists, with parameters not given — [WWDC26 session 289](https://developer.apple.com/videos/play/wwdc2026/289/).
- [THIRD-PARTY] Traffic-light hover transition 100 ms in one library — [uzor](https://docs.rs/crate/uzor/1.0.20/source/src/macos/themes/traffic_lights.rs).
- [THIRD-PARTY] Dock `autohide-time-modifier` default 0.5 per one source (excerpt) — [macOS Defaults notes](https://melastmohican.github.io/posts/macos-defaults/index.html).
- Gestures and shortcuts: see the Mission Control and tiling findings above. Control-Up Arrow is also listed at [Apple's shortcut list](https://support.apple.com/en-us/102650).

### Inferences
- A look-alike has to tune timing by frame-stepping screen recordings of a real Mac.

### Gaps
- Spring parameters, window open/close, Genie, Space switch and Mission Control durations: not documented, no reliable measurements found.
- Reduce Motion behavior on macOS: not specified in the page read.

## Login/Lock Screen and Finder

### Takeaway
Little was confirmed. Wallpapers animate on unlock and Finder inherits the sidebar and toolbar changes, but no source gave a layout for either.

### Cited Findings
- Golden Gate wallpapers animate on unlock and can be used as screen savers — [MacRumors](https://www.macrumors.com/roundup/macos-27/).
- Default wallpaper matches iOS and iPadOS; two Golden Gate Bridge photos added in beta 3 — [Wikipedia](https://en.wikipedia.org/wiki/MacOS_Golden_Gate).
- Finder's sidebar and toolbar follow the new window style; Finder and the save dialog suggest file names based on content (beta) — [Six Colors](https://sixcolors.com/post/2026/07/first-look-macos-golden-gate-public-beta/).
- Finder's bottom status bar shows item count, selection and disk space — [HIG Windows](https://developer.apple.com/design/human-interface-guidelines/windows).
- Rebuilt content indexing should fix Finder sometimes failing to find items — [9to5Mac](https://9to5mac.com/2026/06/08/apple-announces-macos-golden-gate-27/).

### Inferences
- Finder can be built as the reference Golden Gate window: edge-to-edge sidebar, Liquid Glass toolbar controls, optional bottom status bar.

### Gaps
- Login and lock screen layout, including clock position, avatar and password field: **no source found this session**.
- [UNVERIFIED MEMORY] The lock screen shows a large date and time at the top center, with the user avatar and password field low on the screen. Not confirmed for version 27.
- Finder default sidebar sections, view modes and metrics: not retrieved. [UNVERIFIED MEMORY] Sidebar sections are Favorites, iCloud, Locations and Tags; views are Icon, List, Column and Gallery.
