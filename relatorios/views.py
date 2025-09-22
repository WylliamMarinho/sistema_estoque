from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from produtos.models import Produto
from estoque.models import Estoque
from vendas.models import Venda, ItemVenda

@api_view(['GET'])
def relatorio_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return Response({"detail": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    entradas_raw = Estoque.objects.filter(produto=produto).order_by('data_entrada')
    entradas = []
    for entrada in entradas_raw:
        entradas.append({
            "unidades": entrada.quantidade_entrada,
            "vencimento": entrada.data_vencimento.strftime("%Y-%m-%d") if entrada.data_vencimento else None,
            "compra": float(entrada.valor_compra),
            "valor_venda": float(entrada.valor_venda),
            "quantidade_vendida": entrada.quantidade_vendida,
            "status": entrada.quantidade_vendida < entrada.quantidade_entrada
        })

    saidas_raw = ItemVenda.objects.filter(estoque__produto=produto).order_by('venda__data')
    saidas = []
    for saida in saidas_raw:
        saidas.append({
            "data_venda": saida.venda.data.strftime("%Y-%m-%d"),
            "quantidade": saida.quantidade,
            "total": float(saida.total)
        })

    return Response({
        "produto": {
            "nome": produto.descricao,
            "entradas": entradas,
            "saidas": saidas,
        }
    })