FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
EXPOSE 9000
