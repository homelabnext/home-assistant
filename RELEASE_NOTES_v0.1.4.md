# Morning & Evening Cover Control v0.1.4

## Added
- Automatic manual override detection for external/manual cover movements.
- Blueprint-initiated movements are ignored via Home Assistant context.
- Manual override resets at the next regular morning opening.
- Optional fallback timeout (default 12 h, 0 disables it).

## Behavior
Manual movement -> configured Manual Override helper ON -> evening recovery no longer immediately reverses the movement.

## Commit
`Add automatic manual override detection v0.1.4`

## Tag
`morning-evening-v0.1.4`

## Release title
`Morning & Evening Cover Control v0.1.4`
