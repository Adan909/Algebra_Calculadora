import unittest

from modelo.biseccion import FuncionMatematica, biseccion


class PruebasBiseccion(unittest.TestCase):
    # Confirma que el ejemplo de la guía se calcula con siete pasos y el error esperado.
    def test_ejemplo_del_profesor(self):
        resultado = biseccion(
            "x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10", 0.55, 1.1, 1, 100
        )
        self.assertTrue(resultado.convergio)
        self.assertEqual(len(resultado.iteraciones), 7)
        self.assertAlmostEqual(resultado.iteraciones[6].c, 0.760546875)
        self.assertAlmostEqual(resultado.iteraciones[6].error_relativo, 0.56497175)
        self.assertIsNone(resultado.iteraciones[0].error_relativo)
        funcion = FuncionMatematica("x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10")
        for fila in resultado.iteraciones:
            with self.subTest(iteracion=fila.numero):
                self.assertAlmostEqual(fila.fb, funcion.evaluar(fila.b))

    # Usa entradas textuales como las que obtiene el controlador desde los campos Tkinter.
    def test_otra_funcion(self):
        resultado = biseccion("x^2 - 2", "1", "2", "0.01", "100")
        self.assertTrue(resultado.convergio)
        self.assertAlmostEqual(resultado.raiz, 2 ** 0.5, places=4)

    # Una singularidad fuera de los puntos evaluados no invalida toda la expresión.
    def test_funcion_con_singularidad_fuera_del_intervalo(self):
        self.assertEqual(FuncionMatematica("1/x").evaluar(2), 0.5)

    # Comprueba el criterio alternativo que evita dividir por cero cuando c es cero.
    def test_punto_medio_cero_usa_error_alternativo(self):
        resultado = biseccion("x - 0.25", -1.5, 0.5, 0.01, 100)
        fila = resultado.iteraciones[1]
        self.assertEqual(fila.c, 0)
        self.assertEqual(fila.criterio_error, "ancho relativo del intervalo (alternativo para c = 0)")
        self.assertEqual(fila.error_relativo, 100)

    # Rechaza intervalos, tolerancias, funciones y límites de iteraciones inválidos.
    def test_validaciones(self):
        casos = (
            ("x^2 + 1", -1, 1, 1, 100),
            ("x", 1, 1, 1, 100),
            ("x", -1, 1, 0, 100),
            ("x", -1, 1, 1, 0),
            ("sqrt(x)", -1, 1, 1, 100),
            ("1/x", -1, 1, 1, 100),
            ("x +", -1, 1, 1, 100),
            ("__import__('os')", -1, 1, 1, 100),
            ("x", -1, 1, 1, "1.5"),
            ("x", -1, 1, 1, 100001),
        )
        for args in casos:
            with self.subTest(args=args), self.assertRaises(ValueError):
                biseccion(*args)

    # Informa falta de convergencia si se agota el límite antes de alcanzar la tolerancia.
    def test_maximo_de_iteraciones_informa_no_convergencia(self):
        resultado = biseccion("x^2 - 2", 1, 2, 1e-12, 1)
        self.assertFalse(resultado.convergio)
        self.assertEqual(len(resultado.iteraciones), 1)


if __name__ == "__main__":
    unittest.main()