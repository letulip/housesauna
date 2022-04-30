from rest_framework import serializers
from houses.models import House, Sauna


"""
<offer id="2015">
    <name>
        Дом-Баня из клееного бруса "Воронеж"
    </name>
    <url>
        https://domizkleenogobrusa.ru/house-sauna-41-meters
    </url>
    <price>
        2 173 000
    </price>
    <currencyId>
        RUR
    </currencyId>
    <categoryId>
        2
    </categoryId>
    <dimensions>
        5,6х7,2
    </dimensions>
    <square>
        41
    </square>
    <construction>
        ОДИН месяц
    </construction>
    <param name="Брус сечение">
        Ш 130/В 140
    </param>
</offer>
"""

DOMAIN = 'https://domizkleenogobrusa.ru/'


class StructureSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='class_name')
    categoryId = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    price = serializers.CharField(source='cost')
    url = serializers.SerializerMethodField()
    currencyId = serializers.CharField(read_only=True, default='RUR')
    param = serializers.SerializerMethodField()
    imageUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = House
        fields = (
            'category',
            'categoryId',
            'name',
            'url',
            'imageUrl',
            'price',
            'currencyId',
            'dimensions',
            'square',
            'construction',
            'param',
        )

    def get_categoryId(self, obj):
        return 1 if obj.class_name == 'House' else 2

    def get_url(self, obj):
        return f'{DOMAIN}{obj.slug}'

    def get_imageUrl(self, obj):
        return f'{DOMAIN}{obj.slug}-0.jpg'

    def get_param(self, obj):
        return f'Брус сечение: {obj.brus}'
