# HomeLabNext – Adaptive Solar Shading

**Current version:** v0.1.5

Adaptive Solar Shading is responsible only for temporary daytime shading.
Normal morning/evening opening and closing belongs to the separate
**Morning & Evening Cover Control** blueprint.

## Required

- Cover entity with a usable `current_position` attribute
- Outdoor temperature sensor
- `input_boolean` shading state helper

## Restart behavior

v0.1.4 explicitly handles Home Assistant restarts:

1. The `homeassistant start` trigger waits **90 seconds by default** before evaluating.
2. This gives cover and sensor integrations time to restore their states.
3. No immediate blind movement is performed after startup.
4. Normal close/release delays still apply after the startup grace period.
5. The shading ownership `input_boolean` is expected to restore its previous state.
   Do **not** configure an `initial:` value for this helper.
6. If ownership says ON but the cover position no longer matches the shading
   position, stale ownership is cleared after the configured movement grace.
7. A daily movement counter that missed midnight because Home Assistant was
   offline is reset automatically once the blueprint runs again.

If required entities are still unavailable after startup grace, the blueprint
fails safe and does not move the cover. The periodic trigger evaluates again later.

## Day Mode

Day Mode remains optional. When used together with Morning & Evening Cover Control,
select the same Day Mode helper for the same cover.

The direct optional Day Mode entity trigger was removed in v0.1.4 so an empty
optional helper cannot invalidate the automation. Changes are picked up by the
regular evaluation cycle.

## Debugging

The debug status now includes additional operational information:

- Day Mode
- shading ownership
- current cover position
- remaining cooldown
- explicit message when `current_position` is unsupported

Example:

```text
IDLE | SOUTH | Day=ON | Own=OFF | Pos=100 | CD=0m | ...
```

## Import

GitHub:

`https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/solar_shading/solar_shading.yaml`

Raw import URL:

`https://raw.githubusercontent.com/homelabnext/home-assistant/main/blueprints/automation/solar_shading/solar_shading.yaml`


## v0.1.5 counter recovery fix

v0.1.5 fixes a daily movement counter edge case introduced in v0.1.4.

If the counter was already `0` at midnight, `counter.reset` did not change the entity state.
Its `last_changed` timestamp could therefore remain on the previous day. The restart
recovery check then incorrectly treated the counter as stale on every periodic evaluation,
reset it again and stopped the automation before solar shading logic could run.

The recovery reset now only runs outside the midnight trigger when:

- the counter value is greater than `0`, and
- its `last_changed` date is older than the current day.

A counter already at `0` no longer blocks normal shading evaluation.
