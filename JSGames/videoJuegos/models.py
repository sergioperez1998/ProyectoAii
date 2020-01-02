#encoding:utf-8

from django.db import models

class Genero(models.Model):
    generoId = models.AutoField(primary_key=True)
    nombre = models.TextField(verbose_name='Género', unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class VideoJuego(models.Model):
    idVideoJuegos = models.TextField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre') 
    precio = models.TextField(verbose_name='Precio')
    fechaLanzamiento = models.DateField(verbose_name='Fecha de Lanzamiento', null=True)
    desarrollador=models.TextField(verbose_name = 'Desarrollador')
    urlImg=models.URLField(verbose_name = 'Url de la imagen del producto')
    urlProducto=models.URLField(verbose_name = 'Url producto')
    generos = models.ManyToManyField(Genero)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre','fechaLanzamiento','desarrollador' )



class Consola(models.Model):
    idConsola = models.TextField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre',unique=True) 
    urlImg=models.URLField(verbose_name = 'Url de la imagen')
    descripcion=models.TextField(verbose_name='Descripción del producto') 
    videoJuegos = models.ManyToManyField(VideoJuego)
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )



class Cliente(models.Model):
    idUsuario = models.TextField(primary_key=True)
    edad = models.IntegerField(verbose_name='Edad', help_text='Debe introducir una edad')
    sexo = models.CharField(max_length=1, verbose_name='Sexo', help_text='Debe elegir entre M o F')
    codigoPostal = models.TextField(verbose_name='Código Postal')
    consolas = models.ManyToManyField(Consola)
    videoJuegos = models.ManyToManyField(VideoJuego)
    
    def __str__(self):
        return self.idUsuario
    
    class Meta:
        ordering = ('idUsuario', )
        

