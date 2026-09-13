# Alexa Musik bei Bewegung

**Version: v0.1.0**

Startet bzw. setzt Musik auf einem Echo im Gäste-WC fort und pausiert nach einer einstellbaren Zeit ohne Bewegung. Voraussetzung ist die Integration [Alexa Media Player](https://github.com/alandtse/alexa_media_player).

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Falexa_motion_music%2Falexa_motion_music.yaml)

Alternativ diese **Dateiadresse** in den Importdialog kopieren:

```text
https://github.com/homelabnext/home-assistant/blob/main/blueprints/automation/alexa_motion_music/alexa_motion_music.yaml
```

## Einrichtung

1. In der Alexa-App eine Routine namens **Radio Chillout** anlegen bzw. die bereits vorhandene verwenden. Sie soll die gewünschte Musik auf dem Echo im Gäste-WC starten. Ein in der Routine fest hinterlegtes anderes Ausgabegerät wird durch das HA-Ziel nicht zwingend überschrieben.
2. Blueprint importieren, eine Automation erstellen und den Bewegungs-/Präsenzsensor des Raums auswählen.
3. Die **Media-Player-Entität** des Gäste-WC-Echos aus Alexa Media Player auswählen. Eine Geräte-ID ist dafür nicht nötig.
4. Pause nach Abwesenheit einstellen, Standard **5 Minuten**. Bei einem reinen Bewegungsmelder ausreichend Zeit für stilles Sitzen lassen.
5. Routinenname und optional Lautstärke anpassen. Speichern und anhand echter Bewegung testen.

Keine zusätzlichen Helper, keine Änderungen am zentralen Benachrichtigungsskript. Die Routine wird nicht automatisch in Alexa angelegt.

## Verhalten

| Zustand beim Erkennen von Bewegung | Aktion |
| --- | --- |
| `playing` oder `buffering` | Keine Änderung, auch keine Lautstärkeänderung |
| `paused` | Nur `media_player.media_play`; keine Routine und kein Neustart der Playlist |
| `idle`, `off`, `standby` | Zuerst Play; nach standardmäßig 15 Sekunden ohne Start optional Routine aufrufen |
| `unknown`, `unavailable` oder anderer Zustand | Kein Wiedergabebefehl |
| Durchgehend keine Bewegung für X Minuten, Echo spielt | `media_player.media_pause` |

Erneute Bewegung setzt die Abwesenheitsfrist zurück. Es werden weder Stop noch Play/Pause-Toggle verwendet. Bei gestopptem Echo bleibt die Routine aus, sobald die Integration während der Wartezeit `playing` oder `buffering` meldet. Bei `unknown`/`unavailable` wird ebenfalls nicht auf die Routine zurückgefallen.

Ein kurzer Bewegungspuls genügt zum Start. Ein anschließend wieder auf `off` fallender Sensor unterbricht den Startversuch nicht sofort; die eingestellte Abwesenheitsfrist gilt weiterhin.

Ein Zustand `paused` führt bewusst zu keinem automatischen Routinen-Neustart, auch wenn Alexa den Play-Befehl nicht umsetzt. Damit wird eine vorhandene Playlist nicht aufgrund einer bloß langsamen oder fehlgeschlagenen Statusmeldung neu gestartet. In diesem Fall die Wiedergabe zunächst manuell prüfen.

## Einstellungen

| Feld | Vorgabe |
| --- | --- |
| Bewegungs-/Präsenzsensor | Auswählen |
| Echo | Auswählen |
| Pause nach Abwesenheit | 5 Minuten |
| Routine als Rückfall | Ein |
| Routinenname | Radio Chillout |
| Wartezeit nach Play | 15 Sekunden, einstellbar 5–45 |
| Lautstärke einstellen | Aus |
| Lautstärke bei Aktivierung | 20 % |

