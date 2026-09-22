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
    multiplicar_matrices
)
from modelo.conversiones import decimal_a_base, base_a_decimal

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
            elif operacion == "resta":
                resultado = restar_matrices(A, B)
                titulo = "A - B"
            elif operacion == "multiplicacion":
                resultado = multiplicar_matrices(A, B)
                titulo = "A × B"
            elif operacion == "escalar":
                from fractions import Fraction
                escalar = Fraction(self.vista.entrada_escalar_mat.get())
                resultado = multiplicar_matriz_escalar(A, escalar)
                titulo = f"{formatear_fraccion(escalar)}A"
            else:
                return

            texto = f"RESULTADO: {titulo}\n\n"
            texto += self.formatear_matriz_resultado(resultado)
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

