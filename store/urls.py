from django.urls import path
from store.views import RegisterView, LoginView, index, cassettes_redirect, cassettes, logout, ProfileView

urlpatterns = [
    path('', index, name='index'),
    path('cassettes/', cassettes_redirect, name='cassettes_redirect'),
    path('cassettes/<int:page>/', cassettes, name='cassettes'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', RegisterView.as_view(), name='registration'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile')
]
