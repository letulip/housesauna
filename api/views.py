from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db import models
from django.core import serializers
from django.core.files import File
from itertools import chain
from rest_framework import viewsets
from houses.models import House, Sauna
from .serializers import StructureSerializer, SaunaSerializer
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
        # data = serializers.serialize('xml', result_list)
        # f = open('catalog2.xml', 'w')
        # myfile = File(f)
        # myfile.write(data)
        # myfile.close()
        print('Done')
        return result_list
