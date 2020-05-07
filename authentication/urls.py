from django.urls import path
from .views import signup, logout

urlpatterns = [
    path('accounts/signup/', signup, name="signup"),
    path('accounts/logout/', logout, name="logout")
]
