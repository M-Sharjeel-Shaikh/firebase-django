from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    # Here we are assigning the path of our firebase authentication
    path('signin/', signIn),
    path('postsignIn/', postsignIn),
    path('signUp/', signUp, name="signup"),
    path('logout/', logout, name="log"),
    path('postsignUp/', postsignUp),
]