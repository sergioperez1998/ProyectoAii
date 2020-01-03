from django.contrib import admin
from videoJuegos.models import Genero, VideoJuego, Consola, Cliente

# Register your models here.
admin.site.register(Genero)
admin.site.register(VideoJuego)
admin.site.register(Consola)
admin.site.register(Cliente)
