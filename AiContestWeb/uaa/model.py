from gettext import gettext

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class UserInfo(models.Model):
    first_name = models.CharField(gettext('first name'), max_length=150, blank=True)
    last_name = models.CharField(gettext('last name'), max_length=150, blank=True)
    university = models.CharField(gettext('university'), max_length=150, blank=True)
    address = models.CharField(gettext('address'), max_length=150, blank=True)
    phone_number = models.CharField(
        max_length=10,
        null=True,
        validators=[RegexValidator(r'(84|0[3|5|7|8|9])+([0-9]{8})$')]
    )


class MyUser(User):
    is_creator = models.BooleanField(
        gettext('is creator'),
        default=False,
        help_text=gettext('Designates whether the user can log into this creator site.'),
    )
    is_student = models.BooleanField(
        gettext('is student'),
        default=False,
        help_text=gettext('Designates whether the user can log into this student site.'),
    )
    user_info = models.ForeignKey(UserInfo, related_name="user_info", on_delete=models.CASCADE)
