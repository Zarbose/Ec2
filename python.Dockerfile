FROM python:3.11-bullseye


WORKDIR /app
COPY webapp /webapp
COPY script /script

## Pip
RUN pip install --upgrade pip
RUN pip install Django
RUN pip install requests
RUN pip install datetime

# RUN python3 script/startup.py

# RUN pip install datetime
# RUN pip install beautifulsoup4

EXPOSE 8000

# ENTRYPOINT ["python3","webapp/manage.py","runserver","0.0.0.0:8000"]
