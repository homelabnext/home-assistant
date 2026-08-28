# Freezer Monitor – Gefrierschrank überwachen

Überwacht einen Gefrierschrank über eine schaltbare Steckdose mit Leistungsmessung und einen Türkontakt.

## Funktionen

- Warnung wenn die Stromversorgung ausgeschaltet wird
- Warnung bei ungewöhnlich langer sehr niedriger Leistungsaufnahme
- erste Türwarnung nach frei wählbarer Zeit
- zweite kritische Türwarnung
- Prüfung nach Home-Assistant-Neustart
- optionale Entwarnung für die Stromversorgung
- zentrale Benachrichtigung über ein auswählbares Script

## Voraussetzung

- Switch-Entity des Shelly bzw. der Steckdose
- Power-Sensor in Watt
- Binary Sensor für den Türkontakt
- zentrales Notification-Script, z. B. `script.home_notification`

## Import

Blueprint-URL:

```text
https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/freezer_monitor/freezer_monitor.yaml
```

## Empfohlene Startwerte

| Einstellung | Empfehlung |
|---|---:|
| Shelly aus | 5 s |
| Leistung unter | 0,5 W |
| Niedrige Leistung | 45 min |
| Türwarnung | 2 min |
| Kritische Türwarnung | 5 min |
| HA-Startprüfung | 30 s |

> Die Leistungsgrenze und Dauer müssen zum realen Verbrauchsprofil des Gefrierschranks passen. Ein Kompressor kann im normalen Betrieb längere Zeit ausgeschaltet sein.
