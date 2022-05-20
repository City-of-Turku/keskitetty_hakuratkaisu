# base image
FROM python:3

# working directory in the container
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
COPY ./search_backend/requirements.txt .

# copy the content of the local src directory to the working directory
COPY ./search_backend/ .
COPY ./config-backend.yaml ../config.yaml

# Install packages
RUN apt-get clean \
  && apt-get -y update

RUN apt-get -y install nginx python3-dev build-essential

# install dependencies
RUN pip install -r requirements.txt


# Enable wait for script
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

COPY ./search_backend/nginx.conf /etc/nginx
RUN chmod +x ./start-backend.sh

# command to run on container start
CMD ["./start-backend.sh" ]