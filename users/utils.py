import uuid
from datetime import timedelta
from random import randint
from secrets import token_hex, choice

from django.contrib.auth.hashers import make_password
from string import digits

from django.utils.timezone import now


def get_uuid(make_hex=False):
    uid = uuid.uuid4()
    if make_hex:
        return uid.hex
    return uid


def set_lifetime(**kwargs):
    return now() + timedelta(**kwargs)


def build_password_or_otp(password=None):
    # This function will return the hash of a raw password if the password parameter is filled
    # else it will generate an otp

    if not password:
        return ''.join(choice(digits) for i in range(randint(4, 6)))

    return make_password(password, salt=token_hex(16))
