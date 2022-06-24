from rest_framework import serializers

from main.models import Player


class DoScrollSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
