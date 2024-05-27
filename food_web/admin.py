from django.contrib import admin
from .models import Product, Cart, Person, Feedback, Store, Order, OrderHistory

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' , 'price' , 'cat' , 'P_details' , 'is_active']
    list_filter = ['cat' , 'is_active']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id' , 'pid' , 'user_id' , 'Qty']

class PersonAdmin(admin.ModelAdmin):
    list_display = ['user_id' , 'mobile']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' , 'mobile' , 'email' , 'submitted_at']

class StoreAdmin(admin.ModelAdmin):
    list_display = ['name' , 'address']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id' , 'pid' , 'qty' , 'user_id' , 'amount']

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['order_id' , 'pid' , 'qty' , 'user_id' , 'amount' , 'total_amount']

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)