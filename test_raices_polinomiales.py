import tkinter as tk
import unittest

from controlador.controlador import Controlador
from modelo.biseccion import FuncionMatematica
from modelo.raices_polinomiales import encontrar_raices_reales


class PruebasRaicesPolinomiales(unittest.TestCase):
    def test_encuentra_raices_reales_simples_y_repetidas_distintas(self):
        resultado = encontrar_raices_reales(FuncionMatematica("x^3 - 3*x + 2"))

        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado.raices), 2)
        self.assertAlmostEqual(resultado.raices[0], -2)
        self.assertAlmostEqual(resultado.raices[1], 1)

    def test_polinomio_sin_raices_reales(self):
        resultado = encontrar_raices_reales(FuncionMatematica("x^2 + 1"))

        self.assertEqual(resultado.raices, ())

    def test_polinomio_cero_tiene_infinitas_raices(self):
        resultado = encontrar_raices_reales(FuncionMatematica("0*x"))

        self.assertIsNone(resultado.raices)

    def test_funcion_no_polinomica_no_informa_conteo_global(self):
        resultado = encontrar_raices_reales(FuncionMatematica("sin(x)"))

        self.assertIsNone(resultado)

    def test_navega_y_marca_raices_en_ambas_graficas(self):
        root = tk.Tk()
        root.geometry("1280x880")
        try:
            controlador = Controlador(root)
            vista = controlador.vista
            for pestaña, campo, graficar, contador, selector, canvas, navegar in (
                (
                    vista.tab_biseccion, vista.biseccion_funcion, controlador.graficar_biseccion,
                    vista.biseccion_cantidad_raices, vista.biseccion_raiz_seleccionada,
                    vista.biseccion_canvas, vista._navegar_raiz_biseccion,
                ),
                (
                    vista.tab_rf, vista.rf_funcion, controlador.graficar_rf,
                    vista.rf_cantidad_raices, vista.rf_raiz_seleccionada,
                    vista.rf_canvas, vista._navegar_raiz_rf,
                ),
            ):
                vista.nb_main.select(pestaña)
                root.update_idletasks()
                campo.delete(0, tk.END)
                campo.insert(0, "x^3 - 3*x + 2")
                graficar()
                root.update_idletasks()

                self.assertEqual(contador.cget("text"), "2")
                self.assertTrue(canvas.find_withtag("function_trace"))
                navegar(1)
                root.update_idletasks()
                self.assertIn("Raíz 1/2", selector.cget("text"))
                self.assertTrue(canvas.find_withtag("selected_root"))

                navegar(1)
                root.update_idletasks()
                self.assertIn("Raíz 2/2", selector.cget("text"))

                canvas.event_generate("<ButtonPress-1>", x=160, y=100, when="now")
                canvas.event_generate("<B1-Motion>", x=220, y=130, when="now")
                canvas.event_generate("<ButtonRelease-1>", x=220, y=130, when="now")
                root.update_idletasks()
                self.assertTrue(canvas.find_withtag("function_trace"))
                if pestaña == vista.tab_biseccion:
                    self.assertNotEqual(vista._desplazamiento_x_biseccion, 0)
                    self.assertNotEqual(vista._desplazamiento_y_biseccion, 0)
                    vista._reset_zoom_biseccion()
                    self.assertEqual(vista._desplazamiento_x_biseccion, 0)
                    self.assertEqual(vista._desplazamiento_y_biseccion, 0)
                else:
                    self.assertNotEqual(vista._desplazamiento_x_rf, 0)
                    self.assertNotEqual(vista._desplazamiento_y_rf, 0)
                    vista._reset_zoom_rf()
                    self.assertEqual(vista._desplazamiento_x_rf, 0)
                    self.assertEqual(vista._desplazamiento_y_rf, 0)

            vista.biseccion_funcion.delete(0, tk.END)
            vista.biseccion_funcion.insert(0, "sin(x)")
            controlador.graficar_biseccion()
            self.assertEqual(vista.biseccion_cantidad_raices.cget("text"), "N/D")
            self.assertIn("solo para polinomios", vista.biseccion_raiz_seleccionada.cget("text"))
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_trazo_se_recorta_en_el_borde_vertical_sin_perder_el_segmento(self):
        from vista.ventana_principal import VentanaPrincipal

        segmentos = VentanaPrincipal._segmentos_visibles_grafica(
            [(0.0, -2.0), (1.0, 0.0), (2.0, 2.0)], -1.0, 1.0
        )

        self.assertEqual(len(segmentos), 1)
        self.assertEqual(segmentos[0][0], (0.5, -1.0))
        self.assertEqual(segmentos[0][-1], (1.5, 1.0))


if __name__ == "__main__":
    unittest.main()
