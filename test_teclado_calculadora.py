import math
import tkinter as tk
import unittest

from controlador.controlador import Controlador
from modelo.biseccion import FuncionMatematica


class TestFuncionesTeclado(unittest.TestCase):
    def test_funciones_trigonometricas_reciprocas_e_inversas(self):
        casos = (
            ("csc(pi / 2)", 1.0),
            ("sec(0)", 1.0),
            ("cot(pi / 4)", 1.0),
            ("arcsin(1)", math.pi / 2),
            ("arccos(1)", 0.0),
            ("arctan(1)", math.pi / 4),
            ("arccsc(2)", math.pi / 6),
            ("arcsec(2)", math.pi / 3),
            ("arccot(1)", math.pi / 4),
            ("sqrt(4) + e", 2 + math.e),
        )
        for expresion, esperado in casos:
            with self.subTest(expresion=expresion):
                resultado = FuncionMatematica(expresion).evaluar(0)
                self.assertAlmostEqual(resultado, esperado)

    def test_rechaza_valores_fuera_del_dominio_de_arccsc(self):
        with self.assertRaises(ValueError):
            FuncionMatematica("arccsc(0.5)").evaluar(0)


class TestTecladoCalculadora(unittest.TestCase):
    def test_inserta_funciones_en_campo_activo_y_borra_caracter(self):
        root = tk.Tk()
        root.geometry("1000x600")
        try:
            vista = Controlador(root).vista
            vista._al_cambiar_modulo(
                vista.nb_main.index(vista.tab_biseccion),
                "Método de Bisección",
            )
            campo = vista.biseccion_funcion
            campo.delete(0, tk.END)
            campo.insert(0, "2")
            campo.focus_force()
            root.update()

            vista._alternar_teclado()
            root.update()
            self.assertTrue(vista._teclado_ventana.winfo_exists())

            vista._teclado_botones["sin"].invoke()
            vista._teclado_botones["x"].invoke()
            self.assertEqual(campo.get(), "sin(x)")

            vista._teclado_borrar()
            self.assertEqual(campo.get(), "sin()")

            vista._cerrar_teclado()
            self.assertIsNone(vista._teclado_ventana)
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()


if __name__ == "__main__":
    unittest.main()
