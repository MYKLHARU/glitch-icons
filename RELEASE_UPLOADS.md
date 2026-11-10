# Upload signed files to Releases

The repository now has a manual **Upload a signed release asset** GitHub Actions
workflow. It can upload a finished APK or another release file without a browser
file transfer or an extra personal access token.

1. Open **Actions → Upload a signed release asset → Run workflow**.
2. Enter the direct HTTPS URL of the finished file, its versioned filename,
   expected SHA-256 hash and existing release tag. The current pack release tag
   is `v1.0.1`.
3. Run the workflow. Its summary links to the uploaded file.

The URL must return the file without an interactive sign-in. A temporary download
URL must remain valid until the run finishes. Do not enter a keystore, signing
password or account credential: this workflow uploads an already signed artifact.

For APK files the workflow checks the existing Glitch Reflections TV signing
certificate, package `dev.glitchreflections.tv`, APK signatures and ZIP alignment.
Every file must match the supplied SHA-256 hash. Only after validation does the
workflow use its repository-scoped `GITHUB_TOKEN` to upload to the chosen existing
release.

It preserves existing assets. An identical file already published under the same
name is reported as verified; a different file under that name stops the run.
Use a new versioned filename for each update. No release tag, latest-release
designation or release notes are changed by the upload workflow.

The signing key stays outside GitHub. Signing remains a separate step using the
private TV signing backup, which must never be committed or attached to Releases.
