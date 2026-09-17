# modelo/vectores.py

from fractions import Fraction


def sumar_vectores(v1, v2):
    """
    Suma dos vectores de Rn.

    Procedimiento algebraico equivalente:
    Si v1 = (a1, a2, ..., an) y v2 = (b1, b2, ..., bn),
    entonces:

    v1 + v2 = (a1+b1, a2+b2, ..., an+bn)

    Ambos vectores deben tener la misma dimensión.
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión.")

    resultado = []

    for i in range(len(v1)):
        resultado.append(v1[i] + v2[i])

    return resultado


def restar_vectores(v1, v2):
    """
    Resta dos vectores de Rn.

    Procedimiento algebraico equivalente:
    Si v1 = (a1, ..., an) y v2 = (b1, ..., bn),
    entonces:

    v1 - v2 = (a1-b1, ..., an-bn)

    Ambos vectores deben tener la misma dimensión.
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión.")

    resultado = []

    for i in range(len(v1)):
        resultado.append(v1[i] - v2[i])

    return resultado


def multiplicar_vector_escalar(vector, escalar):
    """
    Multiplica un vector por un escalar.

    Procedimiento algebraico equivalente:
    Si v = (a1, a2, ..., an) y c es un escalar:

    c*v = (c*a1, c*a2, ..., c*an)
    """
    resultado = []

    for valor in vector:
        resultado.append(valor * escalar)

    return resultado


def sumar_vectores_multiplicados(vectores, escalares):
    """
    Calcula una combinación lineal de varios vectores.

    Procedimiento algebraico equivalente:

    c1*v1 + c2*v2 + ... + ck*vk

    Primero se multiplica cada vector por su escalar
    y después se suman los vectores resultantes.
    """
    if len(vectores) == 0:
        raise ValueError("Debe existir al menos un vector.")

    if len(vectores) != len(escalares):
        raise ValueError(
            "La cantidad de vectores debe coincidir con "
            "la cantidad de escalares."
        )

    dimension = len(vectores[0])

    for vector in vectores:
        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener la misma dimensión."
            )

    resultado = [Fraction(0) for _ in range(dimension)]

    for i in range(len(vectores)):
        vector_multiplicado = multiplicar_vector_escalar(
            vectores[i],
            escalares[i]
        )

        for j in range(dimension):
            resultado[j] += vector_multiplicado[j]

    return resultado


def es_combinacion_lineal(vectores, b):
    """
    Determina si el vector b es combinación lineal de un conjunto
    de vectores.

    Procedimiento algebraico equivalente:

    Se busca determinar si existen escalares
    c1, c2, ..., ck tales que:

    c1*v1 + c2*v2 + ... + ck*vk = b

    Para ello se construye el sistema:

    A*c = b

    donde las columnas de A son los vectores v1, v2, ..., vk.

    Se utiliza eliminación de Gauss para determinar si el sistema
    es compatible.
    """

    if len(vectores) == 0:
        return False, []

    dimension = len(b)

    for vector in vectores:
        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener la misma dimensión que b."
            )

    cantidad_vectores = len(vectores)

    # Construir la matriz aumentada [A | b].
    #
    # Cada columna corresponde a uno de los vectores.
    # La última columna corresponde al vector b.
    matriz = []

    for i in range(dimension):
        fila = []

        for j in range(cantidad_vectores):
            fila.append(Fraction(vectores[j][i]))

        fila.append(Fraction(b[i]))

        matriz.append(fila)

    solucion, compatible = _resolver_sistema(matriz)

    return compatible, solucion


def _resolver_sistema(matriz):
    """
    Resuelve un sistema lineal utilizando eliminación de Gauss.

    Procedimiento algebraico equivalente:
    Se transforma la matriz aumentada [A|b] mediante operaciones
    elementales sobre las filas hasta obtener una forma escalonada.

    Las operaciones permitidas son:

    1. Intercambiar dos filas.
    2. Multiplicar una fila por un número distinto de cero.
    3. Sumar a una fila un múltiplo de otra.

    Si aparece una fila:

    [0  0  ...  0 | c]

    con c diferente de cero, el sistema es incompatible.
    """
    matriz = [
        [Fraction(valor) for valor in fila]
        for fila in matriz
    ]

    filas = len(matriz)
    columnas = len(matriz[0])

    variables = columnas - 1

    fila_pivote = 0
    pivotes = []

    for columna in range(variables):

        # Buscar una fila que tenga un valor diferente de cero
        # en la columna actual.
        fila_encontrada = None

        for i in range(fila_pivote, filas):
            if matriz[i][columna] != 0:
                fila_encontrada = i
                break

        # Si toda la columna es cero, no existe pivote.
        if fila_encontrada is None:
            continue

        # Intercambiar filas si es necesario.
        if fila_encontrada != fila_pivote:
            matriz[fila_pivote], matriz[fila_encontrada] = (
                matriz[fila_encontrada],
                matriz[fila_pivote]
            )

        # Convertir el pivote en 1.
        pivote = matriz[fila_pivote][columna]

        for j in range(columnas):
            matriz[fila_pivote][j] /= pivote

        # Hacer cero debajo del pivote.
        for i in range(fila_pivote + 1, filas):
            factor = matriz[i][columna]

            if factor != 0:
                for j in range(columnas):
                    matriz[i][j] -= factor * matriz[fila_pivote][j]

        pivotes.append(columna)
        fila_pivote += 1

        if fila_pivote == filas:
            break

    # Comprobar incompatibilidad.
    for i in range(filas):
        todos_cero = True

        for j in range(variables):
            if matriz[i][j] != 0:
                todos_cero = False
                break

        if todos_cero and matriz[i][variables] != 0:
            return [], False

    # Si hay variables libres, tomamos esas variables como 0.
    solucion = [Fraction(0) for _ in range(variables)]

    # Sustitución hacia atrás.
    for i in range(len(pivotes) - 1, -1, -1):
        columna = pivotes[i]

        valor = matriz[i][variables]

        for j in range(columna + 1, variables):
            valor -= matriz[i][j] * solucion[j]

        solucion[columna] = valor / matriz[i][columna]

    return solucion, True