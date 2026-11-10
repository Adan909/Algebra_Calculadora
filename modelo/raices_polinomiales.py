import ast
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoRaicesPolinomio:
    raices: tuple[float, ...] | None


def _recortar(coeficientes):
    while len(coeficientes) > 1 and coeficientes[-1] == 0:
        coeficientes.pop()
    return coeficientes


def _sumar(a, b):
    resultado = [0.0] * max(len(a), len(b))
    for indice, coeficiente in enumerate(a):
        resultado[indice] += coeficiente
    for indice, coeficiente in enumerate(b):
        resultado[indice] += coeficiente
    return _recortar(resultado)


def _multiplicar(a, b):
    if len(a) + len(b) - 2 > 100:
        return None
    resultado = [0.0] * (len(a) + len(b) - 1)
    for indice_a, coeficiente_a in enumerate(a):
        for indice_b, coeficiente_b in enumerate(b):
            resultado[indice_a + indice_b] += coeficiente_a * coeficiente_b
    if not all(math.isfinite(coeficiente) for coeficiente in resultado):
        return None
    return _recortar(resultado)


def _extraer_polinomio(nodo):
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return [float(nodo.value)]
    if isinstance(nodo, ast.Name):
        if nodo.id == "x":
            return [0.0, 1.0]
        if nodo.id == "pi":
            return [math.pi]
        if nodo.id == "e":
            return [math.e]
        return None
    if isinstance(nodo, ast.UnaryOp):
        polinomio = _extraer_polinomio(nodo.operand)
        if polinomio is None:
            return None
        if isinstance(nodo.op, ast.UAdd):
            return polinomio
        if isinstance(nodo.op, ast.USub):
            return [-coeficiente for coeficiente in polinomio]
        return None
    if not isinstance(nodo, ast.BinOp):
        return None

    izquierda = _extraer_polinomio(nodo.left)
    derecha = _extraer_polinomio(nodo.right)
    if izquierda is None or derecha is None:
        return None
    if isinstance(nodo.op, ast.Add):
        return _sumar(izquierda, derecha)
    if isinstance(nodo.op, ast.Sub):
        return _sumar(izquierda, [-coeficiente for coeficiente in derecha])
    if isinstance(nodo.op, ast.Mult):
        return _multiplicar(izquierda, derecha)
    if isinstance(nodo.op, ast.Div) and len(derecha) == 1 and derecha[0] != 0:
        resultado = [coeficiente / derecha[0] for coeficiente in izquierda]
        return resultado if all(math.isfinite(coeficiente) for coeficiente in resultado) else None
    if isinstance(nodo.op, ast.Pow) and len(derecha) == 1:
        exponente = derecha[0]
        if not exponente.is_integer():
            return None
        if exponente < 0:
            if len(izquierda) == 1 and izquierda[0] != 0:
                return [izquierda[0] ** int(exponente)]
            return None
        if exponente > 100:
            return None
        resultado = [1.0]
        for _ in range(int(exponente)):
            resultado = _multiplicar(resultado, izquierda)
            if resultado is None:
                return None
        return resultado
    return None


def _evaluar(coeficientes, x):
    valor = 0.0
    for coeficiente in reversed(coeficientes):
        valor = valor * x + coeficiente
    return valor


def _cerca_de_cero(coeficientes, x, valor):
    escala = 0.0
    magnitud_x = abs(x)
    for coeficiente in reversed(coeficientes):
        escala = escala * magnitud_x + abs(coeficiente)
    return escala == 0 or abs(valor) <= 1e-12 * escala


def _bisecar_raiz(coeficientes, izquierda, derecha, valor_izquierda):
    for _ in range(200):
        medio = izquierda + (derecha - izquierda) / 2
        valor_medio = _evaluar(coeficientes, medio)
        if valor_medio == 0:
            return medio
        if (valor_izquierda < 0) == (valor_medio < 0):
            izquierda, valor_izquierda = medio, valor_medio
        else:
            derecha = medio
        if derecha - izquierda <= 1e-12 * max(1.0, abs(medio)):
            break
    return izquierda + (derecha - izquierda) / 2


def _raices_reales(coeficientes):
    coeficientes = _recortar(coeficientes)
    grado = len(coeficientes) - 1
    if grado <= 0:
        return []
    if not all(math.isfinite(coeficiente) for coeficiente in coeficientes):
        raise OverflowError("Los coeficientes del polinomio exceden el rango numérico.")

    escala = max(abs(coeficiente) for coeficiente in coeficientes)
    coeficientes = [coeficiente / escala for coeficiente in coeficientes]
    if grado == 1:
        return [-coeficientes[0] / coeficientes[1]]

    cota = 1 + max(abs(coeficiente / coeficientes[-1]) for coeficiente in coeficientes[:-1])
    if not math.isfinite(cota):
        raise OverflowError("No se pudo acotar numéricamente las raíces del polinomio.")

    derivada = [indice * coeficientes[indice] for indice in range(1, len(coeficientes))]
    criticos = _raices_reales(derivada)
    puntos = [-cota, *[x for x in criticos if -cota < x < cota], cota]
    raices = [x for x in criticos if _cerca_de_cero(coeficientes, x, _evaluar(coeficientes, x))]

    for izquierda, derecha in zip(puntos, puntos[1:]):
        valor_izquierda = _evaluar(coeficientes, izquierda)
        valor_derecha = _evaluar(coeficientes, derecha)
        if (_cerca_de_cero(coeficientes, izquierda, valor_izquierda)
                or _cerca_de_cero(coeficientes, derecha, valor_derecha)):
            continue
        if (valor_izquierda < 0) != (valor_derecha < 0):
            raices.append(_bisecar_raiz(coeficientes, izquierda, derecha, valor_izquierda))

    raices.sort()
    distintas = []
    for raiz in raices:
        if not distintas or abs(raiz - distintas[-1]) > 1e-12 * max(1.0, abs(raiz)):
            distintas.append(raiz)
    return distintas


def encontrar_raices_reales(funcion):
    """Calcula numéricamente las raíces reales distintas si la expresión es un polinomio."""
    coeficientes = _extraer_polinomio(funcion._expresion_parseada)
    if coeficientes is None:
        return None
    coeficientes = _recortar(coeficientes)
    if not all(math.isfinite(coeficiente) for coeficiente in coeficientes):
        raise OverflowError("Los coeficientes del polinomio exceden el rango numérico.")
    if len(coeficientes) == 1 and coeficientes[0] == 0:
        return ResultadoRaicesPolinomio(None)
    return ResultadoRaicesPolinomio(tuple(_raices_reales(coeficientes)))
