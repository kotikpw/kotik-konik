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

*UWAGA* w ten sposób możemy obsłużyć tylko jeden Request na raz. Strona rejestracji wykorzystuje '/avatar/<e-mail>' aby wyświetlić
awatar, więc najlepiej uruchamiać aplikację przez NGINX z kilkoma procesami.

W tym celu:

$ vim uwsgi.ini # zmodyfikuj chdir
$ uwsgi -C uwsgi.ini
