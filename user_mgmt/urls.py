from django.urls import path
from user_mgmt.controllers.main_page_hello_API import SayHello

urlpatterns = [
    path('', SayHello.as_view(), name='hello'),
]