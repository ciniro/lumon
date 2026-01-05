"""
Management command para migrar fotos de usuários para o novo sistema de nomes únicos.
Uso: python manage.py migrate_user_photos
"""

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Usuario


class Command(BaseCommand):
    help = 'Migra as fotos dos usuários para o novo sistema de nomes únicos (UUID)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando migração de fotos...'))

        # Buscar todos os usuários que têm foto
        usuarios_com_foto = Usuario.objects.exclude(foto='').exclude(foto=None)

        if not usuarios_com_foto.exists():
            self.stdout.write(self.style.WARNING('Nenhum usuário com foto encontrado.'))
            return

        total = usuarios_com_foto.count()
        migrados = 0
        erros = 0

        for usuario in usuarios_com_foto:
            try:
                # Obter o caminho completo do arquivo antigo
                caminho_antigo = usuario.foto.path

                # Verificar se o arquivo existe
                if not os.path.exists(caminho_antigo):
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Arquivo não encontrado para {usuario.nome}: {caminho_antigo}'
                    ))
                    erros += 1
                    continue

                # Salvar referência ao arquivo antigo
                arquivo_antigo = usuario.foto.file
                nome_arquivo_antigo = usuario.foto.name

                # Forçar o Django a reprocessar o arquivo com a nova função upload_to
                # Abrir o arquivo e reatribuir
                with open(caminho_antigo, 'rb') as f:
                    from django.core.files import File
                    novo_arquivo = File(f, name=os.path.basename(caminho_antigo))

                    # Atualizar o campo foto (isso vai usar a nova função usuario_foto_path)
                    usuario.foto.save(
                        os.path.basename(caminho_antigo),
                        novo_arquivo,
                        save=True
                    )

                # Remover o arquivo antigo se for diferente do novo
                if os.path.exists(caminho_antigo) and caminho_antigo != usuario.foto.path:
                    os.remove(caminho_antigo)

                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Foto migrada: {usuario.nome}'
                ))
                self.stdout.write(f'    Antigo: {nome_arquivo_antigo}')
                self.stdout.write(f'    Novo: {usuario.foto.name}')

                migrados += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  ✗ Erro ao migrar foto de {usuario.nome}: {str(e)}'
                ))
                erros += 1

        # Resumo
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Migração concluída!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\nTotal de usuários: {total}')
        self.stdout.write(self.style.SUCCESS(f'Migrados com sucesso: {migrados}'))
        if erros > 0:
            self.stdout.write(self.style.ERROR(f'Erros: {erros}'))
