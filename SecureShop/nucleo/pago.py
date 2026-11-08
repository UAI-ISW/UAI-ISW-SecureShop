"""Contrato de pago y el stub que hoy está conectado.

PasarelaPago es la interfaz. StubWebpay la implementa.
No abre red hacia Transbank: contesta como si Webpay hubiera respondido.
"""
from abc import ABC, abstractmethod


class ResultadoPago:
    def __init__(self, aprobado, codigo, mensaje):
        self.aprobado = aprobado
        self.codigo = codigo
        self.mensaje = mensaje


class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto, medio):
        """medio 'webpay' autoriza. 'rechazo' simula el rechazo de la pasarela."""


class StubWebpay(PasarelaPago):
    def cobrar(self, monto, medio='webpay'):
        if not isinstance(monto, int) or monto <= 0:
            return ResultadoPago(
                False, 'monto-invalido', 'El monto tiene que ser mayor que cero.',
            )
        if medio == 'rechazo':
            return ResultadoPago(False, 'rechazado', 'Webpay rechazó el pago.')
        if medio != 'webpay':
            return ResultadoPago(False, 'medio-invalido', 'Medio de pago desconocido.')
        return ResultadoPago(True, 'autorizado', 'Pago autorizado por el stub de Webpay.')


def pagar_carrito(carrito, pasarela, medio='webpay'):
    """Junta el carrito con la pasarela. Si autoriza, vacía el carrito."""
    resultado = pasarela.cobrar(carrito.total(), medio)
    if resultado.aprobado:
        carrito.vaciar()
    return resultado
