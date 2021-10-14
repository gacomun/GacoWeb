# Dockerfile
# https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application

FROM python:slim-buster

VOLUME ["/GacoWeb/data", "/GacoWeb/log"]

# set environment variables
ENV TZ 'Europe/Madrid'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo $TZ > /etc/timezone && \
	apt update && \
	apt -y upgrade && \
	apt install nginx tzdata cron nano -y --no-install-recommends && \
#	apt install nginx tzdata -y --no-install-recommends && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
	apt -y autoremove && \
    apt clean

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /GacoWeb
RUN mkdir -p /GacoWeb/data
RUN mkdir -p /GacoWeb/log
#RUN pip install --no-cache-dir Django==3.1.2 requests==2.25.0 lxml==4.6.3 beautifulsoup4==4.9.3 djangorestframework==3.12.4 django-cors-headers==3.7.0 django-crontab==0.7.1 gunicorn==20.0.4
COPY . /GacoWeb/
WORKDIR /GacoWeb
RUN crontab -u root /GacoWeb/plani.txt

RUN pip install -r requirements.txt
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["sh","start-server.sh"]