FROM python:3.11-slim

WORKDIR /app

# 1. First install pip system packages (essential for SSL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements FIRST for caching
COPY requirements.txt .

# 3. Install with trusted PyPI mirror
RUN pip install --no-cache-dir \
    --index-url https://pypi.org/simple/ \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# 4. Copy application code
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]