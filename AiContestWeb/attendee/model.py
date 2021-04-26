from gettext import gettext

from django.db import models

from AiContestWeb.contest.model import Contest
from AiContestWeb.uaa.model import MyUser


class Attendee(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="contest")
    register = models.DateTimeField(gettext('deadline to register the contest'))
    result = models.FloatField(gettext('result for contest'), null=True)

    class Meta:
        unique_together = ('user', 'contest',)

