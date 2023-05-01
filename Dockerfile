FROM python:3.10

WORKDIR /app

RUN pip install -U --pre aiogram
RUN pip install python-dotenv

COPY . /app

CMD python3 main.py
