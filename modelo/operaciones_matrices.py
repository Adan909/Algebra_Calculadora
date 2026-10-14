# modelo/operaciones_matrices.py

from fractions import Fraction


def determinante_sarrus(A):
    """Retorna el determinante 3x3 y los pasos de la regla de Sarrus."""
    if len(A) != 3 or any(len(fila) != 3 for fila in A):
        raise ValueError("La regla de Sarrus solo se aplica a matrices 3×3.")

    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    descendentes = (a * e * i, b * f * g, c * d * h)
    ascendentes = (c * e * g, b * d * i, a * f * h)
    suma_descendentes = sum(descendentes, Fraction(0))
    suma_ascendentes = sum(ascendentes, Fraction(0))
    determinante = suma_descendentes - suma_ascendentes

    pasos = [
        "Paso 1: Copiamos las dos primeras columnas a la derecha de la matriz:",
    ]
    ancho = max(len(str(valor)) for fila in A for valor in fila)
    for fila in A:
        parte_original = "  ".join(f"{valor:>{ancho}}" for valor in fila)
        columnas_copiadas = "  ".join(
            f"{valor:>{ancho}}" for valor in fila[:2]
        )
        pasos.append(f"  [ {parte_original}  |  {columnas_copiadas} ]")

    pasos.extend([
        "Paso 2: Identificamos las diagonales descendentes (se suman).",
        f"  aei = {a} × {e} × {i} = {descendentes[0]}",
        f"  bfg = {b} × {f} × {g} = {descendentes[1]}",
        f"  cdh = {c} × {d} × {h} = {descendentes[2]}",
        f"  Suma descendente = {suma_descendentes}",
        "Paso 3: Identificamos las diagonales ascendentes (se restan).",
        f"  ceg = {c} × {e} × {g} = {ascendentes[0]}",
        f"  bdi = {b} × {d} × {i} = {ascendentes[1]}",
        f"  afh = {a} × {f} × {h} = {ascendentes[2]}",
        f"  Suma ascendente = {suma_ascendentes}",
        "Paso 4: Restamos ambas sumas.",
        f"  det(A) = {suma_descendentes} - {suma_ascendentes} = {determinante}",
    ])
    return determinante, pasos


def determinante_cofactores(A):
    """Retorna el determinante y su desarrollo recursivo por cofactores."""
    if len(A) == 0 or any(len(fila) != len(A) for fila in A):
        raise ValueError("Para calcular el determinante, la matriz debe ser cuadrada y no vacía.")

    pasos = []

    def registrar_paso(mensaje, nivel):
        pasos.append(f"Paso {len(pasos) + 1}: {'  ' * nivel}{mensaje}")

    def calcular(matriz, nivel=0):
        orden = len(matriz)

        if orden == 1:
            valor = matriz[0][0]
            registrar_paso(f"Matriz 1×1: det = {valor}.", nivel)
            return valor
        if orden == 2:
            a, b = matriz[0]
            c, d = matriz[1]
            resultado = a * d - b * c
            registrar_paso(
                f"Matriz 2×2: det = ({a} × {d}) - ({b} × {c}) = {resultado}.",
                nivel,
            )
            return resultado

        registrar_paso(
            "Expandimos por la primera fila, alternando los signos +, -, +.",
            nivel,
        )
        terminos = []
        determinante = Fraction(0)
        for columna, valor in enumerate(matriz[0]):
            menor = [
                [matriz[fila][j] for j in range(orden) if j != columna]
                for fila in range(1, orden)
            ]
            signo = -1 if columna % 2 else 1
            menor_formateado = "\n".join(
                "      [ " + "  ".join(str(elemento) for elemento in fila) + " ]"
                for fila in menor
            )
            registrar_paso(
                f"Elemento elegido: {valor} (posición a_1,{columna + 1}).\n"
                f"Para formar su menor, eliminamos la fila 1 y la columna {columna + 1}.\n"
                f"  Signo del cofactor: {'+' if signo > 0 else '-'} por la posición.\n"
                f"  Menor resultante:\n{menor_formateado}",
                nivel,
            )
            determinante_menor = calcular(menor, nivel + 1)
            termino = signo * valor * determinante_menor
            determinante += termino
            terminos.append(
                f"{'+' if signo > 0 else '-'} ({valor} × {determinante_menor})"
            )
            registrar_paso(f"Aportación de este cofactor: {termino}.", nivel)

        registrar_paso(
            f"Sumamos los cofactores: {' '.join(terminos)} = {determinante}.",
            nivel,
        )
        return determinante

    return calcular(A), pasos


