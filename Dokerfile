FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    python3-dev

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
