FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y \
    nginx \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app

# Copy frontend
COPY frontend /var/www/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Create static directory for QR codes
RUN mkdir -p /app/static/qr_codes

# Expose ports
EXPOSE 80 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Start both nginx and uvicorn
CMD ["sh", "-c", "nginx & uvicorn app.main:app --host 0.0.0.0 --port 8000"]
