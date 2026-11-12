import unittest

from modelo.secante import secante


class PruebasSecante(unittest.TestCase):
    def test_formula_y_convergencia(self):
        resultado = secante("x^2 - 2", "1", "2", "0.0001", "20")

        self.assertTrue(resultado.convergio)
        self.assertAlmostEqual(resultado.raiz, 2 ** 0.5, places=6)
        primera = resultado.iteraciones[0]
        self.assertAlmostEqual(
            primera.aproximacion,
            2 - (2 ** 2 - 2) * (2 - 1) / ((2 ** 2 - 2) - (1 ** 2 - 2)),
        )
        self.assertEqual(primera.x_anterior, 1)
        self.assertEqual(primera.x_actual, 2)

    def test_raiz_exacta_en_valor_inicial(self):
        resultado = secante("x - 2", "1", "2", "0.01", "10")

        self.assertTrue(resultado.convergio)
        self.assertEqual(resultado.raiz, 2)
        self.assertEqual(resultado.iteraciones, ())

    def test_denominador_cero_y_valores_iniciales_iguales(self):
        with self.assertRaisesRegex(ValueError, "deben ser distintos"):
            secante("x^2 + 1", "1", "1", "0.01", "10")
        with self.assertRaisesRegex(ValueError, "son iguales"):
            secante("x^2", "-1", "1", "0.01", "10")

    def test_error_alternativo_cuando_aproximacion_es_cero(self):
        resultado = secante("x", "-1", "1", "0.01", "10")

        self.assertTrue(resultado.convergio)
        self.assertEqual(resultado.iteraciones[0].aproximacion, 0)
        self.assertIn("alternativo", resultado.iteraciones[0].criterio_error)

    def test_limite_de_iteraciones_y_entradas_invalidas(self):
        resultado = secante("x^2 - 2", "1", "2", "1e-12", "1")
        self.assertFalse(resultado.convergio)
        self.assertEqual(len(resultado.iteraciones), 1)

        for argumentos in (
            ("x", "inválido", 2, 1, 10),
            ("x", 1, 2, 0, 10),
            ("x", 1, 2, 1, "1.5"),
            ("x +", 1, 2, 1, 10),
        ):
            with self.subTest(argumentos=argumentos), self.assertRaises(ValueError):
                secante(*argumentos)

    def test_integracion_con_pestana_y_tabla(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.withdraw()
        try:
            app = Controlador(root)
            vista = app.vista
            vista.nb_main.select(vista.tab_secante)
            app.calcular_secante()

            self.assertTrue(vista._resultado_secante.convergio)
            self.assertEqual(
                len(vista.secante_tabla.get_children()),
                len(vista._resultado_secante.iteraciones),
            )
            self.assertIn("xₙ₊₁ =", vista.secante_explicacion.cget("text"))
            self.assertEqual(vista.nb_main.index("current"), len(vista.modulos) - 1)
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()


if __name__ == "__main__":
    unittest.main()
