import datetime
import os
import sqlalchemy.schema
from sqlalchemy import desc
from flask import Flask, redirect, render_template, request, url_for, flash, abort
# from validator import validate
from . import validator
from flask_sqlalchemy import SQLAlchemy
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.secret_key = '_pf3or4r^x0*tvss9ihp)=bff4(dnixz!0$cc7o=)gc-4pj1w$'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://amethyst:b1FUh1N6F8osqDDzpIIugRqbKu8vC0Jg@dpg-cldpq9tlo5ps73f2p4pg-a.oregon-postgres.render.com/database_0p5m"
TIMEOUT = int(os.getenv('EXTERNAL_REQUEST_TIMEOUT', 30))
db = SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, name):
        self.name = name


def true_date(time):
    return str(time)[0:10]


class Url_Checks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    h1 = db.Column(db.String(255), unique=False)
    title = db.Column(db.String(255), nullable=True, unique=False)
    description = db.Column(db.String(255), nullable=True, unique=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, url_id, status_code, h1, title, description):
        self.url_id = url_id
        self.status_code = status_code
        self.h1 = h1
        self.title = title
        self.description = description


# with app.app_context():
    # db.drop_all()
    # sqlalchemy.schema.DropSchema(Url_Checks, cascade=True)
    # sqlalchemy.schema.DropSchema(Urls, cascade=)
    # db.create_all()


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/')
def new_url():
    data = request.form.to_dict()
    url = urlparse(data['url'])
    data_url = url.scheme + "://" + url.netloc
    print(data_url)

    errors = validator.validate(data)
    if errors:
        flash(errors['name'])
        return render_template('index.html', errors=errors), 422

    url_id = Urls(data_url)
    urls = Urls.query.order_by('created_at').all()
    for url in urls:
        if data_url == url.name:
            flash('Страница успешно добавлена')
            return redirect(url_for('url_page', id=url.id))

    db.session.add(url_id)
    db.session.commit()
    flash('Страница успешно добавлена')

    return redirect(url_for('url_page', id=url_id.id))


@app.route('/urls')
def all_urls():
    return render_template('urls.html', urls=Urls.query.order_by(desc('created_at')).all(),
                           checks=Url_Checks.query, desc=desc('created_at'), true_date=true_date
                           )


@app.route('/url/<id>')
def url_page(id):
    url = Urls.query.get(id)
    if not url:
        abort(404)
    checks_user = Url_Checks.query.filter_by(url_id=url.id).order_by(desc('created_at')).all()
    return render_template('url.html', url=Urls.query.get(id), checks_user=checks_user,
                           true_date=true_date
                           )


@app.post('/urls/<id>/checks')
def check_url(id):
    url = Urls.query.get(id)
    print(url.name)
    # print(requests.get(url.name).status_code)
    try:
        response = requests.get(url.name, timeout=TIMEOUT)
        print(response.status_code)
        response.raise_for_status()
    except:
        flash('Произошла ошибка при проверке')
        return redirect(url_for('url_page', id=id))

    soup = BeautifulSoup(response.text, 'html.parser')
    tags = {'h1': '', 'title': '', 'content': ''}

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

    checks = Url_Checks(url_id=id, status_code=response.status_code, h1=tags['h1'], title=tags['title'],
                        description=tags['content'])
    db.session.add(checks)
    db.session.commit()
    checks_user = Url_Checks.query.filter_by(url_id=url.id).order_by(desc('created_at')).all()

    flash('Страница успешно проверена')
    return render_template('url.html', url=url, checks_user=checks_user, true_date=true_date)


if __name__ == "__main__":
    app.run()
