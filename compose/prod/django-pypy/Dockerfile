# Alias for the specific PyPy version
FROM pypy:3.10-7.3.15-slim-bookworm as pypy

# Build stage
FROM pypy as build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  wget

# Copy templates and static directories
COPY ./templates/ /templates
COPY ./static/ /static
COPY ./tailwind.config.js .

# Copy requirements
COPY ./requirements.txt .

# Create Python dependency wheels.
RUN pip wheel --wheel-dir /wheels \
  -r requirements.txt
RUN pip wheel --wheel-dir /wheels psycopg

# Download TailwindCSS cli
RUN wget -qO tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-linux-x64
RUN chmod +x tailwindcss

# Create and minify styles
RUN ./tailwindcss -i /static/css/input.css -o /static/css/output.min.css --minify

# Run stage
FROM pypy as run-stage

# Set env variables
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8000

EXPOSE ${PORT}

# Set working directory
WORKDIR $APP_HOME

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq5 \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy dependency wheels from the build stage
COPY --from=build-stage /wheels /wheels/

# Install Python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy application code
COPY . ${APP_HOME}

# Copy final styles
COPY --from=build-stage /static/css ${APP_HOME}/static/css

# Entrypoint
CMD ["pypy3", "manage.py", "runserver", "0.0.0.0:8000"]

