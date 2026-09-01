# modelo/solucionador.py
from modelo.matriz import copiar_matriz

class SolucionadorGauss:
    def __init__(self, A, b):
        """
        Inicializa el solucionador con la matriz de coeficientes A y el vector b.
        Se crean copias profundas para no alterar los datos originales.
        """
        self.A_original = copiar_matriz(A)
        self.b_original = list(b)
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
                        self.aumentada[i][j] = 0.0
                
                if factor != 0:
                    signo = "+" if factor < 0 else "-"
                    self.guardar_paso(f"f_{i+1} -> f_{i+1} {signo} {abs(factor):.3f} * f_{fila_pivote+1}")
                    
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
        self.solucion = [0.0] * self.n
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
