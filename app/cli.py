"""Interface de linha de comando simples para testar o sistema manualmente."""

from __future__ import annotations

import argparse
from decimal import Decimal

from app.pedidos import ItemPedido, Pedido, calcular_total_pedido


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calcula total de pedido da Aula 03.")
    parser.add_argument("--preco", type=Decimal, required=True, help="Preco unitario")
    parser.add_argument("--quantidade", type=int, required=True, help="Quantidade")
    parser.add_argument("--desconto", type=Decimal, default=Decimal("0"), help="Desconto percentual")
    parser.add_argument("--cupom", default=None, help="Cupom promocional")
    parser.add_argument("--expressa", action="store_true", help="Usa entrega expressa")
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    pedido = Pedido(
        itens=[ItemPedido("produto", args.preco, args.quantidade)],
        desconto_percentual=args.desconto,
        cupom=args.cupom,
        entrega_expressa=args.expressa,
    )
    print(calcular_total_pedido(pedido))


if __name__ == "__main__":
    main()
