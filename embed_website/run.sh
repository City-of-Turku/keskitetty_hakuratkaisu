./build.sh
docker run -p 8888:80 --mount src=`pwd`,target=/usr/share/nginx/html,type=bind --rm embed_website
