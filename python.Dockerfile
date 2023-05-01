FROM python:3.11-bullseye

ENV DockerHOME=/home/app
ENV WebHOME=/webapp/

RUN mkdir -p $DockerHOME  
COPY $WebHOME $DockerHOME

# COPY init.sh /root/init.sh

RUN pip install --upgrade pip
RUN pip install Django
# RUN python3 Script/startup.py

# RUN pip install requests
# RUN pip install datetime
# RUN pip install beautifulsoup4

WORKDIR $DockerHOME/Ec2
EXPOSE 8000

# ENTRYPOINT ["./init.sh"]
ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]
