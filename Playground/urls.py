from django.urls import path
from .views import index_page

urlpatterns = [
    path('home/', index_page, name="homepage"),
]
