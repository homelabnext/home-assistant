# HomeLabNext – Morning & Evening Cover Control

Daily opening and closing control for Home Assistant covers.

## What is required?

Only one input is mandatory:

- **Cover** – the cover / roller shutter controlled by this automation.

All helpers are optional.

## Optional helpers

| Helper | Required? | Purpose |
|---|---|---|
| Day Mode (`input_boolean`) | No | Connects this cover to Adaptive Solar Shading |
| Debug status (`input_text`) | No | Shows readable automation status |
| Manual override (`input_boolean`) | No | Suppresses automatic movement, including recovery after reloads/restarts. Can be activated by HA UI actions or selected wall switch inputs. |
| Vacation mode (`input_boolean`) | No | Enables the separate vacation schedule |
| Window / door contacts (`binary_sensor`) | No | Delays evening closing while a contact is open |

## Manual override from a wall switch

Select the Shelly input entity that belongs to the physical wall switch. Depending on
the Shelly input configuration, this is either an `event` entity (Input Mode
`Button`) or a `binary_sensor` (Input Mode `Switch`). The selected input sets
the Manual Override helper, so automatic recovery does not close the cover again.

## Using it with Adaptive Solar Shading

The two blueprints can be used independently.

If the same cover also uses **HomeLabNext Adaptive Solar Shading**, create/select one Day Mode helper for that cover and use the **same helper in both blueprint instances**.

Example:

```text
Morning & Evening Cover Control
Morning opening
→ Day Mode ON
→ Adaptive Solar Shading may control the cover during daytime

Evening
→ Day Mode OFF
→ Morning & Evening Cover Control closes the cover
```

For covers that **do not use solar shading**, leave **Day Mode helper empty**. No `shading_active`, Solar Shading debug, Lux sensor or other Solar Shading-specific helper is needed.

If different covers have different schedules, use one Day Mode helper per cover.

## Import

View on GitHub:

`https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml`

Raw import URL:

`https://raw.githubusercontent.com/homelabnext/home-assistant/main/blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml`

## Version

v0.1.7
