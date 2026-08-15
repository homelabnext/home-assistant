# Changelog

All notable changes to the HomeLabNext Home Assistant repository are documented here.

Blueprints are versioned independently. A repository restructuring does not change blueprint behavior or blueprint versions unless explicitly stated.

## Repository

### 2026-08-15

- Renamed the repository structure from a blueprint-only layout to the general `homelabnext/home-assistant` layout.
- Moved automation blueprints below `blueprints/automation/<blueprint-name>/`.
- Updated all blueprint `source_url` entries to the new repository paths.
- Updated GitHub and Home Assistant import URLs.
- Added stable top-level directories for `packages`, `dashboards`, `templates` and `docs`.
- Consolidated documentation so each blueprint keeps its primary documentation beside its YAML file.

## Adaptive Solar Shading

### v0.1.3

- Added a direct trigger for Day Mode helper state changes.
- Added explicit Day Mode diagnostics to debug output.
- Debug now shows helper state, automatic synchronization state, cover position and day/night state.
- Added Day Mode information to IDLE, CLOSE READY and SHADING status messages.

### v0.1.2

- Added automatic Day Mode synchronization for externally controlled covers.
- Designed for schedules running outside Home Assistant, for example in the Shelly app.
- Day Mode ON: cover >= 95% while sun is above the horizon.
- Day Mode OFF: cover <= 5% while sun is below the horizon.
- Added configurable open/closed thresholds.
- Recommended one Day Mode helper per cover for independent schedules.
- Full manual closing during daytime does not automatically switch Day Mode off.

### v0.1.1

- Added optional Day Mode helper.
- Added coordination with existing sunrise/sunset or morning/evening cover automations.
- Solar shading is disabled while Day Mode is OFF.
- Planned cover movements while Day Mode is OFF no longer trigger manual pause.
- Solar-shading ownership is released when Day Mode is disabled.

### v0.1.0

- Initial public release.

## Morning & Evening Cover Control

### v0.1.1

- Day Mode helper is now optional.
- Debug status helper is now optional.
- Manual override helper is now optional.
- Vacation mode helper is now optional.
- Window/door contacts remain optional.
- Only the cover entity is required.
- Added clearer descriptions for standalone use and integration with Adaptive Solar Shading.
- Updated blueprint source URL for the current repository structure.

### v0.1.0

- Initial public release.
- Added sunrise/sunset offsets and fixed-time schedules.
- Added weekday/weekend time limits.
- Added vacation mode.
- Added optional window/door contacts with deferred evening closing.
- Added manual override and configurable cover positions.
- Added Home Assistant restart recovery.
- Added Day Mode helper synchronization and debug status support.
