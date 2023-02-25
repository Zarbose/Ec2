FROM python

ENV DockerHOME=/home/app
ENV WebHOME=/mysite/

# Installing basic tools
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y iputils-ping vim net-tools dstat wget

RUN mkdir -p $DockerHOME
COPY $WebHOME $DockerHOME

# Installing influxdb client 
ENV SourceHOME=/home/source
RUN mkdir -p $DockerHOME
COPY /sources/ $SourceHOME
RUN cp $SourceHOME/influxdb2-client-2.6.1-linux-amd64/influx /usr/local/bin/

# Installing python modles
RUN pip install --upgrade pip
RUN python3 -m pip install Django
RUN pip install requests
RUN pip install beautifulsoup4

RUN pip install 'influxdb-client[ciso]'
RUN pip install pandas

WORKDIR $DockerHOME
EXPOSE 8000

ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]