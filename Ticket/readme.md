TicketInformationssystem

Anleitung:
    - in terminal zu Projekt navigieren in Directory 'Ticket'
    - venv aktivieren
    - Befehl 'flask run' ausführen
    - http://localhost:5000/ in browser öffnen
    - falls anderer Port gewünscht ist um gleichzeitig beide Applikationen ausführen zu können:
        - flask run -h localhost -p 3000
        - http://localhost:3000/ in browser öffnen

Sollte venv nicht vorhanden sein:
    - in terminal zu Projekt navigieren in Directory 'Ticket'
    - venv im Ordner 'Ticket' erstellen: python3 -m venv venv
    - venv aktivieren (source venv/bin/activate) bzw auf windows: (venv\Scripts\activate)
    - in terminal pakete installieren:
        pip install flask
        pip install python-dotenv
        pip install flask-wtf
        pip install flask-sqlalchemy
        pip install flask-migrate
        pip install email-validator
        pip install flask-login
    - Befehl 'flask run' ausführen
    - http://localhost:5000/ in browser öffnen
    - falls anderer Port gewünscht ist um gleichzeitig beide Applikationen ausführen zu können:
        - flask run -h localhost -p 3000
        - http://localhost:3000/ in browser öffnen

Admin User:
    name: 123 pw: 123

Kunden User:
    name: 1234 pw: 1234