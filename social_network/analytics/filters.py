from django_filters import rest_framework as filters
from api.models import Reaction


class PostFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Reaction
        fields = ['user', 'created_at']
