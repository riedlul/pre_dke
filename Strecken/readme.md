StreckenInformationssystem

Ergänzt seit Abschlussgespräch:
- Bahnhöfe können im Abschnitt geändert werden, wie Warnungen
- Spurweite wird bei Anlegen einer Strecke mittels if-Abfrage überprüft

Anleitung:
LINUX wenn Flask bereits installiert ist lt Mega-tutorial:
- Download ZIP-File von Git
- in shell zu Projekt navigieren und in Directory 'Strecken'
- Befehl 'flask run' ausführen

WINDOWS ohne Download der nötigen Programme:
- Download ZIP-File von Git
- Extract Projekt
- in command prompt zu Projekt in Ordner 'Strecken' navigieren
- Befehl: python3 -m venv venv
- Befehl: venv\Scripts\activate (venv)
- Befehl: pip install "flask<2"
- Befehl: pip install python-dotenv
- Befehl: pip install flask-sqlalchemy
- Befehl: pip install flask-migrate
- Befehl: pip install flask_marshmallow
- Befehl: pip install flask_login
- Befehl: pip install marshmallow_sqlalchemy
- Befehl: pip install flask_wtf
- Befehl: pip install email_validator

- zum Ausführen Befehl eingeben: flask run ODER python3 main.py

Achtung bei Ausführen auf Windows maschine erzeugt sich im Strecken unterodner instance eine neues db file dataabse.db.
Dieses ist leer und hindert an der Ausführung. im Ordner 'Strecken2' wurde daher das db file database.db in instance kopiert und
sollte 'Strecken2' problemlos auf Windows laufen (bei mir tut es das jedenfalls).


Admin User:
    admin@admin.at - pw: 123

Employee User:
    hammer@gmx.at - pw: 123