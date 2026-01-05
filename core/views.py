from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Perfil, Departamento


def login_view(request):
    """
    TELA 1: Tela de autenticação
    Permite que o usuário faça login no sistema com email, senha e perfil.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        perfil_id = request.POST.get('perfil')

        # Validar campos obrigatórios
        if not email or not senha or not perfil_id:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('login')

        try:
            # Buscar usuário pelo email e perfil
            usuario = Usuario.objects.get(email=email, id_perfil_id=perfil_id)

            # Verificar senha
            if usuario.verificar_senha(senha):
                # Login bem-sucedido - armazenar na sessão
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_email'] = usuario.email
                request.session['usuario_perfil'] = usuario.id_perfil.perfil
                messages.success(request, f'Bem-vindo(a), {usuario.nome}!')
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta.')
                return redirect('login')

        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado com este email e perfil.')
            return redirect('login')

    # GET - Exibir formulário de login
    perfis = Perfil.objects.all()
    return render(request, 'login.html', {'perfis': perfis})


def logout_view(request):
    """
    Faz o logout do usuário, limpando a sessão.
    """
    request.session.flush()
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


def home_view(request):
    """
    TELA 2: Menu principal
    Página inicial após o login, exibe a logo da Lumon.
    """
    # Verificar se usuário está logado
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')

    # Buscar dados completos do usuário
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Sessão inválida. Faça login novamente.')
        return redirect('login')

    context = {
        'usuario': usuario,
        'user_authenticated': True
    }
    return render(request, 'home.html', context)


def departamentos_view(request):
    """
    TELA 3: Cadastro de Departamentos
    CRUD completo de departamentos com listagem, criação, edição e exclusão.
    """
    # Verificar se usuário está logado
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')

    # Buscar usuário logado
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Sessão inválida. Faça login novamente.')
        return redirect('login')

    # Processar ações
    if request.method == 'POST':
        acao = request.POST.get('acao')

        # CRIAR NOVO DEPARTAMENTO
        if acao == 'criar':
            departamento_nome = request.POST.get('departamento')
            sigla = request.POST.get('sigla')

            if not departamento_nome:
                messages.error(request, 'O nome do departamento é obrigatório.')
            else:
                # Verificar unicidade
                if Departamento.objects.filter(departamento=departamento_nome).exists():
                    messages.error(request, 'Já existe um departamento com este nome.')
                else:
                    Departamento.objects.create(
                        departamento=departamento_nome,
                        sigla=sigla if sigla else None
                    )
                    messages.success(request, 'Departamento cadastrado com sucesso!')

        # ALTERAR DEPARTAMENTO EXISTENTE
        elif acao == 'alterar':
            dept_id = request.POST.get('id')
            departamento_nome = request.POST.get('departamento')
            sigla = request.POST.get('sigla')

            if not departamento_nome:
                messages.error(request, 'O nome do departamento é obrigatório.')
            else:
                try:
                    dept = Departamento.objects.get(id=dept_id)

                    # Verificar se o novo nome já existe em outro departamento
                    if Departamento.objects.filter(departamento=departamento_nome).exclude(id=dept_id).exists():
                        messages.error(request, 'Já existe outro departamento com este nome.')
                    else:
                        dept.departamento = departamento_nome
                        dept.sigla = sigla if sigla else None
                        dept.save()
                        messages.success(request, 'Departamento alterado com sucesso!')
                except Departamento.DoesNotExist:
                    messages.error(request, 'Departamento não encontrado.')

        # EXCLUIR DEPARTAMENTO
        elif acao == 'excluir':
            dept_id = request.POST.get('id')
            try:
                dept = Departamento.objects.get(id=dept_id)
                dept.delete()
                messages.success(request, 'Departamento excluído com sucesso!')
            except Departamento.DoesNotExist:
                messages.error(request, 'Departamento não encontrado.')
            except Exception as e:
                # Tratamento de erro de integridade (departamento com usuários vinculados)
                messages.error(request, 'Não é possível excluir um departamento que possui funcionários.')

        return redirect('departamentos')

    # GET - Listar departamentos
    departamentos = Departamento.objects.all().order_by('departamento')

    context = {
        'usuario': usuario,
        'user_authenticated': True,
        'departamentos': departamentos
    }
    return render(request, 'departamentos.html', context)


def usuarios_view(request):
    """
    TELA 4: Cadastro de Usuários
    CRUD completo de usuários com upload de foto, ForeignKey e validações.
    """
    # Verificar se usuário está logado
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')

    # Buscar usuário logado
    try:
        usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Sessão inválida. Faça login novamente.')
        return redirect('login')

    # Processar ações
    if request.method == 'POST':
        acao = request.POST.get('acao')

        # CRIAR NOVO USUÁRIO
        if acao == 'criar':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            perfil_id = request.POST.get('perfil')
            departamento_id = request.POST.get('departamento')
            foto = request.FILES.get('foto')

            # Validações
            if not nome or not email or not senha or not perfil_id or not departamento_id:
                messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            elif Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Já existe um usuário com este e-mail.')
            else:
                try:
                    # Buscar ForeignKeys
                    perfil = Perfil.objects.get(id=perfil_id)
                    departamento = Departamento.objects.get(id=departamento_id)

                    # Criar usuário (senha será hasheada automaticamente pelo método save())
                    novo_usuario = Usuario.objects.create(
                        nome=nome,
                        email=email,
                        senha=senha,
                        id_perfil=perfil,
                        id_departamento=departamento,
                        foto=foto if foto else None
                    )
                    messages.success(request, 'Funcionário registrado com sucesso!')
                except (Perfil.DoesNotExist, Departamento.DoesNotExist):
                    messages.error(request, 'Perfil ou departamento inválido.')

        # ALTERAR USUÁRIO EXISTENTE
        elif acao == 'alterar':
            user_id = request.POST.get('id')
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')  # Pode estar vazio
            perfil_id = request.POST.get('perfil')
            departamento_id = request.POST.get('departamento')
            foto = request.FILES.get('foto')

            if not nome or not email or not perfil_id or not departamento_id:
                messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            else:
                try:
                    user = Usuario.objects.get(id=user_id)

                    # Verificar se email já existe em outro usuário
                    if Usuario.objects.filter(email=email).exclude(id=user_id).exists():
                        messages.error(request, 'Já existe outro usuário com este e-mail.')
                    else:
                        # Buscar ForeignKeys
                        perfil = Perfil.objects.get(id=perfil_id)
                        departamento = Departamento.objects.get(id=departamento_id)

                        # Atualizar dados
                        user.nome = nome
                        user.email = email
                        user.id_perfil = perfil
                        user.id_departamento = departamento

                        # Atualizar senha apenas se fornecida
                        if senha:
                            user.senha = senha  # Será hasheada pelo método save()

                        # Atualizar foto apenas se fornecida
                        if foto:
                            user.foto = foto

                        user.save()
                        messages.success(request, 'Funcionário atualizado com sucesso!')
                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuário não encontrado.')
                except (Perfil.DoesNotExist, Departamento.DoesNotExist):
                    messages.error(request, 'Perfil ou departamento inválido.')

        # EXCLUIR USUÁRIO
        elif acao == 'excluir':
            user_id = request.POST.get('id')
            try:
                user = Usuario.objects.get(id=user_id)
                user.delete()
                messages.success(request, 'Funcionário excluído com sucesso!')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao excluir usuário: {str(e)}')

        return redirect('usuarios')

    # GET - Listar usuários com filtro e paginação
    from django.core.paginator import Paginator

    # Filtro por nome
    nome_filtro = request.GET.get('nome', '').strip()
    usuarios = Usuario.objects.select_related('id_perfil', 'id_departamento').all()

    if nome_filtro:
        usuarios = usuarios.filter(nome__icontains=nome_filtro)

    usuarios = usuarios.order_by('nome')

    # Paginação (5 por página)
    paginator = Paginator(usuarios, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    perfis = Perfil.objects.all().order_by('perfil')
    departamentos = Departamento.objects.all().order_by('departamento')

    context = {
        'usuario': usuario_logado,
        'user_authenticated': True,
        'page_obj': page_obj,
        'perfis': perfis,
        'departamentos': departamentos,
        'nome_filtro': nome_filtro
    }
    return render(request, 'usuarios.html', context)


def relatorio_usuarios_departamento_view(request):
    """
    TELA 5: Relatório de Usuários por Departamento
    Exibe relatório filtrado de usuários por departamento.
    Objetivo didático: Ensinar QuerySets com filter().
    """
    # Verificar se usuário está logado
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')

    # Buscar usuário logado
    try:
        usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Sessão inválida. Faça login novamente.')
        return redirect('login')

    # Obter departamento selecionado (se houver)
    departamento_id = request.GET.get('departamento', '')

    # Listar todos os departamentos para o select
    departamentos = Departamento.objects.all().order_by('departamento')

    # Filtrar usuários
    if departamento_id and departamento_id != 'todos':
        # Filtrar por departamento específico
        try:
            usuarios_filtrados = Usuario.objects.filter(
                id_departamento_id=departamento_id
            ).select_related('id_perfil', 'id_departamento').order_by('nome')

            departamento_selecionado = Departamento.objects.get(id=departamento_id)
            titulo_relatorio = f"Funcionários do Departamento: {departamento_selecionado.departamento}"
        except Departamento.DoesNotExist:
            usuarios_filtrados = Usuario.objects.none()
            titulo_relatorio = "Departamento não encontrado"
    elif departamento_id == 'todos':
        # Mostrar todos os usuários
        usuarios_filtrados = Usuario.objects.select_related(
            'id_perfil', 'id_departamento'
        ).all().order_by('nome')
        titulo_relatorio = "Todos os Funcionários"
    else:
        # Nenhum departamento selecionado ainda
        usuarios_filtrados = None
        titulo_relatorio = None

    context = {
        'usuario': usuario_logado,
        'user_authenticated': True,
        'departamentos': departamentos,
        'usuarios_filtrados': usuarios_filtrados,
        'departamento_selecionado': departamento_id,
        'titulo_relatorio': titulo_relatorio,
        'total_usuarios': usuarios_filtrados.count() if usuarios_filtrados is not None else 0
    }
    return render(request, 'relatorio_usuarios_departamento.html', context)
