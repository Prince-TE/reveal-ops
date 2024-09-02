from django.urls import path
from reveal_app.views import ping_view
from reveal_app.views import login_view,set_password_view

urlpatterns = [
    path('ping/',ping_view,name='ping'),
    
    #login and set-password
    path('login/',login_view,name='login'),
    path('set-password/',set_password_view,name='set-password'),
]