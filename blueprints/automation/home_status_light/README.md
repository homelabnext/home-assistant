# Home Status Light

**Version: v0.1.0**

Zentrale Statuslampe für Home Assistant. Mehrere Binary-Sensoren werden Kategorien zugeordnet; die höchste aktive Priorität bestimmt Farbe, Helligkeit und optionales Blinken der ausgewählten RGB-Lampe.

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fhome_status_light%2Fhome_status_light.yaml)

## Prioritäten

1. Alarm
2. Kritisch
3. Warnung
4. Wartung
5. Aufmerksamkeit
6. Aufgabe
7. Normal

Bei mehreren gleichzeitig aktiven Zuständen gewinnt immer die höchste Priorität. Sobald dieser Zustand endet, wird automatisch der nächste aktive Zustand angezeigt.

## Vorgesehene Kategorien

| Kategorie | Standardfarbe | Beispiel |
| --- | --- | --- |
| Aufgabe | Blau | Müll rausstellen |
| Aufmerksamkeit | Orange | Fenster/Tür offen |
| Wartung | Violett | Batterie prüfen |
| Warnung | Rot-Orange | Gefrierschrank / Verbindung beeinträchtigt |
| Kritisch | Rot | Wasser / Rauch |
| Alarm | Rot, blinkend | Alarmanlage ausgelöst |
| Normal | Aus | Optional warmweiß |

Farben und Helligkeiten können in der Blueprint-Instanz angepasst werden. Für Kritisch und Alarm kann Blinken separat aktiviert werden.

## Voraussetzungen

- Eine Home-Assistant-Light-Entität mit RGB-Farbunterstützung.
- Mindestens ein Binary-Sensor für eine Statuskategorie.
- Die eigentliche Bestätigungs- oder Erledigt-Logik liegt außerhalb des Blueprints. Der Blueprint reagiert darauf, dass ein Status-Binary-Sensor von `on` auf `off` wechselt.

## Beispiel: Müll rausstellen

Für die Kategorie **Aufgabe** können beispielsweise folgende Sensoren ausgewählt werden:

```text
binary_sensor.biomull_rausstellen
binary_sensor.papier_rausstellen
binary_sensor.lvp_rausstellen
binary_sensor.restmull_rausstellen
```

Solange mindestens einer dieser Sensoren `on` ist, leuchtet die Statuslampe standardmäßig blau. Wird die Aufgabe am Dashboard bestätigt und der zugehörige Binary-Sensor dadurch `off`, berechnet der Blueprint den Status sofort neu. Sind keine weiteren Zustände aktiv, wird die Lampe ausgeschaltet.

## Neustartverhalten

Der Blueprint wird bei einem Home-Assistant-Start ebenfalls ausgeführt und berechnet den aktuellen Status neu. Damit wird nach einem Neustart nicht erst auf die nächste Zustandsänderung gewartet.

## Manuelle Installation

Die YAML-Datei kann alternativ unter `/config/blueprints/automation/homelabnext/home_status_light.yaml` abgelegt werden. Anschließend Blueprints/Automationen neu laden und daraus eine Automation erstellen.

## Stand

Version `v0.1.0` ist die erste Basisversion. Aktuell vorgesehen sind Binary-Sensoren als Eingaben. Weitere Statusquellen und Funktionen können später ergänzt werden, ohne die Prioritätslogik grundsätzlich zu ändern.
