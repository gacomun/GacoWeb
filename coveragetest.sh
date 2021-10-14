# https://coverage.readthedocs.io/en/coverage-5.5/
# coverage erase
#export SECRET_KEY='msi3%x8#^cv)3o212sgp^7(b0!0_ncc0lnntbvi(@m(0olxuws'
#export DEBUG=True
coverage run --source='.' manage.py test juegos
coverage report
coverage html