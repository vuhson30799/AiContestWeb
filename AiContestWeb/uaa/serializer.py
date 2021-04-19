from django.db import transaction
from rest_framework import serializers

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
        user_info = UserInfo(
            first_name=validated_data['user_info']['first_name'],
            last_name=validated_data['user_info']['last_name'],
            university=validated_data['user_info']['university'],
            address=validated_data['user_info']['address'],
            phone_number=validated_data['user_info']['phone_number'],
        )
        try:
            user_info.save()
        except ValueError:
            transaction.rollback()

        user = MyUser(
            email=validated_data['email'],
            username=validated_data['username'],
            is_staff=validated_data['is_staff'],
            is_creator=validated_data['is_creator'],
            user_info=user_info
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

    def update(self, instance, validated_data):
        user_info = UserInfo(
            id=instance.myuser.user_info.id,
            first_name=validated_data['user_info']['first_name'],
            last_name=validated_data['user_info']['last_name'],
            university=validated_data['user_info']['university'],
            address=validated_data['user_info']['address'],
            phone_number=validated_data['user_info']['phone_number'],
        )
        instance.set_password(validated_data['password'])
        setattr(instance, 'email', validated_data['email'])
        setattr(instance, 'is_staff', validated_data['is_staff'])
        setattr(instance, 'is_student', validated_data['is_student'])
        setattr(instance, 'is_creator', validated_data['is_creator'])
        user_info.save()
        instance.save()
        return instance
