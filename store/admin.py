from django.contrib import admin
from .models import Product,Collection
class Store_Admin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['product_name'],
    }

    list_display=('product_name','price','modified_at','is_available')
    list_display_links=('product_name','price','modified_at','is_available')


class Collection_Admin(admin.ModelAdmin):
    prepopulated_fields={
        'collection_slug': ['collection'],
    }
admin.site.register(Collection,Collection_Admin)

admin.site.register(Product,Store_Admin)
