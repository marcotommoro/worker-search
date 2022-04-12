FROM python:buster

RUN pip install request pyocclient google

RUN mkdir /app
WORKDIR /app

COPY . .

CMD ["python", "main.py"]