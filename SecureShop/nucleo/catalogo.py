"""Catálogo fijo de la tienda. No sale de la base."""


class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio


CATALOGO = [
    Producto(1, 'Collar para perro', 5000),
    Producto(2, 'Correa retráctil', 8000),
    Producto(3, 'Plato de comida', 3000),
    Producto(4, 'Juguete para gato', 4000),
]


def buscar(producto_id):
    return next((p for p in CATALOGO if p.id == producto_id), None)
