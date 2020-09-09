from django_filters import FilterSet, DateFilter, CharFilter

from .models import Claim


class ClaimFilter(FilterSet):
    start_date = DateFilter(field_name="date_added", lookup_expr='gte')
    end_date = DateFilter(field_name="date_added", lookup_expr='lte')

    text = CharFilter(field_name='text', lookup_expr='icontains')

    class Meta:
        model = Claim
        fields = {
            "product": ["exact"],
            "status": ["exact"],
        }
