from django.urls import path

from . import views

from .views import ClaimsView

app_name = 'portal'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # path('claims/', views.claims, name='claims'),
    path('claims/', ClaimsView.as_view(), name='claims'),
    path('claims/<int:claim_id>/', views.claim, name='claim'),
    path('new_claim/<int:product_id>/', views.new_claim, name='new_claim_product'),
    path('new_claim/', views.new_claim, name='new_claim'),
]
