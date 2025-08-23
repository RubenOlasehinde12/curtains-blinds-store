from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

def login_redirect(request):
    if request.user.is_staff:
        return redirect('store:manager_menu')   # managers → manager dashboard
    return redirect('store:product_list')       # customers → product list   