# HomeLabNext – Zigbee Thermostat Scheduler

Steuert Sonoff TRVZB, Aqara E1, Aqara W600 und andere Thermostate über Home-Assistant-`climate`-Entitäten.

## Direkt in der Automation einstellen

Für den normalen Betrieb sind keine Helfer für Zeitplan oder Temperaturen nötig:

- **Betriebsart:** Auto, Manuell oder Aus. Das ist die feste Betriebsart der Automation.
- **Zeitplan:** Getrennte Zeitfenster für Montag bis Freitag und Samstag/Sonntag. Pro Gruppe ist ein zweites Zeitfenster optional; auch Zeitfenster über Mitternacht sind möglich.
- **Temperaturen:** Komfort, Absenkung und Manuell direkt in den Blueprint-Einstellungen festlegen.
- **Modus zur Laufzeit:** optional einen `input_select`-Helfer aktivieren, wenn der Modus im Dashboard oder per Sprache umgeschaltet werden soll. Er muss genau die Optionen `Aus`, `Auto` und `Manuell` haben. Ist der Helfer nicht verfügbar, fällt die Automation auf die fest eingestellte Betriebsart zurück.

Änderungen an diesen Werten erfolgen in der Konfiguration der Automation. Helfer sind nur nötig, wenn Werte im laufenden Betrieb außerhalb der Automationskonfiguration veränderbar sein sollen.

## Optionale Funktionen

- **Fensterkontakt:** Bei mindestens einem offenen ausgewählten Kontakt wird die Fenster-Temperatur verwendet. Im Modus Aus bleibt das Thermostat aus.
- **Alarmo-Urlaub:** Wenn aktiviert und Alarmo den Zustand `armed_vacation` meldet, gilt die Frostschutztemperatur. Urlaub hat Vorrang vor allen anderen Regeln.
- **Anwesenheit / Homeoffice:** Im Modus Auto gilt Komfort, wenn mindestens eine ausgewählte Person zuhause ist **und** der Leistungssensor den Watt-Schwellwert überschreitet. Sonst gilt Absenkung. Die Regel kann auf die Zeitfenster begrenzt oder jederzeit angewendet werden. Sensoren in kW müssen vorher in Watt umgerechnet werden.
- **Prüfintervall:** Standardmäßig jede Minute. Änderungen an Modus, Personen, Sensoren, Alarmo oder Fensterkontakt werden spätestens dann ausgewertet.

Priorität: **Alarmo-Urlaub → Aus → Fenster offen → Manuell → Auto**. Auto schaltet zu Komfort, wenn das Zeitfenster aktiv ist und die aktivierte Anwesenheitsregel erfüllt ist; andernfalls gilt Absenkung.

## Installation

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fzigbee_thermostat_scheduler%2Fzigbee_thermostat_scheduler.yaml)

Alternativ die YAML-Datei nach `/config/blueprints/automation/HomeLabNext/` kopieren und Blueprints in Home Assistant neu laden.

## Hinweise

- Für Geräte wie Aqara E1 und Sonoff TRVZB wird im Regelbetrieb `heat` gesetzt, für Aus `off`. Die Auto-Logik läuft in Home Assistant.
- Frostschutz und Fensterabsenkung sind von 5 bis 12 °C einstellbar.
- Der Blueprint kann in Home Assistant nur mit den gewählten Entitäten abschließend getestet werden.
