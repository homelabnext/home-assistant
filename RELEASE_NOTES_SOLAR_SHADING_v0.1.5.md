# HomeLabNext Adaptive Solar Shading v0.1.5

## Bug fix

### Fixed

- Fixed an issue in the daily movement counter recovery introduced in v0.1.4.
- If the counter was already `0` at midnight, its `last_changed` timestamp could remain on the previous day.
- This caused every periodic blueprint evaluation to enter the counter recovery branch and stop before solar shading logic was evaluated.
- Recovery now only resets an old counter outside midnight when its value is greater than `0`.

### Result

A daily movement counter already at `0` no longer blocks Adaptive Solar Shading after midnight.
