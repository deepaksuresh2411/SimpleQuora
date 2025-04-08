from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from apps.users.forms import SignUpForm

class LandingPageView(TemplateView):
    
    template_name = "landing.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("questions-list-view"))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["signup_form"] = SignUpForm()
        context["signin_form"] = AuthenticationForm()
        return context

class SignUpView(View):
    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('questions-list-view')

        return render(request, 'landing.html', {
            'signup_form': signup_form,
            'signin_form': AuthenticationForm(),
            'show_signup': True,
        })


class SignInView(View):
    def post(self, request, *args, **kwargs):
        signin_form = AuthenticationForm(request, request.POST)
        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
            return redirect('questions-list-view')

        return render(request, 'landing.html', {
            'signin_form': signin_form,
            'signup_form': SignUpForm(),
            'show_signup': False,
        })

class SignOutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")