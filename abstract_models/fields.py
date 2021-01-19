from address.models import AddressField as WhackAddressField
from django.db import models

from abstract_models.utils import AddressFormField


class TwoPlacesDecimalField(models.DecimalField):
    description = "A DecimalField with 2 decimal places"

    def __init__(self, allow_empty=False, *args, **kwargs):
        kwargs['max_digits'] = kwargs.get('max_digits', 10)
        kwargs['decimal_places'] = 2
        self.allow_empty = allow_empty
        if allow_empty:
            kwargs['blank'] = True
            kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_digits']
        del kwargs['decimal_places']
        kwargs['allow_empty'] = self.allow_empty
        if self.allow_empty:
            del kwargs['blank']
            del kwargs['null']
        return name, path, args, kwargs


class MoneyField(TwoPlacesDecimalField):
    description = "An amount of money"


class FullLengthCharField(models.CharField):
    description = "A CharField with 255 max length"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs


class LongCharField(FullLengthCharField):
    description = "A CharField with 100 max length"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)


class MediumCharField(FullLengthCharField):
    description = "A CharField with 50 max length"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50
        super().__init__(*args, **kwargs)


class ShortCharField(FullLengthCharField):
    description = "A CharField with 50 max length"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 25
        super().__init__(*args, **kwargs)


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class ToLowerCaseFieldMixin:
    def to_python(self, value):
        return super(ToLowerCaseFieldMixin, self).to_python(value).lower()


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass


class CICharFieldLowerCase(ToLowerCaseFieldMixin, CICharField):
    pass


class AddressField(WhackAddressField):
    def formfield(self, **kwargs):
        defaults = dict(form_class=AddressFormField)
        defaults.update(kwargs)
        return super().formfield(**defaults)
