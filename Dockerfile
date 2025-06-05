# Use slim image for smaller footprint
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install build tools required for Rust-based or compiled Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    libffi-dev \
    libssl-dev \
    pkg-config \
    cargo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optional: avoid installing Windows-only packages like pywinpty
# Remove this line if pywinpty is required for a Windows target
# RUN sed -i '/pywinpty/d' requirements.txt

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . /code/

RUN python manage.py collectstatic --noinput
# Run the app with Gunicorn
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ecommerce_project.wsgi --bind 0.0.0.0:8000
