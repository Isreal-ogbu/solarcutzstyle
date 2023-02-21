from django.contrib.auth.models import User
from rest_framework import serializers

from phoneverificationapp import verify
from phoneverificationapp.models import phonenumbermodel


class userdetailserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class phonelistserializers(serializers.ModelSerializer):
    owner = userdetailserializer()

    class Meta:
        model = phonenumbermodel
        fields = ["phonenumber", "owner", "verifiednumber"]
        read_only_fields = fields


class phoneverificationserializers(serializers.ModelSerializer):
    phonenumber = serializers.CharField(max_length=14, min_length=14, allow_blank=False)

    class Meta:
        model = phonenumbermodel
        fields = ["phonenumber", "verifiednumber"]

    def create(self, validate_data):
        phonenumber = validate_data["phonenumber"]
        user = validate_data["owner"]
        if str(phonenumber)[0] != '+':
            raise serializers.ValidationError("phone line must be 11 and must begin with +234...")
        if len(phonenumber) < 14 or len(phonenumber) > 14:
            raise serializers.ValidationError("Please Enter a valid Phone Number...!")
        try:
            phonenumbermodel.objects.get(phonenumber=phonenumber, verifiednumber=True)
            raise serializers.ValidationError("Already a user...!")
        except phonenumbermodel.DoesNotExist:
            verify.send(phonenumber)
            number = phonenumbermodel.objects.update(owner=user,
                                                     phonenumber=phonenumber) or phonenumbermodel.objects.create(
                owner=user, phonenumber=phonenumber)
            return phonenumbermodel.objects.get(phonenumber=phonenumber, owner=user)


class phonenumbertokenserializers(serializers.ModelSerializer):
    class Meta:
        model = phonenumbermodel
        fields = ["key"]

    def validate(self, attrs):
        key = attrs["key"]
        if str(key).isalpha() or str(key).isalnum():
            raise serializers.ValidationError("Key must be only Numeric/Number")


class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", 'first_name', 'last_name', 'email']


class userprofileserializers(serializers.ModelSerializer):
    owner = Userserializers()

    class Meta:
        model = phonenumbermodel
        fields = ['owner', 'phonenumber']
