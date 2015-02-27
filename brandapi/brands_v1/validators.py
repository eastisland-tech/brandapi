from six import string_types
from collections import defaultdict

from ..utils import mongodb
from ..utils.validation import Validator


class UpdateBrandValidator(Validator):
    """
    Validation for updating Brands
    """
    validation_schema = {
        'brand_name': ['required', 'is_string'],
    }


class CreateBrandValidator(UpdateBrandValidator):
    """
    Validation for creating Brands
    """
    pass
