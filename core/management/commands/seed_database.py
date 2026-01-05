"""
Management command para popular o banco de dados com dados iniciais.
Uso: python manage.py seed_database
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from core.models import Perfil, Departamento, Usuario


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais do sistema Lumon'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))

        # Limpar dados existentes (opcional - comentar se não quiser limpar)
        self.stdout.write('Limpando dados existentes...')
        Usuario.objects.all().delete()
        Departamento.objects.all().delete()
        Perfil.objects.all().delete()

        # Criar Perfis
        self.stdout.write('Criando perfis...')
        gerente, _ = Perfil.objects.get_or_create(id=1, defaults={'perfil': 'Gerente'})
        funcionario, _ = Perfil.objects.get_or_create(id=2, defaults={'perfil': 'Funcionário'})
        self.stdout.write(self.style.SUCCESS(f'  ✓ Perfil criado: {gerente.perfil}'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ Perfil criado: {funcionario.perfil}'))

        # Criar Departamentos
        self.stdout.write('Criando departamentos...')
        mdr, _ = Departamento.objects.get_or_create(
            id=1,
            defaults={'departamento': 'Refinamento de Macrodados', 'sigla': 'MDR'}
        )
        wellness, _ = Departamento.objects.get_or_create(
            id=2,
            defaults={'departamento': 'Bem Estar', 'sigla': 'Wellness'}
        )
        od, _ = Departamento.objects.get_or_create(
            id=3,
            defaults={'departamento': 'Ótica e Design', 'sigla': 'O&D'}
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Departamento criado: {mdr.departamento} ({mdr.sigla})'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ Departamento criado: {wellness.departamento} ({wellness.sigla})'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ Departamento criado: {od.departamento} ({od.sigla})'))

        # Criar Usuários
        self.stdout.write('Criando usuários...')

        usuarios_data = [
            {
                'id': 1,
                'nome': 'Mark Scout',
                'email': 'mark@lumon.com',
                'senha': '1234',
                'id_perfil': gerente,
                'id_departamento': mdr
            },
            {
                'id': 2,
                'nome': 'Helly Riggs',
                'email': 'helly@lumon.com',
                'senha': '1234',
                'id_perfil': funcionario,
                'id_departamento': mdr
            },
            {
                'id': 3,
                'nome': 'Irving Bailiff',
                'email': 'irving@lumon.com',
                'senha': '1234',
                'id_perfil': funcionario,
                'id_departamento': mdr
            },
            {
                'id': 4,
                'nome': 'Dylan George',
                'email': 'dylan@lumon.com',
                'senha': '1234',
                'id_perfil': funcionario,
                'id_departamento': mdr
            },
            {
                'id': 5,
                'nome': 'Ms. Casey',
                'email': 'casey@lumon.com',
                'senha': '1234',
                'id_perfil': funcionario,
                'id_departamento': wellness
            },
            {
                'id': 6,
                'nome': 'Burt Goodman',
                'email': 'burt@lumon.com',
                'senha': '1234',
                'id_perfil': gerente,
                'id_departamento': od
            },
        ]

        for user_data in usuarios_data:
            # O método save() do modelo já irá hashear a senha automaticamente
            usuario, created = Usuario.objects.get_or_create(
                id=user_data['id'],
                defaults={
                    'nome': user_data['nome'],
                    'email': user_data['email'],
                    'senha': user_data['senha'],  # Será hasheada pelo método save()
                    'id_perfil': user_data['id_perfil'],
                    'id_departamento': user_data['id_departamento']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Usuário criado: {usuario.nome} ({usuario.email}) - '
                    f'{usuario.id_perfil.perfil} - {usuario.id_departamento.sigla}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'  ⚠ Usuário já existe: {usuario.nome} ({usuario.email})'
                ))

        # Carregar fotos dos usuários
        self.stdout.write('\nCarregando fotos dos usuários...')

        # Mapeamento: primeiro nome (lowercase) -> nome completo
        fotos_map = {
            'mark': 'Mark Scout',
            'helly': 'Helly Riggs',
            'irving': 'Irving Bailiff',
            'dylan': 'Dylan George',
            'mscasey': 'Ms. Casey',
            'burt': 'Burt Goodman',
        }

        # Pasta de origem das fotos
        source_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'users_photos')

        fotos_carregadas = 0

        if os.path.exists(source_dir):
            for filename in os.listdir(source_dir):
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    # Extrair o primeiro nome do arquivo (sem extensão)
                    primeiro_nome = os.path.splitext(filename)[0].lower()

                    # Verificar se temos mapeamento para este nome
                    if primeiro_nome in fotos_map:
                        nome_completo = fotos_map[primeiro_nome]

                        try:
                            # Buscar o usuário no banco
                            usuario = Usuario.objects.get(nome=nome_completo)

                            # Abrir e atribuir a foto
                            foto_path = os.path.join(source_dir, filename)
                            with open(foto_path, 'rb') as f:
                                # Usar o método save() do FileField que usa automaticamente usuario_foto_path
                                usuario.foto.save(filename, File(f), save=True)

                            self.stdout.write(self.style.SUCCESS(
                                f'  ✓ Foto carregada: {nome_completo} -> {usuario.foto.name}'
                            ))
                            fotos_carregadas += 1

                        except Usuario.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f'  ⚠ Usuário não encontrado: {nome_completo}'
                            ))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(
                                f'  ✗ Erro ao carregar foto de {nome_completo}: {str(e)}'
                            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'  ⚠ Pasta de fotos não encontrada: {source_dir}'
            ))

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nResumo:')
        self.stdout.write(f'  • Perfis: {Perfil.objects.count()}')
        self.stdout.write(f'  • Departamentos: {Departamento.objects.count()}')
        self.stdout.write(f'  • Usuários: {Usuario.objects.count()}')
        self.stdout.write(f'  • Fotos carregadas: {fotos_carregadas}/{Usuario.objects.count()}')
        self.stdout.write('\nUsuários de teste:')
        self.stdout.write('  • Email: mark@lumon.com | Senha: 1234 | Perfil: Gerente')
        self.stdout.write('  • Email: helly@lumon.com | Senha: 1234 | Perfil: Funcionário')
        self.stdout.write('  • Email: burt@lumon.com | Senha: 1234 | Perfil: Gerente')
