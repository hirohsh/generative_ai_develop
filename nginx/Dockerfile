FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN apk update && apk add logrotate

COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./conf/templates /etc/nginx/templates

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
