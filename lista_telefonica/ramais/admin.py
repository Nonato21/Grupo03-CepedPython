from django.contrib import admin

# Register your models here.

from .models import Setor, Pessoa

admin.site.register(Setor)
admin.site.register(Pessoa)
