from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from abstract_models.fields import FullLengthCharField, AddressField
from .utils import generate_field_kwargs

User = get_user_model()


class AbstractModelFactory:
    @staticmethod
    def as_abstract_model(**kwargs):
        raise NotImplementedError


class HasEmailFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(optional=False):
        class HasEmail(models.Model):
            class Meta:
                abstract = True

            email = models.EmailField(blank=optional)

        return HasEmail


class HasOwnerFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(related_name, one_to_one=False, optional=False):
        owner_field_cls = models.OneToOneField if one_to_one else models.ForeignKey

        class HasOwner(models.Model):
            class Meta:
                abstract = True

            owner = owner_field_cls(User, on_delete=models.PROTECT,
                                    related_name=related_name,
                                    **generate_field_kwargs(optional_null=optional))

        return HasOwner


class HasNameFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(optional=False):
        class HasName(models.Model):
            class Meta:
                abstract = True

            name = FullLengthCharField(blank=optional)

            def __str__(self):
                return self.name if self.name else super(HasName, self).__str__()

        return HasName


class HasDescriptionFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(required=False):
        class HasDescription(models.Model):
            class Meta:
                abstract = True

            description = models.TextField(blank=not required)

        return HasDescription


class HasIconFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(upload_to='', required=False):
        class HasIcon(models.Model):
            class Meta:
                abstract = True

            icon = models.ImageField(upload_to=upload_to, blank=not required)

        return HasIcon


class HasCoverPhotoFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(upload_to='', required=False):
        class HasCoverPhoto(models.Model):
            class Meta:
                abstract = True

            cover_photo = models.ImageField(upload_to=upload_to, blank=not required)

        return HasCoverPhoto


class HasAutoCodeFactory(AbstractModelFactory):
    @staticmethod
    def generate_code(instance, auto_code_field, source_field):
        generate_func = getattr(instance, 'generate_' + auto_code_field, None)
        if generate_func:
            return generate_func()
        else:
            return slugify(getattr(instance, source_field))

    @staticmethod
    def as_abstract_model(auto_code_field, source_field=None):
        class HasAutoCode(models.Model):
            class Meta:
                abstract = True

            def clean(self):
                if not getattr(self, auto_code_field, None):
                    code = HasAutoCodeFactory.generate_code(self, auto_code_field, source_field)
                    if type(self)._default_manager.filter(**{auto_code_field: code}).exists():
                        raise ValidationError(
                            f"{type(self)._meta.verbose_name.capitalize()} with this {auto_code_field} already exists")
                    setattr(self, auto_code_field, code)
                super(HasAutoCode, self).clean()

            def save(self, *args, **kwargs):
                if not getattr(self, auto_code_field, None):
                    code = HasAutoCodeFactory.generate_code(self, auto_code_field, source_field)
                    setattr(self, auto_code_field, code)
                super(HasAutoCode, self).save(*args, **kwargs)

        return HasAutoCode


class HasAutoSlugFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(source_field=None):
        class HasAutoSlug(
            HasAutoCodeFactory.as_abstract_model('slug', source_field),
            models.Model
        ):
            class Meta:
                abstract = True

            slug = models.SlugField(max_length=255, unique=True, editable=False)

        return HasAutoSlug


class HasAddressFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(optional=False):
        class HasAddress(models.Model):
            class Meta:
                abstract = True

            address = AddressField(**generate_field_kwargs(optional_null=optional))

        return HasAddress
