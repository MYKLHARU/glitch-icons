# Glitch Icons

## MyAEW source update — 2.0.3-tv

The Android TV source now contains **1,196 icons** and adds **MyAEW** under Sports with automatic matching. The existing 1,195 animations and 2,120 component mappings are preserved.

- [MyAEW transparent APNG](icons/MY-AEW-Glitch.apng) — 320 × 180, six frames, red/blue source-pixel glitches, a faded reflection at the logo's proportions, and a two-second clean return frame.
- [Android TV source](Glitch-Reflections-TV-source.zip) — version 2.0.3-tv (103), with Android 5+ playback and the existing focus fixes.
- [Matching evidence](mappings/myaew.json) and [appfilter entry](mappings/myaew-appfilter.xml).

| App | Android / Google TV package | Verified launcher activity |
| --- | --- | --- |
| [MyAEW](https://play.google.com/store/apps/details?id=com.kiswe.androidtv.myaew) | `com.kiswe.androidtv.myaew` | `com.kiswe.androidtvlive.ui.ContainerActivity` |

The launcher component was read from MyAEW 2.5.14 (156)'s signed Android manifest. Both appfilter XML files, the searchable catalogue, picker resources, provider alias and thumbnail include the new icon. No unrelated app mappings are replaced.

**Release status:** this is the source update. The published TV APK is still 2.0.2 with 1,195 icons; publishing 2.0.3 requires signing with the existing private TV release key. The website and older release ZIPs retain their published contents.

![MyAEW animation](icons/MY-AEW-Glitch.apng)

## Published six-frame pack

**1,195 animated icons. Real artwork distortion. Red/blue channel splits. Faded reflections.**

Each transparent APNG is **320 × 180** pixels, retains its original `.png` filename and loops through six frames. The first five animation frames are preserved; frame 6 is an exact copy of frame 1 held for **two seconds**.

- [Visit the Glitch Icons website](https://myklharu.github.io/glitch-icons/)
- [Download Glitch-Reflections.apk](https://github.com/MYKLHARU/glitch-icons/releases/latest/download/Glitch-Reflections.apk)
- [Download the complete icon pack](https://github.com/MYKLHARU/glitch-icons/releases/latest/download/Icons-glitch.zip)
- [Download the complete website source](https://github.com/MYKLHARU/glitch-icons/releases/latest/download/Glitch-Icons-GitHub-Pages.zip)
- [View releases](https://github.com/MYKLHARU/glitch-icons/releases)

## Website

The responsive site includes a 20-icon preview in four rows of five, search across all 1,195 icons, enlarged previews, individual icon downloads, pagination and a pause control. Reduced-motion preferences start the gallery on still frames.

The complete website source and assets are attached to each Release as `Glitch-Icons-GitHub-Pages.zip`. The workflow in this repository downloads the source, validates all 1,195 animations, then deploys it to GitHub Pages. To republish, use **Actions → Deploy Glitch Icons to GitHub Pages → Run workflow**. After publishing a new Release, run the workflow from the `main` branch.

## Using the icons

Extract `Icons-glitch.zip` to get the `Icons/` folder. APNG is animated PNG, so the files keep the `.png` extension. Animation support depends on your app or launcher. The Android icon-pack app is available as `Glitch-Reflections.apk`, with the same 1,195 updated animations.

## Source and validation

Extract the website source ZIP to access the HTML, CSS, JavaScript, full catalogue, original APNGs and first-frame stills. To validate and recreate the pack:

```bash
python3 tools/validate_pack.py
python3 tools/package_release.py
```

The validation checks PNG CRCs, dimensions, frame counts, infinite looping, SHA-256 hashes and the exact two-second copy of frame 1.

Names and logos belong to their respective owners. This collection is independent and is not affiliated with the brands shown.


