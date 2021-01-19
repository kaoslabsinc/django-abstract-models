from address.forms import AddressField as WhackAddressFormField
from address.widgets import AddressWidget as WhackAddressWidget


class AddressWidget(WhackAddressWidget):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        if not attrs.get('size'):
            attrs['size'] = 50
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)


class AddressFormField(WhackAddressFormField):
    widget = AddressWidget
