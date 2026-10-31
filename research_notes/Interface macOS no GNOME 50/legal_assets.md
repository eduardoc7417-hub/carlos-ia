# Legal and branding limits for a macOS-inspired distro (Carlos OS Aurora), and free replacement assets

General information as of 31 October 2026, not legal advice. Where a lawyer is needed, the notes say so. The "Cited Findings" bullets report sources. "Inferences" are this researcher's reasoning, not legal conclusions.

Verification key: **[read]** means the primary page or file was retrieved. **[excerpt]** means only a search excerpt or summary was seen. Facts from search results and fetches were read through a summarizing tool, so re-read the original wording before relying on any exact phrase.

## Practical do/don't list (synthesis of the sections below)

**Do**
- Use your own name, logo, wallpapers and marketing, and say plainly that Aurora is not affiliated with Apple.
- Reproduce general ideas: top bar, bottom dock, global-style menu placement, rounded windows, translucency, left-side window buttons.
- Draw window controls, icons and glass effects yourself, or take them from verifiably licensed sources, with distinct geometry and colour.
- Ship Inter (or Geist) under the OFL, with the licence text included.
- Build the ISO from a manifest, publish the matching source for every GPL component, and keep it available.
- Replace Ubuntu branding and rebuild the affected packages. Have a lawyer or Canonical confirm your "based on Ubuntu" wording.

**Don't**
- Ship SF Pro, SF Mono, New York or any font copied from macOS, including through a script that downloads it on first boot. Don't set SF as a default that expects those files.
- Ship the Apple logo in any form, including `activities-apple.svg`, an "apple" option in a tweak tool, or the keyboard glyph.
- Ship Apple's wallpapers, or wallpapers from WhiteSur/MacTahoe whose provenance you cannot document.
- Use "macOS", "Mac", "Aqua", "Finder", "Launchpad", "Spotlight", "Mission Control", "Tahoe" or similar in the product name, app names, theme names, domain or ads. Plain compatibility statements are a separate, narrower matter.
- Advertise "macOS for free", "Hackintosh alternative" or "identical to macOS", or use Apple-style packaging, site design or slogans.
- Name anything "Something Ubuntu" or "*buntu", or redistribute a modified image that still carries Ubuntu's marks.

## What Apple's terms and trademark guidelines restrict

### Takeaway
Apple's fonts, logo and names are the clearest no-go items for a shipped distro: the published SF licence limits use to mock-ups for Apple platforms and bars embedding and redistribution, and the trademark guidelines bar logo use and false association. The current macOS licence and Design Resources terms could not be read and must be checked directly.

