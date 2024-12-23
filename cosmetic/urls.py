from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include,re_path
from django.conf import settings
from store.views import custom_404_view
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('',include('account.urls')),
    path('',include('products.urls')),
    path('admin-access/',include('adminapp.urls')),
    path('review/',include('review.urls')),
    path('',include('cart.urls')),
    re_path(r'^.*$', custom_404_view),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


