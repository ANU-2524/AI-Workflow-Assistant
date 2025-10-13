FROM python:3.11

WORKDIR /app

# Install OS dependencies (build tools, Postgres driver)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your code (Django project)
COPY . .

# Collect static files (ignore errors on first build)
RUN python manage.py collectstatic --noinput || true

# Expose correct port
EXPOSE 8000

# Start with Gunicorn (production recommended)
CMD ["gunicorn", "workflow_ui.wsgi:application", "--bind", "0.0.0.0:8000"]

# For development/testing only (remove/comment in production):
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
