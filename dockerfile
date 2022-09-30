FROM python:3

RUN apt-get update && apt-get -y install cron vim tzdata

ENV TZ="America/New_York"

WORKDIR /app

COPY crontab /etc/cron.d/crontab

COPY dollar.py /app/dollar.py

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab

RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron","-f"]