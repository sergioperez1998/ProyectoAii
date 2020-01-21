"""JSGames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from videoJuegos import views
from django.contrib.auth.views import LoginView, LogoutView
from videoJuegos.views import agregarJuego, showVideoJuegosDelCliente,\
    eliminarJuego, mostrar_videoJuegos_genero

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('videoJuegos/',views.index, name="inicio"),
    path('ingresar/', views.ingresar),
    path('populate/', views.populateDatabase),
    path('videoJuegos/', include("videoJuegos.urls")),
    path('login/', LoginView.as_view(), name="login_url"),
    path('register/', views.registerView, name="register_url"),
    path('videoJuegos/showConsolasDelCliente/', views.showConsolasCliente, name="showConsolasDelCliente_url"),
    path('videoJuegos/showVideoJuegosDelCliente/<nombre>/',showVideoJuegosDelCliente, name="juegosDelCLiente_url"),
    path('videoJuegos/showVideoGames/', views.showVideoJuegosCliente, name="showGames_url"),
    path('videoJuegos/showVideoGames/agregarJuego/<idVideoJuegos>/',agregarJuego, name="agregarJuego_url"),
    path('videoJuegos/showVideoGames/eliminarJuego/<idVideoJuegos>/',eliminarJuego, name="eliminarJuego_url"),
    path('showUser/',views.showUser, name="show_data_url"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('',views.startPage, name="startPage"),
    path('videoJuegos/mostrarVideoJuegosDelCliente2/',mostrar_videoJuegos_genero),
    
    

]
