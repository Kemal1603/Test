from rest_framework import serializers

from main.models import SeoResult


class SeoResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoResult
        fields = '__all__'
        read_only_fields = ('id',)
