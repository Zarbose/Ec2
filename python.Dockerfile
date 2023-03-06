FROM python:3.9.16-bullseye

ENV DockerHOME=/home/app
ENV WebHOME=/mysite/

RUN mkdir -p $DockerHOME  
COPY $WebHOME $DockerHOME

RUN pip install --upgrade pip
RUN python3 -m pip install Django
WORKDIR $DockerHOME
EXPOSE 8000

ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]
