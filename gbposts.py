import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

url = "https://gb.ru"

# ua = UserAgent()
params = {'page': 1}
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

session = requests.session()

all_posts = []
while True:
    response = session.get(url + "/posts", headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    posts = soup.find_all('div', {'class': 'post-item'})
    if not posts:
        break

    for post in posts:
        post_info = {}

        name_info = post.find('a', {'class': 'post-item__title'})
        post_info['name'] = name_info.getText()
        post_info['url'] = url + name_info.get('href')

        add_info = post.find('div', {'class': 'text-muted'}).findChildren('span')
        post_info['views'] = int(add_info[0].getText())
        post_info['comments'] = int(add_info[1].getText())

        all_posts.append(post_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

pprint(all_posts)
pprint(len(all_posts))