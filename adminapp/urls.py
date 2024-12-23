
# from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from store.views import custom_404_view

urlpatterns = [
    path('add_collection/',views.add_collection,name='add_collection'),
    path('dashboard/',views.dashboard,name='dashboard' ),
    path('add_item/',views.add_item,name='add_item'),
    path('catalog/',views.catalog,name='catalog'),
    path('delete_product/<int:id>/',views.remove_product,name='remove_product'),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
    path('users/',views.user_list,name='user_list'),
    path('suspend_user/<int:id>/',views.suspended_user,name='suspend_user'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('active_user/<int:id>/',views.active_user,name='active_user'),
    path('show_collection/',views.show_collection,name='show_collection'),
    path('delete_collection/<int:id>',views.delete_collection,name='delete_collection'),
    path('edit_collection/<int:id>',views.edit_collection,name='edit_collection'),
    path('completed_orders/',views.completed_orders,name="completed_orders"),
    path('pending_orders/',views.pending_orders,name="pending_orders"),
    path('accept_product_order/<order_product_id>/',views.accept_product_order,name='accept_product_order'),

    path('cancel_product_order/<order_product_id>/',views.cancel_product_order,name='cancel_product_order'),
    re_path(r'^.*$', custom_404_view),


]
