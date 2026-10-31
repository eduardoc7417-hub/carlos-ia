# Building Carlos OS Aurora on LFS/BLFS: feasibility and execution notes (status 2026-10-31)

Abbreviations: LFS-sd = https://www.linuxfromscratch.org/lfs/view/stable-systemd/ ; BLFS-sd = https://www.linuxfromscratch.org/blfs/view/stable-systemd/ . All versions below were read from the live books on 2026-10-31.

"Crawl" means a script run for these notes. It fetched the live book pages and added up their published SBU and disk figures. The script's results are derived numbers, not figures published by LFS.

## 1. Versions, init system, GNOME coverage, package counts

### Takeaway
The current books are LFS 13.1-systemd (2026-09-01) and BLFS 13.1 (2026-09-03), with Linux 7.1.8 and GNOME 50.x. Systemd is the only maintained path. BLFS covers GNOME Shell, Mutter, GDM, GTK4, libadwaita, Wayland and Mesa crocus. It does not cover Flatpak, GNOME Software, Calamares or squashfs-tools.

### Cited Findings
- LFS is at 13.1-systemd, published 2026-09-01 — [LFS book](https://www.linuxfromscratch.org/lfs/view/stable-systemd/)
- BLFS is at 13.1, published 2026-09-03 — [BLFS book](https://www.linuxfromscratch.org/blfs/view/stable-systemd/)
- LFS 13.1 ships Linux 7.1.8, systemd 261.2, GCC 16.2.0 and glibc 2.44. It lists 86 package entries (4 are documentation or man-page tarballs) and about 628 MB of downloads — [LFS ch. 3](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter03/packages.html)
- The release upgraded 45 packages and also carries Binutils 2.47 and Python 3.14.7 — [What's new](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter01/whatsnew.html)
- SysV is frozen. On 2026-02-01 the project announced that SysV book development stops at 12.4, citing editor workload and GNOME/KDE dependence on systemd features — [Linuxiac](https://linuxiac.com/linux-from-scratch-drops-system-v-init-calls-decision-regrettable/), [Phoronix](https://www.phoronix.com/news/LFS-Dropping-SysVinit)
- The live `/view/stable/` SysV URL still shows 12.4 (2025-09-01) — [LFS SysV](https://www.linuxfromscratch.org/lfs/view/stable/) — and its BLFS counterpart lists gnome-shell 48.4 — [BLFS SysV GNOME](https://www.linuxfromscratch.org/blfs/view/stable/gnome/gnome.html)
- GNOME in BLFS 13.1: gnome-shell 50.4, Mutter 50.4, gnome-session 50.1, gnome-settings-daemon 50.1, gnome-control-center 50.4, Nautilus 50.2.2, gnome-shell-extensions 50.3, gnome-tweaks 49.0, xdg-desktop-portal-gnome 50.0, gnome-desktop 44.5 — [BLFS GNOME list](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/core.html)
- GDM is 50.2, located in the Display Managers chapter rather than the GNOME part. It has a runtime dependency on systemd — [GDM](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/gdm.html)
- GTK is 4.22.4 — [GTK4](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/gtk4.html). libadwaita is 1.9.3 — [libadwaita](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/libadwaita.html)
- Mutter lists Wayland 1.26.0, wayland-protocols 1.49, libinput 1.31.3 and Xwayland 24.1.13 as recommended for the Wayland compositor. Xorg-Server is optional, and PipeWire is required — [Mutter](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/mutter.html)
- Mesa is 26.1.7. The standard `gallium-drivers=auto` builds crocus, documented for Intel HD graphics on pre-Broadwell CPUs. Haswell Vulkan uses `intel_hasvk`, not `intel`. The kernel needs `CONFIG_DRM_I915` — [Mesa](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/mesa.html)
- A development snapshot dated 2026-10-29 already lists GDM 51.1.1, and another development page lists gnome-system-monitor 51.1 — [BLFS development search result](https://www.linuxfromscratch.org/blfs/view/svn/gnome/gnome-system-monitor.html)
- Crawl of the full index, 0 matches for: Flatpak, gnome-software, PackageKit, ostree, fwupd, malcontent, Calamares, kpmcore, yaml-cpp, squashfs, shim, sbsign, plymouth, pacman, RPM, dpkg — [BLFS index](https://www.linuxfromscratch.org/blfs/view/stable-systemd/longindex.html)

### Inferences
- GNOME 50 matches the project folder name ("macOS no GNOME 50"), so pinning BLFS 13.1 gives a documented GNOME 50 baseline. Moving to GNOME 51 means using the development book or waiting for the next release.
- 13.0 was planned for March and 13.1 shipped in September, which suggests a roughly six-month cadence. Treat this as an observed pattern, not a promise.

### Gaps
- BLFS publishes no total package count that I could find. One read of the index suggested about 500 package entries, and a crude regex counted 998 list elements, so neither is reliable. Quote it as "several hundred, not verified".

## 2. Build time

### Takeaway
Published per-package SBU values add up to about 125 SBU for LFS. The GNOME desktop closure adds roughly 117 SBU, for about 240 SBU in total. Machine time on the i5-4570 can only be known after timing binutils pass 1 on it. Debugging time will likely matter more than compile time.

### Cited Findings
- 1 SBU is the time to compile and install binutils pass 1 on one core. Other book times assume four cores (`-j4`), and Chapter 8 times include tests unless noted. SBUs vary by "dozens of minutes in some cases" — [About SBUs](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter04/aboutsbus.html)
- The book recommends at least four cores and 8 GB RAM — [Host requirements](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/hostreqs.html)
- GCC in Chapter 8 is 53 SBU with tests and needs 7.3 GB — [GCC](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter08/gcc.html)
- The kernel is 0.4 to 32 SBU, typically about 2.5 SBU — [Kernel](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/kernel.html)
- For large C++ packages, limit jobs to RAM in GB divided by 2.5 — [BLFS building notes](https://www.linuxfromscratch.org/blfs/view/stable-systemd/introduction/notes-on-building.html)
- BLFS per-package examples: Mesa 3.4 SBU, GTK4 1.5, libadwaita 1.3, Mutter 0.4 (+6.2 for tests), gnome-shell 0.5, GDM 0.2 — [Mesa](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/mesa.html), [Mutter](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/mutter.html), [gnome-shell](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/gnome-shell.html)

Crawl results, summed from the published per-page figures (not a published total):

| Scope | Sum |
|---|---|
| LFS ch. 5 | 7.0 SBU |
| LFS ch. 6 | 7.8 SBU |
| LFS ch. 7 | 3.4 SBU |
| LFS ch. 8 (with tests) | 104.3 SBU |
| Kernel (typical) | 2.5 SBU |
| **LFS total** | **about 125 SBU** |
| BLFS closure, raw (265 pages, 256 with SBU values) | 171.7 SBU, about 122 GB of build trees |
| BLFS closure, trimmed | about 117 SBU, about 53 GB of build trees |

- The closure was seeded with gnome-session, gnome-shell, shell-extensions, Nautilus, control-center, GDM, gnome-terminal, NetworkManager, BlueZ, PipeWire, WirePlumber, Mesa, GStreamer good and libav, FFmpeg, CUPS, Firefox and portal-gtk. It follows required and recommended links.
- The largest items in the closure are LibreOffice 25, Firefox 15, Qt6 14 (48 GB), LLVM 13, KF6 11 and Rust 10 SBU.
- The raw closure pulls in things a GNOME desktop does not need. Trimming removes LibreOffice, Qt6, KF6, texlive and Okular.

### Inferences
- Labeled estimate: total is about 240 SBU, or about 265 SBU if Qt6 and full KF6 are added for Calamares.
- Hypothetical machine time only. I found no measured SBU for an i5-4570, so these are arithmetic and not predictions:
  - If 1 SBU = 2 min: about 8 h
  - If 1 SBU = 3 min: about 12 h
  - If 1 SBU = 5 min: about 20 h
- The i5-4570 has 4 physical cores, matching the book's `-j4` assumption. A VM adds overhead, and Windows competes for the same cores.
- With 12 GB in the VM, 12/2.5 gives 4 jobs, so memory should not be the limit at `-j4`.
- GCC's tests dominate LFS at 53 of about 125 SBU. Keep them in the first run and in any toolchain change, because they are the main evidence of a sound toolchain.
- The closure is approximate. Runtime and optional links may be missed or over-followed, and BLFS tests are mostly not counted.

### Gaps
- No published whole-book SBU total and no published i5-4570 benchmark were found. The real number comes from timing binutils pass 1 in the actual VM.

## 3. Automation, package manager, updates and security

### Takeaway
jhalfs automates LFS and most of BLFS, but LFS includes no package manager and BLFS documents none. A distribution with an updater needs its own package layer and repository, and this is the largest piece of design work in the project. Pacman has the most LFS-specific precedent.

### Cited Findings
- jhalfs is the official ALFS tool, a rolling release cloned from `https://git.linuxfromscratch.org/jhalfs.git`. It has a BLFS extension where about 1% of scripts need manual edits — [ALFS](https://www.linuxfromscratch.org/alfs/)
- It requires git, libxslt, DocBook XML DTD, DocBook XSL and sudo, with wget optional — [ALFS download](https://www.linuxfromscratch.org/alfs/download.html)
- The BLFS tool assumes a running fresh xLFS system and a dedicated user. The only package manager regularly tested with jhalfs is porg, and that is limited to LFS. A custom-commands mechanism with templates exists — [jhalfs README](https://wiki.linuxfromscratch.org/alfs/browser/README?format=txt) (seen via search result; a direct fetch returned 403)
- LFS deliberately includes no package manager. It describes approaches including `DESTDIR` staging and package archives, as used by RPM and apt — [LFS package management](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter08/pkgmgt.html)
- The same section warns that renamed shared libraries require rebuilding dependents, and that security fixes require restarting processes (including `systemctl daemon-reexec`). It also says a build can be cloned by archiving the root partition — [LFS package management](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter08/pkgmgt.html)
- Pacman precedents:
  - An LFS-with-pacman book variant by DJ Lucas, labeled r12.3-6-wip and SysV, so it predates the current books — [LFS w/Pacman](https://www.linuxfromscratch.org/~dj/lfs-pacman-sysv-2025-03-26/chapter08/chapter08.html)
  - Armin K.'s lfs-pacman PKGBUILD set — [GitHub](https://github.com/elkrejzi/lfs-pacman)
- Other options mentioned by forum users, simplest to most complex: porg or LFSpkg, pkgtools, pkgutils, pacman — [LinuxQuestions](https://www.linuxquestions.org/questions/linux-from-scratch-13/need-a-package-manager-for-my-lfs-system-any-advice-4175694367/)
- The hints project has `dpkg.txt` and `rpm.txt` — [Hints](https://www.linuxfromscratch.org/hints/downloads/files/)
- Security now runs through a searchable Advisories application, filterable by release, package and severity — [Advisories](https://www.linuxfromscratch.org/advisories/)
- The older advisories page is marked obsolete — [old page](https://www.linuxfromscratch.org/lfs/advisories/)
- The legacy consolidated list shows entries 063 to 118 under 13.0, with five dated 2026-06-01 including sshfs (Critical) and libheif, libde265, rpcbind and 7zip (High) — [Consolidated](https://www.linuxfromscratch.org/blfs/advisories/consolidated.html)
- LFS 13.1-systemd errata showed no current items at check time — [Errata](https://www.linuxfromscratch.org/lfs/errata/stable-systemd/)
- The kernel.org longterm list is 6.18 and 6.12 (Dec 2028), 6.6 and 6.1 (Dec 2027), 5.15 and 5.10 (Dec 2026). 7.1 is not longterm — [kernel.org](https://www.kernel.org/category/releases.html)

### Inferences
- Recommended order:
  1. Reach Milestone 1 by following the book by hand or with jhalfs.
  2. Convert LFS and the BLFS closure into build recipes that stage with `DESTDIR` and package with pacman or makepkg.
  3. Rebuild everything in a clean chroot from those recipes.
- Pacman fits because PKGBUILD recipes map closely onto book commands and repository tooling is included, and it has the most LFS precedent. Dpkg and RPM are possible but have less current LFS material and heavier packaging conventions. This is a judgment, not a benchmark.
- Reproducibility basics:
  - Pin one book release.
  - Keep a local source mirror with checksums.
  - Keep recipes and configs in git.
  - Build in clean chroots.
  - Save the toolchain tarball after Chapter 7.
  - Set `SOURCE_DATE_EPOCH`.
  - Record the build log and package list per release.
  "Reproducible" here means rebuildable from pinned inputs. Bit-for-bit reproducibility is a much larger goal.
- The advisory numbering suggests up to 118 advisories for 13.0 by 2026-06-01, or about 40 per month, if numbering started at 001 with 13.0. I did not read the start of the list, so check this before quoting it.
- LFS advisories give instructions for readers, not binary updates. Aurora would have to watch them, rebuild, test and publish packages itself.
- Kernel 7.1 is not longterm, so its stable updates will likely end before long. Using a longterm kernel (6.18) reduces churn but departs from the tested book baseline, and it must be checked against GNOME 50 and the book's toolchain.

### Gaps
- Advisory counts and severities for 13.1 could not be read, because the results are not returned to a static fetch.
- I could not test whether jhalfs works with a pacman hook against 13.1.

## 4. Build host: VirtualBox or WSL2

### Takeaway
A Linux VM in VirtualBox is the reliable option because it can also boot the result. WSL2 is uncertain for loop and block-device steps and cannot test booting. Both need administrator rights on this PC.

### Cited Findings
- Minimum host versions include Bash 3.2 (`/bin/sh` must link to bash), Binutils 2.13.1, Bison 2.7, Coreutils 8.1, GCC 5.4 with g++, Make 4.0, Python 3.4, Texinfo 5.0, and Linux 5.10 with `CONFIG_UNIX98_PTYS` — [Host requirements](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/hostreqs.html)
- The book is not tested with GCC above 16.2.0 or Binutils above 2.47, and newer GCC is likely to break the build. dosfstools is needed to create an ESP — [Host requirements](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/hostreqs.html)
- Partition guidance: about 10 GB minimum, about 30 GB recommended for a primary system, ESP 128–256 MB, GPT for UEFI — [Partitions](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/creatingpartition.html)
- WSL2 runs as a VM with a Microsoft kernel, can use a custom kernel, and defaults to 50% of RAM. Its docs offer systemd support, yet the Boot settings row says "only available on Windows 11 and Server 2022" — [WSL config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)
- Community reports on LFS in WSL2 are mixed. Most of the book is said to work, but mounting and loop use are disputed, and booting is not representative — [Reddit mirror](https://lr.eu.psf.lt/r/linuxfromscratch/comments/vtgu3h), [Dev.to](https://www.Dev.to/krrishdhaneja/linux-from-scratch-on-wsl2-5g10)
- With Hyper-V, VBS or WSL2 active, VirtualBox can fall back to a slower mode (the "green turtle"). `HypervisorPresent` shows whether a hypervisor is active — [Kicksecure](https://www.kicksecure.com/wiki/VirtualBox/Green_Turtle_Issue)

### Inferences
- Use VirtualBox only, and do not enable WSL2 or Hyper-V on this PC during builds. That avoids the slower mode.
- Installing VirtualBox and enabling VT-x (BIOS) require an admin account or firmware access. The user must do these steps personally.
- Suggested VM: 4 vCPU, 12 GB RAM, one host disk of about 40–60 GB, one separate build disk of about 150–200 GB (dynamic), EFI firmware. The 421 GB free covers this, but snapshots grow, and Qt6's 48 GB build is a notable peak.
- A VM cannot test crocus on the real HD 4600. Use USB bare-metal tests for that.
- GDM hides Wayland sessions by default on virtual GPUs, and the fix is symlinking `/dev/null` to `/etc/udev/rules.d/61-gdm.rules` — [GDM](https://www.linuxfromscratch.org/blfs/view/stable-systemd/x/gdm.html). Expect this when testing GNOME inside VirtualBox.

### Gaps
- The VirtualBox manual pages I fetched did not cover Hyper-V, so the Hyper-V claims rest on secondary sources.
- I did not verify which current distro host ships GCC and Binutils at or below the book's tested limits. Run the book's version-check script on any candidate.

## 5. Live ISO, installer, Secure Boot

### Takeaway
None of this is in the books as a recipe. The live boot must be custom-built: initramfs logic, squashfs and overlay, and hybrid GRUB media. Calamares needs a substantial unsupported stack. Secure Boot stays off unless the project passes shim review, which is impractical for one person at this stage.

### Cited Findings
- BLFS `mkinitramfs` handles a single root device (by path, UUID, PARTUUID or LABEL), plus RAID and LVM, then `switch_root`. It has no live or overlay logic and does not support encrypted or network root — [mkinitramfs](https://www.linuxfromscratch.org/blfs/view/stable-systemd/postlfs/initramfs.html)
- LFS covers both BIOS and UEFI GRUB, including `grub-install --target=x86_64-efi --removable`, which writes `EFI/BOOT/BOOTX64.EFI`. Kernel options for UEFI include `EFI`, `EFI_STUB`, `VFAT_FS` and `EFIVAR_FS` — [GRUB](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/grub.html), [Kernel](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/kernel.html)
- The book states: "LFS does not have the essential packages to support Secure Boot", and it must be turned off in firmware — [GRUB](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/grub.html)
- BLFS has libisoburn 1.5.8.pl02, dosfstools 4.2 and efibootmgr 18 — [BLFS index](https://www.linuxfromscratch.org/blfs/view/stable-systemd/longindex.html)
- Hints exist for squashfs, LFS LiveCD remastering and install-from-livecd, but their age was not checked — [Hints](https://www.linuxfromscratch.org/hints/downloads/files/)
- Shim review requires:
  - Verifiable organization or person identity
  - An EV certificate used at the Microsoft Hardware Dev Center
  - Protected signing keys (for example HSM)
  - Two security contacts with PGP keys
  - SBAT entries
  - Kernel lockdown
  - A reproducible Docker build of shim 16.1
  - Since 2026-06-27, shims sent to Microsoft can only be signed by the Microsoft UEFI CA 2023
  — [shim-review](https://raw.githubusercontent.com/rhboot/shim-review/main/README.md)
- Calamares moved to Codeberg — [GitHub notice](https://github.com/calamares/calamares). It is "not a ready to use application" and distributions customize it through branding and modules — [README](https://codeberg.org/Calamares/calamares/raw/branch/calamares/README.md)
- Calamares 3.3 build dependencies: C++17, CMake 3.16+, Qt 5.15+ or 6.5+, yaml-cpp 0.5.1+, Python 3.6+, KPMcore 20.04+ (partition and fsresizer modules), KCoreAddons and extra-cmake-modules 5.78+, optional Boost.Python 1.72+, optional LibPWQuality — [CONTRIBUTING](https://codeberg.org/Calamares/calamares/raw/branch/calamares/CONTRIBUTING.md)
- An older README says `unpackfs` needs squashfs-tools and rsync, and the bootloader module needs GRUB or systemd-boot — [README snapshot](https://git.morozoff.pro/aiden/calamares/raw/commit/d756edfc9a7fcb0e59dbc248756e9446eacaed3b/README.md). This is old, so verify it against the current tree.
- BLFS has Qt 6.11.2 and KF6 but not yaml-cpp, KPMcore or squashfs-tools — [BLFS index](https://www.linuxfromscratch.org/blfs/view/stable-systemd/longindex.html)

### Inferences (not book procedures; prove each in a VM)
- Live design:
  - Compress the finished root with `mksquashfs`.
  - Write a custom init that finds the ISO by label.
  - Mount the squashfs on a loop device, combine it with a tmpfs upper layer through overlayfs, and `switch_root`.
  - Add `SQUASHFS`, `OVERLAY_FS`, `BLK_DEV_LOOP`, `ISO9660_FS` and USB storage to the kernel or initramfs.
- Boot media: `grub-mkrescue` (through xorriso from libisoburn, plus mtools) can make hybrid BIOS and UEFI media. Test CD-ROM and USB separately.
- Calamares must be customized for this system:
  - Module sequence and branding in `settings.conf`
  - Unpack the squashfs
  - Partition with KPMcore
  - Users and locale
  - Regenerate initramfs
  - Install GRUB
  - Remove live-only configuration
  Expect a Qt app on a GNOME desktop. Its look will need theming to fit Aurora.
- Calamares adds roughly Qt6 (14 SBU, 48 GB build tree) plus the needed KF6 pieces and three packages outside BLFS.
- Secure Boot: state plainly in documentation that users must disable it. Users could enroll their own keys, but that is not a mainstream install flow. Treat a signed shim as a later organization-level project.

### Gaps
- I did not find a current published guide for LFS 13.1 live ISO plus Calamares. I also did not verify whether the current Calamares dependency list is complete or the current release number.

## 6. Other missing pieces

### Takeaway
BLFS covers most of the desktop plumbing: network, Bluetooth, audio, printing and codecs. The app store is the main gap. Flatpak and GNOME Software are not in BLFS and need their own packaging work.

### Cited Findings
- BLFS has NetworkManager 1.58.1, BlueZ 5.87, PipeWire 1.6.8, WirePlumber 0.5.15, GStreamer 1.28.6 (base, good, bad, ugly, libav), FFmpeg 9.0.1, CUPS 2.4.19, cups-filters 2.0.1, SANE 1.4.0, Firefox 153.2.0esr, Epiphany 50.6, xdg-desktop-portal 1.22.1, xdg-desktop-portal-gtk 1.15.3, Bubblewrap 0.11.2 and AppStream 1.1.6 — [BLFS index](https://www.linuxfromscratch.org/blfs/view/stable-systemd/longindex.html)
- gnome-bluetooth 47.2 is present, and power-profiles-daemon 0.30 is recommended for the Shell — [GNOME list](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/core.html), [gnome-shell](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/gnome-shell.html)
- BLFS lists 21 GNOME applications, including Terminal, Calculator, Maps, Weather, Loupe, Showtime, Snapshot, Evince, File Roller and Disk Utility. GNOME Software is not listed — [GNOME apps](https://www.linuxfromscratch.org/blfs/view/stable-systemd/gnome/applications.html)
- Firmware comes from the `linux-firmware` repository with `copy-firmware.sh`, installed to `/usr/lib/firmware`. Early microcode loading is preferred, and it is needed for an early Haswell TSX erratum where glibc can misbehave. Intel GuC, HuC and DMC firmware is described for Skylake and newer — [Firmware](https://www.linuxfromscratch.org/blfs/view/stable-systemd/postlfs/firmware.html)
- Flatpak's main branch requires kernel 5.8+ — [Flatpak README](https://raw.githubusercontent.com/flatpak/flatpak/main/README.md)
- Distro packaging shows Flatpak needs ostree, polkit, appstream, bubblewrap, xdg-dbus-proxy, fuse3, libarchive, dconf and xdg-desktop-portal, and it is built with meson — [Arch](https://www.archlinux.org/packages/extra/x86_64/flatpak/), [AlmaLinux spec](https://git.almalinux.org/rpms/flatpak/src/branch/c10/flatpak.spec)
- GNOME Software's build options default to PackageKit, Flatpak, fwupd and malcontent all on — [meson_options](https://gitlab.gnome.org/GNOME/gnome-software/-/raw/main/meson_options.txt)
- Upstream says to disable PackageKit where it would not work, with `-Dpackagekit=false` as the example — [gnome-software README mirror](https://github.com/Vanilla-OS/gnome-software)

### Inferences
- GNOME Software is only a frontend. With no backend plugin it has nothing useful to install. With `-Dpackagekit=false -Dfwupd=false -Dmalcontent=false` and Flatpak on, it can act as a Flathub storefront. That is the shortest route.
- It will not update the OS itself. Aurora's own pacman updates would need a separate mechanism or a custom plugin.
- Packaging needed outside BLFS: ostree, Flatpak, xdg-dbus-proxy (not checked in the index) and gnome-software. Plymouth is also absent, so a graphical boot splash is extra work.
- Redistribution: a public ISO must ship license texts and source, including firmware license terms. Shipping H.264 and similar codecs raises patent questions in some jurisdictions. Get legal advice before a wide public release rather than relying on these notes.
- For Haswell, the crocus and hasvk choices are documented. Software video acceleration for this GPU likely needs `intel-vaapi-driver`, which appears in the index, but I did not read its page.

### Gaps
- Not checked individually: Wi-Fi supplicant page, gnome-initial-setup, and PipeWire Bluetooth codec options.

## 7. Existing LFS-derived distributions and maintenance burden

### Takeaway
Derived distributions exist, and they are generally small projects with their own package tooling. One person can sustain a personal system, but a public distribution with security updates is a continuous job. Reducing scope is the main control.

### Cited Findings
- NuTyX is LFS/BLFS-inspired, French, developed for about 16 years by Thierry Nuttens, with the Cards package tool — [Linux Magazine 2023](https://www.linux-magazine.com/Issues/2023/268/Personal-Touch), [Ubunlog](https://en.ubunlog.com/nutyx/). A 26.06.1 listing exists — [MajorGeeks](https://www.majorgeeks.com/files/details/nutyx_linux.html)
- Venom Linux is LFS-based and CRUX-inspired, with the bash package manager scratchpkg and SysV init. Sources are community pages rather than official documentation — [DistroWatch mirror](https://backiee.wasmer.app/https_distrowatch_com/venom), [scratchpkg](https://github.com/venomlinux/scratchpkg/blob/master/README.md)
- Pacman-based personal LFS systems exist — [DJ Lucas's variant](https://www.linuxfromscratch.org/~dj/lfs-pacman-sysv-2025-03-26/chapter08/chapter08.html), [Armin K.](https://github.com/elkrejzi/lfs-pacman)
- Even the LFS project dropped SysV partly because of volunteer workload — [Linuxiac](https://linuxiac.com/linux-from-scratch-drops-system-v-init-calls-decision-regrettable/)

### Inferences
- Lessons: every lasting derivative added a package manager early. Small teams stay viable by limiting scope and automating builds.
- Recurring work for Aurora:
  - Advisory triage and rebuilds
  - Kernel updates
  - Book upgrades, probably twice a year
  - GNOME updates that can break macOS-like extensions and themes
  - Rebuilding the ISO and testing the installer
  - Hosting and signing a repository
- A rough judgment, not a measurement: several hours per week for a credible public release, with spikes around upgrades.
- Scope controls:
  - One architecture only
  - Follow only BLFS book versions
  - Flatpak for apps
  - A small base
  - Automated VM smoke tests
  - Call early public builds experimental, without security guarantees
- Main risks:
  - Slow or missed security fixes
  - Library-upgrade breakage without dependency metadata
  - Unsupported combinations outside the book
  - Secure Boot excluding some users
  - Qt/KPMcore installer weight
  - Installer bugs that can wipe disks
  - Limited hardware coverage in testing
  - 240+ SBU feedback loops on one machine
  - Sole-maintainer risk

### Gaps
- No reliable published measurement of maintainer hours for LFS derivatives was found.

## 8. Exact starting steps to Milestone 1 (bootable text-mode LFS in a VM)

### Takeaway
Create a Linux host VM, build LFS 13.1-systemd on a second virtual disk, then prove it by booting a new VM containing only that disk. Measuring the SBU in Chapter 5 gives the first real time estimate.

### Cited Findings
- Chapters: II preparation (2–4), III cross toolchain and temporary tools (5–7), IV system, configuration and bootloader (8–11) — [LFS contents](https://www.linuxfromscratch.org/lfs/view/stable-systemd/)
- GRUB, kernel options, partitioning and host requirements are as cited above — [GRUB](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/grub.html), [Kernel](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter10/kernel.html), [Partitions](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/creatingpartition.html), [Host requirements](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter02/hostreqs.html)
- Set a performance power profile before timing builds, and rebuild with one job if a parallel step fails — [About SBUs](https://www.linuxfromscratch.org/lfs/view/stable-systemd/chapter04/aboutsbus.html)

### Inferences (procedure assembled from the book; follow the book's exact commands)
1. **On Windows (user with admin rights):** check that VT-x is enabled in firmware. Check that `HypervisorPresent` is False: `(Get-CimInstance Win32_ComputerSystem).HypervisorPresent`. Install VirtualBox from the official site.
2. **Create the host VM:** EFI, 4 vCPU, 12 GB RAM, host disk 40–60 GB, second disk 150–200 GB. Install a mainstream Linux distro. Take a snapshot.
3. **Verify the host:** install build tools and run the book's `version-check.sh` (section 2.2). Fix `/bin/sh` if it does not link to bash. Confirm GCC is at or below 16.2.0 and Binutils at or below 2.47.
4. **Prepare the target disk:** GPT with ESP (256 MB, vfat), optional BIOS boot partition (1 MB) and ext4 root. Set `LFS=/mnt/lfs`, mount it, and create `$LFS/sources`.
5. **Download sources:** fetch the book's package and patch lists plus `md5sums`, then verify checksums. Keep a copy, since this is the start of the source mirror.
6. **Create the `lfs` user and environment** (Chapter 4), with `MAKEFLAGS=-j4`.
7. **Time binutils pass 1:** `time` it as the book describes. Record 1 SBU. Multiply by about 125 and about 240 for the first evidence-based estimates.
8. **Build Chapters 5–7.** Run the book's cleanup and back up the temporary system, and take a VM snapshot here.
9. **Build Chapter 8** with tests, saving logs. Compare test failures with the book's expected notes before continuing.
10. **Configure the system** (Chapter 9) and build the kernel (Chapter 10). Enable the book's options, the UEFI options and the VM's storage and network drivers (for VirtualBox defaults, likely AHCI and e1000). Install GRUB with `--target=x86_64-efi --removable`.
11. **Pass/fail test:** power off, create a new EFI VM with only the LFS disk attached, and boot it. Milestone 1 passes when all of these hold:
    - A login prompt appears without host help.
    - Root login works.
    - `uname -r` shows 7.1.8.
    - `/etc/lfs-release` shows 13.1 (or the book's equivalent release file).
    - `systemctl --failed` is empty or understood.
    - Network works if configured.
    - The VM reboots cleanly.
12. **Before BLFS:** snapshot and archive the root partition. Then decide on the package manager and re-express the steps as recipes, before the desktop stack is built.

Suggested later milestones:
- M2: pacman-based rebuild in a clean chroot
- M3: GNOME 50 on Wayland in the VM
- M4: GNOME on the real HD 4600 from USB (crocus)
- M5: live ISO without an installer
- M6: Calamares install in a VM
- M7: update repository
- M8: first public experimental ISO

### Gaps
- The VM-specific driver list and exact chapter section numbers were not all verified, so follow the live book text at each step. No personal timing exists until step 7 is run.
