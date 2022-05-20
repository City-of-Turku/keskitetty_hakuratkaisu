# do the yarn install and build
FROM node:16-alpine AS builder
WORKDIR /app
COPY . /app/
RUN yarn install
RUN yarn build

# and then copy the site to a webserver
FROM nginx:alpine
ADD ./docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
