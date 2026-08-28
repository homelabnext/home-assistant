# Notifications & Monitoring v1.0.0

Mit diesem Release kommen zwei neue Monitoring-Blueprints und eine zentrale Benachrichtigungsstruktur für Home Assistant hinzu.

## Neu

- **Battery Monitor**: überwacht beliebig viele Batterie-Sensoren, warnt unter einem frei wählbaren Grenzwert und kann täglich erinnern.
- **Freezer Monitor**: überwacht Stromversorgung, Leistungsaufnahme und Türkontakt eines Gefrierschranks.
- **Zentrale Notifications**: Blueprints senden nur Titel und Nachricht an ein auswählbares Notification-Script. Dort können iPhones, Telegram-Gruppen und weitere Ziele zentral gepflegt werden.
- **Restart-safe Checks**: kritische Zustände werden nach einem Home-Assistant-Neustart erneut geprüft.

Die Blueprints liegen unter `blueprints/automation/battery_monitor/` und `blueprints/automation/freezer_monitor/`.
