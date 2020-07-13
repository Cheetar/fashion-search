FROM python:3.7-alpine

WORKDIR /app

RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .

ENTRYPOINT ["python3", "scraper.py"]
