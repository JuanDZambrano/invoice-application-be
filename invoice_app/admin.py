from django.contrib import admin
from .models import (Product,
                     Contact,
                     Sale,
                     Debt,
                     Employee)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]


class SaleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Sale._meta.fields]


class DebtAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Debt._meta.fields]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.fields]


admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Debt, DebtAdmin)
admin.site.register(Employee, EmployeeAdmin)
