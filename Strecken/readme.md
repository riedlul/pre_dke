StreckenInformationssystem

Ergänzt seit Abschlussgespräch:
- Bahnhöfe können im Abschnitt geändert werden, wie Warnungen
- Spurweite wird bei Anlegen einer Strecke mittels if-Abfrage überprüft

Anleitung:
LINUX wenn Flask bereits downgeloaded ist:
    - Download Zip- File from Git
    - Extract Projekt
    - in shell zu Projekt navigieren 
    - im Projekt zu Directory 'Strecken' navigieren
    - Befehl 'flask run' ausführen

WINDOWS ohne Download der nötigen Programme:
    - Download Zip- File from Git
    - Extract Projekt
    - in shell zu Projekt navigieren 
    - im Projekt zu Ordner 'Strecken/Strecken' navigieren
    - Befehl: python3 -m venv venv
    - Befehl: venv\Scripts\activate 
(venv)
    - Befehl: pip install "flask<2"
    - Befehl: pip install python-dotenv
    - Befehl: pip install flask-sqlalchemy
    - Befehl: pip install flask-migrate
    - Befehl: pip install flask_marshmallow
    - Befehl: pip install flask_login
    - Befehl: pip install marshmallow_sqlalchemy
    - Befehl: pip install flask_wtf
    - Befehl: pip install email_validator

    - Befehl eingeben: flask run ODER python3 main.py
 

Admin User:
    admin@admin.at - pw: 123

Employee User:
    hammer@gmx.at - pw: 123