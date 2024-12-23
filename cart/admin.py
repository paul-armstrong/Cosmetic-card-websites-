from django.contrib import admin
from .models import Cart,Cartitem
from .models import Order,Order_Product,Payment,Personalization

# Register your models here.
class OrderProductInline(admin.TabularInline):
    model=Order_Product
    extra=0
    readonly_fields=('payment','user','product','quantity','product_price','is_ordered')

class cartadmin(admin.ModelAdmin):
    list_display=('cart_id','dated_added')



class cartitemAadmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')

class orderAadmin(admin.ModelAdmin):
   
   list_display=('order_number','full_name','phone','email','city','total','tax','status','is_ordered','created_at')
   list_filter=('status','is_ordered')
   search_fields=('order_number','first_name','last_name','phone','email')
   list_per_page=20
   inlines=[OrderProductInline]

admin.site.register(Cart,cartadmin)
admin.site.register(Cartitem,cartitemAadmin)
admin.site.register(Order,orderAadmin)

admin.site.register([Payment,Order_Product])
admin.site.register(Personalization)