Lautstärke wird nur beim Start-/Fortsetzungsversuch gesetzt. Eine Alexa-Routine kann ihrerseits eine andere Lautstärke setzen. Bleibt die Rückfalloption aus, verwendet der Blueprint ausschließlich Play und Pause. Der eingestellte Routinenname ist ein vorhandener Alexa-Routinenname, kein frei formulierter Musikbefehl und keine automatische Playlist-Suche.

## Neustart, manuelle Wiedergabe und Sensorfehler

Zusätzlich zum Abwesenheits-Trigger prüft der Blueprint einmal pro Minute, ob der Sensor bereits lange genug `off` ist und der Echo noch spielt. Damit wird die Pausenprüfung nach HA-Neustart oder Neuladen wieder aufgenommen. Grundlage ist die von HA gemeldete letzte Zustandsänderung des Sensors; eine während des Ausfalls tatsächlich bestehende Abwesenheit kann nicht nachgewiesen werden.

Beim Neustart wird keine Musik automatisch gestartet. Dafür braucht es einen neuen Wechsel des Sensors nach `on`. Die zusätzliche Prüfung kann auch nachträglich gestartete oder nach einem Fehler wieder erkannte Wiedergabe pausieren. Den Blueprint deshalb für einen dedizierten Raum-Echo verwenden: **Auch manuell gestartete Musik wird bei ausreichend langer Abwesenheit pausiert.**

Ein unbekannter oder nicht verfügbarer Bewegungssensor bricht einen laufenden Startversuch ab; weitere Play-/Routine-/Pause-Befehle unterbleiben bis zu einem gültigen Zustand. Bereits spielende Musik wird bei Sensorfehler nicht automatisch gestoppt. Ein Ausfall von Alexa Media Player verhindert Befehle, eine Zustellgarantie gibt es nicht.

## Routine und Wiedergabeposition

Der Aufruf entspricht der bereitgestellten Routine, mit ausgewählter Entität statt einer fest eingebauten Geräte-ID:

```yaml
action: media_player.play_media
target:
  entity_id: media_player.DEIN_ECHO
data:
  media_content_id: Radio Chillout
  media_content_type: routine
```

Der Blueprint vermeidet erneute Routinenaufrufe bei normalem Pausieren/Fortsetzen. Bei einem echten Stopp ohne fortsetzbare Sitzung kann der Rückfall die Routine neu starten. Die Alexa-Cloud meldet Zustände teilweise verzögert; wenn eine Routine trotz laufender Musik erneut startet, die Wartezeit erhöhen oder den Rückfall ausschalten.

Bei Live-Radio bedeutet Play häufig Rückkehr zum aktuellen Live-Stream. Eine Fortsetzung an der alten Position kann der Blueprint nicht garantieren. Bei Playlists hängt die Fortsetzung von Alexa und dem Musikdienst ab.

Referenzen: [HA Media Player](https://www.home-assistant.io/integrations/media_player/), [Alexa Media Player Implementierung](https://github.com/alandtse/alexa_media_player/blob/dev/custom_components/alexa_media/media_player.py).

## Test

Zuerst die Routine einmal manuell auf dem Echo prüfen. Dann:

1. Echo pausieren und Bewegung auslösen: Wiedergabe wird fortgesetzt.
2. Während laufender Musik erneut Bewegung auslösen: keine neue Routine.
3. Pause auf eine Minute stellen und Raum verlassen: Musik pausiert.
4. Vor Ablauf der Minute erneut Bewegung auslösen: Pause wird verschoben.
5. Bei gestopptem Echo testen, ob Play genügt oder nach der Wartezeit Radio Chillout startet.

„Aktionen ausführen“ ohne Trigger führt absichtlich keine Wiedergabe aus. Nach dem Test die gewünschte Pausenzeit wieder einstellen. YAML und Entscheidungs-Templates wurden lokal getestet; Alexa-Cloud-Verhalten, Import und Wiedergabe müssen auf der Zielinstallation geprüft werden.
