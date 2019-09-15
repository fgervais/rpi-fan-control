FROM python:3.7.4-slim-buster as dev
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "fan-control.py"]

FROM dev
COPY . /app/
