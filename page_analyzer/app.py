import datetime
import os
from flask import (Flask, redirect, render_template,
                   request, url_for, flash, get_flashed_messages)
from dotenv import load_dotenv
from page_analyzer.validator import validate
from urllib.parse import urlparse
from page_analyzer.database import (get_urls, get_url_by_id,
                                    get_id_url_by_name,
                                    get_name_url_by_id, get_url_checks,
                                    get_url_check_last, create_check,
                                    create_url, get_connection)
from page_analyzer.utils import check_response

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls():
    messages = get_flashed_messages()
    urls = get_urls(get_connection())
    for url in urls:
        data_check = get_url_check_last(url['id'], get_connection())
        if data_check is None:
            url['last_check'] = ''
            url['status_code'] = ''
        else:
            url['last_check'] = data_check['created_at'].date()
            url['status_code'] = data_check['status_code']
    return render_template('urls.html', urls=urls, messages=messages)


@app.post('/urls')
def url_add():
    response = request.form.to_dict()
    data_url = url_parse(response)

    errors = validate(response)
    if errors:
        flash(errors['name'])
        return render_template('index.html', errors=errors), 422

    urls = get_urls(get_connection())
    for url in urls:
        if data_url == get_name_url_by_id(url['id'], get_connection())['name']:
            flash('Страница уже существует')
            return redirect(url_for('url_page', id=url['id']))

    create_url(
        {'name': data_url, 'created_at': datetime.datetime.now().date()},
        get_connection()
    )
    data = get_id_url_by_name(data_url, get_connection())
    flash('Страница успешно добавлена')
    return redirect(url_for('url_page', id=data['id']))


@app.get('/urls/<id>')
def url_page(id):
    messages = get_flashed_messages()
    url = get_url_by_id(id, get_connection())
    if not url:
        return render_template('404.html'), 404
    checks = get_url_checks(int(id), conn=get_connection())
    return render_template('url.html', url=url, checks=checks,
                           messages=messages)


@app.post('/urls/<id>/checks')
def check_url(id):
    data = {}
    data['url_id'] = int(id)
    data['created_at'] = datetime.datetime.now().date()
    url = get_name_url_by_id(int(id), get_connection())

    check = check_response(url["name"])
    if check["error"]:
        flash('Произошла ошибка при проверке')
    else:
        data.update(check)
        create_check(data, get_connection())
        flash('Страница успешно проверена')
    return redirect(url_for('url_page', id=data["url_id"]))


def url_parse(response):
    url = urlparse(response['url'])
    data_url = url.scheme + "://" + url.netloc
    return data_url


if __name__ == "__main__":
    app.run()
