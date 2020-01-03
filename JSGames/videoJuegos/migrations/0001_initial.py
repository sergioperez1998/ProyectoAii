# Generated by Django 2.2.5 on 2020-01-03 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consola',
            fields=[
                ('idConsola', models.TextField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True, verbose_name='Nombre')),
                ('urlImg', models.URLField(verbose_name='Url de la imagen')),
                ('descripcion', models.TextField(verbose_name='Descripción del producto')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('generoId', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True, verbose_name='Género')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='VideoJuego',
            fields=[
                ('idVideoJuegos', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('precio', models.TextField(verbose_name='Precio')),
                ('fechaLanzamiento', models.DateField(null=True, verbose_name='Fecha de Lanzamiento')),
                ('urlImg', models.URLField(verbose_name='Url de la imagen del producto')),
                ('urlProducto', models.URLField(verbose_name='Url producto')),
                ('consola', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videoJuegos.Consola')),
                ('generos', models.ManyToManyField(to='videoJuegos.Genero')),
            ],
            options={
                'ordering': ('nombre', 'fechaLanzamiento'),
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idUsuario', models.TextField(primary_key=True, serialize=False)),
                ('edad', models.IntegerField(help_text='Debe introducir una edad', verbose_name='Edad')),
                ('sexo', models.CharField(help_text='Debe elegir entre M o F', max_length=1, verbose_name='Sexo')),
                ('codigoPostal', models.TextField(verbose_name='Código Postal')),
                ('consolas', models.ManyToManyField(to='videoJuegos.Consola')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videoJuegos', models.ManyToManyField(to='videoJuegos.VideoJuego')),
            ],
            options={
                'ordering': ('idUsuario',),
            },
        ),
    ]
