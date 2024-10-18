# Use Python 3.10 slim base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Copy and install dependencies first (leveraging Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the Gunicorn WSGI server for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "financial_app.wsgi:application"]
