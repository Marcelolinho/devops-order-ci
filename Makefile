.PHONY: install test cov lint quality run clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

test:
	pytest -q

cov:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check .

quality: lint cov

run:
	python -m app.cli --preco 100 --quantidade 2 --desconto 10 --cupom DEVOPS10

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov __pycache__ app/__pycache__ tests/__pycache__
