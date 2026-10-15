from fractions import Fraction

from modelo.matriz import copiar_matriz, formatear_fraccion, formatear_matriz

class SolucionadorGauss:
    def __init__(self, A, b):
        """
        Inicializa el solucionador con la matriz de coeficientes A y el vector b.
        Se crean copias profundas para no alterar los datos originales.
        """
        self.A_original = [[Fraction(valor) for valor in fila] for fila in A]
        self.b_original = [Fraction(valor) for valor in b]
        self.m = len(A)       # Filas
        self.n = len(A[0])    # Columnas
        
        # Crear matriz aumentada
        self.aumentada = []
        for i in range(self.m):
            fila = list(self.A_original[i])
            fila.append(self.b_original[i])
            self.aumentada.append(fila)
            
        self.historial = [] # Almacenará tuplas (mensaje, matriz_estado)
        self.solucion = []
        self.clasificacion = ""
        self.es_valido = False

    def guardar_paso(self, mensaje):
        """Guarda una instantánea de la matriz aumentada en el historial."""
        self.historial.append((mensaje, copiar_matriz(self.aumentada)))

    def resolver(self):
        """
        Ejecuta el algoritmo de eliminación gaussiana con pivoteo parcial,
        clasifica el sistema, encuentra las soluciones si aplica, y verifica.
        """
        self.guardar_paso("Matriz Aumentada Inicial:")
        
        # 1. Eliminación hacia adelante (Forward Elimination)
        fila_pivote = 0
        for col in range(self.n):
            if fila_pivote >= self.m:
                break
                
            # Pivoteo Parcial: Buscar el máximo valor absoluto en la columna actual (hacia abajo)
            max_val = abs(self.aumentada[fila_pivote][col])
            max_idx = fila_pivote
            for i in range(fila_pivote + 1, self.m):
                if abs(self.aumentada[i][col]) > max_val:
                    max_val = abs(self.aumentada[i][col])
                    max_idx = i
                    
            # Si el máximo es muy cercano a cero, esta columna no tiene pivote válido
            if max_val < 1e-10:
                continue
                
            # Intercambiar filas si el pivote no está en la fila actual
            if max_idx != fila_pivote:
                self.aumentada[fila_pivote], self.aumentada[max_idx] = self.aumentada[max_idx], self.aumentada[fila_pivote]
                self.guardar_paso(f"f_{fila_pivote+1} <-> f_{max_idx+1}")
                
            # Hacer ceros debajo del pivote
            for i in range(fila_pivote + 1, self.m):
                factor = self.aumentada[i][col] / self.aumentada[fila_pivote][col]
                for j in range(col, self.n + 1):
                    self.aumentada[i][j] -= factor * self.aumentada[fila_pivote][j]
                    # Limpiar errores de punto flotante
                    if abs(self.aumentada[i][j]) < 1e-10:
                        self.aumentada[i][j] = Fraction(0)
                
                if factor != 0:
                    signo = "+" if factor < 0 else "-"
                    self.guardar_paso(f"f_{i+1} -> f_{i+1} {signo} {formatear_fraccion(abs(factor))} * f_{fila_pivote+1}")
                    
            fila_pivote += 1

        # 2. Clasificación del Sistema
        rango_A = 0
        rango_Ab = 0
        
        for i in range(self.m):
            fila_A_no_nula = any(abs(val) > 1e-10 for val in self.aumentada[i][:-1])
            fila_Ab_no_nula = any(abs(val) > 1e-10 for val in self.aumentada[i])
            
            if fila_A_no_nula:
                rango_A += 1
            if fila_Ab_no_nula:
                rango_Ab += 1

        if rango_A < rango_Ab:
            self.clasificacion = "Sistema Inconsistente: Sin Solución"
            self.es_valido = False
        elif rango_A == rango_Ab and rango_A == self.n:
            self.clasificacion = "Sistema Consistente Determinado: Presenta Solución Única."
            self.es_valido = True
            self.sustitucion_hacia_atras()
        elif rango_A == rango_Ab and rango_A < self.n:
            self.clasificacion = "Sistema Consistente Indeterminado: Presenta Infinitas Soluciones"
            self.es_valido = False # No hallamos solución única
            
    def sustitucion_hacia_atras(self):
        """Calcula el vector de soluciones partiendo de la última ecuación hacia arriba."""
        self.solucion = [Fraction(0)] * self.n
        for i in range(self.n - 1, -1, -1):
            suma = sum(self.aumentada[i][j] * self.solucion[j] for j in range(i + 1, self.n))
            # El pivote en la fila i es self.aumentada[i][i]
            # Como sabemos que hay solución única, el pivote no es cero.
            self.solucion[i] = (self.aumentada[i][-1] - suma) / self.aumentada[i][i]

    def verificar(self):
        """Sustituye los valores encontrados en las ecuaciones originales para comprobar precisión."""
        if not self.es_valido:
            return None
            
        errores = []
        for i in range(self.m):
            valor_calculado = sum(self.A_original[i][j] * self.solucion[j] for j in range(self.n))
            error = abs(valor_calculado - self.b_original[i])
            errores.append((valor_calculado, self.b_original[i], error))
        return errores


