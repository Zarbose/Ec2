FROM python:3.11-bullseye


WORKDIR /app
COPY webapp /app/webapp
COPY requirements.txt requirements.txt

## Pip
RUN pip install --upgrade pip
# RUN pip install Django
# RUN pip install requests
# RUN pip install datetime
# RUN pip install beautifulsoup4
# RUN pip install 'influxdb-client[ciso]'

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3","webapp/Ec2/manage.py","runserver","0.0.0.0:8000"]
