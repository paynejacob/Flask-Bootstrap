# -*- coding: utf-8 -*-
""" Helper utilities and decorators. """

import random
from flask import flash


def flash_errors(form, category="warning"):
    """ Flash all errors for a form. """
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)

def generate_token(length=8, alphabet="abcdefghijklmnopqrstuvwxyz0123456789"):
    """ Generate a random token of given length from the specified set of
        characters.  Not guaranteed to be unique.
    """
    return ''.join(random.choice(alphabet) for _ in range(length))
