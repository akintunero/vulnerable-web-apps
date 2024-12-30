# Dockerfile for Vulnerable Airline Application
# FOR EDUCATIONAL PURPOSES ONLY

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p database uploads logs

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"] 