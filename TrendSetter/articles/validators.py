from django.core.exceptions import ValidationError


def image_size_validator(value):
    if value.size> 10 * 1024 * 1024:
        raise ValidationError('File size should be less than 10 MB!')