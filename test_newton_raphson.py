import math
import unittest

from modelo.newton_raphson import derivar, newton_raphson
from modelo.biseccion import FuncionMatematica


class PruebasNewtonRaphson(unittest.TestCase):
    def test_derivada_polinomica_y_convergencia(self):
        funcion = FuncionMatematica("x^2 - 2")
        derivada = derivar(funcion)
        self.assertAlmostEqual(derivada.evaluar(2), 4)

        resultado = newton_raphson(funcion, "3/2", "1/1000", "20")
        self.assertTrue(resultado.convergio)
        self.assertAlmostEqual(resultado.raiz, 2 ** 0.5, places=6)
        self.assertGreater(len(resultado.iteraciones), 1)
        self.assertEqual(resultado.iteraciones[0].x, 1.5)
        self.assertAlmostEqual(
            resultado.iteraciones[0].siguiente_x,
            1.5 - (1.5 ** 2 - 2) / 3,
        )

    def test_derivadas_de_funciones_elementales(self):
        casos = (
            ("sin(x)", 0, 1),
            ("cos(x)", 0, 0),
            ("tan(x)", 0, 1),
            ("exp(x)", 0, 1),
            ("ln(x)", 2, 0.5),
            ("log(x)", 2, 1 / (2 * math.log(10))),
            ("log10(x)", 2, 1 / (2 * math.log(10))),
            ("sqrt(x)", 4, 0.25),
            ("asin(x)", 0, 1),
            ("acos(x)", 0, -1),
            ("atan(x)", 2, 0.2),
            ("abs(x)", 2, 1),
            ("abs(x)", -2, -1),
            ("x^2 / x", 2, 1),
            ("x^x", 2, 4 * (math.log(2) + 1)),
        )
        for expresion, x, esperado in casos:
            with self.subTest(expresion=expresion):
                self.assertAlmostEqual(
                    derivar(FuncionMatematica(expresion)).evaluar(x), esperado
                )

    def test_newton_distingue_logaritmo_natural_y_base_diez(self):
        casos = (("ln(x) - 1", "2.5", math.e), ("log(x) - 1", "9.5", 10))
        for expresion, inicial, raiz_esperada in casos:
            with self.subTest(expresion=expresion):
                resultado = newton_raphson(expresion, inicial, "1e-8", "20")
                self.assertTrue(resultado.convergio)
                self.assertAlmostEqual(resultado.raiz, raiz_esperada, places=7)

    def test_raiz_exacta_en_el_valor_inicial(self):
        resultado = newton_raphson("x - 2", "2", "0.01", "10")
        self.assertTrue(resultado.convergio)
        self.assertEqual(resultado.raiz, 2)
        self.assertEqual(resultado.iteraciones, ())
        resultado_pieza_a_pieza = newton_raphson("floor(x)", "0", "0.01", "10")
        self.assertTrue(resultado_pieza_a_pieza.convergio)
        self.assertEqual(resultado_pieza_a_pieza.raiz, 0)

    def test_derivada_cero(self):
        with self.assertRaisesRegex(ValueError, "derivada es cero"):
            newton_raphson("x^2 + 1", "0", "0.01", "10")

    def test_funciones_sin_derivada_admitida(self):
        for expresion in ("abs(x)", "floor(x)"):
            with self.subTest(expresion=expresion), self.assertRaises(ValueError):
                if expresion == "floor":
                    newton_raphson(expresion, "1", "0.01", "10")
                else:
                    derivar(FuncionMatematica(expresion)).evaluar(0)

    def test_validaciones_de_entradas(self):
        casos = (
            ("x", "no-numérico", 1, 10),
            ("x", "1/0", 1, 10),
            ("x", "1e309", 1, 10),
            ("1/x", 0, 1, 10),
            ("x", 1, 0, 10),
            ("x", 1, -1, 10),
            ("x", 1, 1, 0),
            ("x", 1, 1, "1.5"),
            ("x", 1, 1, 100001),
            ("x +", 1, 1, 10),
            ("__import__('os')", 1, 1, 10),
        )
        for argumentos in casos:
            with self.subTest(argumentos=argumentos), self.assertRaises(ValueError):
                newton_raphson(*argumentos)

    def test_agota_iteraciones_sin_converger(self):
        resultado = newton_raphson("x^2 - 2", "1", "1e-12", "1")
        self.assertFalse(resultado.convergio)
        self.assertEqual(len(resultado.iteraciones), 1)

    def test_integracion_con_pestana_y_tabla_de_iteraciones(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.withdraw()
        try:
            app = Controlador(root)
            vista = app.vista
            vista.nb_main.select(vista.tab_newton)
            for campo, valor in (
                (vista.newton_funcion, "x^2 - 2"),
                (vista.newton_x_inicial, "3/2"),
                (vista.newton_error, "1/1000"),
                (vista.newton_max_iter, "20"),
            ):
                campo.delete(0, tk.END)
                campo.insert(0, valor)

            app.calcular_newton_raphson()

            self.assertTrue(vista._resultado_newton_raphson.convergio)
            self.assertEqual(
                len(vista.newton_tabla.get_children()),
                len(vista._resultado_newton_raphson.iteraciones),
            )
            self.assertIn("x(i+1) = x(i)", vista.newton_explicacion.cget("text"))
            self.assertIn("f'(x)", vista.newton_explicacion.cget("text"))
            self.assertIn("Sustitución: x(i+1)", vista.newton_explicacion.cget("text"))

            for campo, valor in (
                (vista.rf_funcion, "x^3 + 4*x^2 - 10"),
                (vista.rf_a, "1"),
                (vista.rf_b, "2"),
                (vista.rf_error, "0.1"),
                (vista.rf_max_iter, "50"),
            ):
                campo.delete(0, tk.END)
                campo.insert(0, valor)
            app.calcular_rf()
            texto_rf = vista.rf_explicacion.cget("text")
            self.assertIn("Falsa Posición:\n", texto_rf)
            self.assertIn("\nxr = xu - (f(xu)*(xl - xu))/(f(xl) - f(xu)) =", texto_rf)

            app.graficar_newton_raphson()
            root.update_idletasks()
            self.assertEqual(vista.newton_cantidad_raices.cget("text"), "2")
            self.assertTrue(vista.newton_canvas.find_withtag("function_trace"))
            vista._navegar_raiz_newton(1)
            self.assertIn("Raíz 1/2", vista.newton_raiz_seleccionada.cget("text"))
            self.assertTrue(vista.newton_canvas.find_withtag("selected_root"))

            vista.newton_selector.current(0)
            vista._seleccionar_iteracion_newton_raphson()
            self.assertTrue(vista.newton_canvas.find_withtag("newton_tangent"))
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_demostracion_continuidad_analiza_funcion_y_derivada(self):
        import tkinter as tk
        from unittest.mock import patch

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.withdraw()
        try:
            app = Controlador(root)
            vista = app.vista
            with patch.object(vista, "mostrar_demostracion_continuidad") as mostrar:
                app.analizar_continuidad_newton_raphson()

            primitiva, = mostrar.call_args.args
            derivada = mostrar.call_args.kwargs["resultado_derivada"]
            self.assertTrue(primitiva.es_continua)
            self.assertTrue(derivada.es_continua)
            self.assertEqual((primitiva.a, primitiva.b), (derivada.a, derivada.b))
            self.assertAlmostEqual(
                FuncionMatematica(
                    mostrar.call_args.kwargs["expresion_derivada"]
                ).evaluar(1.5),
                3,
            )
            vista.mostrar_demostracion_continuidad(
                primitiva,
                resultado_derivada=derivada,
                expresion_derivada=mostrar.call_args.kwargs["expresion_derivada"],
            )
            root.update_idletasks()
            modal = next(
                child for child in root.winfo_children()
                if isinstance(child, tk.Toplevel)
            )

            def recorrer(widget):
                yield widget
                for hijo in widget.winfo_children():
                    yield from recorrer(hijo)

            texto = next(
                widget for widget in recorrer(modal)
                if isinstance(widget, tk.Text)
            )
            self.assertIn(
                "ANÁLISIS DE CONTINUIDAD DE LA DERIVADA",
                texto.get("1.0", tk.END),
            )
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()


if __name__ == "__main__":
    unittest.main()
