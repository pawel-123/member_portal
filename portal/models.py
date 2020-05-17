from django.db import models
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

class Product(models.Model):
    """A product that offers access to a range of services"""
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of policy"""
        return self.name

class Policy(models.Model):
    """A policy in the name of a member with products attached to it"""
    date_added = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    coverage_start = models.DateField(default=date.today)

    policy_delta = relativedelta(years=1)
    start_plus_delta = date.today() + policy_delta

    coverage_end = models.DateField(default=start_plus_delta)

    # consider more sophisticated version for dates later, i.e.
        # add timezone field and awareness to a policy
        # default should start from tomorrow

    class Meta:
        verbose_name_plural = 'policies'

    def __str__(self):
        """Return a string representation of policy"""
        return str(self.pk)

class Claim(models.Model):
    """A claim submitted by a member for an active policy"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    # Claim status choices
    SUBMITTED = 'Submitted'
    DENIED = 'Denied'
    APPROVED = 'Approved'
    COMPLETED = 'Completed'

    CLAIM_STATUS_CHOICES = [
        (SUBMITTED, 'Claim Submitted'),
        (DENIED, 'Claim Denied'),
        (APPROVED, 'Claim Approved'),
        (COMPLETED, 'Claim Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=CLAIM_STATUS_CHOICES,
        default=SUBMITTED,
    )

    def __str__(self):
        """Return a string representation of a claim"""
        return f"{self.id} - {self.member} - {self.product}"

