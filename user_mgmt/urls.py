from django.urls import path
from .controllers.main_page_hello_API import SayHello
from .controllers.auth_apis import *

urlpatterns = [
    path('', SayHello.as_view(), name='hello'),
    path('auth/signup/', SignUp.as_view(), name='signup'),
    path('auth/login/', Login.as_view(), name='login'),
]