from rest_framework import serializers

from phoneverificationapp.serializers import userdetailserializer
from .models import servicemodel, stylemodel, offermodel, stylistmodel, bookmodels
from drf_extra_fields.fields import HybridImageField


class writeservicemodelserializers(serializers.ModelSerializer):
    service_picture = HybridImageField()

    class Meta:
        model = servicemodel
        fields = ['service_picture', 'service_name']


class readservicemodelserializers(serializers.ModelSerializer):
    service_picture = HybridImageField()

    class Meta:
        model = servicemodel
        fields = ['id', 'service_picture', 'service_name']
        read_only_fields = fields


class writestylemodelserialzers(serializers.ModelSerializer):
    style_picture = HybridImageField()
    service_picture = serializers.SlugRelatedField(slug_field="service_name", queryset=servicemodel.objects.all())

    class Meta:
        model = stylemodel
        fields = "__all__"


class readonlystylemodelserialzers(serializers.ModelSerializer):
    style_picture = HybridImageField()
    # service_picture = readservicemodelserializers() # I can change it anytime

    class Meta:
        model = stylemodel
        fields = ["service_picture", "style_picture", "style_description"]
        read_only_fields = fields


class offermodelserializers(serializers.ModelSerializer):
    offer_picture = HybridImageField()

    class Meta:
        model = offermodel
        fields = ['id', 'offer_picture', 'offer_discription_top', 'offer_discription_button']


class stylistmodelserializers(serializers.ModelSerializer):
    class Meta:
        model = stylistmodel
        fields = "__all__"


class readstylemodelserialzersforbooking(serializers.ModelSerializer):
    style_picture = HybridImageField()

    class Meta:
        model = stylemodel
        fields = ["id", "style_picture", "style_description"]
        read_only_fields = fields


class readbookingserializer(serializers.ModelSerializer):
    user_detail = userdetailserializer()
    service = readservicemodelserializers()
    stylist = stylistmodelserializers()
    style = readstylemodelserialzersforbooking()

    class Meta:
        model = bookmodels
        fields = ["user_detail", 'service', "style", "stylist", 'option', 'service_Time', 'amount', 'additional_info']
        read_only_fields = fields


class writebookserviceserializers(serializers.ModelSerializer):
    class Meta:
        model = bookmodels
        fields = ['service', "style", "stylist", 'option', 'service_Time', 'amount', 'additional_info']