### Cited Findings
- **SF fonts [read].** Apple's fonts page shows a San Francisco licence (EA1370, dated 2/24/2016) limiting use to creating UI mock-ups for software on iOS, OS X or tvOS. It prohibits mock-ups for non-Apple operating systems, embedding in software or other products, redistribution and derivative works, and it requires being a registered Apple Developer — [Apple Fonts](https://developer.apple.com/fonts/).
- **SF Compact [read].** A separate licence (EA1371) has the same structure, limited to watchOS mock-ups — [Apple Fonts](https://developer.apple.com/fonts/).
- **Scope gap in that page [read].** The page summary did not establish which licence governs SF Pro, SF Mono, New York or the script extensions; those are DMG downloads whose installer licence was not read — [Apple Fonts](https://developer.apple.com/fonts/).
- **Apple forum guidance [excerpt].** Forum answers say not to embed downloaded font files in an app bundle and to use system font APIs instead — [Apple Developer Forums](https://developer.apple.com/forums/thread/733267); [related thread](https://developer.apple.com/forums/thread/727961).
- **Logo [read].** Only Apple and its authorized resellers and licensees may use the Apple Logo in advertising; Apple graphic symbols need an express written licence; commercial use of the keyboard Apple glyph without consent is flagged as potentially infringing; variations and real-apple imagery are not permitted — [Apple Trademark Guidelines](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).
- **Names [read].** Apple marks may not be part of a company, product or service name except as the guidelines allow; takeoffs, variations and near-identical domains are barred; "Mac" combined with another word must not suggest false association — [Apple Trademark Guidelines](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).
- **Compatibility wording [read].** Referential phrases such as "runs on" or "compatible with" are allowed only if the product is actually compatible, the Apple mark is less prominent, and no endorsement is implied — [Apple Trademark Guidelines](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).
- **Imitation [read].** The guidelines prohibit imitating "distinctive Apple packaging, web site design, logos, or typefaces" and Apple slogans — [Apple Trademark Guidelines](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html). These are Apple's stated position, not a statement of what a court would hold.
- **Trademark list [read].** Listed: macOS, Mac, Aqua, Finder, Spotlight, Launchpad, Mission Control, Safari, Siri, Time Machine, Retina, San Francisco. Not found on the list in this check: Dock, Liquid Glass, Tahoe, Sequoia, Sonoma, Big Sur, Monterey, Ventura, SF Pro. Apple says absence is not a waiver of rights — [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html).
- **macOS licence, older versions only [excerpt].** Older macOS agreements limit use to Apple-branded computers and tie bundled fonts to use while running the software, with embedding depending on font metadata — [macOS 10.12 SLA](https://apple.com.cn/legal/sla/docs/macOS1012.pdf); [community summary of Monterey terms](https://discussions.apple.com/docs/DOC-250005658). Nothing found addresses wallpapers specifically.

### Inferences
- Copying fonts, wallpapers or icons out of macOS is a problem on several grounds at once: licence terms, copyright and, for logos, trademark. No clause on wallpapers is needed to treat them as off-limits, because copyright is the default position for artwork nobody has licensed to you.
- "Mac-like" in descriptive prose is lower risk than a name, but it still rides on Apple's mark, so keep it out of titles and ads. Absence from Apple's list ("Tahoe", "Liquid Glass") is not a safe harbour, particularly where the use evokes Apple.
- "Compatible with" wording has little real use here, since Aurora does not run on or with macOS in any meaningful sense.

### Gaps
- **The macOS Tahoe licence could not be read.** The [PDF](https://www.apple.com/legal/sla/docs/macOSTahoe.pdf) downloaded but its text could not be extracted, so no current clause or section number is given. Read it directly.
- **Apple Design Resources terms were not found.** The [resources page](https://developer.apple.com/design/resources/) as retrieved shows no terms, only links to agreements and marketing guidelines. The licence attached to each download should be read. Treat those templates as design references at most, and do not ship anything from them unless the terms clearly allow it.
- The SF Pro installer licence was not read. The fonts page licence dates from 2016 and may not be the current text for SF Pro.

## Trade dress and design patent risk for look-alike UIs

### Takeaway
A general macOS-like layout is defensible under the older copyright case law, but this is not immunity: design patents are the sharper risk, because Apple won on a GUI design patent in 2015. Risk rises with closeness to specific icons and screens, plus any marketing that trades on Apple.

### Cited Findings
- **Apple v. Microsoft (9th Cir. 1994) [excerpt].** The court used analytic dissection rather than comparing overall "look and feel", filtered out unprotectable elements, applied a "virtual identity" standard where protectable expression is narrow, and refused patent-like protection for the idea of a GUI or desktop metaphor — [Justia](https://law.justia.com/cases/federal/appellate-courts/F3/35/1435/605245/); [Wikipedia summary](https://en.wikipedia.org/wiki/Apple_Computer,_Inc._v._Microsoft_Corp.). Note that the original dispute was shaped by a licence between the parties, so read the opinion before generalizing.
- **Apple v. Samsung (Fed. Cir. 2015) [excerpt].** The court reversed the dilution verdict because the asserted iPhone trade dress was functional, but affirmed design patent infringement, including the D'305 GUI patent — [Finnegan](https://www.finnegan.com/en/firm/news/apple-v-samsung-a-new-day-for-design-patents.html); [Oblon](https://www.oblon.com/publications/apple-v-samsung-design-patents-hold-firm-trade-dress-gives-way); [Harvard copy of the opinion](https://cyber.harvard.edu/people/tfisher/IP/2015_Apple_Abridged.pdf).
- **Icon design patents exist [excerpt].** Apple-era grants such as D644246 and D644241 claim ornamental icon designs — [D644246](https://patents.justia.com/patent/D644246); [D644241](https://patents.justia.com/patent/D644241). Those two are from 2011, so their term should be checked.
- **Liquid Glass [excerpt].** Searching found a suit against Apple by Peer Global over utility patents, not any Apple design patent or trade dress registration for Liquid Glass — [IIPLA](https://iipla.org/apple-faces-patent-infringement-lawsuit-over-liquid-glass-design/). That is an absence in search results, not evidence that none exists.
- **Zorin [excerpt].** Zorin OS offers a macOS-style layout through Zorin Appearance, reported as a Pro layout alongside Windows-like layouts — [Zorin blog](https://blog.zorin.com/2021/08/09/say-hello-to-zorin-os-pro/); [Zorin forum](https://forum.zorin.com/t/zorin-os-mac-layout/493). The primary-source wording on how it describes the layout was not checked.
- **elementary OS [excerpt].** Wired-attributed reporting says it closely resembled macOS, while developers are reported as saying similarities are unintentional; no official statement was verified — [Wikipedia](https://wikipedia.com/wiki/ElementaryOS).
- **WhiteSur/MacTahoe [read].** They describe themselves as "macOS like" themes and offer an "apple" Activities icon option — [WhiteSur README](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/README.md); [MacTahoe README](https://raw.githubusercontent.com/vinceliuice/MacTahoe-gtk-theme/main/README.md).
- **Brazil [excerpt].** Trade dress has no express statutory definition and is protected through the unfair competition rules of Lei 9.279/96 (arts. 195, 209). The STJ treats protection as independent of INPI registration, requires distinctiveness (REsp 1.677.787/SC is cited as a lead case), and confusion generally calls for expert evidence (REsp 1.778.910/SP) — [Migalhas](https://www.migalhas.com.br/depeso/390744/registro-de-marca-e-posicao-do-stj-a-respeito-do-trade-dress); [Dizer o Direito](https://www.dizerodireito.com.br/2019/02/para-analisar-se-houve-imitacao-de.html); [Lei 9.279 on WIPO Lex](https://www.wipo.int/wipolex/en/text/581197).

### Inferences
- **"As close as lawfully possible" has no fixed line.** Safer practice is to copy the arrangement and behaviour and not the drawings: layout, dock and top bar are lower risk; pixel-matching specific icons, Finder or Settings windows is higher risk.
- Other projects' existence shows tolerance at most. None of the sources found shows that a court cleared these projects, and an absence of suits against small projects says nothing about Aurora's position if it grows or sells.
- Commercial sale, or marketing aimed at people wanting a Mac, likely raises exposure under the confusion and unfair-competition reasoning, more so in Brazil where no registration is needed.

### Gaps
- No Apple enforcement action against a Linux theme or distro was found, but the search was not exhaustive, so this is not evidence of non-enforcement.
- **Lawyer needed:** a design patent and registration search (USPTO, INPI, EUIPO) on Apple's current icons and Liquid Glass, and an opinion on Brazilian exposure. Software copyright under Lei 9.609/9.610 as applied to GUIs and INPI's position on GUI industrial designs were not researched.

## Ubuntu trademark policy for a derivative distro

### Takeaway
Remove Canonical's marks, rebuild the affected binaries, and never suggest endorsement. "MyDistro, based on Ubuntu" appears in Ubuntu community documentation as acceptable, but that is not an express grant in the current policy, so get it confirmed.

### Cited Findings
- **Policy version [read].** The page shows "15 July 2015", and ubuntu.com redirects to canonical.com; no newer revision was seen — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy).
- **Modified versions [read].** Redistribution of modified versions must be approved, certified or provided by Canonical; otherwise you must remove and replace the trademarks and recompile the source to create your own binaries — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy).
- **Unmodified [read].** Canonical's unmodified images and packages may be redistributed — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy).
- **Fees [read].** Canonical says a licence, possibly for a fee, may be needed for approved modified versions — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy).
- **Names [read].** Written permission is needed for use of the marks, for similar marks ending in UBUNTU or BUNTU, and for domains and merchandise; software titles may not use the marks; software for use with Ubuntu may reference it without implying endorsement — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy).
- **Other licences [read].** The policy says it does not reduce rights under the open source licences of Ubuntu's components — [Canonical IP Policy](https://canonical.com/legal/intellectual-property-policy). CIO reports the clause was added in 2015 and notes that critics thought it left uncertainty for non-copyleft packages and for Ubuntu as a whole — [CIO](https://www.cio.com/article/2949217/canonical-changes-licensing-terms-to-comply-with-gpl.html).
- **"Based on Ubuntu" [excerpt].** A Ubuntu wiki page was reported as saying "MyDistroName, based on Ubuntu" is acceptable but "Something Ubuntu" is not, and that only Canonical can give a binding statement. The direct fetch of that page returned 404, so it could not be confirmed — [Ubuntu wiki](https://wiki.ubuntu.com/DerivativeDistroHowto). The current IP policy does not address this phrase directly.
- **History [excerpt].** Canonical asked Linux Mint to sign a licence in the past, and the outcome was not established; a KDE blog argued no licence is needed if marks are removed — [KDE blog](https://blogs.kde.org/2014/02/14/no-licence-needed-kubuntu-derivative-distributions); [LWN](https://lwn.net/Articles/665263/).

### Inferences
- Likely rebranding targets are `/etc/os-release`, `base-files`, `lsb-release`, Plymouth, GDM, installer slides, `ubuntu-wallpapers`, `yaru-theme`, the Ubuntu font, apport and motd text, plus default URLs. This list is engineering judgement and not from Canonical, so audit it with a search of the built image for "ubuntu" and for logo files.
- Pointing at Canonical's unmodified archive is common practice but is not clearly covered by the page's text. What happens with packages you do not rebuild is the core uncertainty here.
- "Pro" repositories and Snap Store defaults may carry separate terms that were not reviewed.

### Gaps
- **Lawyer or Canonical confirmation needed:** whether unrebuilt Ubuntu binaries from Canonical's archive may be used in a rebranded ISO, and the exact "based on Ubuntu" wording, especially if Aurora is sold.
- Whether "Ubuntu" package names, which are hard to avoid in package metadata, cause any issue was not resolved.
- Brazilian handling of Canonical's marks was not researched; the general trademark and unfair competition rules above would be the starting point.

## Free fonts, icon sets, and WhiteSur/MacTahoe licensing

### Takeaway
Inter is the practical font choice and its licence is verified. WhiteSur and MacTahoe should not be shipped as-is: their licences (MIT, GPL-3.0) cover what the authors can license, and they do not clear Apple's rights in any Apple-derived art.

### Cited Findings: fonts

| Font | Licence (read in project file) | Reserved Font Name | Role |
|---|---|---|---|
| Inter | SIL OFL 1.1, © 2016 The Inter Project Authors — [LICENSE](https://github.com/rsms/inter/blob/master/LICENSE.txt) | None listed | UI default |
| Geist | SIL OFL 1.1, © 2023 Vercel with basement.studio — [LICENSE](https://raw.githubusercontent.com/vercel/geist-font/main/LICENSE.txt) | None listed | Alternate UI |
| Roboto Flex | SIL OFL 1.1 — [OFL](https://raw.githubusercontent.com/googlefonts/roboto-flex/main/OFL.txt) | None listed | Variable option |
| JetBrains Mono | SIL OFL 1.1 — [OFL](https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/OFL.txt) | None listed | SF Mono replacement role |

- **OFL conditions [read].** Fonts may be bundled or sold with software, but may not be sold by themselves; each copy must carry the copyright notice and licence; derivatives stay under the OFL — [OFL text](https://openfontlicense.org/open-font-license-official-text/).
- **Inter features [read].** Nine weights with italics, variable version, tabular numbers and other OpenType features — [Inter repo](https://github.com/rsms/inter).
- **Metric closeness: unverified.** Aggregators are the main source and disagree. Similarity figures (88% and 92%) come with no stated method — [Inter vs SF Pro Display](https://fontalternatives.com/compare/inter-vs-sf-pro-display/); [Inter vs San Francisco](https://fontalternatives.com/compare/inter-vs-san-francisco/). The search also returned conflicting x-height figures for Inter, and no published SF Pro figure was found. Do not describe any of these fonts as metric-compatible with SF.

### Cited Findings: icons and themes

| Project | Declared licence | Notes on contents |
|---|---|---|
| WhiteSur GTK | MIT, © 2021 WhiteSur Developers — [COPYING](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/COPYING) | `src/assets/gnome-shell/activities/activities-apple.svg` and a black variant exist, tree checked via [GitHub API](https://api.github.com/repos/vinceliuice/WhiteSur-gtk-theme/git/trees/master?recursive=1) |
| MacTahoe GTK | MIT — [repo](https://github.com/vinceliuice/MacTahoe-gtk-theme) | Same apple SVG paths; `wallpaper/MacTahoe-day.jpeg` and `-night.jpeg`, tree checked via [GitHub API](https://api.github.com/repos/vinceliuice/MacTahoe-gtk-theme/git/trees/main?recursive=1) |
| WhiteSur icons | GPL-3.0 — [repo](https://github.com/vinceliuice/WhiteSur-icon-theme) | Self-described "MacOS Big Sur style"; "alternative" set of "redesigned MacOS default icons"; `-p` option replaces "the Apple logo"; `phone-apple-iphone.svg`, `Appstore.svg` and many `distributor-logo-*` files, tree checked via [GitHub API](https://api.github.com/repos/vinceliuice/WhiteSur-icon-theme/git/trees/master?recursive=1) |
| MacTahoe icons | GPL-3.0 — [repo](https://github.com/vinceliuice/MacTahoe-icon-theme) | "MacOS Tahoe like"; includes `Appstore.svg` and many third-party `distributor-logo-*` files, tree checked via [GitHub API](https://api.github.com/repos/vinceliuice/MacTahoe-icon-theme/git/trees/main?recursive=1) |
| WhiteSur wallpapers | MIT — [repo](https://github.com/vinceliuice/WhiteSur-wallpapers) | Files named WhiteSur, Monterey, Ventura, Sonoma, Mojave-nord; no authorship or credit statement seen |
| Papirus icons | GPL-3.0 — [repo](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) | States logos belong to their trademark holders and that no approval was received |

- **No legal notice [read].** Neither the WhiteSur nor MacTahoe README addresses rights in Apple's art, and neither states a licence in the README body — [WhiteSur README](https://raw.githubusercontent.com/vinceliuice/WhiteSur-gtk-theme/master/README.md); [MacTahoe README](https://raw.githubusercontent.com/vinceliuice/MacTahoe-gtk-theme/main/README.md).
- **Separate licensing per repo [read].** The GTK themes are MIT while the matching icon themes are GPL-3.0, per the table sources above, so each needs its own compliance handling.

### Inferences

| Item | Inclusion risk | Suggested handling |
|---|---|---|
| Apple-logo SVGs | High | Delete from your fork and remove the option from scripts. The SVG path looks like the Apple glyph, based on the file start only |
| Wallpapers named after macOS releases or MacTahoe | High until provenance is shown | Do not ship; commission or use your own art |
| WhiteSur/MacTahoe icons shaped after Apple's | Medium to high | Do not ship as the default; if used as inspiration, draw new icons |
| Theme CSS/SCSS, layout code | Lower, though the code still reproduces a look | Fork with MIT notices retained, recolour, and rework window buttons and assets |
| Third-party logos in icon sets (Papirus etc.) | Common, but no permission | Normally tolerated for identifying apps; review the Windows and distro logos and strip what is not needed |

- An MIT or GPL label is only as good as the licensor's rights. If any file derives from Apple art, the label does not cure that. This reasoning follows from the absence of any provenance statement and is not a finding about specific files.
- Theme names should change too: names like "MacTahoe" and "WhiteSur" evoke Apple and should not be user-facing, even though an MIT licence would permit renaming a fork.
- Recommended stack: Inter + JetBrains Mono; a forked and cleaned MIT GTK theme renamed for Aurora; Adwaita or Papirus as the base with custom Aurora icons on top; original wallpapers.

### Gaps
- **The check for Apple app icons is incomplete.** A filtered listing was cut off, then the GitHub API rate limit blocked the follow-up, so whether the icon themes contain files named after Safari, Finder and so on is unresolved. Before use, run the check locally on a clone: `git ls-files | grep -iE 'safari|finder|launchpad|facetime|xcode|apple'`, and then compare images visually.
- Whether specific wallpapers or icons are copied from Apple was not determined. Filenames suggest inspiration but do not prove derivation.
- Licences not verified in this pass: Adwaita icon theme, Adwaita fonts, SF-like fonts beyond those in the table, Colloid, Tela, Fluent and other icon sets. Also not verified: whether the Papirus base (Paper icon set) carries separate terms.
- MacTahoe COPYING text was not opened; MIT comes from the GitHub sidebar. The wallpapers LICENSE was likewise not read.

## GPL obligations when redistributing an ISO with modified extensions and themes

### Takeaway
Publishing an ISO conveys every GPL package in it, so you must provide complete corresponding source for all of them, including your modified GNOME extensions, and keep it available. The aggregate rule stops the GPL from spreading to separate programs on the same image, but licences must still be honoured package by package.

### Cited Findings (all from [GPLv3 text](https://www.gnu.org/licenses/gpl-3.0.txt) [read])
- **Corresponding Source** means all source needed to generate, install, run and modify the work, including the scripts controlling those activities.
- **§5, modified versions:** carry prominent notices that you modified the work and a relevant date; state the licence; license the whole work under the GPL to anyone who gets a copy.
- **§5, aggregate:** including a covered work with separate and independent works on a storage or distribution medium does not extend the GPL to the others, provided the compilation does not limit users' rights.
- **§6(d), download:** offer equivalent access to source through the same place at no further charge. Source may be on a different server, including a third party's, if you keep clear directions next to the object code. You stay responsible for keeping it available as long as needed.
- **§6(a) and (b), physical media:** include source on durable media, or include a written offer valid for at least three years.
- **§6(c):** passing along someone else's offer is allowed only occasionally and noncommercially.
- **Installation Information:** applies to "User Products", such as consumer hardware. This matters if Aurora ever ships preinstalled on locked-down devices.

Source for FAQ material: the [GPL FAQ](https://www.gnu.org/licenses/gpl-faq.html) retrieval only produced its index, which lists aggregate questions, so no FAQ conclusions are relied on here.

### Inferences
- **Extensions:** GNOME Shell extensions are JavaScript, so "source" looks already present, but publish a public repository with your changes, dated modification notices, retained licence headers and build steps. Most are GPL, but confirm each extension's licence individually.
- **Compiled theme CSS:** for GPL-3.0 icon themes and any GPL theme, publish SCSS, SVG sources and generation scripts, since generated CSS or PNG alone may not be the "preferred form".
- **Practical method:** for each ISO release, archive a package manifest, source packages from your repo and Ubuntu's, ISO build scripts (such as live-build or Cubic configurations), and kernel and module sources. Do not rely only on Ubuntu's archive staying online, because §6(d) leaves the duty on you, and old releases do move. Host per-release snapshots.
- **Also needed:** an in-image licence folder (`/usr/share/doc/*/copyright`, OFL text, MIT notices) and a source-offer page linked next to the ISO download.
- **Trademarks are not licensed by the GPL's copyright grant.** Removing Canonical's or Apple's marks is compatible with these obligations.
- Check GPL-2.0-only and LGPL components, firmware blobs and proprietary codecs separately. The kernel is GPL-2.0, whose source-offer terms differ from GPLv3's.

### Gaps
- GPLv2 §3 text was not retrieved in this pass; the kernel and many packages use it.
- **Lawyer needed:** non-free firmware and codec redistribution, and any commercial sale of Aurora.
- Software patent issues with codecs were not researched.
