# Glitch Reflections

**1,196 animated icons. Real artwork distortion. Red/blue channel splits. Faded reflections.**

Each transparent animated PNG is **320 × 180**, with six frames and an exact copy
of frame 1 held for **two seconds** at the end. Existing icons retain their
original filenames; MyAEW is available as `MY-AEW-Glitch.apng`.

- [Visit the website](https://myklharu.github.io/glitch-icons/)
- [Download Glitch Reflections TV 2.0.3](https://github.com/MYKLHARU/glitch-icons/releases/latest/download/Glitch-Reflections-TV-2.0.3.apk)
- [Download the complete 1,196-icon ZIP](https://myklharu.github.io/glitch-icons/downloads/Icons-glitch-2.0.3.zip)
- [Download the MyAEW APNG](icons/MY-AEW-Glitch.apng)
- [View releases and previous downloads](https://github.com/MYKLHARU/glitch-icons/releases)

## Website

The gallery includes search, enlarged previews, individual icon downloads,
pagination, pause controls and sorting by **Newest first**, **Featured first**,
**A–Z** or **Z–A**. Newest first shows MyAEW ahead of the original imported pack.
Reduced-motion preferences start the gallery on still frames. PayPal and Ko-fi
support links are retained.

The GitHub Pages workflow combines the published base website archive with the
tracked updates in [website/](website/README.md), validates every APNG, publishes
the complete versioned icon ZIP and deploys the site. Run **Actions → Deploy
Glitch Icons to GitHub Pages → Run workflow** from `main` to republish.

The [base website archive](https://github.com/MYKLHARU/glitch-icons/releases/latest/download/Glitch-Icons-GitHub-Pages.zip)
contains the original artwork. The tracked repository updates supply the current
catalogue additions, gallery code, sorting and download links.

## MyAEW Android TV update — 2.0.3-tv

MyAEW appears under Sports with automatic matching. Both appfilter files, the
searchable catalogue, picker resources, provider alias and thumbnail are updated.
All previous 1,195 animations and 2,120 component mappings are preserved.

| App | Android / Google TV package | Verified launcher activity |
| --- | --- | --- |
| [MyAEW](https://play.google.com/store/apps/details?id=com.kiswe.androidtv.myaew) | `com.kiswe.androidtv.myaew` | `com.kiswe.androidtvlive.ui.ContainerActivity` |

The component was read from MyAEW 2.5.14 (156)'s signed Android manifest. See the
[matching evidence](mappings/myaew.json) and [appfilter entry](mappings/myaew-appfilter.xml).

The TV APK uses the existing TV release key and can update TV 2.0.0–2.0.2.
It supports Android 5.0 or later and remains separate from the original
`Glitch-Reflections.apk` app. In Projectivy, choose **Glitch Reflections TV** under
Settings → Appearance → Cards → Icon pack.

## Source and release uploads

- [Android TV source and build instructions](Glitch-Reflections-TV-source.zip)
- [Compatibility source](Glitch-Reflections-TV-compatibility-source.zip)
- [Release-upload instructions](RELEASE_UPLOADS.md)
- [Upload a signed release asset](.github/workflows/release-upload.yml)

The release uploader verifies SHA-256 hashes and the existing TV signing
certificate before publishing an APK. The private signing key stays outside
GitHub. Website validation checks PNG CRCs, dimensions, frame counts, infinite
loops, hashes and the exact two-second copy of the first frame.

Names and logos belong to their respective owners. This independent collection
is not affiliated with those brands.
