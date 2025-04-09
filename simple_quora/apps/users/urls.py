from django.urls import path

from apps.users.views import (
    LandingPageView,
    SignUpView,
    SignInView,
    SignOutView
)

urlpatterns = [
    path("",  LandingPageView.as_view(), name="landing-page"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", SignOutView.as_view(), name="logout"),
]
