from django.contrib import admin

from .models import (Bill, Category, Customer, Employee, Job, Location, Order,
                     OrderItem, Payment, Product)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'email', 'job')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'remuneration', 'company')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'company')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'company')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'unit_price',
                    'inventory', 'category', 'company')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'due_date', 'customer',
                    'payment_method', 'company', 'status', 'employee')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'price', 'order', 'product', 'company')


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'due_date', 'amount', 'type', 'company', 'status')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Bill, BillAdmin)
