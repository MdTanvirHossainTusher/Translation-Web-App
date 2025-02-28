FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

    
# Run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
CMD gunicorn --bind 0.0.0.0:$PORT run:app