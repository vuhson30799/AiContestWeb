from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException

from AiContestWeb.uaa.model import MyUser, UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(many=False)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'is_staff', 'password', 'is_student', 'is_creator', 'user_info']

    def create(self, validated_data):
        user_info_validated_data = validated_data.get('user_info', None)
        if user_info_validated_data:
            user_info = UserInfo(
                    first_name=user_info_validated_data.get('first_name', ''),
                    last_name=user_info_validated_data.get('last_name', ''),
                    university=user_info_validated_data.get('university', ''),
                    address=user_info_validated_data.get('address', ''),
                    phone_number=user_info_validated_data.get('phone_number', ''),
                )
            try:
                user_info.save()
            except ValueError:
                transaction.rollback()
        else:
            raise APIException("user info is needed.")

        try:
            user = MyUser(
                email=validated_data.get('email', ''),
                is_staff=validated_data.get('is_staff', False),
                is_creator=validated_data.get('is_creator', False),
                is_student=validated_data.get('is_student', False),
                username=validated_data['username'],
                user_info=user_info,
            )
            user.set_password(validated_data['password'])

            user.save()
            return user
        except KeyError:
            raise APIException("username need to be defined.")

    def update(self, instance, validated_data):
        user_info_validated_data = validated_data.get('user_info', None)
        if user_info_validated_data:
            user_info = UserInfo(
                id=instance.user_info.id,
                first_name=user_info_validated_data.get('first_name', ''),
                last_name=user_info_validated_data.get('last_name', ''),
                university=user_info_validated_data.get('university', ''),
                address=user_info_validated_data.get('address', ''),
                phone_number=user_info_validated_data.get('phone_number', ''),
            )
            instance.set_password(validated_data['password'])
            setattr(instance, 'email', validated_data.get('email', ''))
            setattr(instance, 'is_staff', validated_data.get('is_staff', False))
            setattr(instance, 'is_student', validated_data.get('is_student', False))
            setattr(instance, 'is_creator', validated_data.get('is_creator', False))
            user_info.save()
            instance.save()
            return instance
        else:
            raise APIException("user info is needed.")
