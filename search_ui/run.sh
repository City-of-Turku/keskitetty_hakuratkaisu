docker build -t haku-frontend .
docker run -p 8004:80 --rm haku-frontend
docker rmi haku-frontend