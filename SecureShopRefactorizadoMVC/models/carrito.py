class Carrito:
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto):
        self.items.append(producto)

    def get_total(self):
        return sum(producto.precio for producto in self.items)

    def get_items(self):
        return self.items

    def vaciar(self):
        self.items = []

    def to_dict(self):
        return {
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total()
        } 