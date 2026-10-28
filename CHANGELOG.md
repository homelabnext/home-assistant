# Changelog

All notable changes to the HomeLabNext Home Assistant repository are documented here.

Blueprints are versioned independently. A repository restructuring does not change blueprint behavior or blueprint versions unless explicitly stated.

## Zigbee Thermostat Scheduler

### v0.10.0

- Replaced periodic Logbook debug entries with an optional input_text helper that stores the latest trigger, selected rule and thermostat state without filling the Logbook.

### v0.9.0

- Added optional Logbook debug entries showing each trigger, the selected scheduler rule, current mode, schedule and override status, and thermostat HVAC/preset states.

### v0.8.0

- Added Aqara preset-aware control: only the configured `auto` preset is scheduled; `manual` and other presets pass through unchanged.
- Kept a thermostat in HVAC `off` off until heating is turned back on.
- Applied temporary target-temperature overrides only while the thermostat is in the scheduler preset; returning to `auto` clears an earlier override expiry.

### v0.7.0

- Replaced weekday/weekend schedule groups with three selectable weekday profiles, each with up to two time windows.
- Added a persistent manual thermostat override for configurable hours using an input_datetime expiry helper.
- Preserved safety priority for vacation mode, off mode and open-window temperature.
- Existing custom weekday/weekend times must be transferred to the new profiles when updating the automation.

## Mailbox Vibration Notification

### v0.1.0

- Added a notification on each vibration sensor transition to `on` through the central notification script.
- Latched a selected Input Boolean helper until the mailbox is emptied, allowing a persistent status light.
- Added setup documentation for the Home Status Light integration.

## Home Status Light

### v0.1.2

- Allowed Input Boolean helpers as status sources alongside binary sensors, so short events can drive persistent status indicators.

## Morning & Evening Cover Control

### v0.1.7

- Added optional physical wall switch input detection using selected Shelly event or binary_sensor entities.
- Physical switch presses activate the existing manual override helper, preventing schedule and recovery logic from reversing the movement.

### v0.1.6

- Fixed the 5-minute evening recovery closing manually opened covers again before sunrise while a manual override is active.
- Applied the same override protection to Home Assistant restart recovery.
- Kept the override active through the configured morning boundary in sunrise/not-before mode until the scheduled opening can actually run.

## Paperless Notifications

### v0.1.0

- Added a daily inbox reminder with a configurable time (default 19:00), current document count and Paperless URL.
- Added optional Paperless update notifications with installed/latest version details when available.
- Added persistent per-version deduplication using a selected input_text helper; startup checks do not repeat the same version.
- Reused the central notification script interface (title and message).
- Added offline tests for notification gates, unavailable states and version deduplication.

## Alexa Motion Music

### v0.1.0

- Added motion-triggered resume and delayed pause for Alexa Media Player Echo devices.
- Kept paused playback on Play only; existing playing/buffering sessions are left unchanged.
- Added optional routine fallback from stopped states after a configurable resume timeout, default Radio Chillout.
- Added optional volume control on resume/start and suppression for unavailable states.
- Added a periodic pause check after reloads and restarts without automatically starting music.
- Added documentation, import link and offline decision-template tests.

## Zigbee Thermostat Scheduler

### v0.6.0

- Added separate weekday and weekend schedules, each with an optional second time window.
- Kept all temperatures directly configurable in the blueprint and the runtime mode helper optional.
- Updated thermostat scheduler documentation and repository index.

### v0.5.0

- Replaced required schedule and temperature helpers with direct blueprint inputs for weekdays, up to two daily windows, and all operating temperatures.
- Added optional fixed operating mode and optional input_select for dashboard/runtime mode switching.
- Made window contacts, Alarmo vacation handling, and presence/power conditions optional.
- Kept vacation, off, window, manual, and auto priority explicit; added overnight time-window handling.
- Set a one-minute default refresh so state changes are applied promptly without helper state triggers.

### v0.4.0

- Added a setting to apply the optional person and power presence rule only during scheduled time windows or at any time in Auto mode.
- Kept schedule-only behavior as the default; vacation, window and operating-mode priority remain unchanged.
- Added the blueprint and documentation to the public `homelabnext/home-assistant` repository.

