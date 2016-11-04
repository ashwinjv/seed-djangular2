from django.conf.urls import url
from .views import serve_folder_view

urlpatterns = [
    url(r'^(.*)$', serve_folder_view, name='serve_folder'),
]