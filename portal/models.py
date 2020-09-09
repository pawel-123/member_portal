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
    # attachment = models.FileField(upload_to='claims/', null=True, blank=True)

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

    # improve with reverse and refer to a view name rather than an absolute url?
    def get_absolute_url(self):
        return "/portal/claims/%i/" % self.id

    # Fix claims table row colouring based on claim status (broken after implementing with django-tables2 and django-filter)
    # def get_row_color(self):
    #     """Returns boostrap class for table row color"""
    #     if self.status == 'Submitted':
    #         return "table-light"
    #     elif self.status == 'Denied':
    #         return "table-danger"
    #     elif self.status == 'Approved':
    #         return "table-active"
    #     elif self.status == 'Completed':
    #         return "table-success"

    def __str__(self):
        """Return a string representation of a claim"""
        return f"{self.id} - {self.member} - {self.product}"

class ClaimAttachment(models.Model):
    """A file attached by the member when submitting a Claim"""
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='claims/')
