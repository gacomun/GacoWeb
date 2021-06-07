#sudo docker run --rm -d --name=gacomun_sonarr -p 9081:8081 gacomun/sickrage:latest
#sudo docker run --rm -d --name=gacomun_sonarr -p 9081:8081 linuxserver/sickrage:latest
sudo docker run --rm -d --name=gacomun_gacoweb -p 8020:8020 -e DJANGO_SUPERUSER_USERNAME=javier -e DJANGO_SUPERUSER_PASSWORD=4058 -e DJANGO_SUPERUSER_EMAIL=admin@example.com gacomun/gacoweb:latest
#sudo docker run -it --rm --name=gacomun_gacoweb gacomun/gacoweb:latest
#sudo docker run -it --rm --name gacomun_sonarr gacomun/sickrage:latest
#sudo docker run -it --rm --name=gacomun_sonarr -p 9081:8081 gacomun/sickrage:latest

