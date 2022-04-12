FROM python

RUN pip3 install pyocclient google

RUN mkdir /app
WORKDIR /app
RUN mkdir docs
COPY . .

CMD ["python", "-u", "main.py"]