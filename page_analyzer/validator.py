def validate(post):
    errors = {}
    if not post.get('url'):
        errors['name'] = "URL обязателен"
    return errors