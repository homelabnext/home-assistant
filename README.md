# HomeLabNext – Home Assistant

Reusable Home Assistant blueprints, packages, dashboard components, templates and documentation from **HomeLabNext**.

The repository is structured so that every component can be used independently. You do not need to install the entire repository.

## Blueprints

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

**Current version:** v0.1.1

**Blueprint file**

`blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml`

**GitHub**

https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml

**Import into Home Assistant**

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fmorning_evening_cover_control%2Fmorning_evening_cover_control.yaml)

[Documentation](blueprints/automation/morning_evening_cover_control/README.md)

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
│       ├── solar_shading/
│       │   ├── README.md
│       │   └── solar_shading.yaml
│       └── morning_evening_cover_control/
│           ├── README.md
│           └── morning_evening_cover_control.yaml
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

After copying a blueprint, reload automations/blueprints or restart Home Assistant if required by your setup.

## Versioning and releases

Blueprints are versioned independently. Release tags should identify both the component and its version, for example:

```text
solar-shading-v0.1.3
morning-evening-v0.1.1
```

Repository-wide structural changes are documented separately in [CHANGELOG.md](CHANGELOG.md).

## License

See [LICENSE](LICENSE).
