from django_filters import FilterSet

from .models import Claim


class ClaimFilter(FilterSet):
    class Meta:
        model = Claim
        fields = {
            "product": ["exact"],
            "text": ["contains"],
            "status": ["exact"],
        }
