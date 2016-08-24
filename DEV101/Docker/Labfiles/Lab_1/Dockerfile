FROM ubuntu
RUN apt-get update;apt-get install -y nodejs npm
EXPOSE 80
ENV PORT 80
RUN mkdir /todo
WORKDIR /todo
ADD . /todo
CMD nodejs app.js
