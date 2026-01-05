"""
Signals do Django para o app core.
Usado para executar ações automáticas quando eventos ocorrem nos models.
"""

import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Usuario


@receiver(pre_delete, sender=Usuario)
def deletar_foto_usuario(sender, instance, **kwargs):
    """
    Signal que é executado ANTES de deletar um usuário.
    Remove o arquivo de foto do sistema de arquivos se existir.
    """
    if instance.foto:
        # Verificar se o arquivo existe
        if os.path.isfile(instance.foto.path):
            try:
                os.remove(instance.foto.path)
                print(f'Foto removida: {instance.foto.path}')
            except Exception as e:
                print(f'Erro ao remover foto: {e}')


@receiver(pre_save, sender=Usuario)
def deletar_foto_antiga_ao_atualizar(sender, instance, **kwargs):
    """
    Signal que é executado ANTES de salvar/atualizar um usuário.
    Se a foto foi alterada, remove a foto antiga do sistema de arquivos.
    """
    if not instance.pk:
        # Se é um novo registro, não há foto antiga para deletar
        return

    try:
        # Buscar o registro antigo no banco
        usuario_antigo = Usuario.objects.get(pk=instance.pk)

        # Verificar se tinha foto antiga
        if usuario_antigo.foto:
            # Verificar se a foto foi alterada
            if instance.foto != usuario_antigo.foto:
                # A foto foi alterada, deletar a antiga
                if os.path.isfile(usuario_antigo.foto.path):
                    try:
                        os.remove(usuario_antigo.foto.path)
                        print(f'Foto antiga removida: {usuario_antigo.foto.path}')
                    except Exception as e:
                        print(f'Erro ao remover foto antiga: {e}')
    except Usuario.DoesNotExist:
        # Usuário não existe ainda, é uma criação
        pass
