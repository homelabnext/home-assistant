# HomeLabNext – Starlink Position Monitor

Monitors a Starlink antenna in Home Assistant and sends push notifications through the central `script.home_notification` script.

## What it monitors

The blueprint watches these Starlink diagnostic binary sensors:

- Unexpected location
- Mast near vertical
- Obstructed / impaired
- Motors stuck (optional)

It can additionally compare the current antenna orientation against configured reference angles:

- Azimuth
- Elevation (shown as “Meereshöhe” in some German Home Assistant translations)

The default reference values are `-22°` azimuth and `71°` elevation. A deviation of up to and including `±1°` is accepted.

## Availability behavior

States such as `unknown` and `unavailable` never trigger a warning. They also do not cause a false recovery notification.

After Home Assistant starts, the blueprint waits for the configured startup delay before evaluating the current states. This gives the Starlink integration time to provide valid data.

## Notification script

The default notification target is:

`script.home_notification`

The script must accept these variables:

```yaml
title: "Notification title"
message: "Notification text"
```

## Default timing

| Setting | Default |
|---|---:|
| Warning delay | 2 minutes, editable as a number |
| Recovery delay | 2 minutes, editable as a number |
| Startup delay | 2 minutes, editable as a number |
| Orientation confirmation | Continuous for the warning delay |
| Azimuth tolerance | ±1° |
| Elevation tolerance | ±1° |

No helper entities are required.

Notification titles use standard blueprint text inputs. Timing values use
numeric minute inputs for compatibility with Home Assistant frontend versions
that do not render the dedicated text or duration selectors correctly.

## Installation

Import the blueprint directly from GitHub:

`https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/starlink_position_notification/starlink_position_notification.yaml`

Raw import URL:

`https://raw.githubusercontent.com/homelabnext/home-assistant/main/blueprints/automation/starlink_position_notification/starlink_position_notification.yaml`

Or copy the YAML file to:

`/config/blueprints/automation/HomeLabNext/starlink_position_notification.yaml`

Then reload automations / blueprints in Home Assistant.

## Version

v0.1.4
