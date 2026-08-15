# Morning & Evening Cover Control v0.1.3

Recovery and reliability update.

## Added

- Periodic missed-trigger recovery every 5 minutes.
- Overdue evening closing is automatically caught up after a blueprint or automation reload.
- Recovery respects the configured sunset offset instead of closing immediately at sunset.
- Recovery does not send another close command when the cover is already at the configured night position.

## Fixed

- Window-close catch-up now respects the configured sunset offset.
- With a positive offset such as `+00:15:00`, closing a window shortly after sunset no longer causes the cover to close before the intended time.
- Existing restart recovery remains available for Home Assistant restarts.

## Example

Sunset: `20:51`
Sunset offset: `+00:15:00`
Expected closing: `21:06`

If the original sunset trigger was missed because the automation was reloaded, the periodic recovery will detect the overdue close on the next 5-minute check and close the cover, provided:

- evening control is enabled
- manual override is off
- all configured windows/doors are closed
- the cover is not already at the configured night position

## Suggested commit

`Add missed-trigger recovery to Morning & Evening Cover Control v0.1.3`

## Release tag

`morning-evening-v0.1.3`

## Release title

`Morning & Evening Cover Control v0.1.3`
