# Glitch Icons

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

