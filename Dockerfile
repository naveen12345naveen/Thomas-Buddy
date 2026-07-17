FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs

# Environment
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Run the agent
CMD ["python", "main.py"]
