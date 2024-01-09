import requests
from bs4 import BeautifulSoup


def check_response(url):
    tags = {'h1': '', 'title': '', 'content': '',
            'status_code': '', 'error': False}
    try:
        response = requests.get(url)
        tags['status_code'] = response.status_code
        if tags['status_code'] != 200:
            raise requests.RequestException

        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.h1:
            tags['h1'] = soup.h1.string
        if soup.title:
            tags['title'] = soup.title.string

        descriprion = soup.find('meta', attrs={'name': 'description'})
        print(descriprion)
        tags['content'] = descriprion.get('content')
        return tags
    except requests.RequestException:
        tags['error'] = True
        return tags
