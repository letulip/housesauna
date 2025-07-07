from datetime import timezone
from itertools import chain

from django.core import serializers
from django.core.files import File
from django.db import models

from houses.models import House, Sauna
from housesauna.logger import logger


def get_object_list(self, model: models.Model) -> models.Model:
    return model.objects.filter(
        pub_date__lte=timezone.now()
    )


def export_to_xml() -> None:
    """Функция для выгрузки каталога в формате xml."""
    chain_list = list(chain(
        get_object_list(House),
        get_object_list(Sauna)
    ))
    result_list = sorted(
        chain_list,
        key=lambda instance: instance.pub_date,
        reverse=True
    )
    data = serializers.serialize('xml', result_list)
    f = open('catalog.xml', 'w')
    logger.debug('Записываем в catalog.xml...')
    myfile = File(f)
    myfile.write(data)
    myfile.close()
    logger.debug('Запись в catalog.xml завершена.')
