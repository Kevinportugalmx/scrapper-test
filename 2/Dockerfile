FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y gnupg2 curl ca-certificates postgresql-client \
    build-essential libpq-dev wget firefox-esr

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O - | tar -xz -C /usr/local/bin

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt 


ENV PYTHONPATH=/app

EXPOSE 8000

RUN ls -la /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]