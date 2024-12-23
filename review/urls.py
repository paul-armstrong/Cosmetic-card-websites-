from django.urls import path,re_path
from store.views import custom_404_view

from review import views
urlpatterns=[
   path('add_review/',views.add_review,name="add_review"),
   re_path(r'^.*$', custom_404_view),


    ]
