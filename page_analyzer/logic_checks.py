import requests
from bs4 import BeautifulSoup

# def find(find_element, soup:BeautifulSoup):
#     if isinstance(find_element, dict):


def check_response(url):
    tags = {'h1': '', 'title': '', 'content': '', 'status_code': '', 'error': False}
    try:
        response = requests.get(url)
        tags['status_code'] = response.status_code
        if tags['status_code'] != 200:
            raise requests.RequestException

        # flash('Произошла ошибка при проверке')
        # return redirect(url_for('url_page', id=id))

        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.h1:
            tags['h1'] = soup.h1.string
        if soup.title:
            tags['title'] = soup.title.string

        descriprion = soup.find('meta', attrs={'name': 'description'})
        print(descriprion)
        try:
            tags['content'] = descriprion.get('content')
        except:
            tags['content'] = ""
        return tags
    except requests.RequestException:
        tags['error'] = True
        return tags
