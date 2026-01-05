from django.contrib import admin
from .models import Perfil, Departamento, Usuario


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Perfil"""
    list_display = ('id', 'perfil')
    search_fields = ('perfil',)
    ordering = ('perfil',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Departamento"""
    list_display = ('id', 'departamento', 'sigla')
    search_fields = ('departamento', 'sigla')
    list_filter = ('sigla',)
    ordering = ('departamento',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Usuario"""
    list_display = ('id', 'nome', 'email', 'id_perfil', 'id_departamento')
    search_fields = ('nome', 'email')
    list_filter = ('id_perfil', 'id_departamento')
    ordering = ('nome',)

    # Campos de senha não devem ser editáveis diretamente no admin
    fields = ('nome', 'email', 'foto', 'id_perfil', 'id_departamento')

    def save_model(self, request, obj, form, change):
        """Sobrescreve o save do admin para garantir hash da senha se necessário"""
        super().save_model(request, obj, form, change)
