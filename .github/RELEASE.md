# Release Process

This document explains how to create a release for TaskHelper.

## Automated Release (Recommended)

The repository includes a GitHub Actions workflow that automatically builds the APK and creates a GitHub release.

### Steps to Create a Release

1. **Create a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Automatic build and release:**
   - The workflow automatically triggers when you push a tag matching the pattern `v*.*.*` (e.g., v1.0.0, v2.1.3)
   - It builds the APK using Flet
   - Creates a GitHub release with auto-generated release notes
   - Uploads the APK to the release

3. **Check the release:**
   - Go to the [Releases page](https://github.com/derDere/task-helper/releases)
   - Find your new release
   - Download the APK from the release assets

## Manual Workflow Trigger

You can also manually trigger the build workflow from the GitHub Actions tab:

1. Go to the [Actions tab](https://github.com/derDere/task-helper/actions)
2. Select "Build APK and Create Release" workflow
3. Click "Run workflow"
4. Optionally specify a version tag
5. Click "Run workflow" button

The APK will be available as an artifact in the workflow run, but won't create a GitHub release (releases are only created for tag pushes).

## Local Build (Development)

For local testing, you can build the APK manually:

```bash
# Install dependencies
pip install 'flet[all]==0.28.3'

# Build APK
flet build apk -v
```

The APK will be available in the `build/apk/` directory.

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version (v1.0.0 → v2.0.0): Incompatible API changes
- **MINOR** version (v1.0.0 → v1.1.0): Backwards-compatible functionality
- **PATCH** version (v1.0.0 → v1.0.1): Backwards-compatible bug fixes

## Prerequisites for Building

The GitHub Actions workflow handles all prerequisites automatically, but for local builds you need:
- Python 3.12+
- Java 17 (for Android SDK)
- Android SDK (installed via Flet)

## Troubleshooting

### Build fails on GitHub Actions

1. Check the workflow logs in the Actions tab
2. Ensure all dependencies are correctly specified
3. Verify the tag format matches `v*.*.*`

### APK not appearing in release

1. Ensure the tag was pushed (not just created locally)
2. Check the workflow completed successfully
3. Verify the `build/apk/` directory contains the APK in the workflow logs
