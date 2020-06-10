from django.urls import path

from . import views

from .views import ClaimsView, FilteredClaimsView, NewClaimView

app_name = 'portal'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # path('claims/', views.claims, name='claims'),
    path('claims/', ClaimsView.as_view(), name='claims'),
    path('filtered_claims/', FilteredClaimsView.as_view(), name='filtered_claims'),
    path('claims/<int:claim_id>/', views.claim, name='claim'),
    path('new_claim/', NewClaimView.as_view(), name='new_claim'),
    path('new_claim/<int:product_id>/', NewClaimView.as_view(), name='new_claim_product'),
]
