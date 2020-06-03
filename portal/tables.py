import django_tables2 as tables
from .models import Claim

class ClaimsTable(tables.Table):

    id = tables.Column(verbose_name="Claim ID")
    member = tables.Column()
    product = tables.Column()
    date_added = tables.Column(verbose_name="Submission Date")
    status = tables.Column(verbose_name="Claim Status")
    text = tables.Column(verbose_name="Message", linkify=True)
    link = tables.TemplateColumn(template_name='portal/claims_link_column.html')

    class Meta:
        template_name = "django_tables2/bootstrap4.html"

    def render_text(self, value):
        return str(value[:30] + "...")
