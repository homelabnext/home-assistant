# HomeLabNext – Adaptive Solar Shading

Adaptive solar shading for Home Assistant covers and roller shutters.

## What it does

The blueprint decides whether solar shading is required by evaluating the actual conditions at the facade instead of relying on fixed times.

With an illuminance sensor configured, the default decision uses:

1. Illuminance
2. Outdoor temperature
3. Solar position

At least **2 of 3** must request shading.

Without an illuminance sensor, **outdoor temperature and solar position must both match**.

## Orientation presets

| Orientation | Azimuth | Minimum elevation |
|---|---:|---:|
| East | 60–140° | 10° |
| South | 120–240° | 15° |
| West | 220–300° | 10° |

All solar values can be overridden per automation.

## Default thresholds

| Setting | Default |
|---|---:|
| Lux close | 20,000 lx |
| Lux release | 15,000 lx |
| Outdoor close | 20 °C |
| Outdoor release | 18 °C |
| Close delay | 10 min |
| Release delay | 20 min |
| Target position | 25 % |
| Cooldown | 30 min |

## Required helper

Each cover needs one `input_boolean` that stores whether HomeLabNext owns the current shading state.

Example:

```yaml
input_boolean:
  homelabnext_shading_example:
    name: "HomeLabNext Shading – Example"
```

A full example helper package is included in:

`packages/solar_shading_helpers.example.yaml`

## Optional helpers

- `input_text` for readable debug status
- `timer` for a manual pause
- `counter` for daily movement limits
- `input_boolean` for manual override
- `input_boolean` for external summer mode
- `input_boolean` / `binary_sensor` for external keep-closed conditions

## Debugging

During setup, assigning an `input_text` helper is strongly recommended.

Example states:

```text
IDLE | WEST | Lux=12500 ✗ | Out=23.4 ✓ | Sun=✗
CLOSE READY | EAST | Lux=24600 ✓ | Out=22.7 ✓ | Sun=✓
WAIT CLOSE | 10 min | WEST
SHADING | Pos=25% | WEST
RELEASE READY | Lux=7800 | Out=21.5 | Hold=OFF
```

This makes it easy to see which condition is preventing a movement.

## Manual control

HomeLabNext will never open a cover just to reach the shading position.

Example with target 25%:

- 100% → HomeLabNext may move it to 25%
- 50% → HomeLabNext may move it to 25%
- 25% → no movement
- 10% → no movement
- 0% → no movement

If a HomeLabNext-controlled cover is moved manually, HomeLabNext releases ownership and can optionally start a pause timer.

## Summer / Winter

In Summer mode, thermal shading is enabled.

In Winter mode, thermal shading is disabled so solar gains can contribute to heating.

An external helper can also control the season mode.


## Day mode / existing morning and evening automations

If another system already opens and closes a cover — for example a schedule in the **Shelly app** — configure an optional `input_boolean` as the **Day mode helper**.

For covers with independent schedules, use **one Day Mode helper per cover**.

### Automatic synchronization

Enable **Automatically synchronize Day Mode** when the external system cannot directly switch a Home Assistant helper.

The default behavior is:

- Cover >= **95% open** + `sun.sun` is `above_horizon` → Day Mode **ON**
- Cover <= **5% open** + `sun.sun` is `below_horizon` → Day Mode **OFF**

This means an external morning opening hands the cover over to Adaptive Solar Shading automatically. An external evening close returns it to night mode.

The additional sun check is important: manually closing a cover completely during the day does **not** switch Day Mode off.

If the external schedule opens slightly before sunrise or closes before sunset, the blueprint also evaluates `sun.sun` changes and can synchronize once the sun crosses the horizon.

Example helper:

```yaml
input_boolean:
  homelabnext_daymode_living_room:
    name: "HomeLabNext Day Mode – Living Room"
```

### Direct Home Assistant control

If your morning/evening automation already runs in Home Assistant, automatic synchronization is not necessary. In that case:

**Morning**
1. Open cover.
2. Turn Day Mode ON.

**Evening**
1. Turn Day Mode OFF.
2. Close cover.

While Day Mode is OFF, thermal solar shading will not start.

## External keep-closed condition

An optional external entity can keep a cover closed even after thermal shading is released.

This is intended for additional modules such as:

- TV glare protection
- privacy
- night mode

## Installation

Import the blueprint directly from GitHub using:

`https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/solar_shading/solar_shading.yaml`

Or copy the YAML file to:

`/config/blueprints/automation/HomeLabNext/solar_shading.yaml`

Then reload automations / blueprints in Home Assistant.


## Debug improvements in v0.1.3

The Day Mode helper now has its own trigger and the debug status shows the values Home Assistant actually sees.

Examples:

```text
IDLE | SOUTH | Day=ON | Lux=... | Out=... | Sun=...
DAY OFF | Helper=off | Auto=ON | Pos=0 | Sun=NIGHT
DAY ON | Helper=on | Auto=ON | Pos=100 | Sun=DAY
```

This makes it much easier to diagnose a wrong helper assignment, stale automation configuration or unexpected external cover movement.

## Status

Release v0.1.3. Test carefully with your own cover integration and facade geometry before relying on it unattended.
