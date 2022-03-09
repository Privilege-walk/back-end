from django.urls import path
from .apis import SayHello

urlpatterns = [
    path('', SayHello.as_view(), name='hello'),
]