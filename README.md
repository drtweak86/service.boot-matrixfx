# Boot Matrix FX (Python)

A Kodi **service** add-on that renders a full-screen “digital rain” effect during startup.
- No screensaver switching
- No video playback
- Pure Python using `xbmcgui.WindowDialog` and `ControlLabel` streams

## Settings
- **Show for (seconds)**: duration overlay is shown
- **Columns**: number of glyph columns
- **Speed (px per tick)**: fall speed
- **Font**: Kodi font name (e.g. `font13`)

## Install
1. Zip the folder so the **top-level directory name equals the add-on id** (`service.boot-matrixfx/…`).
2. In Kodi: **Add-ons → Install from zip** → pick the zip.

## Dev
- Logs: `~/.kodi/temp/kodi.log` (grep `service.boot-matrixfx`)
