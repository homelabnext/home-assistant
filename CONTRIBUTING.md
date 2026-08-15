# Contributing

Contributions, bug reports and improvement suggestions are welcome.

## Repository layout

Keep components in the appropriate directory:

- Automation blueprints: `blueprints/automation/<name>/`
- Packages: `packages/`
- Dashboard components/examples: `dashboards/`
- Templates: `templates/`
- General documentation: `docs/`

A blueprint should keep its YAML file and component-specific README in the same directory.

## Blueprint changes

When changing a blueprint:

1. Update the version in the blueprint name if the change is released as a new version.
2. Keep `source_url` pointed at the exact YAML file in the `main` branch.
3. Update the component README when behavior, requirements or helpers change.
4. Add the change to `CHANGELOG.md`.
5. Test imports and configuration in Home Assistant before publishing a release.

## Naming

Use lowercase directory and file names with underscores where required by the existing component naming convention.
