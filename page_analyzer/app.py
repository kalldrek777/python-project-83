import datetime
import os
from flask import Flask, redirect, render_template, request, url_for, flash, abort, get_flashed_messages
# from validator import validate
from dotenv import load_dotenv
from page_analyzer.validator import validate
from urllib.parse import urlparse
from page_analyzer.database import get_urls, get_url_by_id, get_id_url_by_name, get_name_url_by_id, get_url_checks, get_url_check_last, create_check, create_url
from page_analyzer.logic_checks import check_response

load_dotenv()

# TIMEOUT = int(os.getenv('EXTERNAL_REQUEST_TIMEOUT', 30))
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# db = SQLAlchemy(app)


# class Urls(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#
#     def __init__(self, name):
#         self.name = name
#
#
# # def true_date(time):
# #     return str(time)[0:10]
#
#
# class Url_Checks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     url_id = db.Column(db.Integer, nullable=False)
#     status_code = db.Column(db.Integer, nullable=False)
#     h1 = db.Column(db.String(255), unique=False)
#     title = db.Column(db.String(255), nullable=True, unique=False)
#     description = db.Column(db.String(255), nullable=True, unique=False)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#
#     def __init__(self, url_id, status_code, h1, title, description):
#         self.url_id = url_id
#         self.status_code = status_code
#         self.h1 = h1
#         self.title = title
#         self.description = description


# with app.app_context():
    # db.drop_all()
        # db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/urls')
def urls():
    messages = get_flashed_messages()
    data = get_urls()
    for url in data:
        data_check = get_url_check_last(url['id'])
        if data_check is None:
            url['last_check'] = ''
            url['status_code'] = ''
        else:
            url['last_check'] = data_check['created_at'].date()
            url['status_code'] = data_check['status_code']
    return render_template('urls.html', urls=data, messages=messages)


@app.post('/urls')
def url_add():
    data = {}
    response = request.form.to_dict()
    url = urlparse(response['url'])
    data_url = url.scheme + "://" + url.netloc

    errors = validate(response)
    if errors:
        flash(errors['name'])
        return render_template('index.html', errors=errors), 422

    urls = get_urls()
    for url in urls:   # не видит
        print(url['id'])
        print(data_url)
        print(get_name_url_by_id(url['id'])['name'])
        if data_url == get_name_url_by_id(url['id'])['name']:
            flash('Страница уже существует')
            return redirect(url_for('url_page', id=url['id']))

    data['name'] = data_url
    data['created_at'] = datetime.datetime.now().date()
    create_url(data)
    data = get_id_url_by_name(data_url)
    flash('Страница успешно добавлена')
    return redirect(url_for('url_page', id=data['id']))

# @app.post('/')
# def new_url():
#     data = request.form.to_dict()
#     url = urlparse(data['url'])
#     data_url = url.scheme + "://" + url.netloc
#     print(data_url)
#
#     errors = validator.validate(data)
#     if errors:
#         flash(errors['name'])
#         return render_template('index.html', errors=errors), 422
#
#     url_id = Urls(data_url)
#     urls = Urls.query.order_by('created_at').all()
#     for url in urls:
#         if data_url == url.name:
#             flash('Страница уже существует')
#             return redirect(url_for('url_page', id=url.id))
#
#     db.session.add(url_id)
#     db.session.commit()
#     flash('Страница успешно добавлена')
#
#     return redirect(url_for('url_page', id=url_id.id))


# @app.route('/urls')
# def all_urls():
#     return render_template('urls.html', urls=Urls.query.order_by(desc('created_at')).all(),
#                            checks=Url_Checks.query, desc=desc('created_at'), true_date=true_date
#                            )


@app.get('/urls/<id>')
def url_page(id):
    messages = get_flashed_messages()
    url = get_url_by_id(id)
    if not url:
        return render_template('404.html'), 404
    checks = get_url_checks(int(id))
    return render_template('url.html', url=url, checks=checks, messages=messages
                           )


@app.post('/urls/<id>/checks')
def check_url(id):
    data = {}
    data['url_id'] = int(id)
    data['created_at'] = datetime.datetime.now().date()
    url = get_name_url_by_id(int(id))

    check = check_response(url["name"])
    if check["error"]:
        flash('Произошла ошибка при проверке')
    else:
        data.update(check)
        create_check(data)
        flash('Страница успешно проверена')
    return redirect(url_for('url_page', id=data["url_id"]))


if __name__ == "__main__":
    app.run()
