FROM python

RUN pip3 install pyocclient dotenv

RUN mkdir /app
WORKDIR /app
RUN mkdir docs
COPY . .

CMD ["python", "-u", "main.py"]