# taghub-api

Operativsystem: Windows.

## Kom i gang:
Database beskrivelsen finner du i database.sql.

I app.py må passord (eventuelt bruker) til databasen endres.

Installasjon og kjøring:
```
pip3 install -r requirements.txt
flask run
```

Jeg har testet API-en i Python kommandolinjen og ved hjelp av Postman.

### Eksempel på test i Python ved bruk av requests:
```
requests.get('http://localhost:5000/users').json()
requests.post('http://localhost:5000/users', json={"username": "xyz", "email": "xyz@mm.com", "password": "xxx"}).json()
requests.get('http://localhost:5000/users/2').json()
requests.delete('http://localhost:5000/users/2').json()
```
