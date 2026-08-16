"""Regras de pedido usadas na Aula 03 de DevOps."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTAVOS = Decimal("0.01")


@dataclass(frozen=True)
class ItemPedido:
    nome: str
    preco_unitario: Decimal
    quantidade: int

    def subtotal(self) -> Decimal:
        if self.preco_unitario < 0:
            raise ValueError("preco_unitario nao pode ser negativo")
        if self.quantidade <= 0:
            raise ValueError("quantidade precisa ser maior que zero")
        return dinheiro(self.preco_unitario * self.quantidade)


@dataclass(frozen=True)
class CupomDesconto:
    texto: str
    desconto_percentual: Decimal
    desconta_no_frete: bool = False


CUPONS_VALIDOS: dict[str, CupomDesconto] = {
    "DEVOPS10": CupomDesconto("DEVOPS10", Decimal("10")),
    "FAG15": CupomDesconto("FAG15", Decimal("15")),
    "EXPRESSMISFITS": CupomDesconto("EXPRESSMISFITS", Decimal("0"), True),
}


@dataclass(frozen=True)
class Pedido:
    itens: list[ItemPedido]
    desconto_percentual: Decimal = Decimal("0")
    cupom: str | None = None
    entrega_expressa: bool = False


def dinheiro(valor: Decimal) -> Decimal:
    """Arredonda valores monetarios para duas casas decimais."""
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def validar_desconto(percentual: Decimal) -> None:
    if percentual < 0 or percentual > 100:
        raise ValueError("desconto_percentual precisa estar entre 0 e 100")


def calcular_subtotal(itens: list[ItemPedido]) -> Decimal:
    if not itens:
        raise ValueError("pedido precisa ter pelo menos um item")
    return dinheiro(sum((item.subtotal() for item in itens), Decimal("0")))


def aplicar_desconto_percentual(subtotal: Decimal, percentual: Decimal) -> Decimal:
    validar_desconto(percentual)
    desconto = subtotal * (percentual / Decimal("100"))
    return dinheiro(subtotal - desconto)


def resolver_cupom(cupom: str | None) -> CupomDesconto | None:
    """Converte o codigo informado no CupomDesconto correspondente."""
    if cupom is None or cupom.strip() == "":
        return None
    cupom_normalizado = cupom.strip().upper()
    if cupom_normalizado not in CUPONS_VALIDOS:
        raise ValueError("cupom invalido")
    return CUPONS_VALIDOS[cupom_normalizado]


def percentual_do_cupom(cupom: str | None) -> Decimal:
    cupom_valido = resolver_cupom(cupom)
    if cupom_valido is None:
        return Decimal("0")
    return cupom_valido.desconto_percentual


def calcular_frete(
    subtotal_com_desconto: Decimal,
    entrega_expressa: bool,
    cupom_desconto: CupomDesconto | None = None,
) -> Decimal:
    if subtotal_com_desconto >= Decimal("200") and not entrega_expressa:
        return Decimal("0.00")
    if entrega_expressa:
        if (
            subtotal_com_desconto > Decimal("50.00")
            and cupom_desconto is not None
            and cupom_desconto.desconta_no_frete
        ):
            return Decimal("0.00")
        return Decimal("29.90")
    return Decimal("14.90")


def calcular_total_pedido(pedido: Pedido) -> Decimal:
    subtotal = calcular_subtotal(pedido.itens)
    apos_desconto = aplicar_desconto_percentual(subtotal, pedido.desconto_percentual)
    cupom_valido = resolver_cupom(pedido.cupom)
    cupom_percentual = (
        Decimal("0") if cupom_valido is None else cupom_valido.desconto_percentual
    )
    apos_cupom = aplicar_desconto_percentual(apos_desconto, cupom_percentual)
    frete = calcular_frete(apos_cupom, pedido.entrega_expressa, cupom_valido)
    return dinheiro(apos_cupom + frete)