
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ansible-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN ansible-galaxy collection install community.docker

COPY app.py .

CMD ["python", "app.py"]
