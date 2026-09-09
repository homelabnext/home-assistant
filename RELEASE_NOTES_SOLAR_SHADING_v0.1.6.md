# HomeLabNext Adaptive Solar Shading v0.1.6

## Thermal decision improvement

### Added

- New Outdoor temperature gate setting
- Default mode: Required (recommended)
- Compatibility mode: Legacy 2-of-3

### Required mode

With Lux configured:

Outdoor temperature AND (Lux OR solar position)

Without Lux:

Outdoor temperature AND solar position

This prevents thermal shading on bright but cold days.

### Release behavior

When Required mode is active, falling below the configured outdoor release
temperature is sufficient to release thermal shading.

### Example

Lux: 73,706 lx ✓
Outdoor temperature: 12.8 °C ✗
Solar position: ✓

Result:

BLOCKED CLOSE | Outdoor temperature too low
