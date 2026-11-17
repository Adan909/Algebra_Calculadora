import unittest
from fractions import Fraction

from modelo.solucionador import SolucionadorJacobi


class TestSolucionadorJacobi(unittest.TestCase):
    def test_resuelve_sistema_convergente_y_verifica_el_resultado(self):
        solucionador = SolucionadorJacobi(
            [[Fraction(4), Fraction(1)], [Fraction(2), Fraction(3)]],
            [Fraction(1), Fraction(2)],
        )

        solucionador.resolver()

        self.assertTrue(solucionador.es_valido)
        self.assertTrue(solucionador.clasificacion.startswith("Sistema Consistente"))
        self.assertAlmostEqual(float(solucionador.solucion[0]), 0.1, places=9)
        self.assertAlmostEqual(float(solucionador.solucion[1]), 0.6, places=9)
        self.assertTrue(all(
            error < Fraction(1, 10**9)
            for _, _, error in solucionador.verificar()
        ))
        self.assertTrue(any("Iteración" in mensaje for mensaje, _ in solucionador.historial))

    def test_rechaza_diagonal_nula(self):
        with self.assertRaisesRegex(ValueError, "diagonal"):
            SolucionadorJacobi([[0, 1], [1, 2]], [1, 2])

    def test_informa_cuando_no_converge(self):
        solucionador = SolucionadorJacobi([[1, 2], [2, 1]], [1, 1])

        solucionador.resolver()

        self.assertFalse(solucionador.es_valido)
        self.assertIn("no convergió", solucionador.clasificacion)
        self.assertEqual(solucionador.solucion, [])

    def test_requiere_matriz_cuadrada_y_vector_compatible(self):
        with self.assertRaises(ValueError):
            SolucionadorJacobi([[1, 2]], [1])

    def test_jacobi_tiene_modulo_y_entrada_de_datos_independientes(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        try:
            controlador = Controlador(root)
            vista = controlador.vista
            root.update()
            self.assertIn("Método de Jacobi", vista.modulos)
            self.assertEqual(len(vista.nb_main.tabs()), len(vista.modulos) + 1)
            self.assertEqual(
                vista.modulos.index("Método de Jacobi"),
                vista.modulos.index("Método de la Secante") + 1,
            )
            self.assertEqual(
                vista.nb_main.index(vista.tab_jacobi),
                vista.nb_main.index(vista.tab_secante) + 1,
            )
            self.assertNotIn("Jacobi", vista.selector_metodo["values"])
            self.assertIsNot(vista.jacobi_matriz_entries, vista.matriz_entries)

            vista._al_cambiar_modulo(
                vista.nb_main.index(vista.tab_jacobi), "Método de Jacobi",
            )
            root.update()
            vista.jacobi_spin_n.set(2)
            vista.construir_matriz_jacobi(2)
            valores = ((4, 1), (2, 3))
            for i, fila in enumerate(valores):
                for j, valor in enumerate(fila):
                    vista.jacobi_matriz_entries[i][j].delete(0, tk.END)
                    vista.jacobi_matriz_entries[i][j].insert(0, str(valor))
            for entrada, valor in zip(vista.jacobi_vector_entries, (1, 2)):
                entrada.delete(0, tk.END)
                entrada.insert(0, str(valor))
            for entrada, valor in zip(vista.jacobi_inicial_entries, ("1/2", "-1/2")):
                entrada.delete(0, tk.END)
                entrada.insert(0, valor)
            vista.jacobi_tolerancia.delete(0, tk.END)
            vista.jacobi_tolerancia.insert(0, "1e-8")
            vista.jacobi_max_iter.set(50)

            controlador.resolver_jacobi()

            self.assertEqual(vista._resultado_jacobi.max_iteraciones, 50)
            self.assertAlmostEqual(vista._resultado_jacobi.tolerancia, 1e-8)
            self.assertEqual(
                vista._resultado_jacobi.aproximacion_inicial,
                [Fraction(1, 2), Fraction(-1, 2)],
            )
            self.assertIn(
                "CONVERGIÓ", vista.jacobi_estado.cget("text"),
            )
            self.assertIn("[", vista.jacobi_aproximacion.cget("text"))
            self.assertGreater(len(vista.jacobi_tabla.get_children()), 0)
            self.assertGreater(len(vista.jacobi_canvas.find_withtag("residual_trace")), 0)
            self.assertEqual(vista.txt_solucion.get("1.0", tk.END).strip(), "")

            estado = vista._guardar_estado()
            self.assertEqual(estado["jacobi_mat"][0][0], "4")
            self.assertIn("jacobi_resultado", estado)
            vista.jacobi_matriz_entries[0][0].delete(0, tk.END)
            vista.jacobi_matriz_entries[0][0].insert(0, "99")
            vista._restaurar_estado(estado)
            self.assertEqual(vista.jacobi_matriz_entries[0][0].get(), "4")
            self.assertEqual(vista.jacobi_inicial_entries[0].get(), "1/2")
            self.assertEqual(vista.jacobi_tolerancia.get(), "1e-8")
            self.assertEqual(vista.jacobi_max_iter.get(), "50")
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()


if __name__ == "__main__":
    unittest.main()
