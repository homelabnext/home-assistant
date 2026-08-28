# Zentrale Home-Assistant-Benachrichtigungen

Die Blueprints in diesem Paket enthalten bewusst keine fest verdrahteten iPhone- oder Telegram-Ziele. Stattdessen rufen sie ein zentrales Script auf.

```text
Sensor / Gerät
    ↓
Blueprint
    ↓
script.home_notification
    ├─ iPhone 1
    ├─ iPhone 2
    └─ Telegram-Gruppe
```

## Warum zentral?

Notify-Ziele ändern sich häufiger als die eigentliche Überwachungslogik. Mit einem zentralen Script muss eine Änderung nur einmal vorgenommen werden.

## Beispielscript

Siehe [`examples/scripts/home_notification.yaml`](../examples/scripts/home_notification.yaml).

Das Script erwartet zwei Variablen:

- `title`
- `message`

Die Blueprints rufen das Script über `script.turn_on` und `variables` auf.

## Telegram

Für aktuelle Home-Assistant-Versionen sollte die von der Telegram-Bot-Integration bereitgestellte `notify.`-Entity über `notify.send_message` verwendet werden. Für eine gemeinsame Gruppe wird die Gruppen-Chat-ID als erlaubte Chat-ID in der Integration hinterlegt; danach steht eine eigene Notify-Entity für diesen Chat zur Verfügung.
