# Alias for the specific Python version
FROM python:3.12.2-slim-bookworm as python

# Build stage
FROM python as build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential

# Copy requirements
COPY ./requirements.dev.txt .

# Create Python dependency wheels.
RUN pip wheel --wheel-dir /wheels \
  -r requirements.dev.txt

# Run stage
FROM python as run-stage

# Set env variables
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Expose default port
EXPOSE 8000

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

# Copy application code
COPY . ${APP_HOME}

# Entrypoint
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
