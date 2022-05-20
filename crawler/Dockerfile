# The official Python 3 Docker image.
FROM python:3.9
 
# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

COPY ./crawler .
COPY ./config.yaml ../config.yaml

# Install Scrapy specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
 
# Run the crawler when the container launches.
CMD [ "python", "./go-spider.py" ]
