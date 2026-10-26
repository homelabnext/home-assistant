# HomeLabNext – Home Assistant

Reusable Home Assistant blueprints, packages, dashboard components, templates and documentation from **HomeLabNext**.

The repository is structured so that every component can be used independently. You do not need to install the entire repository.

## Blueprints

### Zigbee Thermostat Scheduler

Control one or more climate entities with up to three selectable weekday profiles, two time windows per profile, direct temperature settings, optional input_select mode switching and a time-limited manual override.

**Current version:** v0.7.0

[Blueprint file](blueprints/automation/zigbee_thermostat_scheduler/zigbee_thermostat_scheduler.yaml) · [Documentation](blueprints/automation/zigbee_thermostat_scheduler/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fzigbee_thermostat_scheduler%2Fzigbee_thermostat_scheduler.yaml)

### Adaptive Solar Shading

Adaptive solar protection for covers based on facade orientation, illuminance, outdoor/indoor temperature, sun position, manual overrides, movement limits and optional Day Mode coordination.

**Current version:** v0.1.3

**Blueprint file**

`blueprints/automation/solar_shading/solar_shading.yaml`

**GitHub**

https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/solar_shading/solar_shading.yaml

**Import into Home Assistant**

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fsolar_shading%2Fsolar_shading.yaml)

[Documentation](blueprints/automation/solar_shading/README.md)

---

### Morning & Evening Cover Control

Daily opening and closing control for covers using sunrise/sunset or fixed schedules, weekday/weekend limits, vacation mode, window contacts, manual override and optional coordination with Adaptive Solar Shading.

**Current version:** v0.1.7

**Blueprint file**

`blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml`

**GitHub**

https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml

**Import into Home Assistant**

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fmorning_evening_cover_control%2Fmorning_evening_cover_control.yaml)

[Documentation](blueprints/automation/morning_evening_cover_control/README.md)

### Starlink Position Monitor

Monitors Starlink location, mast alignment, obstruction/impairment, stuck motors and optional azimuth/elevation deviations. Notifications are sent through a configurable central Home Assistant notification script.

**Current version:** v0.1.4

**Blueprint file**

`blueprints/automation/starlink_position_notification/starlink_position_notification.yaml`

**GitHub**

https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/starlink_position_notification/starlink_position_notification.yaml

**Import into Home Assistant**

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fstarlink_position_notification%2Fstarlink_position_notification.yaml)

[Documentation](blueprints/automation/starlink_position_notification/README.md)

### Waste Collection Notification

Daily waste collection reminder through the central notification script. Select multiple waste sensors and a notification time; all matching collections are combined into one message. No helpers required.

**Current version:** v0.1.1

[Blueprint file](blueprints/automation/waste_collection_notification/waste_collection_notification.yaml) · [Documentation](blueprints/automation/waste_collection_notification/README.md)

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fwaste_collection_notification%2Fwaste_collection_notification.yaml)

### Window Open Notification

Notifies when selected window contacts remain open beyond a configurable duration. Optional reminders repeat independently per window until it closes or becomes unavailable. Uses the central notification script; no helpers required. Timers do not persist across reloads or restarts.

**Current version:** v0.1.0

[Blueprint file](blueprints/automation/window_open_notification/window_open_notification.yaml) · [Documentation](blueprints/automation/window_open_notification/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fwindow_open_notification%2Fwindow_open_notification.yaml)

### Ventilation Notification

Room-specific humidity and ventilation advice based on indoor/outdoor moisture content, with closing reminders, confirmation delays and optional repeats. Requires one dedicated Text helper (maximum length 255) per automation. Automatically resumes observation after restarts.

**Current version:** v0.1.0

[Blueprint file](blueprints/automation/ventilation_notification/ventilation_notification.yaml) · [Documentation](blueprints/automation/ventilation_notification/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fventilation_notification%2Fventilation_notification.yaml)

### Alexa Motion Music

Resume an Alexa Media Player Echo on motion and pause after a configurable period without motion. Optional fallback to an existing Alexa routine (default: Radio Chillout), optional volume setting and periodic pause recovery. No helpers required.

**Current version:** v0.1.0

[Blueprint file](blueprints/automation/alexa_motion_music/alexa_motion_music.yaml) · [Documentation](blueprints/automation/alexa_motion_music/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Falexa_motion_music%2Falexa_motion_music.yaml)

