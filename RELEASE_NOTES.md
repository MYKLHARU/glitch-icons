## 2.0.3-tv — MyAEW source update (APK not yet released)

- Added the approved transparent 320 × 180 MyAEW animation, including the reference's glitch timing, red/blue channel displacement, uncompressed faded reflection, and an exact first-frame copy held for 2,000 ms.
- Added automatic Android / Google TV matching for `com.kiswe.androidtv.myaew/com.kiswe.androidtvlive.ui.ContainerActivity`, verified from the signed MyAEW 2.5.14 (156) manifest.
- Updated the Sports catalogue, provider alias, picker XML, thumbnail and both appfilter XML files. The source has 1,196 icons and 2,121 component mappings; all prior 1,195 animations and 2,120 mappings are preserved.
- Synchronized both TV source archives with the latest Android 5+ compatibility implementation and the new icon. Updated existing verification counts and included MyAEW in the on-device frame sample.
- The APK build passes locally. The release must be signed with the existing private TV key before it can update an installed TV edition. Existing release APKs are unchanged.

---

## Six-frame animation update

1,195 transparent APNG icons, each 320 × 180 pixels, with their original filenames.

- Original five animation frames and timings preserved.
- An exact copy of frame 1 appended as frame 6 and held for two seconds.
- Red/blue glitch effects and faded mirrored reflections retained.
- Infinite looping.

Download **Icons-glitch.zip** for the artwork. Download **Glitch-Icons-GitHub-Pages.zip** for the complete website source and all assets.

The APNGs use `.png` filenames. Animation support depends on your browser, app or launcher. This release does not contain an APK.