def validar_misma_dimension(A, B):
    """
    Verifica que dos matrices tengan las mismas dimensiones.

    Procedimiento algebraico equivalente:
    Para poder realizar A + B o A - B,
    ambas matrices deben tener exactamente el mismo número
    de filas y columnas.
    """
    if len(A) != len(B):
        return False

    if len(A) == 0 or len(B) == 0:
        return True

    if len(A[0]) != len(B[0]):
        return False

    return True


def sumar_matrices(A, B):
    """
    Suma dos matrices de dimensiones m x n.

    Procedimiento algebraico equivalente:

    A + B = C

    donde:

    cij = aij + bij

    La suma solamente es posible cuando ambas matrices
    tienen las mismas dimensiones.
    """
    if not validar_misma_dimension(A, B):
        raise ValueError(
            "Las matrices deben tener las mismas dimensiones."
        )

    resultado = []

    for i in range(len(A)):
        fila = []

        for j in range(len(A[0])):
            fila.append(A[i][j] + B[i][j])

        resultado.append(fila)

    return resultado


def restar_matrices(A, B):
    """
    Resta dos matrices de dimensiones m x n.

    Procedimiento algebraico equivalente:

    A - B = C

    donde:

    cij = aij - bij

    Ambas matrices deben tener las mismas dimensiones.
    """
    if not validar_misma_dimension(A, B):
        raise ValueError(
            "Las matrices deben tener las mismas dimensiones."
        )

    resultado = []

    for i in range(len(A)):
        fila = []

        for j in range(len(A[0])):
            fila.append(A[i][j] - B[i][j])

        resultado.append(fila)

    return resultado


def multiplicar_matriz_escalar(A, escalar):
    """
    Multiplica una matriz por un escalar.

    Procedimiento algebraico equivalente:

    cA = B

    donde:

    bij = c * aij

    Cada elemento de la matriz se multiplica por el escalar.
    """
    resultado = []

    for i in range(len(A)):
        fila = []

        for j in range(len(A[0])):
            fila.append(A[i][j] * escalar)

        resultado.append(fila)

    return resultado


