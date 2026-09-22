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
    de vectores, reutilizando el solucionador de Gauss.
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
    
    # Construir la matriz A (donde cada columna es un vector del conjunto)
    A = []
    for i in range(dimension):
        fila = []
        for j in range(cantidad_vectores):
            fila.append(Fraction(vectores[j][i]))
        A.append(fila)

    # Convertir b a fracciones
    b_frac = [Fraction(val) for val in b]

    # Reutilizar el solucionador existente
    from modelo.solucionador import SolucionadorGaussJordan
    solucionador = SolucionadorGaussJordan(A, b_frac)
    solucionador.resolver()

    # Si es inconsistente, no es combinación lineal
    if "Inconsistente" in solucionador.clasificacion:
        return False, []
        
    # Si tiene solución (única o infinitas) es combinación lineal.
    # En caso de infinitas soluciones, tomamos una solución particular 
    # asumiendo las variables libres como 0. 
    # El SolucionadorGaussJordan no maneja directamente la extracción 
    # completa de la solución paramétrica para uso externo, pero podemos 
    # extraer los coeficientes de la última columna de la matriz reducida.
    
    escalares = [Fraction(0)] * cantidad_vectores
    
    # Extraer los pivotes encontrados en la matriz aumentada reducida
    pivotes = []
    filas = len(solucionador.aumentada)
    cols = len(solucionador.aumentada[0]) - 1 # Sin contar b
    
    # Buscar variables principales
    for r in range(filas):
        for c in range(cols):
            if abs(solucionador.aumentada[r][c]) > 1e-10:
                pivotes.append((r, c))
                break
                
    for fila, col in pivotes:
        escalares[col] = solucionador.aumentada[fila][-1]

    return True, escalares