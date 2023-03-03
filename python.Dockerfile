FROM python

ENV DockerHOME=/home/app
ENV WebHOME=/webapp/

RUN mkdir -p $DockerHOME  
COPY $WebHOME $DockerHOME

RUN pip install --upgrade pip
RUN python3 -m pip install Django
RUN pip install requests
RUN pip install datetime
RUN pip install beautifulsoup4
RUN pip install 'influxdb-client[ciso]'

WORKDIR $DockerHOME
EXPOSE 8000

ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]