def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices.

    Si:

    A es m x n
    B es n x p

    entonces:

    AB es m x p

    Procedimiento algebraico equivalente:

    cij = Σ(aik * bkj)

    para k desde 1 hasta n.

    El número de columnas de A debe ser igual al número
    de filas de B.
    """
    if len(A) == 0 or len(B) == 0:
        raise ValueError("Las matrices no pueden estar vacías.")

    columnas_A = len(A[0])
    filas_B = len(B)

    if columnas_A != filas_B:
        raise ValueError(
            "No se pueden multiplicar las matrices: "
            "el número de columnas de A debe ser igual "
            "al número de filas de B."
        )

    filas_A = len(A)
    columnas_B = len(B[0])

    resultado = []

    for i in range(filas_A):
        fila_resultado = []

        for j in range(columnas_B):
            suma = Fraction(0)

            for k in range(columnas_A):
                suma += A[i][k] * B[k][j]

            fila_resultado.append(suma)

        resultado.append(fila_resultado)

    return resultado


def invertir_matriz(A):
    """
    Calcula la inversa de una matriz cuadrada A usando el método de Gauss-Jordan.

    Procedimiento algebraico equivalente:
    1. Para que una matriz A tenga inversa (A^-1), debe ser cuadrada (n x n).
    2. Se forma la matriz aumentada [A | I_n], donde I_n es la matriz identidad.
    3. Se aplican operaciones elementales por fila para transformar la mitad
       izquierda en la matriz identidad:
       [A | I_n]  --->  [I_n | A^-1]
    4. Si en algún paso una fila de la parte izquierda se compone completamente de ceros
       (o no se encuentra pivote no nulo), el determinante de la matriz es 0
       y por tanto la matriz es singular (no invertible).
    5. La matriz resultante en la mitad derecha corresponde a la matriz inversa A^-1.
    """
    inversa, _ = invertir_matriz_con_pasos(A)
    return inversa


def invertir_matriz_con_pasos(A):
    """
    Calcula la inversa de una matriz cuadrada A junto con el registro detallado
    de operaciones elementales por fila y la verificación de identidad.

    Retorna:
        (inversa, pasos)
    """
    if len(A) == 0:
        raise ValueError("La matriz no puede estar vacía.")

    filas = len(A)
    columnas = len(A[0])

    if filas != columnas:
        raise ValueError(
            f"Para calcular la inversa, la matriz debe ser cuadrada (n × n).\n"
            f"Dimensión actual: {filas} filas × {columnas} columnas."
        )

    n = filas

    # Construir la matriz aumentada [A | I_n] usando Fraction
    M = []
    for i in range(n):
        fila = [Fraction(valor) for valor in A[i]]
        # Agregar la fila correspondiente de la matriz identidad
        for j in range(n):
            fila.append(Fraction(1 if i == j else 0))
        M.append(fila)

    from modelo.matriz import formatear_fraccion

    pasos = []
    pasos.append("1. Construcción de la matriz aumentada [ A | I ] con la matriz identidad de orden " + str(n) + ":")

    def _formatear_aumentada(matriz):
        lineas = []
        for fila in matriz:
            parte_a = "  ".join(f"{formatear_fraccion(v):>8}" for v in fila[:n])
            parte_i = "  ".join(f"{formatear_fraccion(v):>8}" for v in fila[n:])
            lineas.append(f"[ {parte_a}  ┃  {parte_i} ]")
        return "\n".join(lineas)

    pasos.append(_formatear_aumentada(M))

    for i in range(n):
        # Pivoteo parcial: encontrar fila con el mayor valor absoluto en la columna i
        fila_max = max(range(i, n), key=lambda r: abs(M[r][i]))

        if M[fila_max][i] == 0:
            raise ValueError(
                "La matriz es singular (determinante = 0).\n"
                f"No existe pivote no nulo para la columna {i + 1}, por lo que no tiene matriz inversa."
            )

        # Intercambio de filas si es necesario
        if fila_max != i:
            M[i], M[fila_max] = M[fila_max], M[i]
            pasos.append(f"\nOperación elemental: Intercambiar fila f_{i + 1} ⟷ f_{fila_max + 1}")
            pasos.append(_formatear_aumentada(M))

        # Normalizar fila pivote para que el pivote sea 1
        pivote = M[i][i]
        if pivote != 1:
            for j in range(2 * n):
                M[i][j] /= pivote
            pasos.append(f"\nOperación elemental: f_{i + 1} ➔ f_{i + 1} / ({formatear_fraccion(pivote)})  [Normalizar pivote = 1]")
            pasos.append(_formatear_aumentada(M))

        # Hacer ceros en las demás filas
        for k in range(n):
            if k != i:
                factor = M[k][i]
                if factor != 0:
                    for j in range(2 * n):
                        M[k][j] -= factor * M[i][j]
                    signo = "−" if factor > 0 else "+"
                    pasos.append(
                        f"\nOperación elemental: f_{k + 1} ➔ f_{k + 1} {signo} ({formatear_fraccion(abs(factor))}) * f_{i + 1}"
                    )
                    pasos.append(_formatear_aumentada(M))

    # Extraer la submatriz derecha [n:] que contiene la inversa
    inversa = [[M[i][n + j] for j in range(n)] for i in range(n)]
    return inversa, pasos