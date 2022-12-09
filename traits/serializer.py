from rest_framework import serializers, validators
from .models import Trait

class TraitSerializer(serializers.Serializer):
    id         = serializers.IntegerField(read_only=True)
    name       = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(required=False)
