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

# Check using Django's system-check
check:
	@echo "🔍 Running system checks..."
	python manage.py check
	python manage.py check --deploy
	python manage.py check --tag security
	@echo "✨ All checks done!"

# Update dependencies and pre-commit
update:
	@echo "🔄 Updating dependencies and pre-commit..."
	poetry update
	pre-commit autoupdate
	@echo "✨ Update complete!"

# Download Tailwind CSS cli
download-tailwind:
	@echo "🛠️ Installing Tailwind CSS..."
	curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.0/tailwindcss-linux-x64
	chmod +x tailwindcss-linux-x64
	mv tailwindcss-linux-x64 tailwindcss
	@echo "✨ Tailwind CSS installed!"

# Download v1.9.9 htmx script
download-htmx:
	@echo "📥 Downloading htmx script..."
	curl -sL https://unpkg.com/htmx.org@1.9.9/dist/htmx.min.js -o static/js/htmx.js
	curl -sL https://unpkg.com/htmx.org/dist/ext/debug.js -o static/js/debug.js
	@echo "✨ htmx script downloaded and saved!"

# Download v3.x.x Alpine.js script
download-alpine:
	@echo "📥 Downloading Alpine.js script..."
	curl -sL https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js -o static/js/alpine.js
	curl -sL https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js -o static/js/focus.js
	@echo "✨ Alpine.js script downloaded and saved!"

# Run Tailwind CSS minification
tailwind-min:
	@echo "🚀 Running Tailwind CSS minification..."
	./tailwindcss -i ./static/css/input.css -o ./static/css/output.min.css --minify
	@echo "✨ Tailwind CSS minification complete!"

# Run Tailwind CSS in watch mode
tailwind-watch:
	@echo "🚀 Running Tailwind CSS in watch mode..."
	./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
	@echo "✨ Tailwind CSS watch mode started!"

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

docker-logs:
	@echo "👀 Watching container logs..."
	docker-compose -f local.yaml logs -f
	@echo "✨ Watching container logs finished!"

# Start prod Docker compose
prod-start:
	@echo "🚀 Starting prod Docker compose..."
	docker-compose -f prod.yaml up -d --build
	@echo "✨ Prod Docker compose started!"

# Stop prod Docker compose
prod-stop:
	@echo "🛑 Stopping prod Docker compose..."
	docker-compose -f prod.yaml down
	@echo "✨ Prod Docker compose stopped!"

# Setup project with dependencies, Tailwind CSS, and htmx for local development
setup:
	@make download-tailwind
	@make download-alpine
	@make download-htmx
	poetry install
	pre-commit install
	pre-commit run --all-files
	@echo "✨ Project setup complete!"
