import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('SELECT id, name FROM urls ORDER BY id DESC;')
        data = cur.fetchall()
    conn.close()
    return data


def get_url_by_name(name):
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, name, created_at
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_by_id(id):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, name, created_at
                   FROM urls
                   WHERE id = (%s)
                '''
        cur.execute(query, [id])
        data = cur.fetchone()
    conn.close()
    return data


def get_id_url_by_name(name):
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id
                   FROM urls
                   WHERE name = (%s)
        '''
        cur.execute(query, [name])
        data = cur.fetchone()
    conn.close()
    return data


def get_name_url_by_id(id):
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT name
                   FROM urls
                   WHERE id = (%s)
        '''
        cur.execute(query, [id])
        data = cur.fetchone()
    conn.close()
    return data


def get_url_checks(url_id):
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT id, url_id, status_code, h1, title,
                   description, created_at
                   FROM url_checks
                   WHERE url_id = (%s)
                   ORDER BY id DESC;
                '''
        cur.execute(query, [url_id])
        data = cur.fetchall()
    conn.close()
    return data


def get_url_check_last(url_id):
    data = None
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''SELECT status_code, created_at
                   FROM url_checks
                   WHERE url_id = (%s)
                   ORDER BY id DESC;
                '''
        cur.execute(query, [url_id])
        data = cur.fetchone()
    conn.close()
    return data


def create_url(data):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''INSERT INTO urls (name, created_at)
                   VALUES (%s, %s);
                '''
        cur.execute(query, (data['name'], data['created_at']))
        conn.commit()
    conn.close()


def create_check(data):
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = '''INSERT INTO url_checks (url_id, status_code,
                                           h1, title,
                                           description, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s);
                '''
        cur.execute(query, (data['url_id'],
                            data["status_code"],
                            data["h1"],
                            data["title"],
                            data["content"],
                            data['created_at']))
        conn.commit()
    conn.close()
