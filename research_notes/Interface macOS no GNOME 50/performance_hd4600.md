# Performance cost and technical risk of macOS-like effects on GNOME 50 / Mutter Wayland on Intel HD 4600 (i5-4570, 16 GB RAM)

Status as of 2026-10-31. Dates are given for each source; anything before GNOME 49 is labelled "older data".

**Evidence limits that apply to every section**
- I found no benchmark of any of these effects on HD 4600 or any other Haswell GPU under GNOME 49, 50 or 51. Every safe/tune/avoid rating below is therefore an inference, and none of it is a measured frame cost.
- The closest hard data comes from newer Intel iGPUs (Tiger Lake). It does not transfer numerically to Haswell.
- These pages could not be read because of bot blocks or load failures: Arch wiki (Intel graphics, Hardware video acceleration), Mesa GitLab #6008, GTK MR 7153, and two Phoronix articles. Claims from them rest on search-result excerpts only and are marked as such.

## Which effects are safe, which need tuning, and which to avoid on this GPU

### Takeaway
All ratings here are inferred: static blur, simple docks and native animations are the low-risk choices, while dynamic blur, popup blur and stacked shader effects are the ones to avoid until they are measured on this machine. The largest documented risk is not GTK or Mutter itself: it is GPU-memory leaks in popup blur and the Vulkan path for GTK4 apps.

