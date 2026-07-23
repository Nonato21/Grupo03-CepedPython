from django.db import models
from django.core.validators import RegexValidator

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    
    ramal = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='O ramal deve conter exatamente 4 números.'
            )
        ]
    )

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    setores = models.ManyToManyField(Setor, related_name='pessoas')

    def __str__(self):
        return self.nome