from flask import Flask, redirect, render_template, request, url_for, flash
import os
from validator import validate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name


@app.get('/')
def index():
    url = []
    errors = []
    return render_template('index.html', url=url, errors=errors)


@app.post('/')
def new_url():
    data = request.form.to_dict()
    print(data)

    errors = validate(data)
    if errors:
        return render_template('index.html', errors=errors), 422

    db.session.add(Urls(data['url']))
    db.session.commit()
    flash('Success')

    return redirect(url_for('index'))


@app.route('/urls')
def all_urls():
    return render_template('urls.html', urls=Urls.query.all().order_by('created_at'))


@app.route('/url/<id>')
def url_page(id):
    return render_template('url.html', url=Urls.query.filter_by(id=id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()