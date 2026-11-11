from vista.ventana_principal import VentanaPrincipal
from modelo.solucionador import SolucionadorGauss, SolucionadorGaussJordan, SolucionadorLU
from modelo.biseccion import FuncionMatematica, biseccion, verificar_continuidad, ResultadoContinuidad
from modelo.regula_falsi import calcular_regula_falsi
from modelo.newton_raphson import newton_raphson
# Importar funciones de modelo
from modelo.matriz import formatear_fraccion, formatear_matriz
from modelo.vectores import (
    sumar_vectores,
    restar_vectores,
    multiplicar_vector_escalar,
    es_combinacion_lineal
)
from modelo.operaciones_matrices import (
    sumar_matrices,
    restar_matrices,
    multiplicar_matriz_escalar,
    multiplicar_matrices,
    determinante_sarrus,
    determinante_cofactores,
    invertir_matriz,
    invertir_matriz_con_pasos,
    factorizacion_lu,
    factorizacion_lu_con_pasos
)
from modelo.conversiones import decimal_a_base, base_a_decimal
from modelo.romanos import (
    operar_lista_romanos,
    evaluar_expresion_romana,
    romano_a_arabigo,
    arabigo_a_romano
)

class Controlador:
    def __init__(self, root):
        self.vista = VentanaPrincipal(root, self)

    # ==========================================================
    # MÉTODO DE BISECCIÓN
    # ==========================================================
    def calcular_biseccion(self):
        try:
            # El modelo interpreta la función y valida parámetros antes de producir resultados.
            expresion = FuncionMatematica(self.vista.biseccion_funcion.get())
            resultado = biseccion(
                expresion,
                self.vista.biseccion_a.get().strip(),
                self.vista.biseccion_b.get().strip(),
                self.vista.biseccion_error.get().strip(),
                self.vista.biseccion_max_iter.get().strip(),
            )
        except (ValueError, OverflowError) as error:
            # Los errores de entrada vuelven a la vista sin interrumpir el ciclo de Tkinter.
            self.vista.mostrar_error("Entrada no válida", str(error))
            return
        self.vista.mostrar_resultado_biseccion(resultado, expresion)

    def graficar_biseccion(self):
        try:
            funcion = FuncionMatematica(self.vista.biseccion_funcion.get())
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Función no válida", str(error))
            return
        self.vista.mostrar_grafica_biseccion(funcion)

    def analizar_continuidad(self):
        try:
            funcion_str = self.vista.biseccion_funcion.get().strip()
            a_str = self.vista.biseccion_a.get().strip()
            b_str = self.vista.biseccion_b.get().strip()
            if not funcion_str:
                self.vista.mostrar_error("Entrada no válida", "Por favor ingrese una función matemática.")
                return
            expresion = FuncionMatematica(funcion_str)
            resultado_cont = expresion.analizar_continuidad(a_str, b_str)
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Error de Continuidad", str(error))
            return
        self.vista.mostrar_demostracion_continuidad(resultado_cont)

    def cargar_ejemplo_biseccion(self):
        # Mantiene el ejemplo como datos de entrada: la tabla siempre se calcula con el algoritmo.
        valores = (
            (self.vista.biseccion_funcion, "x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10"),
            (self.vista.biseccion_a, "0.55"),
            (self.vista.biseccion_b, "1.1"),
            (self.vista.biseccion_error, "1"),
            (self.vista.biseccion_max_iter, "100"),
        )
        for entrada, valor in valores:
            entrada.delete(0, "end")
            entrada.insert(0, valor)
        self.calcular_biseccion()

    def calcular_rf(self):
        """Ejecuta el método de Regula Falsi capturando los datos de la vista y evaluando continuidad."""
        try:
            func_str = self.vista.rf_funcion.get().strip()
            a_str = self.vista.rf_a.get().strip()
            b_str = self.vista.rf_b.get().strip()
            a = float(a_str)
            b = float(b_str)
            error_esperado = float(self.vista.rf_error.get())
            max_iter = int(self.vista.rf_max_iter.get())

            if not func_str:
                self.vista.mostrar_error("Error", "Debes ingresar una función.")
                return

            from modelo.biseccion import FuncionMatematica 
            funcion = FuncionMatematica(func_str)

            # 1. Analizar continuidad automáticamente usando las variables de texto
            resultado_cont = funcion.analizar_continuidad(a_str, b_str)

            # 2. Llamar al modelo de Regula Falsi
            from modelo.regula_falsi import calcular_regula_falsi
            resultado = calcular_regula_falsi(funcion, a, b, error_esperado, max_iter)

            # 3. Adjuntar el análisis de continuidad al resultado final
            resultado.continuidad = resultado_cont

            # 4. Enviar resultados a la vista
            self.vista.mostrar_resultado_rf(resultado, funcion)

        except ValueError as e:
            self.vista.mostrar_error("Error de Valor", str(e))
        except Exception as e:
            self.vista.mostrar_error("Error de Cálculo", f"Verifica la función y los intervalos: {str(e)}")

    def graficar_rf(self):
        try:
            funcion = FuncionMatematica(self.vista.rf_funcion.get())
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Función no válida", str(error))
            return
        self.vista.mostrar_grafica_rf(funcion)

    def analizar_continuidad_rf(self):
        try:
            # 1. Leer los campos de la pestaña de Regula Falsi
            funcion_str = self.vista.rf_funcion.get().strip()
            a_str = self.vista.rf_a.get().strip()
            b_str = self.vista.rf_b.get().strip()
            
            if not funcion_str:
                self.vista.mostrar_error("Entrada no válida", "Por favor ingrese una función matemática.")
                return
                
            # 2. Crear la expresión matemática y analizar (igual que en Bisección)
            from modelo.biseccion import FuncionMatematica # Solo por si acaso no está importada
            expresion = FuncionMatematica(funcion_str)
            resultado_cont = expresion.analizar_continuidad(a_str, b_str)
            
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Error de Continuidad", str(error))
            return
            
        # 3. Mandar el resultado al mismo modal que ya usas
        self.vista.mostrar_demostracion_continuidad(resultado_cont)

    def cargar_ejemplo_rf(self):
        """Carga un ejemplo predefinido para Regula Falsi."""
        self.vista.rf_funcion.delete(0, 'end')
        self.vista.rf_funcion.insert(0, "x^3 + 4*x^2 - 10")
        
        self.vista.rf_a.delete(0, 'end')
        self.vista.rf_a.insert(0, "1")
        
        self.vista.rf_b.delete(0, 'end')
        self.vista.rf_b.insert(0, "2")
        
        self.vista.rf_error.delete(0, 'end')
        self.vista.rf_error.insert(0, "0.1")
        
        self.vista.rf_max_iter.delete(0, 'end')
        self.vista.rf_max_iter.insert(0, "50")

    def calcular_newton_raphson(self):
        try:
            funcion = FuncionMatematica(self.vista.newton_funcion.get())
            resultado = newton_raphson(
                funcion,
                self.vista.newton_x_inicial.get().strip(),
                self.vista.newton_error.get().strip(),
                self.vista.newton_max_iter.get().strip(),
            )
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Entrada no válida", str(error))
            return
        self.vista.mostrar_resultado_newton_raphson(resultado, funcion)

    def graficar_newton_raphson(self):
        try:
            funcion = FuncionMatematica(self.vista.newton_funcion.get())
        except (ValueError, OverflowError) as error:
            self.vista.mostrar_error("Función no válida", str(error))
            return
        self.vista.mostrar_grafica_newton_raphson(funcion)

    def cargar_ejemplo_newton_raphson(self):
        valores = (
            (self.vista.newton_funcion, "x^2 - 2"),
            (self.vista.newton_x_inicial, "1.5"),
            (self.vista.newton_error, "0.0001"),
            (self.vista.newton_max_iter, "20"),
        )
        for entrada, valor in valores:
            entrada.delete(0, "end")
            entrada.insert(0, valor)
        self.calcular_newton_raphson()

    def limpiar_biseccion(self):
        self.vista.limpiar_biseccion()

    # ==========================================================
    # SISTEMAS DE ECUACIONES (GAUSS)
    # ==========================================================
    def generar_cuadricula(self):
        try:
            m = int(self.vista.spin_m.get())
            n = int(self.vista.spin_n.get())
            
            if not (1 <= m <= 10) or not (1 <= n <= 10):
                self.vista.mostrar_error("Error", "Las dimensiones m y n deben estar entre 1 y 10.")
                return
                
            self.vista.construir_cuadricula(m, n)
            
        except ValueError:
            self.vista.mostrar_error("Error de entrada", "Por favor, ingrese valores enteros válidos para m y n.")
            
    def cargar_ejemplo(self, tipo):
        if tipo == "inversa":
            self.vista.nb_main.select(self.vista.tab_vectorial)
            self.vista.nb_vectorial.select(1)
            self.cargar_ejemplo_matrices("inv_2x2")
            return

        if tipo == "unica":
            A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
            b = [8, -11, -3]
            self.vista.metodo.set("Gauss")
        elif tipo == "lu":
            A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
            b = [8, -11, -3]
            self.vista.metodo.set("Factorización LU")
        elif tipo == "infinitas":
            A = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
            b = [1, 2, 3]
            self.vista.metodo.set("Gauss")
        elif tipo == "inconsistente":
            A = [[1, 2, 3], [1, 2, 3], [2, 1, 1]]
            b = [4, 5, 1]
            self.vista.metodo.set("Gauss")
            
        m = len(A)
        n = len(A[0])
        self.vista.spin_m.set(m)
        self.vista.spin_n.set(n)
        self.vista.construir_cuadricula(m, n)
        
        for i in range(m):
            for j in range(n):
                self.vista.matriz_entries[i][j].delete(0, 'end')
                self.vista.matriz_entries[i][j].insert(0, str(A[i][j]))
            self.vista.vector_entries[i].delete(0, 'end')
            self.vista.vector_entries[i].insert(0, str(b[i]))

    def cargar_ejemplo_matrices(self, tipo):
        if tipo == "inv_2x2":
            A = [[4, 7], [2, 6]]
            B = [[1, 0], [0, 1]]
        elif tipo == "inv_3x3":
            A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
            B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        elif tipo == "inv_det_uno":
            A = [[3, 1], [2, 1]]
            B = [[1, 0], [0, 1]]
        elif tipo == "lu_3x3":
            A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
            B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        elif tipo == "lu_pivoteo":
            A = [[0, 2, 3], [4, 5, 6], [7, 8, 9]]
            B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        else:
            return

        filas_a = len(A)
        columnas_a = len(A[0])
        filas_b = len(B)
        columnas_b = len(B[0])

        self.vista.spin_fa.set(filas_a)
        self.vista.spin_ca.set(columnas_a)
        self.vista.spin_fb.set(filas_b)
        self.vista.spin_cb.set(columnas_b)

        self.vista.construir_matrices_ops(filas_a, columnas_a, filas_b, columnas_b)

        for i in range(filas_a):
            for j in range(columnas_a):
                self.vista.mat_entries_a[i][j].delete(0, 'end')
                self.vista.mat_entries_a[i][j].insert(0, str(A[i][j]))

        for i in range(filas_b):
            for j in range(columnas_b):
                self.vista.mat_entries_b[i][j].delete(0, 'end')
                self.vista.mat_entries_b[i][j].insert(0, str(B[i][j]))

        # Ejecutar operación correspondiente según el ejemplo
        if tipo.startswith("lu_"):
            self.operar_matrices("lu_a")
        else:
            self.operar_matrices("inversa_a")

    def resolver_sistema(self):
        try:
            m = len(self.vista.matriz_entries)
            n = len(self.vista.matriz_entries[0])
            
            from fractions import Fraction
            A = []
            for i in range(m):
                fila = []
                for j in range(n):
                    val = Fraction(self.vista.matriz_entries[i][j].get())
                    fila.append(val)
                A.append(fila)
                
            b = []
            for i in range(m):
                val = Fraction(self.vista.vector_entries[i].get())
                b.append(val)
                
        except ValueError:
            self.vista.mostrar_error("Error de Valor", "Todos los coeficientes deben ser números reales válidos.")
            return

        if self.vista.metodo.get() == "Gauss-Jordan":
            solucionador = SolucionadorGaussJordan(A, b)
        elif self.vista.metodo.get() == "Factorización LU":
            if m != n:
                self.vista.mostrar_error(
                    "Error de Dimensión",
                    f"La factorización LU requiere una matriz de coeficientes cuadrada (m = n).\n"
                    f"Dimensión actual: {m} ecuaciones × {n} incógnitas."
                )
                return
            solucionador = SolucionadorLU(A, b)
        else:
            solucionador = SolucionadorGauss(A, b)
        solucionador.resolver()
        
        clasificacion = solucionador.clasificacion
        texto_sol = ""
        texto_ver = ""
        
        if solucionador.es_valido:
            texto_sol = "Vector de Solución:\n"
            for i, val in enumerate(solucionador.solucion):
                texto_sol += f"x{i+1} = {formatear_fraccion(val)}\n"
                
            errores = solucionador.verificar()
            if errores:
                texto_ver = "Verificación (Ecuaciones originales):\n"
                for i, (calc, orig, err) in enumerate(errores):
                    texto_ver += f"Eq {i+1}: valor calculado = {formatear_fraccion(calc)}, valor original = {formatear_fraccion(orig)} | Error abs: {formatear_fraccion(err)}\n"
        else:
            texto_sol = "No hay una solución única."
            texto_ver = "Verificación no aplicable."
            
        self.vista.actualizar_resumen(clasificacion, texto_sol, texto_ver)
        
        texto_historial = ""
        for paso, item in enumerate(solucionador.historial):
            if isinstance(item, tuple) and len(item) == 2:
                mensaje, estado = item
                texto_historial += f"--- Paso {paso + 1}: {mensaje} ---\n"
                if isinstance(estado, list) and estado and isinstance(estado[0], list):
                    texto_historial += formatear_matriz(estado)
                elif isinstance(estado, str):
                    texto_historial += estado.rstrip() + "\n"
                elif isinstance(estado, list) and estado and not isinstance(estado[0], list):
                    texto_historial += "[ " + ", ".join(formatear_fraccion(v) for v in estado) + " ]\n"
            elif isinstance(item, str):
                texto_historial += f"--- Paso {paso + 1} ---\n{item}\n"
            texto_historial += "\n"
            
        self.vista.actualizar_historial(texto_historial)

    # ==========================================================
    # VECTORIALES Y MATRICIALES
    # ==========================================================
    def generar_vectores(self):
        try:
            dimension = int(self.vista.spin_dim_v.get())
            cantidad = int(self.vista.spin_cant_v.get())
            if not 1 <= dimension <= 10 or not 1 <= cantidad <= 10:
                raise ValueError
        except ValueError:
            self.vista.mostrar_error("Error", "Dimensiones deben estar entre 1 y 10.")
            return

        self.vista.construir_vectores(dimension, cantidad)

    def formatear_vector(self, vector):
        valores = [formatear_fraccion(valor) for valor in vector]
        return "(" + ", ".join(valores) + ")"

    def operar_vectores(self):
        try:
            from fractions import Fraction
            vectores = []
            for fila in self.vista.vec_entries:
                vector = [Fraction(entry.get()) for entry in fila]
                vectores.append(vector)

            b = [Fraction(entry.get()) for entry in self.vista.vec_b_entries]
            texto = ""

            if len(vectores) >= 2:
                suma = vectores[0]
                for i in range(1, len(vectores)):
                    suma = sumar_vectores(suma, vectores[i])
                texto += "SUMA DE VECTORES\n"
                texto += self.formatear_vector(suma) + "\n\n"

                resta = restar_vectores(vectores[0], vectores[1])
                texto += "RESTA v1 - v2\n"
                texto += self.formatear_vector(resta) + "\n\n"

            escalar = Fraction(self.vista.entrada_escalar_vector.get())
            if len(vectores) >= 1:
                multiplicado = multiplicar_vector_escalar(vectores[0], escalar)
                texto += f"MULTIPLICACIÓN {escalar} * v1\n"
                texto += self.formatear_vector(multiplicado) + "\n\n"

            es_combinacion, escalares = es_combinacion_lineal(vectores, b)
            texto += "COMBINACIÓN LINEAL\n"
            if es_combinacion:
                texto += "b SÍ es combinación lineal de los vectores dados.\n"
                texto += "Posibles escalares encontrados:\n"
                for i, valor in enumerate(escalares):
                    texto += f"c{i + 1} = {formatear_fraccion(valor)}\n"
                
                texto += "\nComprobación:\n"
                for i, vector in enumerate(vectores):
                    texto += f"{formatear_fraccion(escalares[i])} * v{i + 1}"
                    if i < len(vectores) - 1:
                        texto += " + "
                texto += " = b\n"
            else:
                texto += "b NO es combinación lineal de los vectores proporcionados.\n"

            self.vista.mostrar_resultado_vectores(texto)
        except ValueError:
            self.vista.mostrar_error("Error de valor", "Todos los elementos deben ser números válidos.")
            
    def generar_matrices_ops(self):
        try:
            filas_a = int(self.vista.spin_fa.get())
            columnas_a = int(self.vista.spin_ca.get())
            filas_b = int(self.vista.spin_fb.get())
            columnas_b = int(self.vista.spin_cb.get())
            dimensiones = [filas_a, columnas_a, filas_b, columnas_b]
            if not all(valor >= 1 for valor in dimensiones):
                raise ValueError
        except ValueError:
            self.vista.mostrar_error("Error", "Las dimensiones deben ser números enteros mayores o iguales a 1.")
            return

        self.vista.construir_matrices_ops(filas_a, columnas_a, filas_b, columnas_b)

    def leer_matriz(self, entradas):
        from fractions import Fraction
        try:
            return [[Fraction(entry.get().strip()) for entry in fila] for fila in entradas]
        except (ValueError, ZeroDivisionError):
            raise ValueError("Todos los elementos de la matriz deben ser números reales válidos (enteros o fracciones como a/b).")

    def formatear_matriz_resultado(self, matriz):
        texto = ""
        for fila in matriz:
            texto += "[ "
            for valor in fila:
                texto += f"{formatear_fraccion(valor):>8} "
            texto += "]\n"
        return texto

    def operar_matrices(self, operacion):
        try:
            if operacion in ("suma", "resta", "multiplicacion"):
                A = self.leer_matriz(self.vista.mat_entries_a)
                B = self.leer_matriz(self.vista.mat_entries_b)
                if operacion == "suma":
                    resultado = sumar_matrices(A, B)
                    titulo = "A + B"
                elif operacion == "resta":
                    resultado = restar_matrices(A, B)
                    titulo = "A − B"
                else:
                    resultado = multiplicar_matrices(A, B)
                    titulo = "A × B"
                texto = f"RESULTADO: {titulo}\n\n" + self.formatear_matriz_resultado(resultado)

            elif operacion == "escalar":
                A = self.leer_matriz(self.vista.mat_entries_a)
                from fractions import Fraction
                escalar = Fraction(self.vista.entrada_escalar_mat.get().strip())
                resultado = multiplicar_matriz_escalar(A, escalar)
                titulo = f"{formatear_fraccion(escalar)}A"
                texto = f"RESULTADO: {titulo}\n\n" + self.formatear_matriz_resultado(resultado)

            elif operacion in ("determinante_sarrus", "determinante_cofactores"):
                A = self.leer_matriz(self.vista.mat_entries_a)
                if operacion == "determinante_sarrus":
                    resultado, pasos = determinante_sarrus(A)
                    metodo = "REGLA DE SARRUS"
                else:
                    resultado, pasos = determinante_cofactores(A)
                    metodo = "EXPANSIÓN POR COFACTORES"
                separador = "=" * 58
                texto = f"DETERMINANTE DE A  |  {metodo}\n{separador}\n"
                texto += f"MATRIZ A ({len(A)}×{len(A[0])}):\n"
                texto += self.formatear_matriz_resultado(A)
                texto += f"\nDESARROLLO PASO A PASO\n{'-' * 58}\n"
                texto += "\n".join(pasos)
                texto += f"\n\n{separador}\n"
                texto += f"RESULTADO FINAL:  det(A) = {formatear_fraccion(resultado)}\n"
                texto += separador + "\n"

            elif operacion == "inversa_a":
                filas_a = len(self.vista.mat_entries_a)
                columnas_a = len(self.vista.mat_entries_a[0]) if filas_a > 0 else 0
                if filas_a == 0 or columnas_a == 0 or filas_a != columnas_a:
                    self.vista.mostrar_error(
                        "Error de Dimensión",
                        f"Para calcular la matriz inversa, la matriz debe ser cuadrada (n × n).\n"
                        f"Dimensión actual de la Matriz A: {filas_a} fila(s) × {columnas_a} columna(s)."
                    )
                    return

                if filas_a > 10:
                    confirmado = self.vista.confirmar_proceso_inversa_grande(filas_a, "Matriz A")
                    if not confirmado:
                        return

                A = self.leer_matriz(self.vista.mat_entries_a)
                try:
                    self.vista.root.config(cursor="watch")
                    self.vista.root.update_idletasks()
                    inversa, pasos = invertir_matriz_con_pasos(A)
                finally:
                    self.vista.root.config(cursor="")

                titulo = f"INVERSA DE LA MATRIZ A (A⁻¹) — ORDEN {filas_a}×{columnas_a}"
                texto = f"==========================================================\n"
                texto += f"RESULTADO: {titulo}\n"
                texto += f"==========================================================\n\n"
                texto += "MATRIZ INVERSA A⁻¹:\n"
                texto += self.formatear_matriz_resultado(inversa) + "\n"

                comprobacion = multiplicar_matrices(A, inversa)
                texto += "COMPROBACIÓN DE IDENTIDAD ( A × A⁻¹ = I ):\n"
                texto += self.formatear_matriz_resultado(comprobacion) + "\n"

                texto += "----------------------------------------------------------\n"
                texto += "DESGLOSE DE OPERACIONES ELEMENTALES POR FILA (GAUSS-JORDAN):\n"
                texto += "----------------------------------------------------------\n"
                texto += "\n".join(pasos) + "\n"

            elif operacion == "inversa_b":
                filas_b = len(self.vista.mat_entries_b)
                columnas_b = len(self.vista.mat_entries_b[0]) if filas_b > 0 else 0
                if filas_b == 0 or columnas_b == 0 or filas_b != columnas_b:
                    self.vista.mostrar_error(
                        "Error de Dimensión",
                        f"Para calcular la matriz inversa, la matriz debe ser cuadrada (n × n).\n"
                        f"Dimensión actual de la Matriz B: {filas_b} fila(s) × {columnas_b} columna(s)."
                    )
                    return

                if filas_b > 10:
                    confirmado = self.vista.confirmar_proceso_inversa_grande(filas_b, "Matriz B")
                    if not confirmado:
                        return

                B = self.leer_matriz(self.vista.mat_entries_b)
                try:
                    self.vista.root.config(cursor="watch")
                    self.vista.root.update_idletasks()
                    inversa, pasos = invertir_matriz_con_pasos(B)
                finally:
                    self.vista.root.config(cursor="")

                titulo = f"INVERSA DE LA MATRIZ B (B⁻¹) — ORDEN {filas_b}×{columnas_b}"
                texto = f"==========================================================\n"
                texto += f"RESULTADO: {titulo}\n"
                texto += f"==========================================================\n\n"
                texto += "MATRIZ INVERSA B⁻¹:\n"
                texto += self.formatear_matriz_resultado(inversa) + "\n"

                comprobacion = multiplicar_matrices(B, inversa)
                texto += "COMPROBACIÓN DE IDENTIDAD ( B × B⁻¹ = I ):\n"
                texto += self.formatear_matriz_resultado(comprobacion) + "\n"

                texto += "----------------------------------------------------------\n"
                texto += "DESGLOSE DE OPERACIONES ELEMENTALES POR FILA (GAUSS-JORDAN):\n"
                texto += "----------------------------------------------------------\n"
                texto += "\n".join(pasos) + "\n"

            elif operacion in ("lu_a", "lu_b"):
                es_a = (operacion == "lu_a")
                entradas = self.vista.mat_entries_a if es_a else self.vista.mat_entries_b
                nombre_mat = "Matriz A" if es_a else "Matriz B"
                letra_mat = "A" if es_a else "B"
                filas = len(entradas)
                columnas = len(entradas[0]) if filas > 0 else 0
                if filas == 0 or columnas == 0 or filas != columnas:
                    self.vista.mostrar_error(
                        "Error de Dimensión",
                        f"Para la factorización LU, la matriz debe ser cuadrada (n × n).\n"
                        f"Dimensión actual de la {nombre_mat}: {filas} fila(s) × {columnas} columna(s)."
                    )
                    return

                M = self.leer_matriz(entradas)
                try:
                    self.vista.root.config(cursor="watch")
                    self.vista.root.update_idletasks()
                    P, L, U, pasos, det, num_swaps = factorizacion_lu_con_pasos(M)
                finally:
                    self.vista.root.config(cursor="")

                tipo_rel = f"{letra_mat} = L · U" if num_swaps == 0 else f"P · {letra_mat} = L · U"
                separador = "=" * 60

                texto = f"{separador}\n"
                texto += f"FACTORIZACIÓN LU (MÉTODO DE DOOLITTLE) — {nombre_mat.upper()}\n"
                texto += f"RELACIÓN FUNDAMENTAL: {tipo_rel}\n"
                texto += f"{separador}\n\n"

                texto += f"{nombre_mat.upper()} ORIGINAL ({filas}×{columnas}):\n"
                texto += self.formatear_matriz_resultado(M) + "\n"

                if num_swaps > 0:
                    texto += f"MATRIZ DE PERMUTACIÓN P ({num_swaps} intercambio(s) de fila):\n"
                    texto += self.formatear_matriz_resultado(P) + "\n"
                else:
                    texto += "MATRIZ DE PERMUTACIÓN P:\n[ P = Matriz Identidad I, no se requirió intercambio de filas ]\n\n"

                texto += "MATRIZ TRIANGULAR INFERIOR L (unos en la diagonal principal):\n"
                texto += self.formatear_matriz_resultado(L) + "\n"

                texto += "MATRIZ TRIANGULAR SUPERIOR U (pivotes en la diagonal):\n"
                texto += self.formatear_matriz_resultado(U) + "\n"

                # Comprobación de la factorización
                LU_prod = multiplicar_matrices(L, U)
                PM_prod = multiplicar_matrices(P, M)
                texto += "----------------------------------------------------------\n"
                texto += f"COMPROBACIÓN DEL PRODUCTO ( L × U  vs  {'P × ' + letra_mat if num_swaps > 0 else letra_mat} ):\n"
                texto += "----------------------------------------------------------\n"
                texto += "  L × U =\n"
                texto += self.formatear_matriz_resultado(LU_prod)
                if num_swaps > 0:
                    texto += f"  P × {letra_mat} =\n"
                    texto += self.formatear_matriz_resultado(PM_prod)
                es_igual = (LU_prod == PM_prod)
                texto += f"  Estado: {'✔ FACTORIZACIÓN EXACTA Y COMPROBADA' if es_igual else '✘ DISCREPANCIA'}\n\n"

                texto += f"DETERMINANTE DERIVADO DE U:\n"
                texto += f"  det({letra_mat}) = (-1)^{num_swaps} × Π(u_ii) = {formatear_fraccion(det)}\n\n"

                texto += "----------------------------------------------------------\n"
                texto += "DESGLOSE Y REGISTRO PASO A PASO:\n"
                texto += "----------------------------------------------------------\n"
                texto += "\n".join(pasos) + "\n"
            else:
                return

            self.vista.mostrar_resultado_matrices(texto)

        except ValueError as error:
            self.vista.mostrar_error("Operación no válida", str(error))

    # ==========================================================
    # CONVERSIONES
    # ==========================================================
    def convertir_a_decimal(self):
        cadena = self.vista.entry_conv_origen.get()
        base_nombre = self.vista.base_origen.get()
        bases = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}
        base_num = bases[base_nombre]
        
        try:
            decimal, proceso = base_a_decimal(cadena, base_num)
            texto = f"--- Conversión de {base_nombre} a Decimal ---\n"
            texto += f"Número original: {cadena}\n\n{proceso}\n"
            texto += f"Número en base decimal: {decimal}"
            self.vista.mostrar_resultado_conversion(texto)
        except ValueError as e:
            self.vista.mostrar_error("Error de conversión", str(e))

    def convertir_desde_decimal(self):
        try:
            decimal = int(self.vista.entry_conv_decimal.get())
        except ValueError:
            self.vista.mostrar_error("Error", "Ingrese un número entero válido (Decimal).")
            return
            
        base_nombre = self.vista.base_destino.get()
        bases = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}
        base_num = bases[base_nombre]
        
        try:
            res, proceso = decimal_a_base(decimal, base_num)
            texto = f"--- Conversión de Decimal a {base_nombre} ---\n"
            texto += f"Número Decimal: {decimal}\n\n"
            texto += "Algoritmo de divisiones sucesivas:\n"
            texto += f"{proceso}\n"
            texto += f"Número en base {base_nombre.lower()}: {res}"
            self.vista.mostrar_resultado_conversion(texto)
        except Exception as e:
            self.vista.mostrar_error("Error", str(e))

    # ==========================================================
    # NÚMEROS ROMANOS
    # ==========================================================
    def generar_campos_romanos(self):
        try:
            cant = int(self.vista.spin_cant_romanos.get())
            if not 2 <= cant <= 10:
                self.vista.mostrar_error("Error", "La cantidad de números romanos debe estar entre 2 y 10.")
                return
            self.vista.construir_campos_romanos(cant)
        except ValueError:
            self.vista.mostrar_error("Error", "Ingrese una cantidad válida de operandos.")

    def cargar_ejemplo_romanos(self, tipo):
        datos = {
            "suma3": (3, "Suma (+)", ["XVI", "IV", "II"]),
            "mult": (2, "Multiplicación (×)", ["XII", "IV"]),
            "div": (2, "División (÷)", ["XXV", "IV"]),
            "resta3": (3, "Resta (-)", ["L", "XV", "V"])
        }
        if tipo in datos:
            cant, op, valores = datos[tipo]
            self.vista.spin_cant_romanos.set(cant)
            self.vista.op_romanos.set(op)
            self.vista.construir_campos_romanos(cant)
            for i, val in enumerate(valores):
                self.vista.romanos_entries[i].delete(0, 'end')
                self.vista.romanos_entries[i].insert(0, val)
            self.calcular_operacion_romanos()

    def calcular_operacion_romanos(self):
        mapa_ops = {
            "Suma (+)": "+",
            "Resta (-)": "-",
            "Multiplicación (×)": "*",
            "División (÷)": "/"
        }
        op_texto = self.vista.op_romanos.get()
        operacion = mapa_ops.get(op_texto, "+")

        lista_valores = [entry.get().strip() for entry in self.vista.romanos_entries]
        
        if any(not v for v in lista_valores):
            self.vista.mostrar_error("Error de Entrada", "Todos los campos de números romanos deben contener un valor.")
            return

        resultado = operar_lista_romanos(lista_valores, operacion)
        if resultado['exito']:
            self.vista.mostrar_resultados_romanos(resultado)
        else:
            self.vista.mostrar_error("Error en Operación", resultado['error'])

    def evaluar_expresion_romana(self):
        if not getattr(self.vista, "entry_expresion_romana", None):
            return
        exp = self.vista.entry_expresion_romana.get().strip()
        if not exp:
            self.vista.mostrar_error("Error", "Por favor ingrese una expresión romana.")
            return
            
        resultado = evaluar_expresion_romana(exp)
        if resultado['exito']:
            self.vista.mostrar_resultados_romanos(resultado)
        else:
            self.vista.mostrar_error("Error en Expresión", resultado['error'])
