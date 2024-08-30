from django.urls import path
from reveal_app.views import ping_view
urlpatterns = [
    path('ping/',ping_view,name='ping'),
]