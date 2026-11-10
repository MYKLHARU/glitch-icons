## 2.0.3-tv — MyAEW release

- Added the approved transparent 320 × 180 MyAEW animation, including the reference's glitch timing, red/blue channel displacement, uncompressed faded reflection, and an exact first-frame copy held for 2,000 ms.
- Added automatic Android / Google TV matching for `com.kiswe.androidtv.myaew/com.kiswe.androidtvlive.ui.ContainerActivity`, verified from the signed MyAEW 2.5.14 (156) manifest.
- Updated the Sports catalogue, provider alias, picker XML, thumbnail and both appfilter XML files. The source has 1,196 icons and 2,121 component mappings; all prior 1,195 animations and 2,120 mappings are preserved.
- Synchronized both TV source archives with the latest Android 5+ compatibility implementation and the new icon. Updated existing verification counts and included MyAEW in the on-device frame sample.
- Published `Glitch-Reflections-TV-2.0.3.apk`, signed with the existing TV key. It updates TV 2.0.0–2.0.2. Signature schemes v1/v2/v3, ZIP alignment, artwork and mapping checks pass.
- Added a manual GitHub Actions workflow for checksum-verified release uploads. APKs must use the existing TV signing certificate; no signing key is stored in GitHub.
- SHA-256: `86362d06388dd215f7416e674a44e75c18feb599b477ec693c1c59e5d4d60c3e`.

---

## Six-frame animation update

1,195 transparent APNG icons, each 320 × 180 pixels, with their original filenames.

- Original five animation frames and timings preserved.
- An exact copy of frame 1 appended as frame 6 and held for two seconds.
- Red/blue glitch effects and faded mirrored reflections retained.
- Infinite looping.

Download **Icons-glitch.zip** for the artwork. Download **Glitch-Icons-GitHub-Pages.zip** for the complete website source and all assets.

The APNGs use `.png` filenames. Animation support depends on your browser, app or launcher. This release does not contain an APK.

