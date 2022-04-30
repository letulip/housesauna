from xml.dom import minidom
from datetime import datetime as dt
from django.db.models import QuerySet

DOMAIN = 'https://domizkleenogobrusa.ru/'


def generate_offer_id(category: str, id: int) -> str:
    prefix = 1000 if category == 'House' else 2000
    new_id = prefix + id
    return new_id


def generate_offer_price(price: str) -> str:
    return price.replace(' ', '')


def generate_yml(structures: QuerySet) -> None:
    root = minidom.Document()

    date = dt.now().strftime('%Y-%m-%d %H:%M')
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', date)

    shop = root.createElement('shop')
    name = root.createElement('name')
    shop_name = root.createTextNode('ДомБаня')
    name.appendChild(shop_name)
    shop.appendChild(name)

    company = root.createElement('company')
    company_name = root.createTextNode('ДомБаня')
    company.appendChild(company_name)
    shop.appendChild(company)

    url = root.createElement('url')
    url_text = root.createTextNode(DOMAIN)
    url.appendChild(url_text)
    shop.appendChild(url)

    currencies = root.createElement('currencies')
    currency = root.createElement('currency')
    currency.setAttribute('id', 'RUB')
    currency.setAttribute('rate', '1')
    currencies.appendChild(currency)
    shop.appendChild(currencies)

    categories = root.createElement('categories')
    x = 1
    while x < 3:
        category = root.createElement('category')
        category.setAttribute('id', f'{x}')
        category_name = 'Дома' if x == 1 else 'Бани'
        category_text = root.createTextNode(f'{category_name}')
        category.appendChild(category_text)
        categories.appendChild(category)
        x += 1
    shop.appendChild(categories)

    offers = root.createElement('offers')

    for structure in structures:
        offer = root.createElement('offer')
        offer_id = generate_offer_id(structure.class_name, structure.id)
        offer.setAttribute('id', f'{offer_id}')

        offer_name = root.createElement('name')
        offer_name_text = root.createTextNode(f'{structure.title}')
        offer_name.appendChild(offer_name_text)
        offer.appendChild(offer_name)

        offer_url = root.createElement('url')
        offer_url_text = root.createTextNode(f'{DOMAIN}{structure.slug}')
        offer_url.appendChild(offer_url_text)
        offer.appendChild(offer_url)

        offer_picture = root.createElement('picture')
        offer_picture_text = root.createTextNode(
            f'{DOMAIN}{structure.slug}-0.jpg'
        )
        offer_picture.appendChild(offer_picture_text)
        offer.appendChild(offer_picture)

        offer_price = root.createElement('price')
        offer_price_text = root.createTextNode(
            f'{generate_offer_price(structure.cost)}'
        )
        offer_price.appendChild(offer_price_text)
        offer.appendChild(offer_price)

        offer_currency_id = root.createElement('currencyId')
        offer_currency_id_text = root.createTextNode('RUR')
        offer_currency_id.appendChild(offer_currency_id_text)
        offer.appendChild(offer_currency_id)

        offer_category_id = root.createElement('categoryId')
        category_id = 1 if category == 'House' else 2
        offer_category_id_text = root.createTextNode(str(category_id))
        offer_category_id.appendChild(offer_category_id_text)
        offer.appendChild(offer_category_id)

        offer_dimensions = root.createElement('dimensions')
        offer_dimensions_text = root.createTextNode(f'{structure.dimensions}')
        offer_dimensions.appendChild(offer_dimensions_text)
        offer.appendChild(offer_dimensions)

        offer_param_constr = root.createElement('param')
        offer_param_constr.setAttribute('name', 'Срок постройки')
        offer_param_constr_text = root.createTextNode(f'{structure.construction}')
        offer_param_constr.appendChild(offer_param_constr_text)
        offer.appendChild(offer_param_constr)

        offer_param_square = root.createElement('param')
        offer_param_square.setAttribute('name', 'Площадь')
        offer_param_square_text = root.createTextNode(f'{structure.square}')
        offer_param_square.appendChild(offer_param_square_text)
        offer.appendChild(offer_param_square)

        offer_param_brus = root.createElement('param')
        offer_param_brus.setAttribute('name', 'Брус сечение')
        offer_param_brus_text = root.createTextNode(f'{structure.brus}')
        offer_param_brus.appendChild(offer_param_brus_text)
        offer.appendChild(offer_param_brus)

        offers.appendChild(offer)
    shop.appendChild(offers)

    xml_root.appendChild(shop)

    xml_str = root.toprettyxml(indent='\t', newl='\n')
    save_path_file = 'yandex.yml'

    with open(save_path_file, 'w') as f:
        f.write(xml_str)
