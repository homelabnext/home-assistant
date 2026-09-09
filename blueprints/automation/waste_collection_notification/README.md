# Müllabholung-Erinnerung

**Version: v0.1.1**

Erinnert täglich zur eingestellten Uhrzeit an die bevorstehende Müllabholung. Mehrere passende Abfallarten werden in einer gemeinsamen Nachricht über das zentrale Benachrichtigungsskript versendet.

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fwaste_collection_notification%2Fwaste_collection_notification.yaml)

## Voraussetzungen

- Eingerichtete Integration [Waste Collection Schedule](https://github.com/mampfes/hacs_waste_collection_schedule).
- Je Abfallart ein Sensor, beispielsweise Biomüll, LVP, Papier und Restmüll. Die Kalender-Entitäten werden hier nicht verwendet.
- Ein Skript, das `title` und `message` annimmt; voreingestellt ist `script.home_notification` (Home Notification v3).
- Keine zusätzlichen Helper.

## Einrichtung

1. Blueprint importieren und daraus eine Automation erstellen.
2. Alle gewünschten Abfall-Sensoren auswählen.
3. Uhrzeit einstellen. Die Vorgabe ist 18:00 Uhr, in der Home-Assistant-Zeitzone.
4. Für die Erinnerung am Vortag den Vorlauf auf 1 Tag lassen.
5. Benachrichtigungsskript auswählen und die Automation speichern.

| Einstellung | Vorgabe | Bedeutung |
| --- | --- | --- |
| Abfall-Sensoren | Auswahl erforderlich | Mehrere Sensoren möglich |
| Uhrzeit | 18:00:00 | Täglicher Prüfzeitpunkt |
| Vorlauf | 1 Tag | 0 = heute, 1 = morgen, bis zu 7 Tage |
| Skript | `script.home_notification` | Empfängt `title` und `message` |
| Titel | 🗑️ Müllabholung | Frei bearbeitbar, kein Template |

Beispiel: „Morgen werden Biomüll und LVP abgeholt. Bitte rechtzeitig bereitstellen.“ Die Namen stammen aus den Anzeigenamen der Sensoren. Bei geändertem Vorlauf passt sich der Nachrichtentext an; ein selbst gewählter Titel bleibt unverändert.

## Unterstützte Sensorzustände

- Standardformat der Integration, zum Beispiel `Biomüll in 1 days`.
- Numerischer Tagesabstand, zum Beispiel `1`.
- Optionales Attribut `daysTo`.

Bei `unknown` oder `unavailable` wird der betreffende Sensor ignoriert, auch wenn er noch Attribute enthält. Andere gültige Sensoren können weiterhin eine Erinnerung auslösen. Ein frei angepasstes Datums- oder Textformat benötigt ein passendes `daysTo`-Attribut.

## Zeitverhalten und Test

Pro täglicher Auslösung wird höchstens eine Sammelmeldung gesendet. Änderungen der Sensorwerte lösen keine zusätzlichen Nachrichten aus. Ohne passende Abholung bleibt die Automation still.

Ist Home Assistant zur eingestellten Uhrzeit ausgeschaltet oder die Automation deaktiviert, wird die Erinnerung nicht nachgeholt. Die nächste automatische Prüfung erfolgt am nächsten Tag zur eingestellten Uhrzeit.

Zum Testen die Uhrzeit kurz in die Zukunft setzen und einen Sensor wählen, dessen Tagesabstand dem Vorlauf entspricht. Danach Uhrzeit und Vorlauf zurückstellen. „Aktionen ausführen“ prüft die Sensoren sofort und kann eine zusätzliche echte Nachricht verschicken.

YAML und Jinja-Templates wurden lokal geprüft. Ein Import- und Versandtest auf der Zielinstallation steht noch aus.

## Manuelle Installation

Die YAML-Datei kann alternativ unter `/config/blueprints/automation/homelabnext/waste_collection_notification.yaml` abgelegt werden. Anschließend Automationen neu laden und unter Blueprints eine Automation erstellen.
