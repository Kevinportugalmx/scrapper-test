FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    curl \
    unzip \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

WORKDIR /app
COPY . /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

RUN playwright install --with-deps firefox

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]