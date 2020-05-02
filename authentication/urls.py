from django.urls import path
from .views import signup

urlpatterns = [
    path('accounts/signup/', signup, name="signup")
]