### Home Status Light

Central RGB status light driven by binary sensors or persistent Input Boolean helpers. Configure a status category color, priority and optional blinking behavior.

**Current version:** v0.1.2

[Blueprint file](blueprints/automation/home_status_light/home_status_light.yaml) · [Documentation](blueprints/automation/home_status_light/README.md)

### Mailbox Vibration Notification

Notifies through the central script when the mailbox vibration sensor triggers and latches a selected Input Boolean until the mail is collected. Use that helper as a Home Status Light source and set its Attention color to yellow.

**Current version:** v0.1.0

[Blueprint file](blueprints/automation/mailbox_vibration_notification/mailbox_vibration_notification.yaml) · [Documentation](blueprints/automation/mailbox_vibration_notification/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fmailbox_vibration_notification%2Fmailbox_vibration_notification.yaml)

### Paperless Notifications

Daily reminders for the Paperless inbox and optional one-time-per-version update alerts. Uses the repository's central `script.home_notification` with `title` and `message`.

**Current version:** v0.1.0

[Blueprint file](blueprints/automation/paperless_notifications/paperless_notifications.yaml) · [Documentation](blueprints/automation/paperless_notifications/README.md)

[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fpaperless_notifications%2Fpaperless_notifications.yaml)

## How the cover blueprints work together

The blueprints are independent. If the same cover uses both, they can share one `input_boolean` as a Day Mode helper.

```text
Morning & Evening Cover Control
            │
            ├── Morning opening
            │        ↓
            │   Day Mode ON
            │        ↓
            └── Adaptive Solar Shading
                     ↓
                Daytime shading
                     ↓
              Evening closing
                     ↓
               Day Mode OFF
```

For covers without Adaptive Solar Shading, the Day Mode helper in Morning & Evening Cover Control can remain empty.

## Repository structure

```text
home-assistant/
├── blueprints/
│   └── automation/
│       ├── mailbox_vibration_notification/\n│       │   ├── README.md\n│       │   └── mailbox_vibration_notification.yaml\n│       ├── home_status_light/\n│       │   ├── README.md\n│       │   └── home_status_light.yaml\n│       ├── paperless_notifications/
│       │   ├── README.md
│       │   └── paperless_notifications.yaml
│       ├── solar_shading/
│       │   ├── README.md
│       │   └── solar_shading.yaml
│       ├── morning_evening_cover_control/
│       │   ├── README.md
│       │   └── morning_evening_cover_control.yaml
│       ├── starlink_position_notification/
│       │   ├── README.md
│       │   └── starlink_position_notification.yaml
│       ├── waste_collection_notification/
│       │   ├── README.md
│       │   └── waste_collection_notification.yaml
│       ├── window_open_notification/
│       │   ├── README.md
│       │   └── window_open_notification.yaml
│       ├── ventilation_notification/
│       │   ├── README.md
│       │   ├── helpers.example.yaml
│       │   └── ventilation_notification.yaml
│       └── alexa_motion_music/
│           ├── README.md
│           └── alexa_motion_music.yaml
├── packages/
│   └── solar_shading_helpers.example.yaml
├── dashboards/
├── templates/
├── docs/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The empty top-level directories are intentional. They provide stable locations for future HomeLabNext packages, dashboard components, templates and documentation.

## Manual blueprint installation

A blueprint can also be copied manually into your Home Assistant configuration, for example:

```text
/config/blueprints/automation/homelabnext/solar_shading.yaml
```

or:

```text
/config/blueprints/automation/homelabnext/morning_evening_cover_control.yaml
```

or:

```text
/config/blueprints/automation/homelabnext/starlink_position_notification.yaml
```

After copying a blueprint, reload automations/blueprints or restart Home Assistant if required by your setup.

## Versioning and releases

Blueprints are versioned independently. Release tags should identify both the component and its version, for example:

```text
solar-shading-v0.1.3
morning-evening-v0.1.1
starlink-position-monitor-v0.1.4
home-status-light-v0.1.2\nmailbox-vibration-notification-v0.1.0\nwaste-collection-notification-v0.1.1
window-open-notification-v0.1.0
ventilation-notification-v0.1.0
alexa-motion-music-v0.1.0
```

Repository-wide structural changes are documented separately in [CHANGELOG.md](CHANGELOG.md).

## License

See [LICENSE](LICENSE).
