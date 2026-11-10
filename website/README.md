# Website updates

The GitHub Pages workflow downloads the published base website archive, adds the
support section, then runs `python3 website/build.py glitch-icons`. The tracked
files here apply the current gallery code, new icons, counts, APK and ZIP links.
The existing animation validator checks the complete result before publication.

## Add an icon

1. Add its APNG and first-frame PNG to the repository's `icons/` folder.
2. Add an entry to `updates.json` with its name, filename, source paths and actual
   addition date. Keep existing entries so their dates remain stable.
3. Bump `packAsset` for a changed collection and set `apkAsset` to the matching
   published TV APK.
4. Run **Deploy Glitch Icons to GitHub Pages** from Actions.

The deployment includes a deterministic full icon ZIP in the website's
`downloads/` folder, then publishes the website using its existing permissions.
Older GitHub release files are preserved. The ZIP filename comes from `updates.json`.

Newest first sorts recorded addition dates descending and breaks ties by name.
The original imported catalogue has no individual addition dates, so those icons
share the older group and sort alphabetically within it. No dates are invented.

`build.py` preserves the five approved animation frames and writes a full-canvas,
two-second copy of the first frame at the end. This retains the existing strict
APNG validation and does not change the visible artwork or animation timing.
