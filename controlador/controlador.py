from vista.ventana_principal import VentanaPrincipal
from modelo.solucionador import SolucionadorGauss, SolucionadorGaussJordan

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
    invertir_matriz,
    invertir_matriz_con_pasos
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
        elif tipo == "infinitas":
            A = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
            b = [1, 2, 3]
        elif tipo == "inconsistente":
            A = [[1, 2, 3], [1, 2, 3], [2, 1, 1]]
            b = [4, 5, 1]
            
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
        elif tipo == "inv_singular":
            A = [[1, 2], [2, 4]]
            B = [[1, 0], [0, 1]]
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

        # Calcular automáticamente la inversa de A
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
        for paso, (mensaje, matriz) in enumerate(solucionador.historial):
            texto_historial += f"--- Paso {paso}: {mensaje} ---\n"
            texto_historial += formatear_matriz(matriz)
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
            if not all(1 <= valor <= 10 for valor in dimensiones):
                raise ValueError
        except ValueError:
            self.vista.mostrar_error("Error", "Las dimensiones deben estar entre 1 y 10.")
            return

        self.vista.construir_matrices_ops(filas_a, columnas_a, filas_b, columnas_b)

    def leer_matriz(self, entradas):
        from fractions import Fraction
        return [[Fraction(entry.get()) for entry in fila] for fila in entradas]

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
            A = self.leer_matriz(self.vista.mat_entries_a)
            B = self.leer_matriz(self.vista.mat_entries_b)

            if operacion == "suma":
                resultado = sumar_matrices(A, B)
                titulo = "A + B"
                texto = f"RESULTADO: {titulo}\n\n"
                texto += self.formatear_matriz_resultado(resultado)
            elif operacion == "resta":
                resultado = restar_matrices(A, B)
                titulo = "A − B"
                texto = f"RESULTADO: {titulo}\n\n"
                texto += self.formatear_matriz_resultado(resultado)
            elif operacion == "multiplicacion":
                resultado = multiplicar_matrices(A, B)
                titulo = "A × B"
                texto = f"RESULTADO: {titulo}\n\n"
                texto += self.formatear_matriz_resultado(resultado)
            elif operacion == "escalar":
                from fractions import Fraction
                escalar = Fraction(self.vista.entrada_escalar_mat.get())
                resultado = multiplicar_matriz_escalar(A, escalar)
                titulo = f"{formatear_fraccion(escalar)}A"
                texto = f"RESULTADO: {titulo}\n\n"
                texto += self.formatear_matriz_resultado(resultado)
            elif operacion == "inversa_a":
                inversa, pasos = invertir_matriz_con_pasos(A)
                titulo = "INVERSA DE LA MATRIZ A (A⁻¹)"
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
                inversa, pasos = invertir_matriz_con_pasos(B)
                titulo = "INVERSA DE LA MATRIZ B (B⁻¹)"
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
            texto += f"Número original: {cadena}\n\n{proceso}"
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
            texto += proceso
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
        exp = self.vista.entry_expresion_romana.get().strip()
        if not exp:
            self.vista.mostrar_error("Error", "Por favor ingrese una expresión romana.")
            return
            
        resultado = evaluar_expresion_romana(exp)
        if resultado['exito']:
            self.vista.mostrar_resultados_romanos(resultado)
        else:
            self.vista.mostrar_error("Error en Expresión", resultado['error'])


