from django.urls import path
from user_mgmt.controllers.main_page_hello_API import SayHello
from .controllers.auth_apis import SignUp

urlpatterns = [
    path('', SayHello.as_view(), name='hello'),
    path('auth/signup/', SignUp.as_view(), name='signup'),
]