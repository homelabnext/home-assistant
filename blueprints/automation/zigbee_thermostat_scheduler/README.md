# HomeLabNext – Zigbee Thermostat Scheduler

**Version: v0.10.0**

Steuert Sonoff TRVZB, Aqara E1, Aqara W600 und andere Thermostate über Home-Assistant-`climate`-Entitäten.

## Direkt in der Automation einstellen

Für Zeitprofile und Temperaturen sind keine Helfer nötig:

- **Betriebsart:** Auto, Manuell oder Aus. Das ist die feste Betriebsart der Automation.
- **Zeitplan:** Bis zu drei Profile. Für jedes Profil können beliebige Wochentage ausgewählt und bis zu zwei Zeitfenster eingestellt werden. Die Profile 1 und 2 starten mit den bisherigen Standardgruppen Mo–Fr und Sa–So; Profil 3 ist optional.
- **Temperaturen:** Komfort, Absenkung und Manuell direkt in den Blueprint-Einstellungen festlegen.
- **Modus zur Laufzeit:** optional einen `input_select`-Helfer aktivieren, wenn der Modus im Dashboard oder per Sprache umgeschaltet werden soll. Er muss genau die Optionen `Aus`, `Auto` und `Manuell` haben. Ist der Helfer nicht verfügbar, fällt die Automation auf die fest eingestellte Betriebsart zurück.

Jeder Wochentag sollte genau einem Profil zugewiesen werden. Bei versehentlicher Mehrfachzuweisung gewinnt Profil 1 vor Profil 2 und Profil 3. Nicht zugewiesene Tage verwenden die Absenktemperatur. Zeitfenster über Mitternacht bleiben dem Profil des Tages zugeordnet, an dem sie beginnen.

Änderungen an Zeitprofilen und Temperaturen erfolgen in der Konfiguration der Automation. Nur für den optionalen, zeitlich begrenzten manuellen Override wird ein Input-Datetime-Helper benötigt.

## Aqara-Preset und Heizmodus

Die Voreinstellung des Thermostats wird standardmäßig berücksichtigt:

- **Preset `auto`:** Der Zeitplan steuert die Temperatur.
- **Preset `manual` oder ein anderes Preset:** Das Thermostat bleibt unverändert. Der Zeitplan greift erst wieder, wenn du das Preset auf `auto` stellst.
- **Heizmodus `off`:** Bleibt aus. Sobald du den Heizmodus wieder einschaltest und `auto` aktiv ist, greift der Zeitplan beim nächsten Prüfintervall.

Der Wert für das Zeitplan-Preset ist konfigurierbar und bei Aqara üblicherweise `auto`. Thermostate ohne `preset_mode`-Attribut werden weiterhin wie bisher gesteuert.

## Manuelle Thermostatänderung

Erstelle unter **Einstellungen → Geräte & Dienste → Helfer** einen
`input_datetime`-Helper mit **Datum und Uhrzeit**. Wähle ihn in der Automation
aus und stelle die Override-Dauer in Stunden ein. Manuelle Änderungen des Temperatur-Sollwerts im `auto`-Preset, die Home
Assistant nicht als Aufruf dieser Automation erkennt, aktivieren den Override. Der Zeitplan
überschreibt diese Einstellung nach Ablauf beim nächsten Prüfintervall wieder.

Der Override gilt für alle Thermostate, die in derselben Automation ausgewählt
sind. Alarmo-Urlaub, Modus Aus, ein ausgeschalteter Heizmodus, ein Preset ungleich `auto` und die Fensterabsenkung behalten Vorrang.

Bei einem Home-Assistant- oder Zigbee-Dienst-Neustart bleibt die Ablaufzeit im
Helper erhalten. Wenn keine manuelle Erkennung gewünscht ist, den Helper leer
lassen.

## Diagnose-Helper

Lege unter **Einstellungen → Geräte & Dienste → Helfer** einen `input_text`-Helper mit maximal 255 Zeichen an und wähle ihn bei **Debug-Helper** aus. Der Blueprint überschreibt den Helper bei jeder Ausführung mit Trigger, erkannter Regel, Modus, Zeitplan-/Override-Status sowie HVAC-Modus und Preset. Es wird nur der letzte Lauf gespeichert; das Logbuch bleibt dadurch frei. Ohne ausgewählten Helper ist die Diagnose deaktiviert.

## Optionale Funktionen

- **Fensterkontakt:** Bei mindestens einem offenen ausgewählten Kontakt wird die Fenster-Temperatur verwendet. Im Modus Aus bleibt das Thermostat aus.
- **Alarmo-Urlaub:** Wenn aktiviert und Alarmo den Zustand `armed_vacation` meldet, gilt die Frostschutztemperatur. Urlaub hat Vorrang vor allen anderen Regeln.
- **Anwesenheit / Homeoffice:** Im Modus Auto gilt Komfort, wenn mindestens eine ausgewählte Person zuhause ist **und** der Leistungssensor den Watt-Schwellwert überschreitet. Sonst gilt Absenkung. Die Regel kann auf die Zeitfenster begrenzt oder jederzeit angewendet werden. Sensoren in kW müssen vorher in Watt umgerechnet werden.
- **Prüfintervall:** Standardmäßig jede Minute. Änderungen an Modus, Personen, Sensoren, Alarmo oder Fensterkontakt werden spätestens dann ausgewertet.

Priorität: **Alarmo-Urlaub → Aus → Fenster offen → manueller Override → Manuell → Auto**. Auto schaltet zu Komfort, wenn das Zeitfenster aktiv ist und die aktivierte Anwesenheitsregel erfüllt ist; andernfalls gilt Absenkung.

## Installation

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fzigbee_thermostat_scheduler%2Fzigbee_thermostat_scheduler.yaml)

Alternativ die YAML-Datei nach `/config/blueprints/automation/HomeLabNext/` kopieren und Blueprints in Home Assistant neu laden.

## Hinweise

- Für Geräte wie Aqara E1 und Sonoff TRVZB wird im Regelbetrieb `heat` gesetzt, für Aus `off`. Die Auto-Logik läuft in Home Assistant.
- Frostschutz und Fensterabsenkung sind von 5 bis 12 °C einstellbar.
- Der Blueprint kann in Home Assistant nur mit den gewählten Entitäten abschließend getestet werden.
