# HomeLabNext – Zigbee Thermostat Scheduler

Steuert Zigbee2MQTT-Thermostate über ihre Home-Assistant-`climate`-Entitäten. Der Blueprint ist nicht an ein bestimmtes Thermostatmodell gebunden.

## Modi

- **Aus:** setzt den HVAC-Modus der Thermostate auf `off`.
- **Auto:** setzt den HVAC-Modus auf `heat` und verwendet während aktiver Zeitfenster die Komforttemperatur. Außerhalb der Zeitfenster gilt die Absenktemperatur.
- **Manuell:** setzt den HVAC-Modus auf `heat` und verwendet die Temperatur aus dem manuellen Temperatur-Helfer.
- **Alarmo Urlaub:** Sobald die ausgewählte Alarmo-Entität den Zustand `armed_vacation` hat, wird die konfigurierbare Frostschutztemperatur verwendet. Sie hat Vorrang vor Aus, Manuell und Zeitplan.
- **Fenster offen:** Ist mindestens einer der ausgewählten Fensterkontakte offen, wird die einstellbare Fenster-Temperatur verwendet. Nach dem Schließen greift wieder der aktive Modus.
- **Anwesenheit / Homeoffice (optional):** In `Auto` gilt die Komforttemperatur, wenn mindestens eine ausgewählte Person zuhause ist und der Leistungs-Sensor über dem Schwellwert liegt. Sonst gilt die Absenktemperatur. In den Blueprint-Einstellungen ist auswählbar, ob diese Regel nur während aktiver Zeitfenster oder jederzeit gilt. Standardmäßig gilt sie nur im Zeitplan.

Der Betriebsmodus wird über einen `input_select` gewählt. Zeitfenster und Wochentage werden über einen Home-Assistant-Schedule-Helfer konfiguriert. Dort können pro Wochentag beliebig viele Zeitfenster hinterlegt werden.

## Benötigte Helfer

Lege unter **Einstellungen → Geräte & Dienste → Helfer** folgende Helfer an:

1. **Auswahl** mit den Optionen exakt `Aus`, `Auto` und `Manuell`.
2. **Zeitplan** für die gewünschten Wochentage und Zeitfenster.
3. Drei **Zahl**-Helfer für manuelle Temperatur, Komforttemperatur und Absenktemperatur. Stelle Einheit auf `°C` und wähle einen passenden Bereich, zum Beispiel 5 bis 30 °C mit Schrittweite 0,5 °C.
4. Einen oder mehrere Fensterkontakte als `binary_sensor` sowie die Alarmo-Entität (`alarm_control_panel`). Alarmo muss den Urlaubsmodus `armed_vacation` aktiviert haben.
5. Die Frostschutztemperatur bei Urlaub und die Fenster-Temperatur werden in den Blueprint-Einstellungen gesetzt (je 5 bis 12 °C, Standard 7 °C).
6. Optional die Anwesenheitsregel aktivieren, Personen und einen Leistungs-Sensor (Geräteklasse `power`, Einheit Watt) auswählen und den Schwellwert festlegen. Entscheide zusätzlich, ob die Regel nur im Zeitplan gelten soll. Die Komfort- und Absenktemperatur-Helfer liefern dabei die beiden Temperaturen, zum Beispiel 22 °C und 20 °C.

Pro Raum bzw. unabhängig gesteuerter Thermostatgruppe werden ein eigener Modus-Helfer und Zeitplan empfohlen. Temperatur-Helfer können ebenfalls pro Raum angelegt werden, wenn die Zielwerte verschieden sind. Wähle bei jeder Automation nur die Fensterkontakte aus demselben Raum, damit ein geöffnetes Fenster nicht alle Heizkörper im Haus absenkt.

## Installation

Blueprint importieren über:

`https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/zigbee_thermostat_scheduler/zigbee_thermostat_scheduler.yaml`

Oder die YAML-Datei nach `/config/blueprints/automation/HomeLabNext/` kopieren und in Home Assistant die Blueprints neu laden. Anschließend eine Automation aus dem Blueprint erstellen und die Climate-Entitäten sowie Helfer auswählen.

## Unterstützte Thermostate und Hinweise

- Der Blueprint arbeitet mit Home-Assistant-Climate-Entitäten. Sonoff TRVZB, Aqara E1 und Aqara W600 stellen über Zigbee2MQTT jeweils Solltemperatur und HVAC-Modi bereit. Der Blueprint setzt im Betrieb `heat`, in Aus `off`; die eigene Thermostat-Zeitautomatik wird dadurch nicht verwendet.
- Die Temperaturgrenze für Frostschutz/Fenster beginnt bei 5 °C, damit sie mit E1 und W600 kompatibel ist.
- Der Urlaubsmodus von Alarmo muss in den Alarmo-Einstellungen aktiviert sein. Alarmo meldet ihn als `armed_vacation`.
- Bei aktiver Anwesenheitsregel wird Personenstatus und Leistung spätestens nach dem eingestellten Prüfintervall neu ausgewertet. Für eine schnellere Reaktion das Intervall auf eine Minute stellen; Standard sind fünf Minuten.
- Die Anwesenheitsregel gilt standardmäßig nur während des Schedule-Zeitplans. Deaktiviere „Anwesenheitsregel nur im Zeitplan anwenden“, wenn sie auch außerhalb der eingestellten Zeitfenster Komforttemperatur bei Anwesenheit und aktiver Leistung setzen soll.
- Fensterkontakte werden als `binary_sensor` gewählt. Bei mehreren Kontakten reicht ein offener Sensor, damit abgesenkt wird.
- Eine manuelle Temperaturänderung am Thermostat selbst wird bei der nächsten Prüfung vom ausgewählten Helferwert überschrieben. Für manuelle Änderungen den Modus `Manuell` wählen und den manuellen Temperatur-Helfer anpassen.
- Der Blueprint aktualisiert nach einem Neustart und zusätzlich standardmäßig alle fünf Minuten. Die Prüfhäufigkeit ist in der Automation einstellbar.
- Ein nicht verfügbarer Zeitplan oder Temperatur-Helfer führt zu keiner passenden Aktion. Die letzte Thermostateinstellung bleibt dann bestehen.
