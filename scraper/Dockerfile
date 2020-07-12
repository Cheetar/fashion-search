FROM python:3.7-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
RUN pip install -r ./requirements.txt

COPY . .

ENTRYPOINT ["python3", "scraper.py"]
