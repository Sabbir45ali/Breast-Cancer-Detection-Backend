from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )

class UppercaseLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter.")

class LowercaseLetterValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 lowercase letter.")

class DigitValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 digit."),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 digit.")

class SymbolValidator:
    def validate(self, password, user=None):
        if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?" for char in password):
            raise ValidationError(
                _("This password must contain at least 1 symbol."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 symbol.")