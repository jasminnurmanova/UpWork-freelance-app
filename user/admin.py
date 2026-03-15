from django.contrib import admin
from .models import User, Bid, Review, Contract

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Review)
admin.site.register(Contract)