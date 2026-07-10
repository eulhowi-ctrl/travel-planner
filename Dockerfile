# Multi-stage build
FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app

# Final stage - with nginx
FROM nginx:alpine

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend to nginx
COPY frontend /usr/share/nginx/html

# Copy Python app from builder
COPY --from=backend-builder /app /app

# Install Python and dependencies
RUN apk add --no-cache python3 py3-pip curl && \
    pip install --no-cache-dir uvicorn fastapi python-multipart pydantic sqlalchemy psycopg2-binary python-jose passlib python-dotenv qrcode pillow aiofiles httpx requests alembic pytz pydantic-settings email-validator

# Create static directory for QR codes
RUN mkdir -p /app/static/qr_codes

# Expose ports
EXPOSE 80 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Start both nginx and uvicorn
CMD ["sh", "-c", "nginx & uvicorn app.main:app --host 0.0.0.0 --port 8000"]