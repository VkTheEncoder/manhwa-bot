FROM python:3.10-slim

# Install Tesseract for OCR
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy your bot code
COPY . .

# Expose the port (Render will map PORT env to this)
EXPOSE 10000

# Run the bot directly
CMD ["python", "bot.py"]
