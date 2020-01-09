# Generated by Django 2.2.5 on 2020-01-09 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consola',
            fields=[
                ('idConsola', models.AutoField(primary_key=True, serialize=False)),
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
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('password', models.CharField(max_length=30, verbose_name='Contraseña')),
                ('edad', models.IntegerField(help_text='Debe introducir una edad', verbose_name='Edad')),
                ('sexo', models.CharField(help_text='Debe elegir entre M o F', max_length=1, verbose_name='Sexo')),
                ('codigoPostal', models.CharField(max_length=5, verbose_name='Código Postal')),
                ('consolas', models.ManyToManyField(blank=True, to='videoJuegos.Consola')),
                ('videoJuegos', models.ManyToManyField(blank=True, to='videoJuegos.VideoJuego')),
            ],
            options={
                'ordering': ('idUsuario',),
            },
        ),
    ]
