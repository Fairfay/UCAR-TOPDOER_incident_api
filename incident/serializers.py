from rest_framework import serializers

from server.settings import DATETIME_FORMAT
from incident.models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    """Сериализатор для инцидента"""

    created_at = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
