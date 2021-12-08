from django.urls import path
from . import views, user

urlpatterns = [
    path('user/', user.ApiUser.urls)
]
