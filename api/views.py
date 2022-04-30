from django.utils import timezone
from django.db import models
from itertools import chain
from rest_framework import viewsets
from houses.models import House, Sauna
from .serializers import StructureSerializer
from .ymlgenerator import generate_yml


class StructuresViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Отображение всех существующих построек.
    """

    serializer_class = StructureSerializer

    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(
            pub_date__lte=timezone.now()
        )

    def get_queryset(self) -> list:
        chain_list = list(chain(
            self.get_object_list(House),
            self.get_object_list(Sauna)
        ))
        result_list = sorted(
            chain_list,
            key=lambda instance: instance.pub_date,
            reverse=True
        )
        generate_yml(result_list)
        print('Done')
        return result_list
