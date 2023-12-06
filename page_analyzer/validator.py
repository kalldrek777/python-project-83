from urllib.parse import urlparse
import validators
from validators import ValidationError


def validate(post):
    errors = {}
    if not post.get('url'):
        errors['name'] = "URL обязателен"
        return errors
    # try:
    if validators.url(post.get('url')) is not True:
    # except ValidationError:
        print(2)
        errors['name'] = 'Некорректный URL'

    if len(post.get('url')) > 255:
        errors['name'] = 'Некорректный URL'

    return errors
