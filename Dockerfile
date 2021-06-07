FROM python:3.10.0b1-slim-buster

ENV TZ 'Europe/Madrid'

RUN echo $TZ > /etc/timezone && \
	apt update && \
	apt -y upgrade && \
	apt install nginx tzdata -y && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
	apt -y autoremove && \
    apt clean

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY . /GacoWeb/
WORKDIR /GacoWeb

RUN pip3 install -r requirements.txt