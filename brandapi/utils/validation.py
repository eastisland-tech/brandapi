from collections import defaultdict
from six import string_types


class ValidationError(Exception):
    """
    A custom Exception to pass along
    validation errors.
    """
    def __init__(self, errors):
        self.errors = errors


class Validator(object):
    """
    The following Class provides some basic tools
    for validating json-like data. It includes some
    basic validators to give you an idea of how it
    could be used.

    Please note that this version does not support
    the ability to configure parameters for each
    validator.
    """
    validation_schema = {}
    errors = defaultdict(list)

    def __init__(self, data):
        """
        Constructor sets our data.
        """
        self.data = data

    def validate(self):
        """
        Runs our validation methods.
        """
        self.errors.clear()
        try:
            self._check_required()
        except ValidationError, e:
            ek, ev = e.errors
            self.errors[ek].append(ev)
        self._validate()
        return len(self.errors) == 0

    def _validate(self):
        """
        The primary validation takes place here.

        Iterates over our validation_schema to
        determine what validators to run on what
        data and then runs them.
        """
        errors = self.errors
        for k,v in self.data.items():
            for name, validators in self.validation_schema.items():
                for validator in validators:
                    if name in errors and len(errors[name]) > 0:
                        continue
                    try:
                        getattr(self, 'validate_{0}'.format(validator))(name, v)
                    except ValidationError, e:
                        ek, ev = e.errors
                        errors[ek].append(ev)

    def _check_required(self):
        """
        A pre-validation validator for required data.

        This method catches scenarios where the user
        sent data but it didn't included our required
        ones.
        """
        for name, v in self.validation_schema.items():
            if 'required' in v and name not in self.data:
                raise ValidationError((name, 'data required'))

    def validate_required(self, key, data):
        """
        A validator to ensure that the data was included.
        """
        if not data:
            raise ValidationError((key, 'data required'))

    def validate_is_string(self, key, data):
        """
        A validator to ensure that the data is a string.
        """
        if not isinstance(data, string_types):
            raise ValidationError((key, 'data must be a string'))
