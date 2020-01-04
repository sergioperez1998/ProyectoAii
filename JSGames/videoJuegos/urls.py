from django.urls import path
from videoJuegos import views

urlpatterns = [
    
    path('showClient/', views.client_show),
    path('createClient/',views.client_form),

]