import unittest

from controlador.controlador import Controlador


class EntradaFalsa:
    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return self.valor


class VistaFalsa:
    def __init__(self, campo_funcion, expresion):
        setattr(self, campo_funcion, EntradaFalsa(expresion))
        self.funcion_graficada = None
        self.errores = []

    def mostrar_grafica_biseccion(self, funcion):
        self.funcion_graficada = funcion

    def mostrar_grafica_rf(self, funcion):
        self.funcion_graficada = funcion

    def mostrar_error(self, titulo, mensaje):
        self.errores.append((titulo, mensaje))


class PruebasGraficarFuncion(unittest.TestCase):
    def test_graficar_no_requiere_intervalo_ni_cambio_de_signo(self):
        casos = (
            ("graficar_biseccion", "biseccion_funcion", "x^2 + 1"),
            ("graficar_rf", "rf_funcion", "x^2 + 1"),
        )
        for metodo, campo, expresion in casos:
            with self.subTest(metodo=metodo):
                controlador = Controlador.__new__(Controlador)
                controlador.vista = VistaFalsa(campo, expresion)

                getattr(controlador, metodo)()

                self.assertEqual(controlador.vista.funcion_graficada.evaluar(2), 5)
                self.assertEqual(controlador.vista.errores, [])

    def test_graficar_rechaza_funcion_mal_digitada(self):
        casos = (
            ("graficar_biseccion", "biseccion_funcion"),
            ("graficar_rf", "rf_funcion"),
        )
        for metodo, campo in casos:
            with self.subTest(metodo=metodo):
                controlador = Controlador.__new__(Controlador)
                controlador.vista = VistaFalsa(campo, "x +")

                getattr(controlador, metodo)()

                self.assertIsNone(controlador.vista.funcion_graficada)
                self.assertEqual(len(controlador.vista.errores), 1)

    def test_graficar_funciones_sin_cambio_de_signo_en_la_interfaz(self):
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        try:
            controlador = Controlador(root)
            for campo in (controlador.vista.biseccion_funcion, controlador.vista.rf_funcion):
                campo.delete(0, tk.END)
                campo.insert(0, "x^2 + 1")

            controlador.graficar_biseccion()
            controlador.graficar_rf()

            self.assertEqual(controlador.vista._funcion_grafica_biseccion.evaluar(0), 1)
            self.assertEqual(controlador.vista._funcion_grafica_rf.evaluar(0), 1)
            self.assertEqual(controlador.vista._rango_grafica_biseccion, (-2.0, 2.0))
            self.assertEqual(controlador.vista._rango_grafica_rf, (-2.0, 2.0))
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
