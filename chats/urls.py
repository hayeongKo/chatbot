from django.urls import path
from .views import *

urlpatterns = [
    path('', openai_chat, name='openai_chat'),
    path('hello', print_hello)
]