class SolucionadorGaussJordan(SolucionadorGauss):
    def resolver(self):
        self.guardar_paso("Matriz Aumentada Inicial:")

        fila_pivote = 0
        pivotes = []
        for col in range(self.n):
            if fila_pivote >= self.m:
                break

            max_idx = max(
                range(fila_pivote, self.m),
                key=lambda indice: abs(self.aumentada[indice][col])
            )
            max_val = abs(self.aumentada[max_idx][col])
            if max_val < 1e-10:
                continue

            if max_idx != fila_pivote:
                self.aumentada[fila_pivote], self.aumentada[max_idx] = (
                    self.aumentada[max_idx], self.aumentada[fila_pivote]
                )
                self.guardar_paso(f"f_{fila_pivote+1} <-> f_{max_idx+1}")

            pivote = self.aumentada[fila_pivote][col]
            self.aumentada[fila_pivote] = [
                valor / pivote for valor in self.aumentada[fila_pivote]
            ]
            self.guardar_paso(f"f_{fila_pivote+1} -> f_{fila_pivote+1} / {formatear_fraccion(pivote)}")

            for indice in range(self.m):
                if indice == fila_pivote:
                    continue
                factor = self.aumentada[indice][col]
                if abs(factor) < 1e-10:
                    continue
                for j in range(self.n + 1):
                    self.aumentada[indice][j] -= factor * self.aumentada[fila_pivote][j]
                    if abs(self.aumentada[indice][j]) < 1e-10:
                        self.aumentada[indice][j] = Fraction(0)
                signo = "+" if factor < 0 else "-"
                self.guardar_paso(
                    f"f_{indice+1} -> f_{indice+1} {signo} {formatear_fraccion(abs(factor))} * f_{fila_pivote+1}"
                )

            pivotes.append((fila_pivote, col))
            fila_pivote += 1

        rango_A = sum(
            any(abs(valor) > 1e-10 for valor in fila[:-1])
            for fila in self.aumentada
        )
        rango_Ab = sum(
            any(abs(valor) > 1e-10 for valor in fila)
            for fila in self.aumentada
        )

        if rango_A < rango_Ab:
            self.clasificacion = "Sistema Inconsistente: Sin Solución"
        elif rango_A == self.n:
            self.clasificacion = "Sistema Consistente Determinado: Presenta Solución Única."
            self.es_valido = True
            self.solucion = [0] * self.n
            for fila, col in pivotes:
                self.solucion[col] = self.aumentada[fila][-1]
        else:
            self.clasificacion = "Sistema Consistente Indeterminado: Presenta Infinitas Soluciones"


