# modelo/matriz.py

from fractions import Fraction


def copiar_matriz(matriz):
    """
    Realiza una copia profunda de una matriz bidimensional (lista de listas).
    """
    return [fila[:] for fila in matriz]

def crear_matriz_ceros(filas, columnas):
    """
    Crea una matriz de dimensiones 'filas' x 'columnas' inicializada con ceros flotantes.
    """
    return [[0.0 for _ in range(columnas)] for _ in range(filas)]

def formatear_fraccion(valor):
    """Devuelve una fracción sin mostrar decimales innecesarios."""
    valor = Fraction(valor)
    if valor.denominator == 1:
        return str(valor.numerator)
    return f"{valor.numerator}/{valor.denominator}"

def formatear_conversiones(valor):
    """Devuelve resultados y divisiones sucesivas en distintas bases."""
    valor = Fraction(valor)
    if valor.denominator != 1:
        return "Binario: no disponible (requiere un entero)\nOctal: no disponible (requiere un entero)\nHexadecimal: no disponible (requiere un entero)"

    entero = valor.numerator
    signo = "-" if entero < 0 else ""
    absoluto = abs(entero)

    def divisiones(base, nombre, simbolo):
        if absoluto == 0:
            pasos = "  0 / {} = 0, residuo 0".format(base)
            digitos = "0"
        else:
            actual = absoluto
            residuos = []
            lineas = []
            while actual > 0:
                cociente, residuo = divmod(actual, base)
                residuos.append(residuo)
                lineas.append(
                    "  {} / {} = {}, residuo {}".format(
                        actual, base, cociente, format(residuo, "X") if base == 16 else residuo
                    )
                )
                actual = cociente
            pasos = "\n".join(lineas)
            digitos = "".join(
                format(residuo, "X") if base == 16 else str(residuo)
                for residuo in reversed(residuos)
            )

        resultado = signo + simbolo + digitos

        return "{}: {}\nDivisiones entre {}:\n{}\nResiduos de abajo hacia arriba: {}".format(
            nombre, resultado, base, pasos, digitos
        )

    return (
        f"{divisiones(2, 'Binario', '0b')}\n\n"
        f"{divisiones(8, 'Octal', '0o')}\n\n"
        f"{divisiones(16, 'Hexadecimal', '0x')}"
    )

def convertir_desde_base(texto, base):
    """Convierte un valor escrito en una base y devuelve todas sus conversiones."""
    valor = texto.strip().lower()
    prefijos = {2: "0b", 8: "0o", 16: "0x"}
    prefijo = prefijos.get(base, "")
    if prefijo and valor.startswith(prefijo):
        valor = valor[len(prefijo):]
    if not valor:
        raise ValueError("Ingrese un valor para convertir.")

    try:
        decimal = int(valor, base)
    except ValueError as error:
        raise ValueError("El valor no es válido para la base seleccionada.") from error

    return decimal, formatear_conversiones(decimal)

def formatear_matriz(matriz):
    """
    Devuelve una representación en cadena (string) formateada de la matriz.
    Útil para mostrar el historial en la interfaz gráfica.
    """
    texto = ""
    for fila in matriz:
        texto += "[ " + "  ".join(f"{formatear_fraccion(val):>8}" for val in fila) + " ]\n"
    return texto


def suma_vectores(v1, v2):
    """
    Procedimiento algebraico: Suma componente a componente.
    Sean los vectores v1, v2 en R^n, el vector resultante w = v1 + v2 
    se define de tal forma que cada componente w_i = v1_i + v2_i.
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión (n).")
    return [v1[i] + v2[i] for i in range(len(v1))]

def resta_vectores(v1, v2):
    """
    Procedimiento algebraico: Resta componente a componente.
    Equivalente a v1 + (-v2). Cada componente w_i = v1_i - v2_i.
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión (n).")
    return [v1[i] - v2[i] for i in range(len(v1))]

