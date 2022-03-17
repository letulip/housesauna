from xml.dom import minidom


root = minidom.Document()

date = '2021-05-07 10:44'

xml_root = root.createElement('yml_catalog')
root.appendChild(xml_root)
xml_root.setAttribute('date', date)

shop = root.createElement('shop')

name = root.createElement('name')
shop_name = root.createTextNode('SK Design')
name.appendChild(shop_name)

company = root.createElement('company')
company_name = root.createTextNode('SK Design')
company.appendChild(company_name)

url = root.createElement('url')
url_text = root.createTextNode('https://skdesign.ru/')
url.appendChild(url_text)

platformChild = root.createElement('platform')
textPlatform = root.createTextNode('Yml for Yandex Market')
platformChild.appendChild(textPlatform)

versionChild = root.createElement('version')
textVersion = root.createTextNode('001')
versionChild.appendChild(textVersion)

currencies = root.createElement('currencies')

currency = root.createElement('currency')
currency.setAttribute('id', 'RUB')
currency.setAttribute('rate', '1')

categories = root.createElement('categories')

x = 0
while x < 10:
    category = root.createElement('category')
    category.setAttribute('id', f'44454 {x}')
    category.setAttribute('parentId', '2520')
    textCategory = root.createTextNode(f'Aldo {x}')
    category.appendChild(textCategory)
    categories.appendChild(category)
    x += 1

offers = root.createElement('offers')
y = 0

while y < 10:
    offer = root.createElement('offer')
    offer.setAttribute('group_id', f'162497{y}')
    offer.setAttribute('id', f'162499{y}')
    offer.setAttribute('available', 'true')
    offers.appendChild(offer)
    y += 1
    i = 0
    while i < 5:
        paramChild = root.createElement('param')
        paramChild.setAttribute('name', f'name-{i}')
        textParam = root.createTextNode(f'text - {i}')
        paramChild.appendChild(textParam)
        offer.appendChild(paramChild)
        i += 1
    offer_name = root.createElement('name')
    offer_name_text = root.createTextNode(f'Table{y}')
    offer_name.appendChild(offer_name_text)
    offer.appendChild(offer_name)
    offer_picture = root.createElement('picture')
    offer_picture_url = root.createTextNode(f'url{y}')
    offer_picture.appendChild(offer_picture_url)
    offer.appendChild(offer_picture)
    offer_url = root.createElement('url')
    textUrlOffer = root.createTextNode(f'url-variation{y}')
    offer_url.appendChild(textUrlOffer)
    offer.appendChild(offer_url)

shop.appendChild(name)
shop.appendChild(company)
shop.appendChild(url)
shop.appendChild(platformChild)
shop.appendChild(versionChild)
shop.appendChild(currencies)
currencies.appendChild(currency)
shop.appendChild(categories)
shop.appendChild(offers)

xml_root.appendChild(shop)

xml_str = root.toprettyxml(indent="\t")
save_path_file = "yandex.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
