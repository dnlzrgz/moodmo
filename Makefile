# Delete all compiled Python files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✨ Clean up complete!"

# Lint using Ruff
lint:
	@echo "🔍 Linting with Ruff..."
	ruff . --fix
	@echo "✨ Linting complete!"

# Update dependencies and pre-commit
update:
	@echo "🔄 Updating dependencies and pre-commit..."
	poetry update
	pre-commit autoupdate
	@echo "✨ Update complete!"

# Run tests
test:
	@echo "🧪 Running all tests..."
	python manage.py test
	@echo "✨ All tests complete!"

# Collect static files
collect:
	@echo "📦 Collecting static files..."
	python manage.py collectstatic
	@echo "✨ Static files collected!"

# Run moods app tests
test-moods:
	@echo "🧪 Running moods app tests..."
	python manage.py test moods
	@echo "✨ Moods app tests complete!"

# Run pages app tests
test-pages:
	@echo "🧪 Running pages app tests..."
	python manage.py test pages
	@echo "✨ Pages app tests complete!"

# Start local Docker compose
local-start:
	@echo "🚀 Starting local Docker compose..."
	docker-compose -f local.yaml up -d --build
	@echo "✨ Local Docker compose started!"

# Stop local Docker compose
local-stop:
	@echo "🛑 Stopping local Docker compose..."
	docker-compose -f local.yaml down
	@echo "✨ Local Docker compose stopped!"