from vista.ventana_principal import VentanaPrincipal
from vista.ventana_operaciones import VentanaOperaciones
from modelo.solucionador import SolucionadorGauss, SolucionadorGaussJordan

# Importar TODAS las funciones matemáticas desde tu archivo unificado matriz.py
from modelo.matriz import (
    suma_vectores,
    resta_vectores,
    multiplicacion_escalar_vector,
    es_combinacion_lineal,
    suma_matrices,
    resta_matrices,
    multiplicacion_escalar_matriz,
    multiplicacion_matrices,
    convertir_desde_base,
    formatear_fraccion,
    formatear_matriz
)

class Controlador:
    def __init__(self, root):
        self.vista = VentanaPrincipal(root, self)

    def convertir_numero(self):
        try:
            bases = {
                "Decimal": 10,
                "Binario": 2,
                "Octal": 8,
                "Hexadecimal": 16,
            }
            base_nombre = self.vista.base_entrada.get()
            decimal, conversiones = convertir_desde_base(
                self.vista.entrada_conversion.get(), bases[base_nombre]
            )
        except ValueError:
            self.vista.mostrar_error("Error de valor", "Ingrese un valor válido para la base seleccionada.")
            return

        self.vista.actualizar_conversiones(
            f"Entrada ({base_nombre}): {self.vista.entrada_conversion.get()}\n"
            f"Valor decimal equivalente: {decimal}\n\n{conversiones}"
        )
        
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
            # 3x3 consistente determinado
            A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
            b = [8, -11, -3]
        elif tipo == "infinitas":
            # 3x3 consistente indeterminado
            A = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
            b = [1, 2, 3]
        elif tipo == "inconsistente":
            # 3x3 inconsistente
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

        # Instanciar modelo y ejecutar lógica
        if self.vista.metodo.get() == "Gauss-Jordan":
            solucionador = SolucionadorGaussJordan(A, b)
        else:
            solucionador = SolucionadorGauss(A, b)
        solucionador.resolver()
        
        # Extraer y formatear datos del modelo
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
        
        # Formatear historial
        texto_historial = ""
        for paso, (mensaje, matriz) in enumerate(solucionador.historial):
            texto_historial += f"--- Paso {paso}: {mensaje} ---\n"
            texto_historial += formatear_matriz(matriz)
            texto_historial += "\n"
            
        self.vista.actualizar_historial(texto_historial)


    # ==========================================================
    # OPERACIONES DE VECTORES Y MATRICES
    # ==========================================================

    def abrir_operaciones(self):
        """
        Abre la ventana de operaciones de vectores y matrices.

        Procedimiento algebraico equivalente:
        La aplicación principal delega las operaciones adicionales
        a una ventana especializada sin modificar el solucionador
        original de sistemas Ax=b.
        """
        self.ventana_operaciones = VentanaOperaciones(
            self.vista.root,
            self
        )

    def generar_vectores(self):
        """
        Genera las entradas necesarias para los vectores.

        Procedimiento algebraico equivalente:
        Para vectores de Rn se crean n componentes para cada vector.
        """
        try:
            dimension = int(
                self.ventana_operaciones.spin_dimension_vector.get()
            )

            cantidad = int(
                self.ventana_operaciones.spin_cantidad_vectores.get()
            )

            if not 1 <= dimension <= 10:
                raise ValueError

            if not 1 <= cantidad <= 10:
                raise ValueError

        except ValueError:
            self.vista.mostrar_error(
                "Error",
                "La dimensión y la cantidad de vectores "
                "deben estar entre 1 y 10."
            )
            return

        self.ventana_operaciones.construir_vectores(
            dimension,
            cantidad
        )

    def operar_vectores(self):
        """
        Lee los vectores y realiza las operaciones vectoriales.

        Procedimiento algebraico equivalente:
        Se calculan suma, resta, multiplicación escalar y se
        determina si b pertenece al espacio generado por los
        vectores dados.
        """
        try:
            ventana = self.ventana_operaciones

            vectores = []

            for fila in ventana.vector_entries:
                vector = []

                for entry in fila:
                    from fractions import Fraction
                    vector.append(Fraction(entry.get()))

                vectores.append(vector)

            b = []

            for entry in ventana.vector_b_entries:
                from fractions import Fraction
                b.append(Fraction(entry.get()))

            texto = ""

            # Suma de vectores
            if len(vectores) >= 2:
                suma = vectores[0]

                for i in range(1, len(vectores)):
                    suma = suma_vectores(
                        suma,
                        vectores[i]
                    )

                texto += "SUMA DE VECTORES\n"
                texto += self.formatear_vector(suma)
                texto += "\n\n"

                # Resta
                resta = resta_vectores(
                    vectores[0],
                    vectores[1]
                )

                texto += "RESTA v1 - v2\n"
                texto += self.formatear_vector(resta)
                texto += "\n\n"

            # Multiplicación escalar
            escalar = Fraction(
             ventana.entrada_escalar_vector.get()
              )

            multiplicado = multiplicacion_escalar_vector(
                vectores[0],
                escalar
            )

            texto += f"MULTIPLICACIÓN {escalar} * v1\n"
            texto += self.formatear_vector(multiplicado)
            texto += "\n\n"

            # Combinación lineal
            es_combinacion, escalares = es_combinacion_lineal(
                vectores,
                b
            )

            texto += "COMBINACIÓN LINEAL\n"

            if es_combinacion:
                texto += "b SÍ es combinación lineal de los vectores.\n"
                texto += "Escalares encontrados:\n"

                for i, valor in enumerate(escalares):
                    texto += (
                        f"c{i + 1} = "
                        f"{formatear_fraccion(valor)}\n"
                    )

                texto += "\nPor lo tanto:\n"

                for i, vector in enumerate(vectores):
                    texto += (
                        f"{formatear_fraccion(escalares[i])}"
                        f" * v{i + 1}"
                    )

                    if i < len(vectores) - 1:
                        texto += " + "

                texto += " = b\n"

            else:
                texto += (
                    "b NO es combinación lineal de "
                    "los vectores proporcionados.\n"
                )

            ventana.mostrar_resultado_vectores(texto)

        except ValueError:
            self.vista.mostrar_error(
                "Error de valor",
                "Todos los elementos de los vectores "
                "deben ser números válidos."
            )

    def formatear_vector(self, vector):
        """
        Convierte un vector en texto para mostrarlo en la interfaz.

        Procedimiento algebraico equivalente:
        Un vector de Rn se representa como:

        (v1, v2, ..., vn)
        """
        valores = []

        for valor in vector:
            valores.append(formatear_fraccion(valor))

        return "(" + ", ".join(valores) + ")"

    def generar_matrices(self):
        """
        Genera las entradas para las matrices A y B.

        Procedimiento algebraico equivalente:
        Las matrices se construyen con dimensiones m x n y p x q.
        """
        try:
            filas_a = int(
                self.ventana_operaciones.spin_filas_a.get()
            )

            columnas_a = int(
                self.ventana_operaciones.spin_columnas_a.get()
            )

            filas_b = int(
                self.ventana_operaciones.spin_filas_b.get()
            )

            columnas_b = int(
                self.ventana_operaciones.spin_columnas_b.get()
            )

            dimensiones = [
                filas_a,
                columnas_a,
                filas_b,
                columnas_b
            ]

            if not all(1 <= valor <= 10 for valor in dimensiones):
                raise ValueError

        except ValueError:
            self.vista.mostrar_error(
                "Error",
                "Las dimensiones deben estar entre 1 y 10."
            )
            return

        self.ventana_operaciones.construir_matrices(
            filas_a,
            columnas_a,
            filas_b,
            columnas_b
        )

    def leer_matriz(self, entradas):
        """
        Convierte las entradas de una matriz en una lista bidimensional.

        Procedimiento algebraico equivalente:
        Cada entrada corresponde al elemento aij de la matriz.
        """
        from fractions import Fraction

        matriz = []

        for fila_entries in entradas:
            fila = []

            for entry in fila_entries:
                fila.append(Fraction(entry.get()))

            matriz.append(fila)

        return matriz

    def formatear_matriz_resultado(self, matriz):
        """
        Convierte una matriz en texto para la interfaz.

        Procedimiento algebraico equivalente:
        La matriz se representa fila por fila como:

        [a11 a12 ...]
        [a21 a22 ...]
        """
        texto = ""

        for fila in matriz:
            texto += "[ "

            for valor in fila:
                texto += f"{formatear_fraccion(valor):>8} "

            texto += "]\n"

        return texto

    def operar_matrices(self, operacion):
        """
        Realiza la operación matricial seleccionada.

        Procedimiento algebraico equivalente:

        A + B
        A - B
        cA
        AB

        respetando las condiciones dimensionales de cada operación.
        """
        try:
            ventana = self.ventana_operaciones

            A = self.leer_matriz(
                ventana.matriz_entries_a
            )

            B = self.leer_matriz(
                ventana.matriz_entries_b
            )

            if operacion == "suma":
                resultado = suma_matrices(A, B)
                titulo = "A + B"

            elif operacion == "resta":
                resultado = resta_matrices(A, B)
                titulo = "A - B"

            elif operacion == "multiplicacion":
                resultado = multiplicacion_matrices(A, B)
                titulo = "A × B"

            elif operacion == "escalar":
                from fractions import Fraction

                escalar = Fraction(
                    ventana.entrada_escalar.get()
                )

                resultado = multiplicacion_escalar_matriz(
                    A,
                    escalar
                )

                titulo = (
                    f"{formatear_fraccion(escalar)}A"
                )

            else:
                return

            texto = f"RESULTADO: {titulo}\n\n"
            texto += self.formatear_matriz_resultado(
                resultado
            )

            ventana.mostrar_resultado_matrices(texto)

        except ValueError as error:
            self.vista.mostrar_error(
                "Operación no válida",
                str(error)
            )
