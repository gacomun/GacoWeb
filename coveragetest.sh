# https://coverage.readthedocs.io/en/coverage-5.5/
# coverage erase
coverage run --source='.' manage.py test juegos
coverage report
coverage html