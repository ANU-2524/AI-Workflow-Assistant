FROM python:3.11

WORKDIR /app

# Install OS dependencies for Python, Postgres driver, etc.
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy only now to use Docker cache efficiently
COPY . .

# Collect static files (optional, will ignore errors if STATIC_ROOT is unset)
RUN python manage.py collectstatic --noinput || true

# Expose the correct port to the cloud
EXPOSE 8000

# Run Django with gunicorn (production)
CMD ["gunicorn", "workflow_ui.wsgi:application", "--bind", "0.0.0.0:8000"]

# (For dev only—commented out)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
