from dataclasses import dataclass

VALOR_FRETE_GRATIS = 50.0
LIMITE_INDISPONIVEL = 0.25

@dataclass
class Item:
    nome: str
    preco: float
    quantidade: int = 1

class Pedido:
    def __init__(self, cliente: str, itens: list):
        self.cliente = cliente
        self.itens = itens

    def quantidade_total(self) -> int:
        return sum(item.quantidade for item in self.itens)

    def subtotal(self) -> float:
        return sum(item.preco * item.quantidade for item in self.itens)

    def tem_frete_gratis(self) -> bool:
        return self.subtotal() >= VALOR_FRETE_GRATIS

    def item_mais_caro(self) -> Item:
        return max(self.itens, key=lambda item: item.preco)

    def item_mais_barato(self) -> Item:
        return min(self.itens, key=lambda item: item.preco)

    def total_com_desconto(self, percentual: float) -> float:
        return self.subtotal() - self.subtotal() * percentual / 100
    
    def contar_frete_gratis(pedidos: list) -> int:
        return sum(1 for pedido in pedidos if pedido.tem_frete_gratis())
    
    def situacao(self, unidades_indisponiveis: int) -> str:
        if unidades_indisponiveis / self.quantidade_total() > LIMITE_INDISPONIVEL:
            return "Cancelado por falta de estoque"
        if self.tem_frete_gratis():
            return "Confirmado com frete grátis"
        return "Confirmado"
    
    def sugerir_frete_gratis(self, sms_service) -> None:
        if not self.tem_frete_gratis():
            valor_faltante = round(VALOR_FRETE_GRATIS - self.subtotal(), 2)
            sms_service.enviar(self.cliente, valor_faltante)
    
def contar_frete_gratis(pedidos: list) -> int:
    return 0