def multiplicacion_escalar_vector(v, c):
    """
    Procedimiento algebraico: Multiplicación por escalar.
    (Ajustado para recibir el vector primero y el escalar después)
    """
    return [c * elemento for elemento in v]

def es_combinacion_lineal(conjunto_vectores, b):
    """
    Procedimiento algebraico: Evaluación de combinación lineal.
    Retorna una tupla: (Booleano, lista_de_escalares)
    """
    n = len(b)
    k = len(conjunto_vectores)
    
    # Construir matriz aumentada [A | b]
    matriz_aumentada = []
    for i in range(n):
        fila = [conjunto_vectores[j][i] for j in range(k)] + [b[i]]
        matriz_aumentada.append(fila)

    # Reducción de Gauss-Jordan adaptada
    filas = n
    columnas = k + 1
    pivote_col = 0
    
    for r in range(filas):
        if pivote_col >= columnas - 1:
            break
        
        # Buscar pivote
        i = r
        while matriz_aumentada[i][pivote_col] == 0:
            i += 1
            if i == filas:
                i = r
                pivote_col += 1
                if pivote_col == columnas - 1:
                    break
        if pivote_col >= columnas - 1:
            break

        # Intercambiar filas
        matriz_aumentada[i], matriz_aumentada[r] = matriz_aumentada[r], matriz_aumentada[i]

        # Hacer 1 el pivote
        valor_pivote = matriz_aumentada[r][pivote_col]
        matriz_aumentada[r] = [elemento / valor_pivote for elemento in matriz_aumentada[r]]

        # Hacer 0 el resto de la columna
        for i in range(filas):
            if i != r:
                factor = matriz_aumentada[i][pivote_col]
                matriz_aumentada[i] = [
                    matriz_aumentada[i][j] - factor * matriz_aumentada[r][j] 
                    for j in range(columnas)
                ]
        pivote_col += 1

    # Verificar si el sistema es inconsistente
    for fila in matriz_aumentada:
        ceros_en_A = all(x == 0 for x in fila[:-1])
        if ceros_en_A and fila[-1] != 0:
            return False, [] # Sistema inconsistente, no es combinación lineal
            
    # Extraer los escalares de la última columna
    escalares = [0] * k
    for i in range(min(n, k)):
        escalares[i] = matriz_aumentada[i][-1]
        
    return True, escalares


def suma_matrices(A, B):
    """
    Procedimiento algebraico: Suma de matrices de dimensiones iguales (m x n).
    Se suman los elementos en la misma posición: C_ij = A_ij + B_ij.
    """
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    
    if filas_A != filas_B or cols_A != cols_B:
        raise ValueError("Error: Las matrices deben tener la misma dimensión (m x n).")
        
    return [[A[i][j] + B[i][j] for j in range(cols_A)] for i in range(filas_A)]

def resta_matrices(A, B):
    """
    Procedimiento algebraico: Resta de matrices de dimensiones iguales (m x n).
    Se restan los elementos en la misma posición: C_ij = A_ij - B_ij.
    """
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    
    if filas_A != filas_B or cols_A != cols_B:
        raise ValueError("Error: Las matrices deben tener la misma dimensión (m x n).")
        
    return [[A[i][j] - B[i][j] for j in range(cols_A)] for i in range(filas_A)]

def multiplicacion_escalar_matriz(A, c):
    """
    Procedimiento algebraico: Multiplicación de matriz por escalar.
    (Ajustado para recibir la matriz primero y el escalar después)
    """
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplicacion_matrices(A, B):
    """
    Procedimiento algebraico: Producto matricial AB.
    Se requiere que las columnas de A (m x n) coincidan con las filas de B (n x p).
    El elemento C_ij es el producto punto de la fila i de A y la columna j de B.
    """
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    
    if cols_A != filas_B:
        raise ValueError("Error: El número de columnas de A debe ser igual al número de filas de B.")
        
    # Inicializar matriz resultante C de dimensiones (filas_A x cols_B) con ceros
    C = [[0 for _ in range(cols_B)] for _ in range(filas_A)]
    
    for i in range(filas_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
                
    return C