# modelo/matriz.py

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

def formatear_matriz(matriz):
    """
    Devuelve una representación en cadena (string) formateada de la matriz.
    Útil para mostrar el historial en la interfaz gráfica.
    """
    texto = ""
    for fila in matriz:
        texto += "[ " + "  ".join(f"{val:8.3f}" for val in fila) + " ]\n"
    return texto
