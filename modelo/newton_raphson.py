import ast
import copy
import math
from dataclasses import dataclass
from fractions import Fraction

from modelo.biseccion import FuncionMatematica


@dataclass(frozen=True)
class FuncionDerivada:
    arbol: ast.expr
    expresion: str

    def evaluar(self, x):
        try:
            resultado = FuncionMatematica._evaluar_nodo(self.arbol, x)
            resultado = float(resultado)
            if not math.isfinite(resultado):
                raise ValueError("La derivada no está definida en el punto evaluado.")
            return resultado
        except ValueError:
            raise
        except Exception as error:
            raise ValueError(f"No se pudo evaluar f'({x:g}): {error}") from error


@dataclass(frozen=True)
class IteracionNewtonRaphson:
    numero: int
    x: float
    fx: float
    derivada: float
    siguiente_x: float
    siguiente_fx: float
    error_relativo: float | None
    criterio_error: str


@dataclass(frozen=True)
class ResultadoNewtonRaphson:
    raiz: float
    error_final: float | None
    iteraciones: tuple
    convergio: bool
    motivo: str
    expresion_derivada: str


def _constante(valor):
    return ast.Constant(value=valor)


def _binario(operador, izquierda, derecha):
    return ast.BinOp(left=izquierda, op=operador(), right=derecha)


def _producto(izquierda, derecha):
    if isinstance(izquierda, ast.Constant) and izquierda.value == 0:
        return _constante(0)
    if isinstance(derecha, ast.Constant) and derecha.value == 0:
        return _constante(0)
    if isinstance(izquierda, ast.Constant) and izquierda.value == 1:
        return derecha
    if isinstance(derecha, ast.Constant) and derecha.value == 1:
        return izquierda
    return _binario(ast.Mult, izquierda, derecha)


def _suma(izquierda, derecha):
    if isinstance(izquierda, ast.Constant) and izquierda.value == 0:
        return derecha
    if isinstance(derecha, ast.Constant) and derecha.value == 0:
        return izquierda
    return _binario(ast.Add, izquierda, derecha)


def _negar(expresion):
    return ast.UnaryOp(op=ast.USub(), operand=expresion)


def _llamada(nombre, *argumentos):
    return ast.Call(
        func=ast.Name(id=nombre, ctx=ast.Load()),
        args=list(argumentos),
        keywords=[],
    )


def _derivar(nodo):
    if isinstance(nodo, ast.Constant):
        return _constante(0)
    if isinstance(nodo, ast.Name):
        return _constante(1 if nodo.id == "x" else 0)
    if isinstance(nodo, ast.UnaryOp):
        derivada = _derivar(nodo.operand)
        if isinstance(nodo.op, ast.USub):
            return _negar(derivada)
        return derivada
    if isinstance(nodo, ast.BinOp):
        izquierda = copy.deepcopy(nodo.left)
        derecha = copy.deepcopy(nodo.right)
        derivada_izquierda = _derivar(nodo.left)
        derivada_derecha = _derivar(nodo.right)
        if isinstance(nodo.op, ast.Add):
            return _suma(derivada_izquierda, derivada_derecha)
        if isinstance(nodo.op, ast.Sub):
            return _binario(ast.Sub, derivada_izquierda, derivada_derecha)
        if isinstance(nodo.op, ast.Mult):
            return _suma(
                _producto(derivada_izquierda, derecha),
                _producto(izquierda, derivada_derecha),
            )
        if isinstance(nodo.op, ast.Div):
            numerador = _binario(
                ast.Sub,
                _producto(derivada_izquierda, derecha),
                _producto(izquierda, derivada_derecha),
            )
            return _binario(
                ast.Div, numerador, _binario(ast.Pow, derecha, _constante(2))
            )
        if isinstance(nodo.op, ast.Pow):
            if isinstance(derivada_derecha, ast.Constant) and derivada_derecha.value == 0:
                if isinstance(nodo.right, ast.Constant) and nodo.right.value == 0:
                    return _constante(0)
                exponente_menos_uno = _binario(
                    ast.Sub, copy.deepcopy(nodo.right), _constante(1)
                )
                return _producto(
                    _producto(
                        copy.deepcopy(nodo.right),
                        _binario(ast.Pow, izquierda, exponente_menos_uno),
                    ),
                    derivada_izquierda,
                )
            return _producto(
                _binario(ast.Pow, izquierda, derecha),
                _suma(
                    _producto(
                        derivada_derecha,
                        _llamada("ln", copy.deepcopy(nodo.left)),
                    ),
                    _binario(
                        ast.Div,
                        _producto(copy.deepcopy(nodo.right), derivada_izquierda),
                        copy.deepcopy(nodo.left),
                    ),
                ),
            )
    if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
        nombre = nodo.func.id
        if nombre == "floor":
            raise ValueError(
                f"Newton-Raphson requiere una derivada; no se puede derivar "
                f"automáticamente la función {nombre}."
            )
        if len(nodo.args) != 1:
            raise ValueError(
                "Newton-Raphson solo admite funciones matemáticas con un argumento."
            )
        argumento = copy.deepcopy(nodo.args[0])
        derivada_argumento = _derivar(nodo.args[0])
        if nombre == "abs":
            factor = _binario(
                ast.Div, copy.deepcopy(nodo.args[0]), _llamada("abs", argumento)
            )
        elif nombre == "sin":
            factor = _llamada("cos", argumento)
        elif nombre == "cos":
            factor = _negar(_llamada("sin", argumento))
        elif nombre == "tan":
            factor = _binario(
                ast.Div,
                _constante(1),
                _binario(ast.Pow, _llamada("cos", argumento), _constante(2)),
            )
        elif nombre == "exp":
            factor = _llamada("exp", argumento)
        elif nombre == "ln":
            factor = _binario(ast.Div, _constante(1), argumento)
        elif nombre in {"log", "log10"}:
            factor = _binario(
                ast.Div,
                _constante(1 / math.log(10)),
                argumento,
            )
        elif nombre == "sqrt":
            factor = _binario(
                ast.Div,
                _constante(1),
                _producto(_constante(2), _llamada("sqrt", argumento)),
            )
        elif nombre == "asin":
            factor = _binario(
                ast.Div,
                _constante(1),
                _llamada(
                    "sqrt",
                    _binario(
                        ast.Sub,
                        _constante(1),
                        _binario(ast.Pow, argumento, _constante(2)),
                    ),
                ),
            )
        elif nombre == "acos":
            factor = _negar(
                _binario(
                    ast.Div,
                    _constante(1),
                    _llamada(
                        "sqrt",
                        _binario(
                            ast.Sub,
                            _constante(1),
                            _binario(ast.Pow, argumento, _constante(2)),
                        ),
                    ),
                )
            )
        elif nombre == "atan":
            factor = _binario(
                ast.Div,
                _constante(1),
                _suma(_constante(1), _binario(ast.Pow, argumento, _constante(2))),
            )
        else:
            raise ValueError(
                f"No hay una regla de derivación disponible para {nombre}."
            )
        return _producto(factor, derivada_argumento)
    raise ValueError("No se pudo obtener la derivada de la expresión.")


