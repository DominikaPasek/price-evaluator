from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver as web


# making_soup works for biltema, byggmax, clasohlson, monter, nysted
def making_soup(url):
    browser = webdriver.Firefox(executable_path=r'C:\Users\domip\PycharmProjects\geckodriver-v0.29.1-win64\geckodriver.exe')
    browser.get(url)
    html_source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html_source, 'html.parser')
    return soup


# new_soup works for
def new_soup(url):
    browser = web.Firefox(executable_path=r'C:\Users\domip\PycharmProjects\geckodriver-v0.29.1-win64\geckodriver.exe')
    browser.get(url)


def biltema(url):
    soup = making_soup(url)
    get_price = soup.find_all('div', {'class': 'ga__data--holder'})
    products = []
    for item in get_price:
        products.append([item.get("data-product-name"), item.get("data-product-price")])
    # if ',-' in get_price:
    #     l = len(get_price)
    #     price = get_price[:l-2]
    # else:
    #     rev_price = list(get_price[::-1])
    #     rev_price.insert(2, '.')
    #     price = "".join(rev_price)
    #     price = price[::-1]
    return products

# def biltema(url):
#     soup = making_soup(url)
#     get_price = soup.find('div', {'class': 'price__sum'}).text
#     if ',-' in get_price:
#         l = len(get_price)
#         price = get_price[:l-2]
#     else:
#         rev_price = list(get_price[::-1])
#         rev_price.insert(2, '.')
#         price = "".join(rev_price)
#         price = price[::-1]
#     return price


# print(biltema('https://www.biltema.no/verktoy/sliping/slipepapir/slipepapir-2000019224'))
# print(biltema('https://www.biltema.no/bygg/kjemikalier/lim/trelim-2000024076'))
# print(biltema('https://www.biltema.no/bygg/hengsler/dorhengsel/hengselretter-2000017312'))


def byggmax(url):
    soup = making_soup(url)
    get_product = soup.find_all('span', {'class': 'price'})[-1]
    price_integer = get_product.find('span', {'class': 'integer'}).text
    price_decimal = get_product.find('span', {'class': 'decimal'}).text

    price = price_integer + '.' + price_decimal
    price = price.replace(u'\xa0', u' ')
    price += '00'
    price = price.replace(' ', '')
    return price

# print(byggmax('https://www.byggmax.no/sokkel-eik-fin%C3%A9r-barlinek-p13390'))
# print(byggmax('https://www.byggmax.no/21x95-terrassebord-gr%C3%B8nn-p08722095'))
# print(byggmax('https://www.byggmax.no/terrasseskrue-rustkfri-a2-42x42-1000stk-p24474'))


def clasohlson(url):
    soup = making_soup(url)
    try:
        get_product = soup.find('span', {'class': 'product__price-value'}).text
    except AttributeError:
        get_product = soup.find('span', {'class': 'product__discount-price'}).text
    price = get_product.replace(',', '.')
    # price = price.replace(u'\xa0', u' ')
    return price

# print(clasohlson('https://www.clasohlson.com/no/Gummiklubbe/p/40-7558'))
# print(clasohlson('https://www.clasohlson.com/no/Ryobi-R18DD3-113S-drill/p/41-2127'))


def monter(url):
    soup = making_soup(url)
    get_product = soup.find('span', {'class': 'add-to-cart__price-container'}).text
    price = get_product.strip()
    price = price.replace(',', '.')
    return price

# print(monter('https://www.monter.no/maling/utemaling/utendors-beis/opus-oljedekkbeis-30-base-f8a5388b/7557187/'))


def nysted(url):
    soup = making_soup(url)
    get_product = soup.find_all('bdi')[4].text
    price = get_product.lstrip('kr')
    price = price.replace(u'\xa0', u'')
    return price

# print(nysted('https://www.nysted.no/produkt/spraylakk/spraylakk-2/quick-spray-153-sort-matt/'))


def maxbo(url):
    pass

# print(maxbo('https://www.maxbo.no/terrasseskrue-ruspert-4-2x55-a200-utvendig-senk-t20-fiberkutt-p2659979/'))


def obsbygg(url):
    pass
#

# print(obsbygg('https://www.obsbygg.no/gulv-og-tilbehor/heltregulv/2360007?v=ObsBygg-7040430016649'))
# print(obsbygg('https://www.obsbygg.no/maling-tapet-og-tilbehor/lim-fug-og-sparkel/casco-multiseal-bygg-fugemasse-d5c54719?v=ObsBygg-7311980132012'))
# print(obsbygg('https://www.obsbygg.no/maling-tapet-og-tilbehor/lim-fug-og-sparkel/fugemasse-casco-akryl-63b09248?v=ObsBygg-7311980100509'))


def flugger(url):
    soup = making_soup(url)
    pass


def jernia(url):
    soup = making_soup(url)
    pass


def jula(url):
    options = {
    'port': 9999  # Tell the backend to listen on port 9999 (not normally necessary to set this)
    }
    my_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/74.0.3729.169 Safari/537.36'}
    cap = DesiredCapabilities().FIREFOX
    # browser = web.Firefox(executable_path=r'C:\Users\domip\PycharmProjects\geckodriver-v0.29.1-win64\geckodriver.exe')
    browser = web.Firefox(capabilities=cap,
                       executable_path=r'C:\Users\domip\PycharmProjects\geckodriver-v0.29.1-win64\geckodriver.exe',
                       seleniumwire_options=options)
    browser.get(url)
    for request in browser.requests:
        if request.response:
            my_data = (
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
        else:
            my_data = 'No response'
    browser.quit()
    my_data = 'Nic nie wiem'
    return my_data


# print(jula('https://www.jula.no/catalog/bygg-og-maling/spiker-og-skruer/rustfrie-skruer/treskruer/treskruer-014441/'))


def optimera(url):
    soup = making_soup(url)
    pass
#     trzeba być zalogowanym...
