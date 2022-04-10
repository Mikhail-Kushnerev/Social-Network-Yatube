from multiprocessing import context
import re
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# from .models import Profile
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')


# def picture(request, username):
#     template = 'posts/profile_page.html'
#     pp = Pro.objects.filter(user=request.user).first()
#     context = {
#         'pp': pp
#     }
#     return render(
#         request,
#         template,
#         context
#     )
