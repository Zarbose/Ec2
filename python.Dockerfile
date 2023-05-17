FROM python:3.11-bullseye


WORKDIR /app
COPY webapp /app/webapp
COPY script /app/script
COPY requirements.txt requirements.txt

## Pip
RUN pip install --upgrade pip
# RUN pip install Django
# RUN pip install requests
# RUN pip install datetime
# RUN pip install beautifulsoup4
# RUN pip install 'influxdb-client[ciso]'

RUN pip install -r requirements.txt

# ENV SECRET_KEY='django-insecure-sk=@gdj#ldi&pyc7mj1bgfyzciyr)7phny7cnf!en8+0%rh!)r'
# ENV DOCKER_INFLUXDB_INIT_ADMIN_TOKEN='c5gyOEb7KSRLIoFuFrFDMUo9UDgmAlSMty9GJJZEMN3X5qfn6mkgVRCSxXottjfG8BZduRNOLivEql4FCngFjQ=='

EXPOSE 8000

ENTRYPOINT ["python3","webapp/Ec2/manage.py","runserver","0.0.0.0:8000"]
