# Morning & Evening Cover Control v0.1.2

Bugfix release for the HomeLabNext Morning & Evening Cover Control blueprint.

## Fixed

- Corrected malformed `input_text.set_value` action blocks.
- Fixed `data:` indentation for debug status updates.
- Prevents Home Assistant from rejecting/disabling automations generated from the blueprint because of malformed action configuration.

## Upgrade

Replace:

`blueprints/automation/morning_evening_cover_control/morning_evening_cover_control.yaml`

with the v0.1.2 file and reload automations/blueprints or restart Home Assistant.

Existing automations can continue to use the same blueprint path.

## Suggested commit

`Fix Morning & Evening Cover Control action syntax v0.1.2`

## Suggested release tag

`morning-evening-v0.1.2`

## Suggested release title

`Morning & Evening Cover Control v0.1.2`
