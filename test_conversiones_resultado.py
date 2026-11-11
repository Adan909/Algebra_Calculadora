import unittest

from controlador.controlador import Controlador


class ValorFalso:
    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return self.valor


class VistaFalsa:
    def mostrar_resultado_conversion(self, texto):
        self.resultado = texto

    def mostrar_error(self, titulo, mensaje):
        raise AssertionError(f"{titulo}: {mensaje}")


class TestResultadoConversiones(unittest.TestCase):
    def test_conversion_binaria_a_decimal_muestra_el_resultado_final(self):
        vista = VistaFalsa()
        vista.entry_conv_origen = ValorFalso("10")
        vista.base_origen = ValorFalso("Binario")
        controlador = Controlador.__new__(Controlador)
        controlador.vista = vista

        controlador.convertir_a_decimal()

        self.assertIn("Número original: 10", vista.resultado)
        self.assertTrue(vista.resultado.endswith("Número en base decimal: 2"))

    def test_conversion_decimal_a_binario_muestra_el_resultado_final(self):
        vista = VistaFalsa()
        vista.entry_conv_decimal = ValorFalso("2")
        vista.base_destino = ValorFalso("Binario")
        controlador = Controlador.__new__(Controlador)
        controlador.vista = vista

        controlador.convertir_desde_decimal()

        self.assertTrue(vista.resultado.endswith("Número en base binario: 10"))


if __name__ == "__main__":
    unittest.main()
