# Paperless Notifications

Der Blueprint sendet eine tägliche Erinnerung für den Paperless-Posteingang und kann optional neue Paperless-Updates melden. Er verwendet den zentralen Benachrichtigungsweg des Repositories.

## Benachrichtigungs-Script

Standardmäßig wird `script.home_notification` aufgerufen. Das Beispielscript unter [`examples/scripts/home_notification.yaml`](https://github.com/homelabnext/home-assistant/blob/main/examples/scripts/home_notification.yaml) verteilt an die dort konfigurierten Notify-Ziele und erwartet die Variablen `title` und `message`. In der Automation kann ein anderes Script mit derselben Schnittstelle ausgewählt werden.

## Tägliche Erinnerung

Wähle den numerischen Paperless-Sensor **Dokumente im Posteingang** aus, gib die URL deiner Paperless-Instanz an und stelle die gewünschte Erinnerungszeit ein. Standard ist **19:00 Uhr**. Eine Nachricht wird nur gesendet, wenn der Sensor verfügbar ist, einen numerischen Wert größer null liefert und eine URL eingetragen ist. Der Nachrichtentext enthält die aktuelle Anzahl und den Paperless-Link.

Zustände wie `unknown`, `unavailable`, leere oder nicht numerische Werte werden still ignoriert.

## Optionale Update-Meldungen

Aktiviere **Über Paperless-Updates benachrichtigen**, wähle die Paperless-Update-Entität und einen `input_text`-Helfer für den zuletzt gemeldeten Versionsstand aus. Der Helfer muss mindestens 100 Zeichen erlauben. Lege ihn über **Einstellungen → Geräte & Dienste → Helfer → Text** an und lasse den Anfangswert leer, damit Home Assistant den zuletzt gespeicherten Wert nach einem Neustart wiederherstellt.

Die Automation benachrichtigt, wenn die Update-Entität den Zustand `on` hat und ihre verfügbare Version noch nicht im Helfer gespeichert ist. Danach speichert sie die Version dort. Dadurch wird dieselbe Version nach einem Home-Assistant-Neustart nicht erneut gemeldet. Sind Versionsattribute vorhanden, enthält die Meldung installierte und verfügbare Version; sonst wird nur gemeldet, dass ein Update verfügbar ist. Eine `unknown`- oder `unavailable`-Update-Entität oder ein nicht verfügbarer Versions-Helfer löst keine Update-Meldung aus.

Die Versionsnummer wird im Helper gespeichert. Wird der Helper gelöscht oder zurückgesetzt, kann die gleiche Version erneut gemeldet werden.

## Import

[In Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fhomelabnext%2Fhome-assistant%2Fmain%2Fblueprints%2Fautomation%2Fpaperless_notifications%2Fpaperless_notifications.yaml)

## Hinweise

- Die tägliche Erinnerung wird nur zum eingestellten Zeitpunkt geprüft; sie wird beim Neustart nicht nachträglich gesendet.
- Update-Meldungen werden bei verfügbarer neuer Version ausgelöst und beim Home-Assistant-Start erneut geprüft.
- Der Blueprint benötigt keine Paperless-API-Zugangsdaten; er liest ausschließlich die ausgewählten Home-Assistant-Entitäten.
