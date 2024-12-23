
from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='Login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_details'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('change_password/', views.change_password, name='change_password'),

]

