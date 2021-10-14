#url https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
from django.core.management.base import BaseCommand
import juegos.tools as t
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
         t.toolpreciojuegos()


  