import unittest
from fractions import Fraction

from modelo.solucionador import SolucionadorGaussSeidel


class TestSolucionadorGaussSeidel(unittest.TestCase):
    def test_resuelve_sistema_convergente_y_verifica_el_resultado(self):
        solucionador = SolucionadorGaussSeidel(
            [[Fraction(4), Fraction(1)], [Fraction(2), Fraction(3)]],
            [Fraction(1), Fraction(2)],
        )
        solucionador.resolver()

        self.assertTrue(solucionador.es_valido)
        self.assertIn("Gauss-Seidel", solucionador.clasificacion)
        self.assertAlmostEqual(float(solucionador.solucion[0]), 0.1, places=9)
        self.assertAlmostEqual(float(solucionador.solucion[1]), 0.6, places=9)
        self.assertTrue(all(
            error < Fraction(1, 10**9)
            for _, _, error in solucionador.verificar()
        ))

    def test_rechaza_diagonal_nula(self):
        with self.assertRaisesRegex(ValueError, "diagonal"):
            SolucionadorGaussSeidel([[0, 1], [1, 2]], [1, 2])

    def test_requiere_matriz_cuadrada_y_vector_compatible(self):
        with self.assertRaises(ValueError):
            SolucionadorGaussSeidel([[1, 2]], [1])

    def test_tiene_modulo_y_datos_independientes_en_la_vista(self):
        import tkinter as tk
        from controlador.controlador import Controlador

        root = tk.Tk()
        try:
            controlador = Controlador(root)
            vista = controlador.vista
            root.update()
            self.assertIn("Método de Gauss-Seidel", vista.modulos)
            self.assertIn("Método de Gauss-Seidel", vista.nb_main.tab(vista.tab_gauss_seidel)["text"])
            self.assertIsNot(
                vista.gauss_seidel_matriz_entries,
                vista.jacobi_matriz_entries,
            )

            vista._al_cambiar_modulo(
                vista.nb_main.index(vista.tab_gauss_seidel),
                "Método de Gauss-Seidel",
            )
            vista.gauss_seidel_spin_n.set(2)
            vista.construir_matriz_gauss_seidel(2)
            valores = ((4, 1), (2, 3))
            for i, fila in enumerate(valores):
                for j, valor in enumerate(fila):
                    vista.gauss_seidel_matriz_entries[i][j].delete(0, tk.END)
                    vista.gauss_seidel_matriz_entries[i][j].insert(0, str(valor))
            for entrada, valor in zip(vista.gauss_seidel_vector_entries, (1, 2)):
                entrada.delete(0, tk.END)
                entrada.insert(0, str(valor))
            for entrada, valor in zip(vista.gauss_seidel_inicial_entries, ("1/2", "-1/2")):
                entrada.delete(0, tk.END)
                entrada.insert(0, valor)
            vista.gauss_seidel_tolerancia.delete(0, tk.END)
            vista.gauss_seidel_tolerancia.insert(0, "1e-8")
            vista.gauss_seidel_max_iter.set(50)

            controlador.resolver_gauss_seidel()

            self.assertEqual(vista._resultado_gauss_seidel.max_iteraciones, 50)
            self.assertAlmostEqual(vista._resultado_gauss_seidel.tolerancia, 1e-8)
            self.assertEqual(
                vista._resultado_gauss_seidel.aproximacion_inicial,
                [Fraction(1, 2), Fraction(-1, 2)],
            )
            self.assertIn("CONVERGIÓ", vista.gauss_seidel_estado.cget("text"))
            self.assertGreater(len(vista.gauss_seidel_tabla.get_children()), 0)
            self.assertGreater(
                len(vista.gauss_seidel_canvas.find_withtag("residual_trace")),
                0,
            )

            estado = vista._guardar_estado()
            vista.gauss_seidel_matriz_entries[0][0].delete(0, tk.END)
            vista.gauss_seidel_matriz_entries[0][0].insert(0, "99")
            vista._restaurar_estado(estado)
            self.assertEqual(vista.gauss_seidel_matriz_entries[0][0].get(), "4")
            self.assertEqual(vista.gauss_seidel_inicial_entries[0].get(), "1/2")
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()


if __name__ == "__main__":
    unittest.main()