def derivar(funcion):
    arbol = ast.fix_missing_locations(_derivar(funcion._expresion_parseada))
    return FuncionDerivada(arbol, ast.unparse(arbol))


def _numero_real(valor, nombre):
    try:
        numero = float(Fraction(str(valor).strip()))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError(f"{nombre} debe ser un número real finito.") from error
    if not math.isfinite(numero):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    return numero


def newton_raphson(expresion, x_inicial, error_permitido, max_iteraciones):
    funcion = expresion if isinstance(expresion, FuncionMatematica) else FuncionMatematica(expresion)
    x = _numero_real(x_inicial, "El valor inicial x₀")
    error_permitido = _numero_real(error_permitido, "El error porcentual permitido")
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

    fx = funcion.evaluar(x)
    if fx == 0:
        return ResultadoNewtonRaphson(
            x, None, (), True, "El valor inicial ya es una raíz exacta.",
            "",
        )

    funcion_derivada = derivar(funcion)
    filas = []
    for numero in range(1, max_iteraciones + 1):
        derivada_actual = funcion_derivada.evaluar(x)
        if derivada_actual == 0:
            raise ValueError(
                f"La derivada es cero en x = {x:.10g}; no se puede continuar "
                "con el método de Newton-Raphson."
            )
        siguiente_x = x - fx / derivada_actual
        if not math.isfinite(siguiente_x):
            raise ValueError("La iteración produjo un valor no finito.")
        siguiente_fx = funcion.evaluar(siguiente_x)

        error = None
        criterio = "error relativo porcentual"
        if numero > 1:
            if siguiente_x != 0:
                error = abs((siguiente_x - x) / siguiente_x) * 100
            else:
                escala = max(abs(x), 1.0)
                error = abs(siguiente_x - x) / escala * 100
                criterio = "error relativo alternativo para x(i+1) = 0"

        filas.append(IteracionNewtonRaphson(
            numero, x, fx, derivada_actual, siguiente_x, siguiente_fx, error, criterio,
        ))

        if siguiente_fx == 0:
            return ResultadoNewtonRaphson(
                siguiente_x, error, tuple(filas), True, "Se encontró una raíz exacta.",
                funcion_derivada.expresion,
            )
        if error is not None and error < error_permitido:
            return ResultadoNewtonRaphson(
                siguiente_x, error, tuple(filas), True, "Se alcanzó el error permitido.",
                funcion_derivada.expresion,
            )
        x, fx = siguiente_x, siguiente_fx

    return ResultadoNewtonRaphson(
        filas[-1].siguiente_x, filas[-1].error_relativo, tuple(filas), False,
        f"No se alcanzó el error permitido en {max_iteraciones} iteraciones.",
        funcion_derivada.expresion,
    )
