import validators


def validate(post):
    errors = {}
    if not post.get('url'):
        errors['name'] = "URL обязателен"
        return errors

    if validators.url(post.get('url')) is not True:
        errors['name'] = 'Некорректный URL'

    if len(post.get('url')) > 255:
        errors['name'] = 'URL превышает 255 символов'

    return errors
