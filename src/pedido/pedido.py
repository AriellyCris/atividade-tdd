from dataclasses import dataclass

VALOR_FRETE_GRATIS = 50.0

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
        return self.subtotal() > VALOR_FRETE_GRATIS

    def item_mais_caro(self) -> Item:
        return max(self.itens, key=lambda item: item.preco)

    def item_mais_barato(self) -> Item:
        return max(self.itens, key=lambda item: item.preco)

    def total_com_desconto(self, percentual: float) -> float:
        return self.subtotal() + self.subtotal() * percentual / 100