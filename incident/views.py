from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from incident.models import Incident
from incident.serializers import IncidentSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с инцидентами."""

    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [
        IsAuthenticated
    ]
    pagination_class = PageNumberPagination

    # Расширение схемы для выбора фильтра
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='status',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Фильтр по статусу инцидента',
                enum=[choice[0] for choice in Incident.IncidentStatus.choices],
            ),
        ]
    )
    def list(self, request):
        queryset = self.get_queryset()
        status_param = self.request.query_params.get('status')
        # Фильтр по статусу
        if status_param:
            queryset = queryset.filter(status=status_param)
        page = self.paginate_queryset(queryset)
        serializer = IncidentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
