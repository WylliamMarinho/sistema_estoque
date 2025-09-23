from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Produto
from sistema_estoque.auth_required import auth_required

@api_view(['GET', 'POST'])
@auth_required # Protege a rota de listagem e criação
def produtos_list(request):
    if request.method == 'GET':
        s = request.query_params.get('s', None)
        if s:
            produtos = Produto.objects.filter(codigo__icontains=s) | Produto.objects.filter(descricao__icontains=s)
        else:
            produtos = Produto.objects.all()
        data = [
            {
                "id": p.id,
                "codigo": p.codigo,
                "descricao": p.descricao,
                "perecivel": p.perecivel,
            } for p in produtos
        ]
        return Response(data)

    elif request.method == 'POST':
        codigo = request.data.get('codigo').strip().upper()
        descricao = request.data.get('nome')
        perecivel = request.data.get('perecivel', False)
        try:
            Produto.objects.create(codigo=codigo, descricao=descricao, perecivel=perecivel)
            return Response({"mensagem": "Produto cadastrado com sucesso"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"detail": "Código já existente."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erro inesperado: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@auth_required # Protege a rota de atualização
def produto_detail(request, id_produto):
    try:
        produto = Produto.objects.get(id=id_produto)
    except Produto.DoesNotExist:
        return Response({"detail": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    codigo = request.data.get('codigo').strip().upper()
    descricao = request.data.get('nome')
    perecivel = request.data.get('perecivel', False)

    if Produto.objects.filter(codigo=codigo).exclude(id=id_produto).exists():
        return Response({"detail": "Código já existente em outro produto"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        produto.codigo = codigo
        produto.descricao = descricao
        produto.perecivel = perecivel
        produto.save()
        return Response({"mensagem": "Produto atualizado com sucesso"})
    except Exception as e:
        return Response({"detail": f"Erro inesperado: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
