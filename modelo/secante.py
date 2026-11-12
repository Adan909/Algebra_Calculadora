import math
from dataclasses import dataclass
from fractions import Fraction

from modelo.biseccion import FuncionMatematica


@dataclass(frozen=True)
class IteracionSecante:
    numero: int
    x_anterior: float
    x_actual: float
    fx_anterior: float
    fx_actual: float
    aproximacion: float
    f_aproximacion: float
    error_relativo: float
    criterio_error: str


@dataclass(frozen=True)
class ResultadoSecante:
    raiz: float
    error_final: float | None
    iteraciones: tuple
    convergio: bool
    motivo: str


def _numero_real(valor, nombre):
    try:
        numero = float(Fraction(str(valor).strip()))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError(f"{nombre} debe ser un número real finito.") from error
    if not math.isfinite(numero):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    return numero


def secante(expresion, x_anterior, x_actual, error_permitido, max_iteraciones):
    funcion = expresion if isinstance(expresion, FuncionMatematica) else FuncionMatematica(expresion)
    x_anterior = _numero_real(x_anterior, "El valor inicial x₀")
    x_actual = _numero_real(x_actual, "El valor inicial x₁")
    error_permitido = _numero_real(error_permitido, "El error porcentual permitido")
    if x_anterior == x_actual:
        raise ValueError("Los valores iniciales x₀ y x₁ deben ser distintos.")
    if error_permitido <= 0:
        raise ValueError("El error porcentual permitido debe ser mayor que cero.")
    try:
        iteraciones_numericas = float(Fraction(str(max_iteraciones).strip()))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError("El máximo de iteraciones debe ser un entero positivo.") from error
    if (isinstance(max_iteraciones, bool) or not math.isfinite(iteraciones_numericas)
            or not iteraciones_numericas.is_integer()
            or not 1 <= iteraciones_numericas <= 100000):
        raise ValueError("El máximo de iteraciones debe ser un entero entre 1 y 100000.")
    max_iteraciones = int(iteraciones_numericas)

    fx_anterior = funcion.evaluar(x_anterior)
    if fx_anterior == 0:
        return ResultadoSecante(
            x_anterior, None, (), True, "El valor inicial x₀ ya es una raíz exacta.",
        )
    fx_actual = funcion.evaluar(x_actual)
    if fx_actual == 0:
        return ResultadoSecante(
            x_actual, None, (), True, "El valor inicial x₁ ya es una raíz exacta.",
        )

    filas = []
    for numero in range(1, max_iteraciones + 1):
        denominador = fx_actual - fx_anterior
        if denominador == 0:
            raise ValueError(
                "f(x₁) y f(x₀) son iguales; la fórmula de la secante no está definida."
            )
        aproximacion = x_actual - fx_actual * (x_actual - x_anterior) / denominador
        if not math.isfinite(aproximacion):
            raise ValueError("La iteración produjo un valor no finito.")
        f_aproximacion = funcion.evaluar(aproximacion)

        criterio = "error relativo porcentual"
        if aproximacion != 0:
            error = abs((aproximacion - x_actual) / aproximacion) * 100
        else:
            escala = max(abs(x_anterior), abs(x_actual), 1.0)
            error = abs(aproximacion - x_actual) / escala * 100
            criterio = "error relativo alternativo para x(n+1) = 0"

        filas.append(IteracionSecante(
            numero, x_anterior, x_actual, fx_anterior, fx_actual,
            aproximacion, f_aproximacion, error, criterio,
        ))

        if f_aproximacion == 0:
            return ResultadoSecante(
                aproximacion, error, tuple(filas), True, "Se encontró una raíz exacta.",
            )
        if error < error_permitido:
            return ResultadoSecante(
                aproximacion, error, tuple(filas), True, "Se alcanzó el error permitido.",
            )
        x_anterior, x_actual = x_actual, aproximacion
        fx_anterior, fx_actual = fx_actual, f_aproximacion

    return ResultadoSecante(
        filas[-1].aproximacion, filas[-1].error_relativo, tuple(filas), False,
        f"No se alcanzó el error permitido en {max_iteraciones} iteraciones.",
    )
