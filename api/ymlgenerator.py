from datetime import datetime as dt

from django.db.models import QuerySet

from xml.etree.ElementTree import Element, SubElement, tostring


DOMAIN = 'https://domizkleenogobrusa.ru/'


def generate_offer_id(category: str, id: int) -> str:
    prefix = 1000 if category == 'House' else 2000
    new_id = prefix + id
    return new_id


def generate_offer_price(price: str) -> str:
    return price.replace(' ', '')


def generate_yml2(structures: QuerySet) -> None:
    date = dt.now().strftime('%Y-%m-%dT%H:%M')
    catalog = Element('yml_catalog')
    catalog.set('date', date)

    shop = SubElement(catalog, 'shop')

    name = SubElement(shop, 'name')
    name.text = 'ДомБаня'

    company = SubElement(shop, 'company')
    company.text = 'ДомБаня'

    url = SubElement(shop, 'url')
    url.text = DOMAIN

    currencies = SubElement(shop, 'currencies')
    currency = SubElement(currencies, 'currency')
    currency.set('id', 'RUB')
    currency.set('rate', '1')

    categories = SubElement(shop, 'categories')
    x = 1
    while x < 3:
        category = SubElement(categories, 'category')
        category.set('id', f'{x}')
        category.text = 'Дома' if x == 1 else 'Бани'
        x += 1

    offers = SubElement(shop, 'offers')

    for structure in structures:
        offer = SubElement(offers, 'offer')
        offer_id = generate_offer_id(structure.class_name, structure.id)
        offer.set('id', f'{offer_id}')

        offer_name = SubElement(offer, 'name')
        offer_name.text = f'{structure.title}'

        offer_url = SubElement(offer, 'url')
        offer_url.text = f'{DOMAIN}{structure.slug}'

        offer_picture = SubElement(offer, 'picture')
        offer_picture.text = f'{DOMAIN}{structure.slug}-0.jpg'

        offer_price = SubElement(offer, 'price')
        offer_price.text = f'{generate_offer_price(structure.cost)}'

        offer_currency_id = SubElement(offer, 'currencyId')
        offer_currency_id.text = 'RUR'

        offer_category_id = SubElement(offer, 'categoryId')
        category_id = 1 if category == 'House' else 2
        offer_category_id.text = str(category_id)

        offer_dimensions = SubElement(offer, 'dimensions')
        offer_dimensions.text = f'{structure.dimensions}'

        offer_param_constr = SubElement(offer, 'param')
        offer_param_constr.set('name', 'Срок постройки')
        offer_param_constr.text = f'{structure.construction}'

        offer_param_square = SubElement(offer, 'param')
        offer_param_square.set('name', 'Площадь')
        offer_param_square.text = f'{structure.square}'

        offer_param_brus = SubElement(offer, 'param')
        offer_param_brus.set('name', 'Брус сечение')
        offer_param_brus.text = f'{structure.brus}'

    encoded_cat = tostring(catalog, encoding='unicode', xml_declaration=True)

    save_path_file = 'yandex2.yml'

    with open(save_path_file, 'w') as f:
        f.write(encoded_cat)
    return encoded_cat
