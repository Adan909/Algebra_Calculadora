import unittest
from fractions import Fraction

from modelo.operaciones_matrices import (
    multiplicar_matrices,
    multiplicar_matrices_con_pasos,
    restar_matrices,
    restar_matrices_con_pasos,
    sumar_matrices,
    sumar_matrices_con_pasos,
)


class TestPasosOperacionesMatrices(unittest.TestCase):
    def test_suma_muestra_calculo_de_cada_elemento_y_conserva_api(self):
        A = [[Fraction(1), Fraction(1, 2)], [Fraction(-2), Fraction(3)]]
        B = [[Fraction(2), Fraction(1, 2)], [Fraction(4), Fraction(-1)]]

        resultado, pasos = sumar_matrices_con_pasos(A, B)

        self.assertEqual(resultado, [[3, 1], [2, 2]])
        self.assertIn("c_1,2 = 1/2 + 1/2 = 1", pasos)
        self.assertEqual(sumar_matrices(A, B), resultado)

    def test_resta_muestra_calculo_de_cada_elemento_y_conserva_api(self):
        A = [[Fraction(1), Fraction(1, 2)], [Fraction(-2), Fraction(3)]]
        B = [[Fraction(2), Fraction(1, 2)], [Fraction(4), Fraction(-1)]]

        resultado, pasos = restar_matrices_con_pasos(A, B)

        self.assertEqual(resultado, [[-1, 0], [-6, 4]])
        self.assertIn("c_2,1 = -2 - 4 = -6", pasos)
        self.assertEqual(restar_matrices(A, B), resultado)

    def test_multiplicacion_muestra_producto_punto_y_conserva_api(self):
        A = [[1, 2, 3], [-1, 0, 2]]
        B = [[4, 1], [2, 3], [-1, 5]]

        resultado, pasos = multiplicar_matrices_con_pasos(A, B)

        self.assertEqual(resultado, [[5, 22], [-6, 9]])
        self.assertIn(
            "c_1,2 = (1 × 1) + (2 × 3) + (3 × 5) = 22",
            pasos,
        )
        self.assertEqual(multiplicar_matrices(A, B), resultado)


if __name__ == "__main__":
    unittest.main()
