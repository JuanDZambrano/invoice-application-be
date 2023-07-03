from django.contrib import admin
from .models import (Product, 
                     Contact, 
                     Sale, 
                     Debt, 
                     Employee)

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Sale)
admin.site.register(Debt)
admin.site.register(Employee)