### Cited Findings
- Blur my Shell's static mode uses a static image of the wallpaper, whereas dynamic mode makes the component translucent and blurs what is behind it — [Blur my Shell README](https://github.com/aunetx/blur-my-shell)
- Dynamic blur reached about 80% iGPU on Intel UHD (Tiger Lake GT1) under GNOME 50 with an older extension version; a collaborator said v76 replaced that backend, so those numbers no longer apply — [Issue #869, May-Oct 2026](https://github.com/aunetx/blur-my-shell/issues/869)
- Popup blur has documented GPU-memory leaks in both static and dynamic modes — [Issue #1099, Oct 2026](https://github.com/aunetx/blur-my-shell/issues/1099); [Issue #1116, Oct 2026](https://github.com/aunetx/blur-my-shell/issues/1116)

### Inferences

| Effect | Rating (inferred) | Recommended setting | Basis |
|---|---|---|---|
| Static blur: panel, overview | Safe, verify | Static, default pipeline | Wallpaper image is not re-blurred against live content |
| Dynamic blur: panel, dock | Tune | Off at first; trial on v76 or newer only, with measurement | Tiger Lake load report on the older backend; no v76 Haswell data |
| Dynamic blur: application windows | Avoid | Off | Full-window area, repainted while content changes (reasoning, not a measurement) |
| Popup blur | Avoid | Off; or `pipeline_default` at minimum | #1099, #1116 |
| Rounded corners + refraction pipeline in BMS | Avoid until confirmed fixed | Use the default pipeline | #1099 |
| Rounded Window Corners extension | Tune | Trial alone, then with blur | No current performance data; 2022 leak claim from one secondary source |
| Dock magnification | Tune | Trial with few icons and watch for missed frames | No measurement found for any GPU |
| Native GNOME animations | Safe | Leave on; disable only if measurements justify it | No Haswell regression found (absence of evidence only) |
| Extra animation-shader extensions | Avoid | Off | Unmeasured, and adds crash surface |
| GTK4 renderer | Tune | Keep `GSK_RENDERER=ngl` ready; set it if blank windows or glitches appear | openSUSE 2025 report; GTK guidance on old hardware |

- 16 GB of RAM makes system memory a smaller concern than GPU throughput, except for leaks. Haswell's iGPU uses shared system memory, so a leak such as #1116 would consume the same RAM pool (hardware background, not from the sources above).

### Gaps
- No frame-time cost in milliseconds for any effect on HD 4600. It must be measured locally.

## Blur cost in GNOME Shell (Blur my Shell static vs dynamic, benchmarks, Intel iGPU issues)

### Takeaway
No published benchmark compares static and dynamic blur on Intel iGPUs, but the available reports favour static. The extension changes quickly: v76 replaced the dynamic backend in 2026, so version number matters as much as mode.

### Cited Findings
- The current release supports GNOME Shell 46 through 51 from `master` — [Blur my Shell README](https://github.com/aunetx/blur-my-shell)
- Project documentation surfaced by search calls dynamic blur not very efficient and prefers static where possible, and says static can still be slow with some non-native effects or many Monte Carlo iterations (search excerpt; I did not find this wording in the README summary of the fetched repo, so it may be from another version or fork) — [Blur my Shell, Schneegans repo](https://github.com/Schneegans/blur-my-shell)
- Reporter on Ubuntu 26.04, GNOME 50, kernel 7.0.0-15, Intel UHD TGL GT1 and 32 GB: dynamic blur pushed the iGPU to about 80% and RAM to 2 GB+. Lowering Hack level helped only a little. The machine also has an NVIDIA GPU, and this is a single-user anecdote — [Issue #869](https://github.com/aunetx/blur-my-shell/issues/869)
- Collaborator statement in that issue: v76 replaced old dynamic blur and Hack level with a backend that reuses the blur when the background is unchanged, so v73/v74 numbers no longer apply. The issue closed "not planned" on 2026-10-18 — [Issue #869](https://github.com/aunetx/blur-my-shell/issues/869)
- GNOME's automatic extension updates can replace a GitHub-installed v76 with v75 at login — [Issue #869](https://github.com/aunetx/blur-my-shell/issues/869)
- Static popup leak, on Tiger Lake, i915, GNOME 46, Mesa 25.2.8, BMS v74: about 27-29 MB unreclaimed per notification with the rounded pipeline, about 2 MB (within noise) with default, 0 with popup blur disabled. Real use: about 5.7 GB after about 21 hours. Closed 2026-10-13 and attributed to PR #976, though one commenter still saw about 5 GiB (and was unsure of testing the latest code) — [Issue #1099](https://github.com/aunetx/blur-my-shell/issues/1099)
- Workaround from that issue: `dconf write /org/gnome/shell/extensions/blur-my-shell/popup/pipeline "'pipeline_default'"` — [Issue #1099](https://github.com/aunetx/blur-my-shell/issues/1099)
- Dynamic popup leak, on Intel `xe`, GNOME Shell 50.1, BMS v75: about 120-170 MiB per VLC open/close, about 24 GiB after 202 launches. It did not reproduce on the #976 branch. Closed 2026-10-17 with no linked commit shown — [Issue #1116](https://github.com/aunetx/blur-my-shell/issues/1116)
- A sluggishness report exists even at the "high performance" hack level, without Intel details — [Issue #668](https://github.com/aunetx/blur-my-shell/issues/668)
- A fork's README warns that "No artifact" can make the whole system slower even with no visible blur (fork, search excerpt only) — [codasaii fork](https://github.com/codasaii/blur-my-shell)
- Older data (2013, Unity, not GNOME Shell): active blur was slow on GM45, while static or no blur was smooth. It is only a directional parallel — [Launchpad list](https://lists.launchpad.net/dx-packages/msg00169.html)

### Inferences
- Use BMS v76 or newer, and verify the installed version after each login given the auto-update downgrade reported in #869.
- Hack-level advice in older guides is obsolete on v76 and should not be carried into the configuration.
- Because v76 reuses blur when the background is unchanged, its benefit should be largest on a still desktop and smallest during video or scrolling behind a blurred surface. Test those worst cases rather than an idle desktop.
- Treat #1099 and #1116 as not definitively closed for this setup until a local test shows flat GPU memory.

### Gaps
- No v76 measurement on any Intel iGPU, and none on Haswell.
- Which release contains PR #976 was not confirmed.
- Whether #869's 80% refers to render-engine busy time or another metric is not stated.

## Mesa driver status for Haswell: crocus, hasvk, GTK4 renderer default, bugs, GSK_RENDERER

### Takeaway
OpenGL through crocus is the conservative path; Haswell's Vulkan is officially flagged as incomplete by Mesa's own warning. GTK4's Vulkan-first preference has produced a reported blank-window failure on Haswell, and `GSK_RENDERER=ngl` is the reported workaround. Whether this still occurs on current Mesa and GTK is unconfirmed.

### Cited Findings
- Crocus is a Gallium3D OpenGL driver for Intel Gen4 through Haswell, merged for Mesa 21.2 (2021, older data) — [Phoronix](https://www.phoronix.com/news/Crocus-Has-Landed)
- A 2021 Phoronix headline says crocus was performing well on old Intel hardware (headline only; article blocked, no numbers used) — [Phoronix review](https://www.phoronix.com/review/intel-haswell-crocus)
- Mesa warning: "Haswell Vulkan support is incomplete" (title via search; page blocked, date and status unknown) — [Mesa #6008](https://gitlab.freedesktop.org/mesa/mesa/-/issues/6008)
- Mesa 26.1 (May 2026) added VirtIO-GPU native-context support to Intel i915, Iris, Crocus and ANV, excluding hasvk. This shows crocus still receiving feature work in 2026 — [GamingOnLinux](https://www.gamingonlinux.com/2026/05/mesa-26-1-0-released-bringing-lots-of-linux-graphics-driver-enhancements/)
- A May 2026 Phoronix headline says Mesa developers were considering branching off some older GPU drivers. I could not confirm whether crocus or hasvk are included (headline only) — [Phoronix i965 index](https://www.phoronix.com/search/i965)
- A GTK merge request set renderer preference to vulkan > ngl > gl > cairo (search excerpt; page failed to load) — [GTK MR 7153](https://gitlab.gnome.org/GNOME/gtk/-/merge_requests/7153)
- GTK developers advised in January 2024 that very old hardware may be better off with the old GL renderer (older data, predates the Vulkan default) — [GTK blog](https://blog.gtk.org/2024/01/28/new-renderers-for-gtk/)
- June 2025, openSUSE Tumbleweed with Mesa 25.1.3: GTK4 apps showed blank windows on Wayland. The poster suspected Haswell's Vulkan but no root cause was confirmed and no upstream bug was linked. Workarounds were an Xorg session, `GSK_RENDERER=ngl` in `/etc/environment`, or per-app `GSK_RENDERER=ngl nautilus` — [openSUSE forum](https://forums.opensuse.org/t/gtk4-native-apps-on-gnome-show-blank-windows-with-mesa-25-1-3-417-1-haswell-graphics/185713)

### Inferences
- Default plan: check `vulkaninfo` and run a few GTK4 apps with and without `GSK_RENDERER=ngl`. If there is any defect, set `GSK_RENDERER=ngl` globally. It is a low-risk change that is easily reversed.
- The Xorg workaround should not be planned around, since the target here is a Wayland session and its availability on GNOME 50 distributions was not verified in this research.
- The legacy-branch proposal is a medium-term maintenance risk for crocus if it is extended to Intel. Check before a Mesa major upgrade.

### Gaps
- Actual default renderer in GTK 4.20/4.22 on Haswell, and whether GTK falls back automatically when required Vulkan features are absent. The GTK NEWS file and source were not reviewed.
- GTK's Vulkan version requirement relative to what hasvk exposes; a search excerpt mentions a 1.3 requirement but the release is unconfirmed, and hasvk's current version was not found.
- Whether hasvk remains built by default in current Mesa and distribution packages.
- Whether Mutter 50 itself ever uses Vulkan on this GPU. No source found; check with the local logs.
- Current status of the `gl` value of `GSK_RENDERER`, which may alias ngl in newer GTK. Use `ngl`.

## Dock magnification, rounded-corner shaders, window animations: frame impact and regressions on GNOME 49/50

### Takeaway
No frame-impact measurement exists for any of these in the sources found. The only confirmed GNOME 50 Mutter performance regression concerned NVIDIA, not Intel.

### Cited Findings
- Mutter 50.1 reverted a change around `META_DEADLINE_TIMER_STATE_INHIBITED` because it caused performance problems with at least some NVIDIA drivers, and fixed NVIDIA freezes and deadlocks (search excerpt, article blocked; April 2026) — [Phoronix](https://www.phoronix.com/news/GNOME-Mutter-50.1)
- Dash to Dock show/hide animation lag was reported, with size and opacity tweaks not helping (filed against GNOME 3.36, older data; search excerpt, and which of the two linked issues holds which report was not confirmed by opening them) — [dash-to-dock #424](https://github.com/micheleg/dash-to-dock/issues/424)
- A GNOME 45 report describes the dock intermittently rendering at the wrong scale during hide (older data; same caveat) — [dash-to-dock #2175](https://github.com/micheleg/dash-to-dock/issues/2175)
- A Rounded Window Corners listing declares GNOME 45-50 support — [extensions.gnome.org](https://extensions.gnome.org/extension/9668/rounded-window-corners/)
- One secondary article says a memory leak reported in the project in 2022 remains unresolved; I did not verify this against the tracker — [comss.ru](https://www.comss.ru/page.php?id=20377)
- `CornerEffect` and `RefractionEffect` leaked GPU memory in BMS v74 tests (+239 MB and +482 MB over 10 isolated cycles), while native static blur and simple colour effects did not. Note this is BMS's corner effect, not the Rounded Window Corners extension — [Issue #1099](https://github.com/aunetx/blur-my-shell/issues/1099)

### Inferences
- Since magnification, per-window corner shaders and animations all act per frame, their cost should compound with blur. Enable one at a time and compare (reasoning, not measured).
- Magnification's interaction with Dash to Dock's existing animation lag is plausible but undocumented.
- An absence of Haswell regression reports on GNOME 50 is weak evidence, because few users of this hardware file reports and the search was limited.

### Gaps
- No source addresses dock magnification performance at all, and I did not identify which dock extension provides magnification on GNOME 50.
- GNOME 49 regressions were not found. Searching GNOME GitLab directly was limited by access controls.

## VA-API on Haswell, linux-firmware, i915 vs xe on kernel 7.0

### Takeaway
Use the i965 VA-API driver (`i965-va-driver` / `intel-vaapi-driver`), not intel-media-driver. Current kernel-side status for Haswell on 7.0 could not be confirmed from a primary source, though i915 is the expected driver.

### Cited Findings
- intel-vaapi-driver covers Intel GPUs in Haswell and earlier CPUs — [BLFS](https://linuxfromscratch.org/blfs/view/git/multimedia/intel-vaapi-driver.html)
- Debian's package metadata lists Haswell among i965-va-driver's supported platforms — [Debian](https://packages.debian.org/hu/sid/i965-va-driver)
- An Arch forum reply says intel-media-driver supports Broadwell and newer only, so it does not work on Haswell (forum claim, older data; not verified against the project README) — [Arch forums](https://bbs.archlinux.org/viewtopic.php?id=255931)
- A Haswell-ULT system reported i965 2.4.0 working with no `LIBVA_DRIVER_NAME` override (Arch thread, older data) — [Arch forums](https://bbs.archlinux.org/viewtopic.php?id=255931)
- Linux 7.0's DRM changes centred on Xe SR-IOV, SVM and new hardware, with nothing found about Haswell — [Phoronix](https://phoronix.com/news/Linux-7.0-Graphics-Drivers)
- Ubuntu 26.04 systems were observed on kernel 7.0.0-x — [Issue #869](https://github.com/aunetx/blur-my-shell/issues/869)

### Inferences
- `vainfo` should report the i965 driver; set `LIBVA_DRIVER_NAME=i965` only if autodetection fails.
- Haswell's codec limits mean some modern formats will fall back to CPU decoding, which matters on a 4-core i5 if blur is also active. The specific codec list must be taken from `vainfo` output, as it is not established by these sources.

### Gaps
- No primary source confirming Xe does not bind Haswell on 7.0. My background understanding is that Haswell uses i915 and Xe targets newer GPUs. Verify locally with `lspci -k`.
- Whether linux-firmware is needed for HD 4600 graphics. My unverified understanding is that GuC/HuC firmware applies to later generations, so Haswell should not depend on it. Check `dmesg | grep -i firmware`.
- Decode/encode profile list for Haswell under i965, and maintenance status of intel-vaapi-driver in 2026.

## Memory footprint, boot time, extension stability and Wayland session crashes

### Takeaway
No reliable GNOME 50 memory or boot-time baseline was found, so both must be measured locally. The stability risk is well understood: on Wayland, a Shell crash ends the entire session and all unsaved work in it.

### Cited Findings
- On Wayland, GNOME Shell is also the compositor, so its death ends every client session and returns to GDM, looking like a logout. In one case the fault was a NULL dereference in `libgjs`, seen on GNOME 46 with Quick Settings Tweaks. Removing the extension stopped the crashes, but the mechanism was a hypothesis with no core dump — [dev.to](https://dev.to/ordinary_techie/anatomy-of-a-shell-crash-3jm3)
- The same author reports stability after upgrading to Ubuntu 26.04 with GNOME 50 (single anecdote) — [dev.to](https://dev.to/ordinary_techie/anatomy-of-a-shell-crash-3jm3)
- A CSS-only stub extension with empty enable/disable functions was reported to crash the Shell on lock on GNOME 45 (older data) — [gnome-shell #7339](https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/7339)
- Repeated logout/login cycles crashing the Shell and disabling extensions was reported on GNOME 40 (older data) — [gnome-shell #4382](https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/4382)
- Memory leaks in an extension can reach tens of GiB in gnome-shell: about 24 GiB after 202 window launches, and disabling popup blur on one AMD system dropped active GPU memory from 14.22 to 1.405 GiB — [Issue #1116](https://github.com/aunetx/blur-my-shell/issues/1116)
- Older data on gnome-shell memory: about 200 MB post-boot in 2013 — [Red Hat Bugzilla](https://bugzilla.redhat.com/show_bug.cgi?id=1014265). Growth of 50-100 MB per sleep cycle in GNOME 3.28 — [gnome-shell #1776](https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/1776). Neither should be used as a GNOME 50 number.
- Much of apparent "used" RAM is reclaimable buffer and cache — [Ubuntu Discourse](https://discourse.ubuntu.com/t/very-high-memory-usage-in-ubuntu-minimal/4961)

### Inferences
- Stability risk scales with the number of extensions and whether they patch Shell internals. Keep a minimal set, and prefer extensions with an active maintainer and confirmed support for the exact Shell version. Abandonment was the issue in the dev.to case.
- GNOME 51 already exists (reports in #869 and #1116), so a distribution update could break a tuned extension set. Pin the Shell version where practical, and have a recovery route: from a TTY or SSH, `gnome-extensions disable <uuid>`, or `gsettings set org.gnome.shell disable-user-extensions true` (commands from background knowledge, test before relying on them).
- For leak checks, compare gnome-shell's memory before and after a repeatable open/close loop, as in #1116.

### Gaps
- GNOME 50 idle RSS with and without extensions: no reliable source.
- Boot-time data for GNOME 50 or Haswell: none found. Use `systemd-analyze blame` and `systemd-analyze critical-chain` locally (background knowledge). I found no evidence on how much extensions add to login time.

## How to measure in practice, and why VirtualBox tests do not represent real GPU performance

### Takeaway
Use Sysprof for missed frames and frame phases, `intel_gpu_top` for GPU load, and test on the real machine. VirtualBox has a different driver stack, often software rendering, so its results cannot rate HD 4600.

### Cited Findings
- Mutter and GNOME Shell have Sysprof integration since GNOME 3.33/3.34, covering missed-frame profiling (2019, older data; the feature's current form was not re-verified) — [Phoronix](https://www.phoronix.com/news/GNOME-Mutter-Sysprof-Lands)
- The integration tracks size negotiation, paint and pick, and helps identify when a frame was missed and what was running — [feaneron.com, 2019](https://feaneron.com/2019/05/31/profiling-gnome-shell/)
- Timing marks are hard to interpret without call stacks — [same author, 2023](https://feaneron.com/2023/02/07/profiling-optimizing-gnome-software/)
- `intel_gpu_top` reads i915 PMU counters, plus RAPL power and IMC memory bandwidth — [Debian manpage](https://dyn.manpages.debian.org/bookworm/intel-gpu-tools/intel_gpu_top.1.en.html)
- A 2024 VMSVGA guest with 3D enabled reported an SVGA3D renderer, yet the GNOME session reported llvmpipe (software) — [OpenMandriva forum](https://forum.openmandriva.org/t/gnome-and-virtual-box-fails-to-get-to-desktop-after-install-and-update/6557)
- A forum benchmark on VirtualBox 7.1.4 with GNOME Wayland scored 240 with 3D off and 520 with it on (one user, unnamed benchmark; only shows VM-configuration sensitivity) — [linux.org.ru](https://www.linux.org.ru/forum/desktop/17788423)
- A 2025 report found VMSVGA 3D rendering GNOME incorrectly on NixOS guests — [r/virtualbox mirror](https://lr.us.psf.lt/r/virtualbox/comments/1k4bgbd/nixos_guest_3d_acceleration_rendering_problems)
- Older data: a 2015 report of GDM leaving a guest on llvmpipe — [GNOME Bugzilla 749390](https://bugzilla.gnome.org/show_bug.cgi?id=749390)

### Inferences
- A VM does not use crocus, hasvk or i915 on the guest side, so it cannot reproduce Haswell driver bugs, its frame timing, or its video decode. It remains useful for testing extension loading, settings and crash recovery only.
- Suggested protocol on the real machine (procedure is my recommendation, not a sourced benchmark):
  1. Confirm the renderer: `glxinfo -B` or GNOME Settings > System > About, and check `lspci -k` for i915.
  2. Baseline: no extensions, record idle `intel_gpu_top` and gnome-shell RSS.
  3. Add one effect at a time. Run the same script for each: overview toggle, window open/close, video playing behind a blurred panel, scrolling.
  4. Capture with Sysprof during that script, and count missed frames against the display's refresh budget (16.7 ms at 60 Hz).
  5. Leak test: 50 window open/close cycles and notifications, then compare gnome-shell memory.
  6. Check `journalctl -b 0` for `JS ERROR` or segfaults, and `journalctl -b -1` after a crash ([dev.to](https://dev.to/ordinary_techie/anatomy-of-a-shell-crash-3jm3) documents the journal commands).
- Pass rule (my suggestion): keep an effect only if it adds no sustained missed frames in the script and memory returns to a stable level after the leak test.

### Gaps
- Whether Haswell exposes all PMU counters to `intel_gpu_top` on kernel 7.0 was not found. Run it to check.
- Current Sysprof UI and Mutter counter names in GNOME 50 were not verified.
- No official VirtualBox statement was found on current Wayland/VMSVGA acceleration limits. VM evidence here is forum-grade.
