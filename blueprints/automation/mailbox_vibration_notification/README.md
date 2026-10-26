# Briefkasten-Benachrichtigung

Sendet bei einer erkannten Vibration eine Benachrichtigung über das zentrale Skript
`script.home_notification` und merkt den Posteingang in einem `input_boolean`.

## Einrichtung

1. Erstelle unter **Einstellungen → Geräte & Dienste → Helfer** einen Input-Boolean,
   zum Beispiel **Post im Briefkasten**.
2. Importiere den Blueprint und wähle den Vibrations-Binärsensor, den neuen Helper
   und dein zentrales Benachrichtigungsskript aus.
3. Öffne die Automation **Home Status Light**. Wähle den Helper **Post im Briefkasten**
   unter **Aufmerksamkeit** aus und stelle **Farbe – Aufmerksamkeit** auf Gelb.
   Die Statuslampe zeigt den Zustand bis zum Abholen der Post an.
4. Schalte den Helper am Dashboard wieder aus, wenn du den Briefkasten geleert hast.

Der Vibrationssensor darf nach dem Ereignis wieder auf `off` zurückgehen. Der Helper
bleibt eingeschaltet und hält damit die Anzeige aktiv. Der Statuslicht-Blueprint
akzeptiert dafür ab v0.1.2 auch Input-Boolean-Helper als Statusquellen.

## Benachrichtigung

Standardtitel: **📬 Post war da**

Standardnachricht: **Im Briefkasten wurde eine Vibration erkannt. Es könnte Post angekommen sein.**

Titel und Nachricht können in der Automation angepasst werden. Das Notify-Skript muss
die Variablen `title` und `message` annehmen.

## Import

[Blueprint in Home Assistant importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fhomelabnext%2Fhome-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmailbox_vibration_notification%2Fmailbox_vibration_notification.yaml)

Raw-URL:

`https://raw.githubusercontent.com/homelabnext/home-assistant/main/blueprints/automation/mailbox_vibration_notification/mailbox_vibration_notification.yaml`

## Verhalten

Bei jedem Zustandswechsel des ausgewählten Vibrationssensors zu `on` wird der Helper
eingeschaltet und eine Benachrichtigung gesendet. Der Helper wird nicht automatisch
zurückgesetzt, da der Sensor nur die Erschütterung und nicht das Abholen der Post
erkennt.
