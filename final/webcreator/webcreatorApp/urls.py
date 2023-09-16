from django.urls import path
from . import views


urlpatterns = [
    path("",views.appindex),
    path('create/',views.create),

]