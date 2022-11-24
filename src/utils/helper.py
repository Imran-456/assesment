import re
from src.models.db_models import user


def validate_email(email):
    '''
    This function validates the email
    '''

    email_regx = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if email and re.match(email_regx, email) is None:
        return (False, 'Flag1')

    current_user = user.query.filter_by(email=email).one_or_none()
    if current_user is not None:
        return (False, 'Flag2')

    return (True, email)


def validate_title_and_description(title, description):
    '''
    This function validates title and description
    '''

    if title is not None and description is not None:
        return True
    return False


def validate_name(name):
    '''
    This function validates name of the user
    '''
    name_regx = r'\b[A-Za-z]\b'
    if name and not re.match(name_regx, name):
        return False

    return name


def validate_password(password):
    '''
    This function validates password length of user.
    '''
    if len(password) < 8:
        return False

    return password
