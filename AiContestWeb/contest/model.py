from gettext import gettext

from django.db import models


class Contest(models.Model):
    name = models.CharField(gettext('name'), max_length=150)
    begin = models.DateTimeField(gettext('begin time'))
    end = models.DateTimeField(gettext('end time'))
    description = models.TextField(gettext('description'))
    is_java_available = models.BooleanField(gettext('condition if java language is permitted for contest'),
                                            default=False)
    is_python_available = models.BooleanField(gettext('condition if python language is permitted for contest'),
                                              default=False)
    register_deadline = models.DateTimeField(gettext('deadline to register the contest'))
    build_timeout = models.TimeField(gettext('time out building code'), default='00:05:00')
