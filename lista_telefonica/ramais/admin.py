from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Setor, Pessoa, Usuario

admin.site.register(Setor)
admin.site.register(Pessoa)
admin.site.register(Usuario)