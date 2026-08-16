from decimal import Decimal

import pytest

from app.pedidos import (
    ItemPedido,
    Pedido,
    aplicar_desconto_percentual,
    calcular_frete,
    calcular_subtotal,
    calcular_total_pedido,
    percentual_do_cupom,
)


def D(valor: str) -> Decimal:
    return Decimal(valor)


def test_calcula_subtotal_com_um_item():
    itens = [ItemPedido("Cafe", D("8.50"), 2)]
    assert calcular_subtotal(itens) == D("17.00")


def test_calcula_subtotal_com_multiplos_itens():
    itens = [
        ItemPedido("Cafe", D("8.50"), 2),
        ItemPedido("Pao de queijo", D("6.00"), 3),
    ]
    assert calcular_subtotal(itens) == D("35.00")


def test_subtotal_recusa_lista_vazia():
    with pytest.raises(ValueError, match="pelo menos um item"):
        calcular_subtotal([])


def test_item_recusa_quantidade_zero():
    item = ItemPedido("Cafe", D("8.50"), 0)
    with pytest.raises(ValueError, match="maior que zero"):
        item.subtotal()


@pytest.mark.parametrize(
    "subtotal, percentual, esperado",
    [
        (D("100.00"), D("0"), D("100.00")),
        (D("100.00"), D("10"), D("90.00")),
        (D("250.00"), D("20"), D("200.00")),
    ],
)
def test_aplica_desconto_percentual(subtotal, percentual, esperado):
    assert aplicar_desconto_percentual(subtotal, percentual) == esperado


@pytest.mark.parametrize("percentual", [D("-1"), D("101")])
def test_desconto_percentual_invalido(percentual):
    with pytest.raises(ValueError, match="entre 0 e 100"):
        aplicar_desconto_percentual(D("100.00"), percentual)


@pytest.mark.parametrize(
    "cupom, esperado",
    [
        (None, D("0")),
        ("", D("0")),
        ("DEVOPS10", D("10")),
        (" devops10 ", D("10")),
        ("FAG15", D("15")),
    ],
)
def test_percentual_do_cupom(cupom, esperado):
    assert percentual_do_cupom(cupom) == esperado


def test_cupom_invalido_dispara_erro():
    with pytest.raises(ValueError, match="cupom invalido"):
        percentual_do_cupom("PROMO999")


@pytest.mark.parametrize(
    "subtotal, expressa, esperado",
    [
        (D("199.99"), False, D("14.90")),
        (D("200.00"), False, D("0.00")),
        (D("500.00"), True, D("29.90")),
    ],
)
def test_calcula_frete(subtotal, expressa, esperado):
    assert calcular_frete(subtotal, expressa) == esperado


def test_total_do_pedido_com_desconto_cupom_e_frete():
    pedido = Pedido(
        itens=[ItemPedido("Combo", D("100.00"), 2)],
        desconto_percentual=D("10"),
        cupom="DEVOPS10",
        entrega_expressa=False,
    )
    # 200 - 10% = 180; cupom DEVOPS10 aplica mais 10% = 162; frete comum = 14.90
    assert calcular_total_pedido(pedido) == D("176.90")


def test_total_do_pedido_com_frete_gratis():
    pedido = Pedido(
        itens=[ItemPedido("Kit", D("250.00"), 1)],
        desconto_percentual=D("0"),
        cupom=None,
        entrega_expressa=False,
    )
    assert calcular_total_pedido(pedido) == D("250.00")

def test_desconta_frete_express_com_cupom_desconta_frete():
    pedido = Pedido(
        itens=[ItemPedido("Kit", D("250.00"), 1)],
        desconto_percentual=D("0"),
        cupom="EXPRESSMISFITS",
        entrega_expressa=True,
    )
    assert calcular_total_pedido(pedido) == D("250.00")