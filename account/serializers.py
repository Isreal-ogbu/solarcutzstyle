import re
from abc import ABC
from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import userdetails
from phoneverificationapp.serializers import userdetailserializer


class profilepictureserializers(serializers.ModelSerializer):
    class Meta:
        model = userdetails
        fields = ["userprofilepicture"]


class userRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, allow_blank=False)
    password = serializers.CharField(max_length=50, allow_blank=False)
    confirm_password = serializers.CharField(max_length=50, allow_blank=False)

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password"]
        read_only_fields = fields
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']

        # password validations
        if password != confirm_password:
            raise serializers.ValidationError('Password and Confirm Password are not matched....!')
        if len(password) < 8:
            raise serializers.ValidationError('Password Must be atleast 8 characters....!')
        if re.search('[0-9]', password) is None:
            raise serializers.ValidationError("Make sure your password has a number in it")
        if re.search('[A-Z]', password) is None:
            raise serializers.ValidationError("Make sure your password has a capital letter in it")
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError("Already used this username...!")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            user1 = userdetails.objects.create(owner=user)
            return user


class logindetailsserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class userdetailsserializers(serializers.ModelSerializer):
    owner = userdetailserializer()

    class Meta:
        model = userdetails
        fields = ['owner', 'userprofilepicture']
        read_only_fields = fields