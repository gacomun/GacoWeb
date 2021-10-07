#!/usr/bin/env bash
# start-server.sh
sh makemigrate.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
python manage.py collectstatic
(gunicorn GacoWeb.wsgi --user root --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"