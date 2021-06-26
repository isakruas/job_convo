from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    Usuario
)
from .forms import (
    UsuarioCreateForm
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioCreateForm
    list_display = (
        'id',
        'tipo',
        'email',
    )


admin.site.unregister(Group)
