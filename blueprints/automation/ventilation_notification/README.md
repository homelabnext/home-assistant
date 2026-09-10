# Lüftungsempfehlung zur Feuchteprävention

**Version: v0.1.0**

Pro Raum eine Automation: Sie empfiehlt Lüften bei erhöhtem Feuchtebedarf und ausreichend trockener Außenluft. Sie meldet bei Bedarf auch ungünstige Außenluft und erinnert an das Schließen. Versand über `script.home_notification` mit `title` und `message`.

[Blueprint importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fventilation_notification%2Fventilation_notification.yaml)

Direkte Datei für den Importdialog:

```text
https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/ventilation_notification/ventilation_notification.yaml
```

Die Datei mit `/blob/main/` importieren, nicht die Ordnerseite mit `/tree/main/`.

## Voraussetzungen

- Raumtemperatur und Raumluftfeuchtigkeit als Sensoren.
- Außentemperatur und Außenluftfeuchtigkeit als Sensoren. Diese können mehrere Räume gemeinsam verwenden.
- Alle Temperaturen in °C, alle Feuchtigkeiten in %. Andere Einheiten werden nicht automatisch umgerechnet.
- Mindestens ein Fensterkontakt des Raums: `on` = offen, `off` = geschlossen. Sobald einer offen ist, gilt der Raum als gelüftet.
- Ein eigenes `input_text` pro Automation, maximale Länge 255.
- Ein Benachrichtigungsskript, das `title` und `message` annimmt.

## Einrichtung

1. Unter **Einstellungen → Geräte & Dienste → Helfer → Helfer erstellen → Text** einen Helfer wie „Lüftungsstatus Schlafzimmer“ anlegen. **Maximale Länge auf 255 setzen.** Der Anfangsinhalt darf leer sein.
2. Blueprint importieren und daraus eine Automation erstellen.
3. Raumname, vier Sensoren, Fensterkontakte und den neuen Text-Helfer auswählen.
4. Notify-Skript auswählen; voreingestellt ist `script.home_notification`.
5. Schwellen und Zeiten einstellen und speichern. Das Feuchteziel muss kleiner als die Bedarfsschwelle sein.
6. Eine vorhandene einfache Fenster-offen-Erinnerung für diese Kontakte deaktivieren, wenn keine doppelten Schließhinweise gewünscht sind.

Den Helfer nicht zwischen Räumen teilen und seinen Inhalt nicht manuell bearbeiten. Ein YAML-Beispiel liegt in [helpers.example.yaml](helpers.example.yaml); bei Einrichtung per Oberfläche ist es nicht nötig.

## Einstellbare Vorgaben

| Einstellung | Standard | Wirkung |
| --- | --- | --- |
| Bedarfsschwelle | 60 % | Aktiviert den Feuchtebedarf |
| Feuchteziel | 55 % | Beendet den Bedarf bei geschlossenen Fenstern |
| Trocknungsvorteil | 1 g/m³ | Innen-/Außenvergleich bei gleicher Raumtemperatur |
| Bestätigung der Empfehlung | 10 Minuten | Zustand muss so lange bestehen |
| Bestätigung des Schließhinweises | 2 Minuten | Auch bei Zeit- und Temperaturgrenze |
| Maximale Lüftungszeit | 15 Minuten | Danach beginnt die Bestätigung für den Schließhinweis |
| Minimale Raumtemperatur | 17 °C | Darunter beginnt die Bestätigung für den Schließhinweis |
| Ungünstige Außenluft melden | Ein | Optionaler Hinweis, dass Lüften wenig bringt |
| Wiederholung | Aus | Einmal je Meldungsart im jeweiligen Vorgang |
| Wiederholungsabstand | 60 Minuten | Bei eingeschalteter Wiederholung |

Die Vorgaben müssen zum Raum passen. Sie sind keine bauphysikalischen Sicherheitsgrenzen.

## Ablauf und Schutz vor wechselnden Meldungen

Bei geschlossenen Fenstern wird Feuchtebedarf ab der oberen Schwelle gesetzt. Er bleibt aktiv, bis das untere Feuchteziel erreicht ist. Ein Rückgang von 61 auf 59 % beendet einen bei 60 % gesetzten Bedarf also nicht. Innerhalb dieses Bedarfs entscheidet der Außenvergleich zwischen „Bitte stoßlüften“ und „Lüften bietet aktuell zu wenig Trocknungsvorteil“.

Der Trocknungsvorteil hat ebenfalls zwei Schwellen: Einschalten ab dem eingestellten Wert, Ausschalten bei dessen Hälfte. Jede Änderung des Empfehlungszustands beginnt dessen Bestätigungszeit neu. Unterbrechungen durch ungültige Sensorwerte setzen die Beobachtung vollständig zurück.

Ohne Wiederholung kommt jede der beiden Bedarfsmeldungen höchstens einmal pro Feuchteepisode. Eine neue Episode beginnt nach Erreichen des Feuchteziels bei geschlossenen Fenstern. Ein Schließhinweis kommt höchstens einmal pro zusammenhängendem Zeitraum mit mindestens einem offenen Fenster. Ein anderer Schließgrund erzeugt keinen zusätzlichen Hinweis. Nach Neustart oder ungültigen Messwerten beginnt eine neue Beobachtung; nach voller Bestätigung ist eine erneute Meldung möglich.

Bei geöffnetem Fenster gibt es keine Aufforderung zum Öffnen. Ein Schließhinweis wird bestätigt, wenn mindestens einer dieser Gründe besteht:

- Feuchteziel nach Wiederaufwärmen erreicht.
- Außenluft führt keine Feuchtigkeit mehr ab.
- Raumtemperatur zu niedrig.
- Maximale Lüftungszeit erreicht.

