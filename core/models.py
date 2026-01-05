import os
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


def usuario_foto_path(instance, filename):
    """
    Gera um nome único para o arquivo de foto do usuário.
    Formato: usuarios/fotos/<uuid>_<nome_original>
    Isso garante que nunca haverá conflito de nomes de arquivo.
    """
    # Obter a extensão do arquivo original
    ext = os.path.splitext(filename)[1]
    # Gerar nome único usando UUID
    novo_nome = f"{uuid.uuid4()}{ext}"
    return os.path.join('usuarios', 'fotos', novo_nome)


class Perfil(models.Model):
    """
    Modelo que representa os perfis de acesso dos usuários no sistema.
    Exemplo: Gerente, Funcionário
    """
    perfil = models.CharField(
        max_length=300,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Perfil'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        db_table = 'perfil'

    def __str__(self):
        return self.perfil


class Departamento(models.Model):
    """
    Modelo que representa os departamentos da empresa Lumon.
    Exemplo: Refinamento de Macrodados (MDR), Bem Estar (Wellness)
    """
    departamento = models.CharField(
        max_length=300,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Departamento'
    )
    sigla = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Sigla'
    )

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        db_table = 'departamento'

    def __str__(self):
        return f"{self.departamento} ({self.sigla})" if self.sigla else self.departamento


class Usuario(models.Model):
    """
    Modelo que representa os usuários/funcionários do sistema Lumon.
    Inclui autenticação personalizada (sem usar django.contrib.auth.User).
    """
    nome = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Nome Completo'
    )
    email = models.EmailField(
        max_length=300,
        unique=True,
        null=False,
        blank=False,
        verbose_name='E-mail'
    )
    senha = models.CharField(
        max_length=128,  # Hash da senha será armazenado aqui
        null=False,
        blank=False,
        verbose_name='Senha'
    )
    foto = models.ImageField(
        upload_to=usuario_foto_path,
        null=True,
        blank=True,
        verbose_name='Foto'
    )
    id_perfil = models.ForeignKey(
        Perfil,
        on_delete=models.RESTRICT,  # Não permite excluir perfil se houver usuários vinculados
        db_column='id_perfil',
        verbose_name='Perfil'
    )
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.RESTRICT,  # Não permite excluir departamento se houver usuários vinculados
        db_column='id_departamento',
        verbose_name='Departamento'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nome} ({self.email})"

    def set_senha(self, senha_texto):
        """
        Método para criptografar e salvar a senha.
        Uso: usuario.set_senha('1234')
        """
        self.senha = make_password(senha_texto)

    def verificar_senha(self, senha_texto):
        """
        Método para verificar se a senha está correta.
        Uso: if usuario.verificar_senha('1234'):
        Retorna: True se a senha estiver correta, False caso contrário
        """
        return check_password(senha_texto, self.senha)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a senha seja sempre hasheada.
        Se a senha não começar com 'pbkdf2_sha256$', significa que é uma senha em texto puro
        e precisa ser hasheada.
        """
        # Verificar se a senha precisa ser hasheada (não começa com o prefixo do algoritmo)
        if self.senha and not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
