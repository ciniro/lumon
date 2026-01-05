"""
Management command para carregar fotos dos usuários.
Uso: python manage.py load_user_photos
"""

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Usuario


class Command(BaseCommand):
    help = 'Carrega as fotos dos usuários da pasta static/img/users_photos para o banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando carregamento de fotos...'))

        # Mapeamento: primeiro nome (lowercase) -> nome completo do usuário
        nome_map = {
            'mark': 'Mark Scout',
            'helly': 'Helly Riggs',
            'irving': 'Irving Bailiff',
            'dylan': 'Dylan George',
            'mscasey': 'Ms. Casey',
            'burt': 'Burt Goodman',
        }

        # Pasta de origem das fotos
        source_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'users_photos')

        # Criar pasta de destino se não existir
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'usuarios', 'fotos')
        os.makedirs(dest_dir, exist_ok=True)

        # Verificar se a pasta de origem existe
        if not os.path.exists(source_dir):
            self.stdout.write(self.style.ERROR(f'Pasta não encontrada: {source_dir}'))
            return

        # Processar cada foto
        for filename in os.listdir(source_dir):
            if filename.endswith('.png'):
                # Extrair o primeiro nome do arquivo (sem extensão)
                primeiro_nome = filename.replace('.png', '').lower()

                # Verificar se temos mapeamento para este nome
                if primeiro_nome in nome_map:
                    nome_completo = nome_map[primeiro_nome]

                    try:
                        # Buscar o usuário no banco
                        usuario = Usuario.objects.get(nome=nome_completo)

                        # Copiar arquivo para a pasta media
                        source_file = os.path.join(source_dir, filename)
                        dest_file = os.path.join(dest_dir, filename)
                        shutil.copy2(source_file, dest_file)

                        # Atualizar o campo foto do usuário
                        usuario.foto = f'usuarios/fotos/{filename}'
                        usuario.save()

                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Foto carregada: {nome_completo} -> {filename}'
                        ))

                    except Usuario.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'  ⚠ Usuário não encontrado: {nome_completo}'
                        ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Nome não mapeado: {filename}'
                    ))

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Fotos carregadas com sucesso!'))
        self.stdout.write(self.style.SUCCESS('='*60))

        # Mostrar resumo
        usuarios_com_foto = Usuario.objects.exclude(foto='').exclude(foto=None).count()
        total_usuarios = Usuario.objects.count()
        self.stdout.write(f'\nUsuários com foto: {usuarios_com_foto}/{total_usuarios}')
