from gettext import install

import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================

def test_bug1_subtotal_considera_a_quantidade(pedido_pequeno):
    # 6,00 + 2 x 4,50 = 15,00 (o código original ignora a quantidade e devolve 10,50)
    assert pedido_pequeno.subtotal() == 15.0
    
def test_bug2_frete_gratis_com_subtotal_exatamente_50():
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True    
    
def test_bug3_item_mais_barato_retorna_o_menor_preco(pedido_pequeno):
    assert pedido_pequeno.item_mais_barato().nome == "Pão de queijo"    

def test_bug4_desconto_diminui_o_subtotal():
    pedido = Pedido("Carla", [Item("Combo", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0

# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função

def test_req1_lista_vazia_retorna_zero():
    assert contar_frete_gratis([]) == 0

def test_req1_todos_com_frete_gratis(pedido_grande):
    outro = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_grande, outro]) == 2

def test_req1_nenhum_com_frete_gratis(pedido_pequeno):
    outro = Pedido("Dani", [Item("Suco", 8.0, 1)])
    assert contar_frete_gratis([pedido_pequeno, outro]) == 0
    
def test_req1_lista_mista(pedido_pequeno, pedido_grande):
    assert contar_frete_gratis([pedido_pequeno, pedido_grande]) == 1
    
# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método

def test_req2_sem_indisponiveis_e_abaixo_de_50_esta_confirmado(pedido_pequeno):
    # subtotal 15,00, nada indisponível
    assert pedido_pequeno.situacao(0) == "Confirmado"
    
def test_req2_sem_indisponiveis_e_a_partir_de_50_tem_frete_gratis(pedido_grande):
    # subtotal 73,00, nada indisponível
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"

def test_req2_mais_de_25_por_cento_indisponivel_cancela_mesmo_com_frete_gratis(pedido_grande):
    # 5 unidades no total, 2 indisponíveis = 40%
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"

def test_req2_exatamente_25_por_cento_indisponivel_segue_para_o_frete():
    # 4 unidades, 1 indisponível = exatamente 25%; subtotal 60,00
    pedido = Pedido("Eva", [Item("Combo", 15.0, 4)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"
    
def test_req2_pouco_acima_de_25_por_cento_indisponivel_cancela():
    # 11 unidades, 3 indisponíveis = 27,3%
    pedido = Pedido("Fábio", [Item("Combo", 10.0, 11)])
    assert pedido.situacao(3) == "Cancelado por falta de estoque"

# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_req3_abaixo_de_50_envia_sms_com_cliente_e_valor_faltante(pedido_pequeno):
    sms_service = MagicMock()  # serviço de SMS falso

    pedido_pequeno.sugerir_frete_gratis(sms_service)

    # subtotal 15,00 -> faltam 35,00 para o frete grátis
    sms_service.enviar.assert_called_once_with("Bruno", 35.0)
    
def test_req3_acima_de_50_nao_envia_sms(pedido_grande):
    sms_service = MagicMock()

    pedido_grande.sugerir_frete_gratis(sms_service)

    sms_service.enviar.assert_not_called()

def test_req3_exatamente_50_nao_envia_sms():
    sms_service = MagicMock()
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])

    pedido.sugerir_frete_gratis(sms_service)

    sms_service.enviar.assert_not_called()
    
def test_req3_valor_faltante_vem_arredondado_em_centavos():
    sms_service = MagicMock()
    pedido = Pedido("Gui", [Item("Lanche", 33.3, 1)])

    pedido.sugerir_frete_gratis(sms_service)

    # 50,00 - 33,30 dá 16.700000000000003 em ponto flutuante; o SMS deve levar 16,70
    sms_service.enviar.assert_called_once_with("Gui", 16.7)