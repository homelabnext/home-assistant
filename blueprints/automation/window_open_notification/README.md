# Fenster-offen-Erinnerung

**Version: v0.1.0**

Sendet eine Benachrichtigung, sobald ein Fenster die eingestellte Zeit ununterbrochen offen ist. Optional folgen weitere Erinnerungen im gewählten Abstand.

[In Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fwindow_open_notification%2Fwindow_open_notification.yaml)

## Voraussetzungen und Einrichtung

- Einzelne Fensterkontakte als `binary_sensor` mit `on` = offen und `off` = geschlossen.
- Zentrales Skript mit den Variablen `title` und `message`, standardmäßig `script.home_notification` (Home Notification v3).
- Keine zusätzlichen Helper.

Blueprint importieren, eine Automation erstellen und die Kontakte auswählen. Mehrere Kontakte werden unabhängig voneinander überwacht; jeder erhält seine eigene Nachricht und Wartezeit. Für unterschiedliche Zeitvorgaben pro Raum mehrere Automationen erstellen. Denselben Kontakt nicht in mehreren Automationen auswählen, wenn keine doppelten Meldungen gewünscht sind.

| Einstellung | Vorgabe |
| --- | --- |
| Erste Meldung nach | 15 Minuten durchgehend offen |
| Wiederholung | Aus |
| Wiederholungsabstand | 15 Minuten ab der ersten Meldung |
| Benachrichtigungsskript | `script.home_notification` |
| Titel | 🪟 Fenster noch offen |

Beispiel bei 15 Minuten Offenzeit und 10 Minuten Wiederholungsabstand: Meldungen nach 15, 25, 35 Minuten, solange das Fenster offen bleibt.

Nachricht: „Fenster Küche ist seit 25 Minuten offen. Bitte schließen.“ Der Name stammt aus dem Anzeigenamen des Kontakts; die Minuten werden auf ganze Minuten abgerundet.

## Schließen, Ausfälle und erneutes Öffnen

Schließen vor Ablauf der Offenzeit verhindert die erste Meldung. Schließen nach der ersten Meldung beendet die Wiederholungen. Auch `unknown`, `unavailable` oder das Entfernen eines Kontakts beenden den laufenden Vorgang. Keine Entwarnungsnachricht.

Ein erneuter Wechsel nach `on` startet die vollständige Offenzeit neu. Das gilt auch nach einer Unterbrechung durch einen ungültigen Zustand. Kurzes Schließen und sofortiges Wiederöffnen darf keine alte Wiederholung fortsetzen; der Blueprint prüft deshalb zusätzlich den Zeitpunkt des Öffnungsvorgangs. Reine Attributänderungen setzen die Offenzeit nicht zurück.

Bis zu 100 gleichzeitig laufende Erinnerungen pro Automation. Nachrichten werden über `script.turn_on` mit `data.variables.title` und `data.variables.message` übergeben.

## Neustart und Neuladen

Wartezeiten und laufende Wiederholungen werden nicht gespeichert. HA-Neustart, Neuladen oder Deaktivieren der Automation brechen sie ab. Nach dem Laden wird eine neue Wartezeit durch einen Zustandswechsel nach `on` gestartet. Ein Kontakt, der bereits davor `on` war und unverändert bleibt, wird nicht automatisch nachträglich gemeldet. Nach dem Import mit einem geschlossenen Fenster beginnen und es zum Test öffnen.

Dieses Verhalten entspricht der [Home-Assistant-Dokumentation zu Triggern](https://www.home-assistant.io/docs/automation/trigger/). Diese Version enthält keine Wiederaufnahme über persistente Helper.

## Test auf der Zielinstallation

1. Offenzeit und Wiederholungsabstand auf jeweils 1 Minute stellen, Wiederholung einschalten.
2. Fenster öffnen: erste Nachricht nach 1 Minute, weitere Nachricht nach einer weiteren Minute.
3. Fenster schließen: keine weiteren Nachrichten.
4. Erneut öffnen und vor Ablauf einer Minute schließen: keine Nachricht.
5. Zwei Kontakte testen: beide müssen unabhängig voneinander melden.
6. Anschließend gewünschte Zeiten einstellen.

„Aktionen ausführen“ verschickt absichtlich keine Nachricht, da dabei der auslösende Fensterkontakt fehlt. Zum Test einen echten Zustandswechsel verwenden. YAML und Jinja-Logik werden lokal geprüft; der Import- und Versandtest muss in Home Assistant erfolgen.
