# Home Assistant Notifications & Monitoring

Dieses Paket enthält die neuen Blueprints für Batterie- und Gefrierschranküberwachung sowie ein Beispiel für ein zentrales Notification-Script.

## Enthalten

- `blueprints/automation/battery_monitor/battery_monitor.yaml`
- `blueprints/automation/freezer_monitor/freezer_monitor.yaml`
- `examples/scripts/home_notification.yaml`
- `docs/notifications.md`
- `CHANGELOG-notifications.md`
- `RELEASE-v1.0.0.md`
- `COMMIT_MESSAGE.txt`

## Prinzip

Die Blueprints erkennen Zustände und übergeben nur `title` und `message` an ein auswählbares Script. Das Script verteilt anschließend an die gewünschten Kanäle.

```text
Blueprint → script.home_notification → iPhones / Telegram / weitere Ziele
```

Damit bleiben Monitoring und Zustellung voneinander getrennt.
