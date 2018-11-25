init:
	pipenv install --dev --skip-lock

lock:
	pipenv lock

flake8:
	pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 grst

test:
	pipenv run pytest -s --tb=short
