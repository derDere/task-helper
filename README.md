# TaskHelper

![Screenshot](screenshot.png)

[derdere.github.io/task-helper](https://derdere.github.io/task-helper/)

TaskHelper is a tiny cross‑platform hobby app (built with [Flet](https://flet.dev)) that helps you stay focused on only your TOP 3 personal chores or free‑time tasks instead of drowning in an endless list. You add tasks quickly, optionally give them a due date, then run a super‑light pairwise comparison to let a simple Elo algorithm float the most important items to the surface. The Tasks page only shows what really matters now; everything else waits quietly.

> Goal: Make daily task triage frictionless – add quickly, prioritize intelligently, execute confidently.

## Key Features

- See ONLY your current top 3 tasks (auto‑sorted by importance).
- Fast add form (title, description, optional due date).
- Simple pairwise "which is more important" sorter using Elo – stops early, no overthinking.
- Calendar view with quick per‑day progress (completed/total) and day drill‑down.
- Recently completed list (undo mistakes).
- Inline edit, delete, complete/undo.
- Local JSON file storage (no accounts, no cloud, no complexity).
- Light purple theme, minimal UI.

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

