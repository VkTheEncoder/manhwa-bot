# Use an official lightweight Python image.
FROM python:3.10-slim

# Install system dependencies for OCR.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port your Flask app listens on
EXPOSE 10000

# Default command: run Gunicorn serving the Flask app
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:10000"]
