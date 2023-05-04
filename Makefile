generate:
	alembic revision --m="${NAME}" --autogenerate

migrate:
	alembic upgrade head

lint:
	flake8 . --ignore=E402,F841,E302,E305,W503 --max-line-length=120 --statistics --show-source --extend-exclude=venv
