# Alias for the specific Python version
FROM python:3.12.1-slim-bookworm as python

# Build stage
FROM python as build-stage

# Install packages
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

# Download TailwindCSS cli
RUN wget -qO tailwindcss https://github.com/tailwindlabs/tailwindcss/download/v3.4.1/tailwindcss-linux-x64
RUN chmod +x tailwindcss

# Create and minify styles
RUN ./tailwindcss -i /static/css/input.css -o /static/css/output.min.css --minify

# Run stage
FROM python as run-stage

# Set env variables
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8000

# Expose default port
EXPOSE ${PORT}

# Set working directory
WORKDIR $APP_HOME

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy dependency wheels from the build stage
COPY --from=build-stage /wheels /wheels/

# Install Python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x ${APP_HOME}/entrypoint.sh

# Copy application code
COPY . ${APP_HOME}

# Copy final styles
COPY --from=build-stage /static/css ${APP_HOME}/static/css

# Entrypoint
ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]
