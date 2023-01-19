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


def generate_yml_market(structures: QuerySet) -> str:
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
        offer_url.text = f'{DOMAIN}projects/{structure.class_name.lower()}s/{structure.slug}'

        offer_picture = SubElement(offer, 'picture')
        offer_picture.text = f'{DOMAIN}static/img/projects/{structure.short_name}/{structure.short_name}-0.jpeg'

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

    save_path_file = 'yandex_market.yml'

    with open(save_path_file, 'w') as f:
        f.write(encoded_cat)
    return encoded_cat


def generate_yml_realty(structures: QuerySet) -> str:
    date = dt.now().strftime('%Y-%m-%dT%H:%M')
    catalog = Element('realty-feed')
    catalog.set(
        'xmlns',
        'http://webmaster.yandex.ru/schemas/feed/realty/2010-06'
    )

    generation_date = SubElement(catalog, 'generation-date')
    generation_date.text = f'{date}'

    for structure in structures:
        offer = SubElement(catalog, 'offer')
        offer_id = generate_offer_id(structure.class_name, structure.id)
        offer.set('internal-id', f'{offer_id}')

        offer_type = SubElement(offer, 'type')
        offer_type.text = 'продажа'

        offer_prop_type = SubElement(offer, 'prop_type')
        offer_prop_type.text = 'жилая'

        offer_category_id = SubElement(offer, 'categoryId')
        category_id = 'дом'
        offer_category_id.text = str(category_id)

        # sales-agent info
        offer_agent = SubElement(offer, 'sales-agent')

        offer_agent_name = SubElement(offer_agent, 'name')
        offer_agent_name.text = 'ДомБаня'

        offer_agent_phone = SubElement(offer_agent, 'phone')
        offer_agent_phone.text = '79857601534'

        offer_agent_category = SubElement(offer_agent, 'category')
        offer_agent_category.text = 'застройщик'

        offer_agent_organisation = SubElement(offer_agent, 'organisation')
        offer_agent_organisation.text = 'ДомБаня'

        offer_agent_url = SubElement(offer_agent, 'url')
        offer_agent_url.text = DOMAIN

        offer_agent_photo = SubElement(offer_agent, 'photo')
        offer_agent_photo.text = f'{DOMAIN}static/img/logo.svg'

        # bargain info
        offer_price = SubElement(offer, 'price')

        offer_price_value = SubElement(offer_price, 'value')
        offer_price_value.text = f'{generate_offer_price(structure.cost)}'

        offer_price_currency_id = SubElement(offer_price, 'currency')
        offer_price_currency_id.text = 'RUR'

        # area info
        offer_area = SubElement(offer, 'area')

        offer_area_value = SubElement(offer_area, 'value')
        offer_area_value.text = f'{structure.square}'

        offer_area_unit = SubElement(offer_area, 'unit')
        offer_area_unit.text = 'кв. м'

        # deal info
        offer_deal = SubElement(offer, 'deal-status')
        offer_deal.text = 'продажа от застройщика'

    encoded_cat = tostring(catalog, encoding='unicode', xml_declaration=True)

    save_path_file = 'yandex_realty.ymr'

    with open(save_path_file, 'w') as f:
        f.write(encoded_cat)
    return encoded_cat
