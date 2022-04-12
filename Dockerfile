FROM python

RUN pip3 install pyocclient google

RUN mkdir /app
WORKDIR /app

COPY . .

CMD ["python", "main.py"]