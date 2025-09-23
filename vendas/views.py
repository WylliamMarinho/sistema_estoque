from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from sistema_estoque.auth_required import auth_required
from .models import Venda, ItemVenda
from clientes.models import Cliente
from estoque.models import Estoque


@api_view(['POST'])
@auth_required
def registrar_venda(request):
    try:
        with transaction.atomic():
            cliente_id = request.data.get('cliente_id')
            total = request.data.get('total')
            produtos = request.data.get('produtos')

            cliente = Cliente.objects.get(id=cliente_id)

            venda = Venda.objects.create(cliente=cliente, total=total)

            for item in produtos:
                produto_id = item['produto_id']
                quantidade_necessaria = item['quantidade']

                lotes = Estoque.objects.filter(
                    produto_id=produto_id,
                    quantidade_entrada__gt=models.F('quantidade_vendida')
                ).order_by('data_vencimento')

                if not lotes:
                    raise Exception(f"Produto ID {produto_id} sem estoque disponível")

                for lote in lotes:
                    disponivel = lote.quantidade_entrada - lote.quantidade_vendida
                    usar = min(disponivel, quantidade_necessaria)

                    lote.quantidade_vendida += usar
                    lote.save()

                    total_item = usar * float(lote.valor_venda)
                    ItemVenda.objects.create(
                        venda=venda,
                        estoque=lote,
                        quantidade=usar,
                        total=total_item
                    )

                    quantidade_necessaria -= usar
                    if quantidade_necessaria <= 0:
                        break

                if quantidade_necessaria > 0:
                    raise Exception(f"Estoque insuficiente para produto ID {produto_id}")

            return Response({"mensagem": "Venda registrada com sucesso", "venda_id": venda.id},
                            status=status.HTTP_201_CREATED)

    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)