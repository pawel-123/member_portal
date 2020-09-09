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

def index(request):
    """The home page for member portal"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'portal/index.html', context)

# @login_required
# def claims(request):
#     """The overview of claims"""
#     claims = Claim.objects.filter(member=request.user).order_by('-date_added')
#     context = {'claims': claims}
#     return render(request, 'portal/claims.html', context)

class ClaimsView(LoginRequiredMixin, SingleTableView):
    table_class = ClaimsTable
    # queryset = Claim.objects.all()
    template_name = "portal/claims.html"

    def get_queryset(self):
        return Claim.objects.filter(member=self.request.user).order_by('-date_added')

class FilteredClaimsView(LoginRequiredMixin, SingleTableMixin, FilterView):
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
    # claim = Claim.objects.get(id=claim_id)
    claim = get_object_or_404(Claim, id=claim_id)
    if claim.member != request.user:
        raise Http404
    attachments = ClaimAttachment.objects.filter(claim__member=request.user, claim__id=claim_id)

    context = {'claim': claim, 'attachments': attachments}
    return render(request, 'portal/claim.html', context)


# @login_required
# def new_claim(request, product_id=1):
#     """Submit a new claim"""
#     if request.method != 'POST':
#         # No data submitted; create a blank form
#         form = ClaimForm(initial={'product': product_id})
#     else:
#         # POST data submitted; process data
#         form = ClaimForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_claim = form.save(commit=False)
#             new_claim.member = request.user
#             form.save()
#             return redirect('portal:claims')

#     # Display a blank or invalid form
#     context = {'form': form}
#     return render(request, 'portal/new_claim.html', context)

# pre-selection of product for homepage links still needs to be implemented
class NewClaimView(LoginRequiredMixin, CreateView):
    model = Claim
    form_class = NewClaimForm
    template_name = 'portal/new_claim.html'

    # commented out as we use "get_absolute_url from the model to redirect to newly created claim detail view"
    # success_url = '/portal/'

    def get(self, request, product_id=None, *args, **kwargs):
        form = self.form_class(initial={'product': product_id})
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.member = self.request.user
        return super(NewClaimView, self).form_valid(form)

from bs4 import BeautifulSoup
import requests
from requests import get

def attachment_download(request):

    domain = "http://localhost:8000"
    page = requests.get("http://localhost:8000/portal/claims/17/")
    html = page.text
    print(html)
    # soup = BeautifulSoup(html, "html.parser")

#     # for link in soup.find_all('a'):
#     #     url = link.get('href')
#     #     print(domain + url)
#     #     with open(url, "wb") as file:
#     #         response = get(domain + url)
#     #         file.write(response.content)

