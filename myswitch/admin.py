from django.contrib import admin

from myswitch.models import Rate
from myswitch.models import Transaction

# Register model
admin.site.register(Rate)
admin.site.register(Transaction)
