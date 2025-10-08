FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
