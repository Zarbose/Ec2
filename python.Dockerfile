FROM python:3.11-bullseye

ENV DockerHOME=/home/app
ENV WebHOME=/webapp/

RUN mkdir -p $DockerHOME  
COPY $WebHOME $DockerHOME

RUN pip install --upgrade pip
RUN pip install Django

# RUN pip install requests
# RUN pip install datetime
# RUN pip install beautifulsoup4

WORKDIR $DockerHOME/Ec2
EXPOSE 8000

ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]
