import unittest

from modelo.biseccion import FuncionMatematica, biseccion, verificar_continuidad, ResultadoContinuidad


class PruebasBiseccion(unittest.TestCase):
    def test_acciones_de_calculo_aparecen_antes_de_las_entradas(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.geometry("1280x1000")
        try:
            vista = Controlador(root).vista
            root.update()

            self.assertIn(vista.btn_resolver, vista.barra_resolver_gauss.pack_slaves())
            self.assertLess(
                vista.barra_resolver_gauss.master.pack_slaves().index(
                    vista.barra_resolver_gauss
                ),
                vista.barra_resolver_gauss.master.pack_slaves().index(vista.scroll_matriz),
            )
            self.assertIn(
                vista.btn_calcular_vectores,
                vista.barra_calcular_vectores.pack_slaves(),
            )
            self.assertLess(
                vista.barra_calcular_vectores.master.pack_slaves().index(
                    vista.barra_calcular_vectores
                ),
                vista.barra_calcular_vectores.master.pack_slaves().index(
                    vista.scroll_vectores
                ),
            )
            self.assertLess(
                vista.barra_operaciones_matriz.master.pack_slaves().index(
                    vista.barra_operaciones_matriz
                ),
                vista.barra_operaciones_matriz.master.pack_slaves().index(
                    vista.scroll_matrices_ops
                ),
            )
            self.assertLess(
                vista.barra_calcular_romanos.master.pack_slaves().index(
                    vista.barra_calcular_romanos
                ),
                vista.barra_calcular_romanos.master.pack_slaves().index(
                    vista.scroll_romanos
                ),
            )
            self.assertIn(
                vista.btn_calcular_romanos,
                vista.barra_calcular_romanos.pack_slaves(),
            )
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_areas_de_entrada_y_resultado_ajustan_su_altura(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.geometry("1280x880")
        try:
            vista = Controlador(root).vista
            root.update()

            alto_matriz = int(vista.scroll_matriz.canvas.cget("height"))
            vista.construir_cuadricula(10, 10)
            root.update()
            self.assertGreater(
                int(vista.scroll_matriz.canvas.cget("height")),
                alto_matriz,
            )

            alto_inicial = int(vista.scroll_vectores.canvas.cget("height"))
            vista.construir_vectores(10, 10)
            root.update()
            alto_ampliado = int(vista.scroll_vectores.canvas.cget("height"))
            self.assertGreater(alto_ampliado, alto_inicial)

            alto_matrices = int(vista.scroll_matrices_ops.canvas.cget("height"))
            vista.construir_matrices_ops(10, 10, 10, 10)
            root.update()
            self.assertGreater(
                int(vista.scroll_matrices_ops.canvas.cget("height")),
                alto_matrices,
            )

            consola = vista.txt_resultados_conv
            vista._write(consola, "línea corta")
            root.update_idletasks()
            alto_corto = int(consola.cget("height"))

            vista._write(consola, "\n".join(f"paso {i}" for i in range(8)))
            root.update_idletasks()
            alto_largo = int(consola.cget("height"))
            self.assertGreater(alto_largo, alto_corto)
            self.assertLessEqual(alto_largo, 18)

            vista._write(consola, "")
            root.update_idletasks()
            self.assertLess(int(consola.cget("height")), alto_largo)
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_resultados_romanos_se_alinean_arriba_a_la_izquierda(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        try:
            vista = Controlador(root).vista
            self.assertEqual(vista.lbl_res_romano.cget("anchor"), "nw")
            self.assertEqual(vista.lbl_res_romano.cget("justify"), "left")
            self.assertEqual(str(vista.scroll_res_romano.cget("orient")), "horizontal")
            self.assertEqual(str(vista.scroll_res_normal.cget("orient")), "horizontal")
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_gauss_resultados_debajo_de_matriz_y_en_dos_paneles(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.geometry("1280x1000")
        try:
            app = Controlador(root)
            vista = app.vista
            root.update()

            tarjeta_matriz = vista.scroll_matriz.master.master
            tarjeta_resultados = vista.paneles_resultado_gauss.master.master
            diagnostico, historial = vista.paneles_resultado_gauss.winfo_children()

            self.assertLess(
                tarjeta_matriz.winfo_rooty() + tarjeta_matriz.winfo_height(),
                tarjeta_resultados.winfo_rooty(),
            )
            self.assertLess(diagnostico.winfo_rootx(), historial.winfo_rootx())
            self.assertGreater(diagnostico.winfo_width(), 0)
            self.assertGreater(historial.winfo_width(), 0)
            self.assertGreater(
                vista.txt_historial.winfo_width(),
                vista.txt_historial.winfo_reqwidth(),
            )
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_menu_de_metodos_vertical_a_la_izquierda(self):
        import tkinter as tk

        from controlador.controlador import Controlador

        root = tk.Tk()
        root.geometry("1280x880")
        try:
            app = Controlador(root)
            vista = app.vista
            root.update_idletasks()

            self.assertEqual(vista.nav_segmentada.orient, tk.VERTICAL)
            self.assertEqual(len(vista.nav_segmentada.botones), len(vista.modulos))
            self.assertTrue(all(
                boton.pack_info()["fill"] == tk.X
                for boton in vista.nav_segmentada.botones
            ))
            self.assertLess(
                vista.nav_segmentada.winfo_rootx(),
                vista.nb_main.winfo_rootx(),
            )

            vista.nav_segmentada.seleccionar(len(vista.modulos) - 1)
            root.update()
            self.assertEqual(vista.nb_main.index("current"), len(vista.modulos) - 1)
            vista.nb_main.select(0)
            root.update()
            self.assertEqual(vista.nav_segmentada.seleccionado, 0)
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

    def test_ultima_iteracion_seleccionada_permanece_visible(self):
        import tkinter as tk
        from controlador.controlador import Controlador

        root = tk.Tk()
        root.geometry("1280x880")
        try:
            app = Controlador(root)
            vista = app.vista
            vista.nb_main.select(vista.tab_biseccion)
            root.update_idletasks()

            for campo, valor in (
                (vista.biseccion_funcion, "x^2 - 2"),
                (vista.biseccion_a, "1"),
                (vista.biseccion_b, "2"),
                (vista.biseccion_error, "0.0000001"),
                (vista.biseccion_max_iter, "100"),
            ):
                campo.delete(0, tk.END)
                campo.insert(0, valor)

            app.calcular_biseccion()
            root.update_idletasks()

            seleccion = vista.biseccion_tabla.selection()
            self.assertTrue(seleccion)
            self.assertTrue(vista.biseccion_tabla.bbox(seleccion[0]))
            self.assertIn("Intervalo actual:", vista.biseccion_explicacion.cget("text"))
            self.assertIn("Punto medio:", vista.biseccion_explicacion.cget("text"))

            primera = vista._resultado_biseccion.iteraciones[0]
            vista.biseccion_selector.current(1)
            vista._seleccionar_iteracion_biseccion()
            root.update_idletasks()
            self.assertEqual(vista.biseccion_tabla.selection(), ("0",))
            self.assertTrue(vista.biseccion_tabla.bbox("0"))
            self.assertIn("Punto medio:\nc = (a + b) / 2", vista.biseccion_explicacion.cget("text"))
            self.assertIn(f"c = (a + b) / 2 = {primera.c:.10g}",
                          vista.biseccion_explicacion.cget("text"))
            self.assertEqual(vista.biseccion_explicacion.cget("fg"), vista.rf_explicacion.cget("fg"))
        finally:
            for callback in root.tk.call("after", "info"):
                root.after_cancel(callback)
            root.destroy()

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
        self.assertIsNotNone(resultado.continuidad)
        self.assertTrue(resultado.continuidad.es_continua)
        self.assertEqual(resultado.continuidad.tipo_funcion, "Polinómica")
        funcion = FuncionMatematica("x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10")
        for fila in resultado.iteraciones:
            with self.subTest(iteracion=fila.numero):
                self.assertAlmostEqual(fila.fb, funcion.evaluar(fila.b))

    # Prueba la función polinómica 3*x^3 + 2*x^2 - 1.54 y su continuidad en [0, 1].
    def test_continuidad_polinomica_usuario(self):
        analisis = verificar_continuidad("3*x^3 + 2*x^2 - 1.54", 0, 1)
        self.assertTrue(analisis.es_continua)
        self.assertEqual(analisis.tipo_funcion, "Polinómica")
        self.assertTrue(analisis.cambio_signo)
        self.assertTrue(analisis.aplica_bolzano)
        self.assertIn("✓ CUMPLIDA", analisis.condicion_1_evaluacion)
        self.assertIn("✓ CUMPLIDA", analisis.condicion_2_limites)
        self.assertIn("✓ CUMPLIDA", analisis.condicion_3_coincidencia)
        self.assertIn("TEOREMA DE BOLZANO", analisis.teorema_bolzano)

        # Cálculo de raíz mediante bisección
        res = biseccion("3*x^3 + 2*x^2 - 1.54", 0, 1, 0.01, 100)
        self.assertTrue(res.convergio)
        self.assertAlmostEqual(res.raiz, 0.62935, places=3)

    # Verifica detección de discontinuidades en funciones racionales o radicales fuera de dominio.
    def test_deteccion_discontinuidades(self):
        # 1/x en [-1, 1] presenta una discontinuidad en x = 0
        analisis_inv = verificar_continuidad("1/x", -1, 1)
        self.assertFalse(analisis_inv.es_continua)
        self.assertFalse(analisis_inv.aplica_bolzano)
        self.assertTrue(len(analisis_inv.puntos_discontinuidad) > 0)

        # sqrt(x) en [-2, 2] no está definida para x < 0
        analisis_sqrt = verificar_continuidad("sqrt(x)", -2, 2)
        self.assertFalse(analisis_sqrt.es_continua)
        self.assertFalse(analisis_sqrt.aplica_bolzano)

        # tan(x) en [1, 2] tiene asíntota vertical en pi/2 ≈ 1.5708
        analisis_tan = verificar_continuidad("tan(x)", 1, 2)
        self.assertFalse(analisis_tan.es_continua)
        self.assertFalse(analisis_tan.aplica_bolzano)

        # log(x) en [-0.5, 2] no está definida para x <= 0
        analisis_log = verificar_continuidad("log(x)", -0.5, 2)
        self.assertFalse(analisis_log.es_continua)
        self.assertFalse(analisis_log.aplica_bolzano)

    # Verifica funciones continuas sin cambio de signo.
    def test_continuidad_sin_cambio_signo(self):
        analisis = verificar_continuidad("x^2 + 1", 0, 2)
        self.assertTrue(analisis.es_continua)
        self.assertFalse(analisis.cambio_signo)
        self.assertFalse(analisis.aplica_bolzano)

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

    # Prueba funciones trigonométricas y logarítmicas en Regla Falsa y Bisección
    def test_trigonometricas_y_logaritmos(self):
        from modelo.regula_falsi import calcular_regula_falsi

        # 1. Logaritmo natural con ln(x) y log(x)
        f_ln = FuncionMatematica("ln(x) - 1")
        res_rf_ln = calcular_regula_falsi(f_ln, 2.0, 3.0, 0.001, 100)
        self.assertTrue(res_rf_ln.convergio)
        self.assertAlmostEqual(res_rf_ln.raiz, 2.71828, places=3)

        f_log = FuncionMatematica("log(x) - 1")
        res_rf_log = calcular_regula_falsi(f_log, 2.0, 3.0, 0.001, 100)
        self.assertTrue(res_rf_log.convergio)
        self.assertAlmostEqual(res_rf_log.raiz, 2.71828, places=3)

        # 2. Funciones trigonométricas con sin/sen, cos, tan/tg
        f_sen = FuncionMatematica("sen(x)")
        res_rf_sen = calcular_regula_falsi(f_sen, 3.0, 4.0, 0.001, 100)
        self.assertTrue(res_rf_sen.convergio)
        self.assertAlmostEqual(res_rf_sen.raiz, 3.14159, places=3)

        f_cos = FuncionMatematica("cos(x) - x")
        res_rf_cos = calcular_regula_falsi(f_cos, 0.5, 1.0, 0.001, 100)
        self.assertTrue(res_rf_cos.convergio)
        self.assertAlmostEqual(res_rf_cos.raiz, 0.73908, places=3)

        f_tg = FuncionMatematica("tg(x) - 1")
        res_rf_tg = calcular_regula_falsi(f_tg, 0.5, 1.0, 0.001, 100)
        self.assertTrue(res_rf_tg.convergio)
        self.assertAlmostEqual(res_rf_tg.raiz, 0.78539, places=3)

    # Informa falta de convergencia si se agota el límite antes de alcanzar la tolerancia.
    def test_maximo_de_iteraciones_informa_no_convergencia(self):
        resultado = biseccion("x^2 - 2", 1, 2, 1e-12, 1)
        self.assertFalse(resultado.convergio)
        self.assertEqual(len(resultado.iteraciones), 1)

    # Verifica la integración con el Controlador y la Vista gráfica.
    def test_integracion_controlador_vista(self):
        import tkinter as tk
        from controlador.controlador import Controlador

        root = tk.Tk()
        root.withdraw()
        try:
            app = Controlador(root)
            app.cargar_ejemplo_biseccion()
            self.assertIsNotNone(app.vista._resultado_biseccion)
            self.assertIsNotNone(app.vista._resultado_biseccion.continuidad)
            self.assertTrue(app.vista._resultado_biseccion.continuidad.es_continua)
            app.analizar_continuidad()
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()