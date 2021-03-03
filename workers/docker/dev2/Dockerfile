# pull official base image
FROM python:3.7-slim-buster

# set environment variables and arguments
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG PROJECT=fl-demo-worker2
ARG PROJECT_DIR=/var/www/${PROJECT}
#ARG BASE_PROJECT_DIR=server

# Install linux dependencies
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim \
    nano

# Set work directory & install Python dependencies

RUN mkdir -p $PROJECT_DIR
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR $PROJECT_DIR

# Server
EXPOSE 7102
STOPSIGNAL SIGINT
ENTRYPOINT [ "python" ]
CMD [ "run_single_server.py", "--is_docker", "--port=7102"]
#RUN ls
#ENTRYPOINT [ "python" ]

