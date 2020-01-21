from django.urls import path
from videoJuegos import views

urlpatterns = [
    path('/recomendacion', views.recomendarVideojuegos, name="recomendacion"),
]