def resolver_Ax_b(A, b):
    """
    Procedimiento algebraico: Resolución de sistema de ecuaciones lineales.
    1. Se crea la matriz aumentada uniendo A (m x n) y el vector columna b (m x 1).
    2. Se aplica Eliminación de Gauss-Jordan con pivoteo parcial para escalonar.
    3. Se evalúa la consistencia del sistema y se extrae el vector solución x.
    """
    n = len(A)
    if any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError("El sistema requiere una matriz cuadrada A (n x n) y un vector b de tamaño n.")

    # Crear matriz aumentada M = [A | b]
    M = [A[i][:] + [b[i]] for i in range(n)]

    for i in range(n):
        # Pivoteo Parcial: Buscar el máximo valor absoluto en la columna actual
        fila_max = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[fila_max] = M[fila_max], M[i]

        if abs(M[i][i]) < 1e-9:
            raise ValueError("El sistema es singular (no tiene solución única).")

        # Normalizar fila dividiendo entre el pivote
        pivote = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivote

        # Eliminación hacia abajo y hacia arriba
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]

    # Extraer el vector solución x (última columna de la matriz M ya reducida)
    x = [M[i][-1] for i in range(n)]
    return x


class SolucionadorLU:
    """
    Solucionador de sistemas de ecuaciones lineales A x = b mediante Factorización LU
    (Método de Doolittle con soporte para pivoteo P * A = L * U).
    
    Procedimiento algebraico:
    1. Se descompone la matriz de coeficientes: P * A = L * U
       donde L es triangular inferior con 1s en la diagonal y U es triangular superior.
    2. Se resuelve L * y = P * b mediante sustitución progresiva (hacia adelante).
    3. Se resuelve U * x = y mediante sustitución regresiva (hacia atrás).
    4. Se comprueba sustituyendo x en el sistema original A * x = b.
    """
    def __init__(self, A, b):
        self.A_original = [[Fraction(valor) for valor in fila] for fila in A]
        self.b_original = [Fraction(valor) for valor in b]
        self.m = len(A)
        self.n = len(A[0]) if self.m > 0 else 0
        
        self.historial = []  # Lista de tuplas (mensaje, matriz_o_texto)
        self.solucion = []
        self.solucion_y = []
        self.clasificacion = ""
        self.es_valido = False
        self.L = []
        self.U = []
        self.P = []
        self.num_intercambios = 0

    def guardar_paso(self, mensaje, estado):
        self.historial.append((mensaje, estado))

    def resolver(self):
        if self.m != self.n:
            self.clasificacion = (
                f"Error: La factorización LU requiere una matriz de coeficientes cuadrada (m = n).\n"
                f"Dimensión ingresada: {self.m} ecuaciones × {self.n} incógnitas."
            )
            self.es_valido = False
            self.guardar_paso(
                "Dimensiones incompatibles para LU",
                f"El sistema tiene {self.m} filas y {self.n} columnas. No es una matriz cuadrada."
            )
            return

        n = self.n
        U = [fila[:] for fila in self.A_original]
        L = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        P = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

        aumentada_inicial = [self.A_original[i] + [self.b_original[i]] for i in range(n)]
        self.guardar_paso("Matriz Aumentada Inicial [ A | b ]:", aumentada_inicial)

        for k in range(n):
            # Pivoteo si el elemento diagonal es 0
            if U[k][k] == 0:
                fila_swap = None
                for r in range(k + 1, n):
                    if U[r][k] != 0:
                        fila_swap = r
                        break
                if fila_swap is not None:
                    U[k], U[fila_swap] = U[fila_swap], U[k]
                    P[k], P[fila_swap] = P[fila_swap], P[k]
                    for c in range(k):
                        L[k][c], L[fila_swap][c] = L[fila_swap][c], L[k][c]
                    self.num_intercambios += 1
                    self.guardar_paso(
                        f"Pivoteo parcial: Intercambio de fila f_{k + 1} ⟷ f_{fila_swap + 1}",
                        [fila[:] for fila in U]
                    )

            if U[k][k] == 0:
                self.clasificacion = (
                    "Sistema Singular (det(A) = 0): No presenta solución única.\n"
                    f"El pivote en la columna {k + 1} es nulo sin filas candidatas para intercambio."
                )
                self.es_valido = False
                self.guardar_paso(
                    "Pivote nulo encontrado (Matriz Singular)",
                    f"Columna {k + 1} contiene ceros en todas las filas activas. det(A) = 0."
                )
                return

            pivote = U[k][k]
            for i in range(k + 1, n):
                elemento = U[i][k]
                if elemento != 0:
                    factor = elemento / pivote
                    L[i][k] = factor
                    for j in range(k, n):
                        U[i][j] -= factor * U[k][j]
                    U[i][k] = Fraction(0)
                    signo = "−" if factor > 0 else "+"
                    msg = (
                        f"Eliminación: f_{i + 1} ➔ f_{i + 1} {signo} ({formatear_fraccion(abs(factor))}) * f_{k + 1}  "
                        f"[Multiplicador m_{i + 1},{k + 1} = {formatear_fraccion(factor)}]"
                    )
                    self.guardar_paso(msg, [fila[:] for fila in U])

        self.L = L
        self.U = U
        self.P = P

        det = Fraction(-1) ** self.num_intercambios
        for i in range(n):
            det *= U[i][i]

        tipo_fact = "A = L · U" if self.num_intercambios == 0 else "P · A = L · U"
        resumen_mat = f"=== FACTORIZACIÓN {tipo_fact} COMPLETADA ===\n\n"
        if self.num_intercambios > 0:
            resumen_mat += "Matriz de Permutación P:\n" + formatear_matriz(P) + "\n"
        resumen_mat += "Matriz Triangular Inferior L (unos en diagonal):\n" + formatear_matriz(L) + "\n"
        resumen_mat += "Matriz Triangular Superior U:\n" + formatear_matriz(U) + "\n"
        resumen_mat += f"Determinante det(A) = {formatear_fraccion(det)}\n"
        self.guardar_paso(f"Estructura matricial final ({tipo_fact})", resumen_mat)

        # ── FASE 1: Sustitución hacia adelante ( L · y = P · b ) ─────────────
        b_perm = [sum(P[i][j] * self.b_original[j] for j in range(n)) for i in range(n)]
        pasos_adelante = "Resolución del sistema triangular inferior L · y = P · b:\n\n"
        y = [Fraction(0)] * n
        for i in range(n):
            suma = sum(L[i][j] * y[j] for j in range(i))
            y[i] = b_perm[i] - suma
            terminos = " + ".join(f"({formatear_fraccion(L[i][j])})·({formatear_fraccion(y[j])})" for j in range(i))
            if terminos:
                pasos_adelante += (
                    f"  y{i + 1} = {formatear_fraccion(b_perm[i])} − [{terminos}] "
                    f"= {formatear_fraccion(y[i])}\n"
                )
            else:
                pasos_adelante += f"  y{i + 1} = {formatear_fraccion(b_perm[i])}\n"

        self.solucion_y = y
        self.guardar_paso("Fase 1: Sustitución hacia adelante ( L · y = P · b )", pasos_adelante)

        # ── FASE 2: Sustitución hacia atrás ( U · x = y ) ────────────────────
        pasos_atras = "Resolución del sistema triangular superior U · x = y:\n\n"
        x = [Fraction(0)] * n
        for i in range(n - 1, -1, -1):
            suma = sum(U[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - suma) / U[i][i]
            terminos = " + ".join(f"({formatear_fraccion(U[i][j])})·({formatear_fraccion(x[j])})" for j in range(i + 1, n))
            if terminos:
                pasos_atras += (
                    f"  x{i + 1} = ({formatear_fraccion(y[i])} − [{terminos}]) / ({formatear_fraccion(U[i][i])}) "
                    f"= {formatear_fraccion(x[i])}\n"
                )
            else:
                pasos_atras += (
                    f"  x{i + 1} = {formatear_fraccion(y[i])} / ({formatear_fraccion(U[i][i])}) "
                    f"= {formatear_fraccion(x[i])}\n"
                )

        self.solucion = x
        self.guardar_paso("Fase 2: Sustitución hacia atrás ( U · x = y )", pasos_atras)

        self.clasificacion = "Sistema Consistente Determinado: Presenta Solución Única (por Factorización LU)."
        self.es_valido = True

    def verificar(self):
        """Sustituye los valores encontrados en las ecuaciones originales para comprobar precisión."""
        if not self.es_valido:
            return None
        errores = []
        for i in range(self.m):
            calc = sum(self.A_original[i][j] * self.solucion[j] for j in range(self.n))
            err = abs(calc - self.b_original[i])
            errores.append((calc, self.b_original[i], err))
        return errores