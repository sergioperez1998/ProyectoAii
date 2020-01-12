#encoding:utf-8

from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    generoId = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Género', unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        

class Consola(models.Model):
    idConsola = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre',unique=True) 
    urlImg=models.URLField(verbose_name = 'Url de la imagen')
    descripcion=models.TextField(verbose_name='Descripción del producto') 
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )



        
class VideoJuego(models.Model):
    idVideoJuegos = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre') 
    precio = models.TextField(verbose_name='Precio')
    fechaLanzamiento = models.DateField(verbose_name='Fecha de Lanzamiento', null=True)
    urlImg=models.URLField(verbose_name = 'Url de la imagen del producto')
    urlProducto=models.URLField(verbose_name = 'Url producto')
    generos = models.ManyToManyField(Genero)
    consola=models.ForeignKey(Consola, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre','fechaLanzamiento', )




class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    consolas = models.ManyToManyField(Consola, blank=True)
    videoJuegos = models.ManyToManyField(VideoJuego, blank=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('idCliente', )
        

