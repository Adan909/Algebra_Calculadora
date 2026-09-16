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
