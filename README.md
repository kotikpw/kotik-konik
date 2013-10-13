kotik-konik
===========

Strona rejestracji kotik

Zależności
==========

* uwsgi (apt-get install uwsgi-core uwsgi-plugins-python)
* sqlalchemy (pip install sqlalchemy)
* sqlite3 (apt-get install sqlite3)
* webpy (pip install webpy)

Instalacja
==========

Stwórz bazę danych (kotik.db):

$ python models.py

Uruchom aplikację:

$ python app.py
