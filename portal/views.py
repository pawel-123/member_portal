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

    context = {'claim': claim}
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
    # if not product_id:
    #     product_id = 1
    # product_id=1 # somehow this stays when the view is getting generated, so I need to figure out a way for the URL from index.html to override it
    model = Claim
    form_class = NewClaimForm
    template_name = 'portal/new_claim.html'
    # initial={'product': product_id}
    # success_url = 'portal/' # commented it out for now but I'm not sure how to set it if I wanted to redirect elsewhere - by default it redirects according to get_absolute_url of Claim model

    def form_valid(self, form):
        form.instance.member = self.request.user
        return super(NewClaimView, self).form_valid(form)
