# HomeLabNext Adaptive Solar Shading v0.1.4

## Stability / restart release

### Changed

- Removed the legacy Morning Opening function from Adaptive Solar Shading.
  Morning/evening operation belongs to the separate Morning & Evening Cover Control blueprint.
- Removed the direct trigger on the optional Day Mode helper.
- Added configurable Home Assistant startup grace period (default: 90 seconds).
- Added restart-safe re-evaluation after Home Assistant starts.
- Added recovery for a daily movement counter when Home Assistant was offline at midnight.
- Added explicit detection for covers without `current_position`.
- Extended debug status with Day Mode, ownership, position and cooldown.
- Updated `source_url` for the current `homelabnext/home-assistant` repository.

### Home Assistant restart behavior

- Shading ownership is preserved through the required `input_boolean`.
- Existing ownership is validated against the real cover position after startup.
- No cover movement is performed blindly during startup.
- If required sensors/covers are unavailable, the blueprint waits for a later evaluation.
- Normal close/release delays remain active after restart.

### Important helper note

Do not set an `initial:` value on the shading ownership `input_boolean`.
Home Assistant can restore the previous input_boolean state when no initial
value is configured.
