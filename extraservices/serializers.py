from rest_framework import serializers

from extraservices.models import idea_suggestionmodel


class ideaserializers(serializers.ModelSerializer):
    class Meta:
        model = idea_suggestionmodel
        fields = ["idea_suggestion"]


class contactserializers(serializers.ModelSerializer):
    class Meta:
        model = idea_suggestionmodel
        fields = ["contact_problem"]
