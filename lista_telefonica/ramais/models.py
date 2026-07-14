from django.db import models

# Create your models here.

from django.db import models

class Setor(models.Model):
    # O Django já cria o ID (Auto-increment Primary Key) automaticamente!
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    ramal = models.CharField(max_length=10)
    text_alter = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    setores = models.ManyToManyField(Setor, related_name='pessoas')

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    senha = models.CharField(max_length=255)
    status_usuario = models.CharField(max_length=10)
    nivel_acesso = models.CharField(max_length=20)

    def __str__(self):
        return self.nome