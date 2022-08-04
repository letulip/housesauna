from django.utils import timezone
from django.db import models

from itertools import chain
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from houses.models import House, Sauna
from .serializers import StructureSerializer
from .ymlgenerator import generate_yml2


class StructuresApiView(APIView):
    serializer_class = StructureSerializer
    http_method_names = ['get', ]
    parser_classes = (XMLParser,)
    render_classes = (XMLRenderer,)

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
        result_yml = generate_yml2(result_list)
        return result_yml

    def get(self, format=None):

        return Response(
            data=self.get_queryset(),
            status=HTTP_200_OK
        )
