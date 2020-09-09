from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Claim, ClaimAttachment
from .forms import NewClaimForm

from django.views.generic.edit import FormView, CreateView

from django_tables2 import SingleTableMixin, SingleTableView
from .tables import ClaimsTable
from django_filters.views import FilterView
from .filters import ClaimFilter

from bs4 import BeautifulSoup
import requests
from requests import get

def index(request):
    """The home page for member portal"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'portal/index.html', context)

class ClaimsView(LoginRequiredMixin, SingleTableView):
    """Shows a list of claims sorted by date_added"""
    table_class = ClaimsTable
    template_name = "portal/claims.html"

    def get_queryset(self):
        return Claim.objects.filter(member=self.request.user).order_by('-date_added')

class FilteredClaimsView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """Shows a list of claims that can be filtered and sorted"""
    table_class = ClaimsTable
    model = Claim
    template_name = "portal/filtered_claims.html"

    filterset_class = ClaimFilter

    table_pagination = {
        "per_page": 3
    }

    def get_queryset(self):
        return Claim.objects.filter(member=self.request.user).order_by('-date_added')

@login_required
def claim(request, claim_id):
    """The claim detail page"""
    claim = get_object_or_404(Claim, id=claim_id)
    if claim.member != request.user:
        raise Http404
    attachments = ClaimAttachment.objects.filter(claim__member=request.user, claim__id=claim_id)

    context = {'claim': claim, 'attachments': attachments}
    return render(request, 'portal/claim.html', context)

class NewClaimView(LoginRequiredMixin, CreateView):
    """Page to submit a new claim"""
    model = Claim
    form_class = NewClaimForm
    template_name = 'portal/new_claim.html'

    def get(self, request, product_id=None, *args, **kwargs):
        # Preselects the Product field in the form if passed via URL
        form = self.form_class(initial={'product': product_id})
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.member = self.request.user
        return super(NewClaimView, self).form_valid(form)

# Need to figure out how to enable downloading all attachments with one click

# def attachment_download(request):

#     domain = "http://localhost:8000"
#     page = requests.get("http://localhost:8000/portal/claims/17/")
#     html = page.text
#     print(html)
#     soup = BeautifulSoup(html, "html.parser")

#     for link in soup.find_all('a'):
#         url = link.get('href')
#         print(domain + url)
#         with open(url, "wb") as file:
#             response = get(domain + url)
#             file.write(response.content)

