# modelo/operaciones_matrices.py

from fractions import Fraction


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