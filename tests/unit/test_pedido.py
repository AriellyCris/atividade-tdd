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



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
