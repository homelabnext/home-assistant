# Battery Monitor – Low Battery Notification

Überwacht beliebig viele Batterie-Sensoren und meldet niedrige Batteriestände über ein zentrales Notification-Script.

## Funktionen

- mehrere `sensor`-Entities mit `device_class: battery`
- Warnschwelle frei wählbar, Standard 10 %
- Warnung beim Unterschreiten
- Prüfung nach Home-Assistant-Neustart
- manueller Test über „Aktionen ausführen“
- optionale tägliche Erinnerung
- optionale Entwarnung

## Voraussetzung

Ein Script, das die Variablen `title` und `message` verarbeitet, z. B. `script.home_notification`.

Beispiel: [`examples/scripts/home_notification.yaml`](../../../examples/scripts/home_notification.yaml)

## Import

Blueprint-URL:

```text
https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/battery_monitor/battery_monitor.yaml
```

## Empfohlene Einstellung

| Einstellung | Empfehlung |
|---|---:|
| Warnschwelle | 10 % |
| Startverzögerung | 30 s |
| Tägliche Erinnerung | Ein |
| Erinnerung | 10:00 Uhr |
| Entwarnung | Optional |

## Test

Für einen Test kann die Warnschwelle kurzzeitig über den aktuellen Batteriestand gesetzt werden. Danach in der erzeugten Automation „Aktionen ausführen“ verwenden. Der Blueprint prüft dann alle ausgewählten Sensoren direkt.
