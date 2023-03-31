from django.urls import path, include
from users.views import Register, MyLoginView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('auth/', MyLoginView.as_view(), name='auth')
]