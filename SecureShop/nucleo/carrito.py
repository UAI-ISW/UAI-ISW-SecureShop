"""Un carrito para todo el proceso.

Quien entre ve lo que agregó otro navegador. Se vacía al reiniciar.
Es el hallazgo A06 de la guía del 4 nov: no es el carrito de una sesión.
"""


class Carrito:
    def __init__(self):
        self._items = []

    def agregar(self, producto):
        self._items.append(producto)

    def total(self):
        return sum(producto.precio for producto in self._items)

    def vaciar(self):
        self._items.clear()

    def clear(self):
        self.vaciar()

    def __iter__(self):
        return iter(self._items)

    def __bool__(self):
        return bool(self._items)

    def __len__(self):
        return len(self._items)


carrito_del_proceso = Carrito()