## Repository

### 2026-08-15

- Renamed the repository structure from a blueprint-only layout to the general `homelabnext/home-assistant` layout.
- Moved automation blueprints below `blueprints/automation/<blueprint-name>/`.
- Updated all blueprint `source_url` entries to the new repository paths.
- Updated GitHub and Home Assistant import URLs.
- Added stable top-level directories for `packages`, `dashboards`, `templates` and `docs`.
- Consolidated documentation so each blueprint keeps its primary documentation beside its YAML file.

## Ventilation Notification

### v0.1.0

- Added per-room humidity advice using indoor/outdoor vapor pressure and a configurable drying margin.
- Added humidity and drying-margin hysteresis, continuous confirmation and optional repetitions.
- Added closing advice based on reheating-adjusted humidity, cooling, drying potential and maximum opening time.
- Added automatic observation recovery after startup/reload and suppression during invalid readings.
- Added a dedicated Text helper per automation for timing and notification bookkeeping.
- Added an import link, helper example, documentation and offline template behavior tests.
- Documented physical limitations; this blueprint does not measure mold or wall-surface humidity.

## Window Open Notification

### v0.1.0

- Added independently timed reminders for multiple window contacts.
- Required a continuous configurable open duration before the first notification.
- Added optional repeated reminders with a separate interval.
- Stopped reminders on closing, unknown/unavailable states and rapid close/reopen cycles.
- Passed the contact name and elapsed open minutes to the central notification script.
- Added editable minute fields, import link and setup documentation; no helpers required.
- Documented that pending timers and repetitions do not survive automation reloads or HA restarts.

## Waste Collection Notification

### v0.1.1

- Added the blueprint to the repository with documentation and import link.
- Corrected the message to say today, tomorrow or in N days according to the configured lead time.
- Used a neutral default notification title and a standard text input.
- Added the canonical blueprint source URL.

### v0.1.0

- Initial standalone blueprint.
- Daily notification at a configurable time, default 18:00, one day before collection.
- Combined selected waste sensors into one message through `script.home_notification`.
- Supported numeric states, the standard `TYPE in N days` state and the optional `daysTo` attribute.
- Ignored unknown and unavailable sensors; no helper entities required.

## Starlink Position Monitor

### v0.1.4

- Added continuous anti-flapping confirmation for all warning states.
- Binary diagnostic sensors must remain problematic for the configured warning delay.
- Azimuth and elevation deviations now use a template trigger with the same continuous warning delay.
- Any return to normal, unknown or unavailable resets the pending warning.
- Home Assistant startup recovery also requires a continuously confirmed problem.
- Removed the periodic orientation polling interval because continuous state confirmation now handles orientation changes directly.

### v0.1.3

- Fixed malformed Jinja syntax in `actions[2].value_template`.
- Removed an extra closing parenthesis that prevented Home Assistant from saving blueprint automations.
- Validated delimiter balance across every Jinja template in the blueprint.

### v0.1.2

- Replaced text selectors with standard blueprint text inputs for broader frontend compatibility.
- Replaced duration selectors with editable numeric minute fields.
- Made the stuck-motors sensor optional so a missing selection no longer blocks saving.
- Kept unknown and unavailable states excluded from warnings and recovery notifications.
- Preserved the configurable orientation check interval.

### v0.1.1

- Fixed missing input controls for notification titles and time durations in the Home Assistant blueprint editor.
- Added explicit editable hours, minutes and seconds for warning, recovery and startup delays.
- Added a configurable orientation check interval.
- Updated blueprint UI defaults and documentation.

### v0.1.0

- Initial public release.
- Added monitoring for unexpected location, mast alignment, impairment/obstruction and stuck motors.
- Added optional azimuth and elevation monitoring with configurable reference values and tolerances.
- Added correct circular azimuth deviation calculation across the -180°/180° boundary.
- Suppressed warning and recovery notifications while required states are `unknown` or `unavailable`.
- Added delayed warning, paired recovery notification and Home Assistant startup evaluation.
- Added support for the central `script.home_notification` script.
- No helper entities required.

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
