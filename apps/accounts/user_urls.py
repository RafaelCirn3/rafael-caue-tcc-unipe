from django.urls import path
from .views import UserMeView

urlpatterns = [
    path('me/', UserMeView.as_view(), name='users_me'),
]