Die Bestätigung bezieht sich auf „Schließen empfohlen“ insgesamt; der einzelne Grund kann währenddessen wechseln. Schließen aller Fenster beendet diesen Vorgang. Kurzes Schließen/Wiederöffnen beginnt einen neuen Lüftungszeitraum.

## Feuchtevergleich und Wiederaufwärmen

Aus Temperatur und relativer Feuchtigkeit wird der Wasserdampf-Partialdruck mit der Magnus-Näherung über Wasser berechnet:

```text
e(T, RH) = RH/100 × 6.112 × exp(17.62 × T / (243.12 + T))
Trocknungsvorteil = 216.7 × (e_innen − e_außen) / (273.15 + T_innen)
```

Der Unterschied ist auf dieselbe Raumtemperatur bezogen, damit reine Temperaturunterschiede keinen falschen Trocknungsvorteil vortäuschen. Prozentwerte innen und außen werden nicht direkt verglichen. Die Näherung dient einer Lüftungsempfehlung; insbesondere Frostbedingungen und Sensorungenauigkeit begrenzen die Genauigkeit.

Beim Öffnen wird die zuletzt beobachtete Temperatur bei geschlossenen Fenstern als Referenz genutzt. Während des Lüftens wird berechnet, welche relative Feuchtigkeit die aktuelle Luft bei dieser Temperatur hätte. Beispiel: Bei 15 °C und 70 % liegt sie nach Erwärmung auf 20 °C ungefähr bei 51 %. So verhindert der Blueprint unnötiges Weiterlüften nur wegen des kühlen Raumsensors. Zusätzliche Feuchteabgabe durch Wände, Möbel oder Personen kann diese Prognose verändern.

Die Raumsonde sollte repräsentativ und nicht direkt im kalten Luftstrom am Fenster liegen. Außenwerte sollten aus einer geschützten, repräsentativen Messung stammen.

## Neustart, Ausfälle und Versand

Auswertung bei Sensor-/Kontaktänderungen und mindestens einmal pro Minute. Bei unveränderten Werten kann ein Hinweis bis zu ungefähr einer Minute nach Ablauf seiner Bestätigungszeit eintreffen. Mit Standardwerten kommt die zeitbedingte Schließerinnerung nach etwa 17–18 Minuten, nicht schon nach 15 Minuten.

HA-Start, Neuladen der Automationen oder eine Beobachtungslücke von mehr als drei Minuten setzen die Beobachtung zurück. Bereits offene Fenster werden automatisch wieder erfasst, ihre Offenzeit wird ab der neuen Beobachtung gezählt. Offline-Zeit zählt nicht als bestätigtes Lüften. Auch nach Wiederverfügbarkeit der Sensoren läuft die vollständige Bestätigung neu an.

`unknown`, `unavailable`, fehlende Kontakte, nicht numerische Werte, falsche Einheiten und außerhalb der geprüften Bereiche liegende Messwerte erzeugen keine Empfehlung. Geprüfte Bereiche: innen −20 bis 60 °C, außen −50 bis 60 °C, Feuchte größer 0 bis 100 %. Ein eingefrorener, aber weiterhin numerischer Sensor wird nicht zuverlässig erkannt.

Der Text-Helfer speichert automatisch einen kurzen technischen Status. Ein fehlender Helfer, eine zu kurze maximale Länge oder ein Feuchteziel oberhalb der Bedarfsschwelle beendet den Lauf mit einem erklärenden Trace-Fehler.

Der Meldungszeitpunkt wird vor dem Skriptaufruf gespeichert. Ein fehlgeschlagener Versand erzeugt deshalb keine Meldungsschleife. Es gibt keine Zustellbestätigung; Wiederholung bedeutet erneuten Versandversuch im gewählten Abstand. `script.turn_on` übergibt die Variablen gemäß [HA-Skript-Dokumentation](https://www.home-assistant.io/integrations/script/).

## Grenzen

Dies ist Feuchteprävention und Lüftungsunterstützung, kein Schimmelsensor. Kalte Wandoberflächen, Wärmebrücken, eindringendes Wasser und vorhandener Schimmel werden nicht erkannt. Für eine zusätzliche Oberflächenabschätzung lässt sich später ein kalibrierter [Mold Indicator](https://www.home-assistant.io/integrations/mold_indicator/) ergänzen. Allgemeine Hinweise zur Vorbeugung: [Umweltbundesamt](https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/schimmel).

Keine Fenster-, Heizungs- oder Entfeuchtersteuerung und keine CO₂-Lüftungsempfehlung. Ein Hinweis auf geringen Trocknungsvorteil bedeutet nicht, dass Lüften aus anderen Gründen unnötig wäre.

## Prüfung

Offline-Tests verwenden das tatsächliche Entscheidungstemplate mit simulierten Sensorzuständen:

```bash
python3 -m pip install PyYAML Jinja2
python3 tests/test_ventilation_notification.py
```

Geprüft werden unter anderem Winter-/Sommerbedingungen, Bestätigungszeiten, Wiederholungen, Hysterese, ungültige Werte, Helferinhalt, Schließgründe, Wiederöffnen und Wiederaufnahme. Diese Tests ersetzen keinen Import- und Versandtest in Home Assistant.

Zum Test im Raum die Bestätigung auf eine Minute stellen. Über den echten Sensorzustand prüfen, ob die passende Meldung erscheint und ein geöffnetes Fenster die Öffnungsempfehlung beendet. „Aktionen ausführen“ sendet ohne echten Trigger absichtlich nichts. Anschließend die gewünschten Zeiten einstellen.
