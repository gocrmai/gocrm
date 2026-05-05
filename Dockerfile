FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media directory and database
RUN mkdir -p /app/media/uploads && \
    touch /app/db.sqlite3 && \
    chmod 666 /app/db.sqlite3

# Run migrations
RUN python manage.py migrate --noinput

# Create superuser (will be created if not exists)
RUN python manage.py shell -c "from apps.users.models import User; \
if not User.objects.filter(username='gopos').exists(): \
    User.objects.create_superuser('gopos', 'info@gopos.hk', 'goposadmin123')"

# Expose port 8000
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "120", "gopos_crm.wsgi:application"]