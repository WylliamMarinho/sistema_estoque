from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sistema_estoque.auth_required import auth_required
from .models import Cliente

@api_view(['GET', 'POST'])
@auth_required
def clientes_list(request):
    if request.method == 'GET':
        s = request.query_params.get('s', None)
        if s:
            clientes = Cliente.objects.filter(cpf__icontains=s) | Cliente.objects.filter(nome__icontains=s)
        else:
            clientes = Cliente.objects.all()
        data = [{"id": c.id, "cpf": c.cpf, "nome": c.nome} for c in clientes]
        return Response(data)

    elif request.method == 'POST':
        cpf = request.data.get('cpf')
        nome = request.data.get('nome')
        try:
            Cliente.objects.create(cpf=cpf, nome=nome)
            return Response({"mensagem": "Cliente cadastrado com sucesso"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"detail": "CPF já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def cliente_detail(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id=id_cliente)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    cpf = request.data.get('cpf')
    nome = request.data.get('nome')
    try:
        if Cliente.objects.filter(cpf=cpf).exclude(id=id_cliente).exists():
            return Response({"detail": "CPF já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        cliente.cpf = cpf
        cliente.nome = nome
        cliente.save()
        return Response({"mensagem": "Cliente atualizado com sucesso"})
    except Exception:
        return Response({"detail": "Erro ao atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)