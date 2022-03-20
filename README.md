# Ebay-Kleinanzeigen Scraper mit E-Mail Funktion

Die Grundidee hatte ich von https://github.com/tax0r/Ebay-Kleinanzeigen-Scraper

Das Phyton Script sucht automatisch nach ebay-Kleinanzeigen Anzeigen die interresant aussehen.

Dabei filtert das Script Anzeigen raus, die Woerter enthalten die nicht im Titel stehen sollen, wie z.B. defekt oder kaputt wenn man nach intakten Dingen sucht. Desweitern sortiert das Script auch Anzeigen aus, die unerwuenschte Woerter in der Beschreibung stehen haben.

Auch kann es nach Wortern filtern die umbedingt im Anzeigentitel stehen muessen.

Das Script sucht ist darauf ausgelegt 24/7 zu laufen und jede neu erstellte Anzeige zu ueberpruefen.

Wenn es eine passende Anzeige gefunden hat schickt es Ihnen eine e-Mail mit dem Link der Anzeige zu.

greenlist.txt = Woerter die im Titel stehen muessen
blacklist.txt = Woerter die nicht Titel stehen sollen
blacklistbsp.txt = Woerter die nicht in der Beschreibung stehen sollen
url.txt = ebay Kleinanzeigen URL der Suche
gmailUser = EmailAdresse ihres gmail Konots
gmailPasswort = passwort ihres gmail Konots

Das mainraspi.py Script ist fuer den Dauerbetrieb auf einem Raspberry pi ausgelegt.
