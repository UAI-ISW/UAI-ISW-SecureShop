class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    @staticmethod
    def get_all():
        # Por ahora, retornamos una lista estática de productos
        return [
            Producto(1, 'Collar para perro', 5000),
            Producto(2, 'Correa retráctil', 8000),
            Producto(3, 'Plato de comida', 3000),
            Producto(4, 'Juguete para gato', 4000)
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        } 