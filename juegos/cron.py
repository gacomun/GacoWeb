import juegos.tools as t
from juegos.models import Oferta  # Import the model classes we just wrote.
import logging

logger = logging.getLogger(__name__)

def precios_job():
  t.toolpreciojuegos()

def ofertas_job():
  t.toolofertas("")

def borrar_job():
    logger.info("Inicio borrar_job")
    Oferta.objects.all().delete()