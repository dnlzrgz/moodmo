.PHONY: clean lint start-local

# Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

# Lint using Ruff
lint:
	ruff . --fix

# Run tests
test:
	python manage.py test

# Run moods app tests
test-moods:
	python manage.py test moods

# Run pages app tests
test-pages:
	python manage.py test pages

# Start local Docker compose
local-start:
	docker-compose -f local.yaml up -d --build

# Stop local Docker compose
local-stop:
	docker-compose -f local.yaml down