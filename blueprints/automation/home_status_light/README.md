# Home Status Light

**Version: v0.1.1**

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

## Zeitsteuerung für Aufgaben

Für die Kategorie **Aufgabe** gibt es die Einstellung **Aufgabe – früheste Anzeigezeit**. Standard ist `17:00:00`.

Das ist besonders für Müll geeignet: Ein Müll-Binary-Sensor kann bereits direkt nach Mitternacht auf `on` wechseln, die Statuslampe bleibt aber bis zur eingestellten Uhrzeit aus. Zur eingestellten Uhrzeit prüft der Blueprint den Status automatisch erneut und schaltet die Lampe ein, wenn weiterhin eine offene Aufgabe vorhanden ist.

Andere Kategorien wie Warnung, Kritisch oder Alarm sind von dieser Zeitbegrenzung nicht betroffen.

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

Solange mindestens einer dieser Sensoren `on` ist und die eingestellte Startzeit erreicht wurde, leuchtet die Statuslampe standardmäßig blau. Wird die Aufgabe am Dashboard bestätigt und der zugehörige Binary-Sensor dadurch `off`, berechnet der Blueprint den Status sofort neu. Sind keine weiteren Zustände aktiv, wird die Lampe ausgeschaltet.

## Neustartverhalten

Der Blueprint wird bei einem Home-Assistant-Start ebenfalls ausgeführt und berechnet den aktuellen Status neu. Vor der eingestellten Aufgabe-Startzeit bleibt eine reine Aufgabenanzeige aus; nach der Startzeit wird sie bei einem Neustart direkt wiederhergestellt.

## Manuelle Installation

Die YAML-Datei kann alternativ unter `/config/blueprints/automation/homelabnext/home_status_light.yaml` abgelegt werden. Anschließend Blueprints/Automationen neu laden und daraus eine Automation erstellen.

## Stand

Version `v0.1.1` ergänzt eine frei einstellbare Startzeit für die Kategorie Aufgabe. Dadurch kann z. B. Müll erst am Nachmittag oder Abend optisch signalisiert werden, obwohl der zugrunde liegende Binary-Sensor bereits seit Mitternacht aktiv ist.
