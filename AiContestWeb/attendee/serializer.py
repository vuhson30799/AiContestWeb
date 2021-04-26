from datetime import datetime

import pytz
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException

from AiContestWeb.attendee.model import Attendee
from AiContestWeb.contest.model import Contest
from AiContestWeb.uaa.serializer import UserSerializer


class AttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    contest = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Attendee
        fields = ['contest', 'user']

    def create(self, validated_data):
        contest_id = self.context['view'].kwargs['contest_id']
        attendee = Attendee(
            user_id=self.context['request'].user.id,
            contest_id=contest_id
        )
        contest = Contest.objects.get(id=contest_id)

        if pytz.utc.localize(datetime.now()) <= contest.register_deadline:
            attendee.register = pytz.utc.localize(datetime.now())
        else:
            raise APIException(detail="The register is overdue.")
        try:
            attendee.save()
        except IntegrityError:
            raise APIException(detail="This user has been already registered")
        return attendee



