from django.urls import path
from . import views 
from .views import SignUpView

app_name = "users"

urlpatterns = [
    path('redirect/', views.login_redirect, name='login_redirect'),
    path('signup/',SignUpView.as_view(), name='signup'),
]