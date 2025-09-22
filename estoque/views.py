from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import Estoque
from produtos.models import Produto


@api_view(['GET', 'POST'])
def estoque_list(request, codigo):
    try:
        produto = Produto.objects.get(codigo=codigo)
    except Produto.DoesNotExist:
        return Response({"detail": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        entradas = Estoque.objects.filter(produto=produto).order_by('data_entrada')
        data = [
            {
                "data_entrada": str(e.data_entrada),
                "quantidade_entrada": e.quantidade_entrada,
                "valor_compra": float(e.valor_compra),
                "valor_venda": float(e.valor_venda),
                "quantidade_vendida": e.quantidade_vendida,
                "data_vencimento": str(e.data_vencimento) if e.data_vencimento else None,
            } for e in entradas
        ]
        return Response(data)

    elif request.method == 'POST':
        try:
            data_entrada_str = request.data.get('data_entrada')
            data_vencimento_str = request.data.get('data_vencimento')
            data_entrada = datetime.strptime(data_entrada_str, "%d/%m/%Y").date()
            data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y").date() if data_vencimento_str else None

            Estoque.objects.create(
                produto=produto,
                data_entrada=data_entrada,
                quantidade_entrada=request.data.get('quantidade_entrada'),
                valor_compra=request.data.get('valor_compra'),
                valor_venda=request.data.get('valor_venda'),
                data_vencimento=data_vencimento
            )
            return Response({"mensagem": "Entrada de estoque registrada com sucesso"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Erro ao adicionar entrada: {e}"}, status=status.HTTP_400_BAD_REQUEST)