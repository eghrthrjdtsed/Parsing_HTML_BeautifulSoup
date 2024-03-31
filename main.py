import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

# url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
url = "https://www.boxofficemojo.com"

# ua = UserAgent()

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
params = {"ref_": "bo_nb_hm_tab"}

session = requests.session()

response = session.get(url + "/intl", params=params, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
test_link = soup.find("a", {'class': 'a-link-normal'})
rows = soup.find_all('tr')
films = []
for row in rows[2:-3]:
    film = {}

    # aria_info = row.find('td', {'class': 'mojo-field-type-area_id'}).find('a')
    aria_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]
    film['area'] = [aria_info.getText(), url + aria_info.get('href')]

    weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
    film['weekend'] = [weekend_info.getText(), url + weekend_info.get('href')]

    film['releases'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText())

    f_releases_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
    film['f_releases'] = [f_releases_info.getText(), url + f_releases_info.get('href')]

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(), url + distributor_info.get('href')]
    except:
        print('Exception with f_releases, object = ', film['f_releases'])
        film['distributor'] = None

    film['gross'] = row.find('td', {'class': 'mojo-field-type-money'}).getText()

    films.append(film)

pprint(films)
