#export SECRET_KEY='msi3%x8#^cv)3o212sgp^7(b0!0_ncc0lnntbvi(@m(0olxuws'
#export DEBUG=False
#python3 manage.py collectstatic
#gunicorn GacoWeb.wsgi --user javier --bind 0.0.0.0:8020 --workers 3
python3 manage.py runserver 0.0.0.0:8020
#python3 manage.py runserver 192.168.1.38:8020