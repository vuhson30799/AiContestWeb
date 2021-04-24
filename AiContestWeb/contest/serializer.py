from rest_framework import serializers

from AiContestWeb.contest.model import Contest


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

