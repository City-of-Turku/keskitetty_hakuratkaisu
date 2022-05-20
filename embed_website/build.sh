docker build -t embed_website .
docker rmi europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/embed_website
docker tag embed_website europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/embed_website
