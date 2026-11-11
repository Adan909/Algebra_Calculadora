from unittest.mock import patch
import unittest

import vista.ventana_principal as ventana_principal
from modelo.operaciones_matrices import validar_misma_dimension


class WidgetFalso:
    def __init__(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass


class ContenedorFalso:
    def winfo_children(self):
        return []


class ScrollFalso:
    def __init__(self):
        self.scrollable_frame = ContenedorFalso()

    def observar_contenido(self):
        pass


class VistaFalsa:
    def __init__(self):
        self.scroll_matrices_ops = ScrollFalso()


class TestDimensionesMatrices(unittest.TestCase):
    def test_matrices_generadas_con_mismas_dimensiones_se_validan(self):
        vista = VistaFalsa()

        with patch.object(ventana_principal, "CeldaMatriz", WidgetFalso), patch.object(
            ventana_principal.tk, "Label", WidgetFalso
        ):
            ventana_principal.VentanaPrincipal.construir_matrices_ops(
                vista, 2, 3, 2, 3
            )

        self.assertEqual([len(fila) for fila in vista.mat_entries_a], [3, 3])
        self.assertEqual([len(fila) for fila in vista.mat_entries_b], [3, 3])
        self.assertTrue(
            validar_misma_dimension(vista.mat_entries_a, vista.mat_entries_b)
        )


if __name__ == "__main__":
    unittest.main()
