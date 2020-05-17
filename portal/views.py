from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Product, Claim
from .forms import ClaimForm

def index(request):
    """The home page for member portal"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'portal/index.html', context)

@login_required
def claims(request):
    """The overview of claims"""
    # claims = Claim.objects.all()
    claims = Claim.objects.filter(member=request.user).order_by('-date_added')
    context = {'claims': claims}
    return render(request, 'portal/claims.html', context)

@login_required
def claim(request, claim_id):
    """The claim detail page"""
    # claim = Claim.objects.get(id=claim_id)
    claim = get_object_or_404(Claim, id=claim_id)
    if claim.member != request.user:
        raise Http404

    context = {'claim': claim}
    return render(request, 'portal/claim.html', context)

@login_required
def new_claim(request, product_id=1):
    """Submit a new claim"""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = ClaimForm(initial={'product': product_id})
    else:
        # POST data submitted; process data
        form = ClaimForm(data=request.POST)
        if form.is_valid():
            new_claim = form.save(commit=False)
            new_claim.member = request.user
            form.save()
            return redirect('portal:claims')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'portal/new_claim.html', context)
