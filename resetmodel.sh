# en BBDD DROP TABLE juegos_juego; DELETE FROM django_migrations WHERE app="juegos";
chmod 664 db.sqlite3 
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python3 manage.py makemigrations