FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install requests beautifulsoup4

# Copy all code
COPY . .

# Run bot
CMD ["python", "cr.py"]
