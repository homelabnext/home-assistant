# Repository Structure

The HomeLabNext Home Assistant repository is intentionally broader than a blueprint-only repository.

## Blueprints

```text
blueprints/<domain>/<component-name>/
```

Current automation blueprints:

```text
blueprints/automation/solar_shading/
blueprints/automation/morning_evening_cover_control/
```

Keeping each component in its own directory allows its YAML, README and future examples/assets to stay together.

## Packages

Reusable Home Assistant package examples belong in:

```text
packages/
```

## Dashboards

Dashboard examples, cards and views belong in:

```text
dashboards/
```

## Templates

Reusable template sensors or template snippets belong in:

```text
templates/
```

## Documentation

Repository-wide documentation belongs in:

```text
docs/
```

Component-specific documentation stays beside the component itself whenever possible.
