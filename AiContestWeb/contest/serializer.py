from rest_framework import serializers
from rest_framework.exceptions import APIException

from AiContestWeb.contest.model import Contest
from AiContestWeb.uaa.serializer import UserSerializer


class ContestSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Contest
        fields = '__all__'

    def create(self, validated_data):
        try:
            contest = Contest(name=validated_data['name'],
                              description=validated_data.get('description', ''),
                              begin=validated_data['begin'],
                              end=validated_data['end'],
                              is_java_available=validated_data.get('is_java_available', False),
                              is_python_available=validated_data.get('is_python_available', False),
                              is_cpp_available=validated_data.get('is_cpp_available', False),
                              register_deadline=validated_data['register_deadline'],
                              build_timeout=validated_data.get('build_timeout', None),
                              creator_id=self.context['request'].user.id)
            contest.save()
            return contest
        except KeyError:
            raise APIException('Missing required field.')
