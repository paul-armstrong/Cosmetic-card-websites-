from . import views

from django.urls import path
urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payement,name='payements'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>',views.remove_cart_item,name='remove_cart_item'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',views.remove_item,name='remove_item'),


]
