import ast
import math
import operator
import re
from dataclasses import dataclass


class FuncionMatematica:
    """Evalúa expresiones reales limitadas a operaciones matemáticas conocidas."""

    # Solo se exponen funciones matemáticas conocidas; no se permite ejecutar código arbitrario.
    FUNCIONES = {
        "abs": abs,
        "acos": math.acos,
        "asin": math.asin,
        "atan": math.atan,
        "cos": math.cos,
        "exp": math.exp,
        "floor": math.floor,
        "log": math.log,
        "log10": math.log10,
        "sin": math.sin,
        "sqrt": math.sqrt,
        "tan": math.tan,
    }

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def __init__(self, expresion):
        expresion = expresion.strip()
        if not expresion or len(expresion) > 200:
            raise ValueError("Ingrese una función válida de hasta 200 caracteres.")
        if re.search(r"\*{3,}", expresion):
            raise ValueError("La función contiene un operador de potencia inválido.")

        # Acepta la notación habitual de potencias y la traduce al formato del evaluador.
        self.expresion = expresion.replace("^", "**")
        try:
            self._expresion_parseada = ast.parse(self.expresion, mode="eval").body
        except SyntaxError as error:
            raise ValueError("La expresión matemática tiene una sintaxis inválida.") from error
        try:
            self._validar(self._expresion_parseada)
        except Exception as error:
            raise ValueError(f"Función inválida: {error}") from error

    @classmethod
    def _validar(cls, nodo):
        if isinstance(nodo, ast.Constant):
            if isinstance(nodo.value, bool) or not isinstance(nodo.value, (int, float)):
                raise ValueError("Solo se permiten números reales.")
        elif isinstance(nodo, ast.Name):
            if nodo.id not in {"x", "pi", "e"}:
                raise ValueError(f"Nombre no permitido: {nodo.id}.")
        elif isinstance(nodo, ast.BinOp) and type(nodo.op) in cls.OPERADORES:
            cls._validar(nodo.left)
            cls._validar(nodo.right)
        elif isinstance(nodo, ast.UnaryOp) and type(nodo.op) in cls.OPERADORES:
            cls._validar(nodo.operand)
        elif (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
              and nodo.func.id in cls.FUNCIONES and not nodo.keywords):
            for argumento in nodo.args:
                cls._validar(argumento)
        else:
            raise ValueError("La expresión contiene una operación no permitida.")

    @staticmethod
    def _potencia_limitada(base, exponente):
        # Impide expresiones con exponentes extremos que puedan consumir recursos excesivos.
        if abs(exponente) > 100:
            raise ValueError("El exponente debe tener magnitud igual o menor que 100.")
        return base ** exponente

    @classmethod
    def _evaluar_nodo(cls, nodo, x):
        if isinstance(nodo, ast.Constant):
            return nodo.value
        if isinstance(nodo, ast.Name):
            return {"x": x, "pi": math.pi, "e": math.e}[nodo.id]
        if isinstance(nodo, ast.BinOp):
            izquierda = cls._evaluar_nodo(nodo.left, x)
            derecha = cls._evaluar_nodo(nodo.right, x)
            if isinstance(nodo.op, ast.Pow):
                return cls._potencia_limitada(izquierda, derecha)
            return cls.OPERADORES[type(nodo.op)](izquierda, derecha)
        if isinstance(nodo, ast.UnaryOp):
            return cls.OPERADORES[type(nodo.op)](cls._evaluar_nodo(nodo.operand, x))
        if isinstance(nodo, ast.Call):
            argumentos = [cls._evaluar_nodo(argumento, x) for argumento in nodo.args]
            return cls.FUNCIONES[nodo.func.id](*argumentos)
        raise ValueError("La expresión contiene una operación no permitida.")

    def evaluar(self, x):
        try:
            resultado = self._evaluar_nodo(self._expresion_parseada, x)
            if isinstance(resultado, bool) or not isinstance(resultado, (int, float)):
                raise ValueError("La función debe producir un valor real.")
            resultado = float(resultado)
            if not math.isfinite(resultado):
                raise ValueError("La función no está definida en uno de los puntos evaluados.")
            return resultado
        except ValueError:
            raise
        except Exception as error:
            raise ValueError(f"No se pudo evaluar f({x:g}): {error}") from error


@dataclass(frozen=True)
class IteracionBiseccion:
    numero: int
    a: float
    b: float
    c: float
    fa: float
    fb: float
    fc: float
    signo_producto: str
    error_relativo: float | None
    extremo_modificado: str
    nuevo_a: float
    nuevo_b: float
    criterio_error: str


@dataclass(frozen=True)
class ResultadoBiseccion:
    raiz: float
    error_final: float | None
    iteraciones: tuple
    convergio: bool
    motivo: str
    criterio_error: str


def _signo(valor):
    if valor < 0:
        return "−"
    if valor > 0:
        return "+"
    return "0"


def biseccion(expresion, a, b, error_permitido, max_iteraciones):
    """Calcula una raíz y conserva cada intervalo y evaluación para explicar el método."""
    funcion = expresion if isinstance(expresion, FuncionMatematica) else FuncionMatematica(expresion)
    a, b, error_permitido = float(a), float(b), float(error_permitido)
    if not math.isfinite(a) or not math.isfinite(b) or a >= b:
        raise ValueError("El intervalo debe tener extremos reales finitos con a < b.")
    if not math.isfinite(error_permitido) or error_permitido <= 0:
        raise ValueError("El error porcentual permitido debe ser mayor que cero.")
    try:
        iteraciones_numericas = float(max_iteraciones)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("El máximo de iteraciones debe ser un entero positivo.") from error
    if (isinstance(max_iteraciones, bool) or not math.isfinite(iteraciones_numericas)
            or not iteraciones_numericas.is_integer() or not 1 <= iteraciones_numericas <= 100000):
        raise ValueError("El máximo de iteraciones debe ser un entero entre 1 y 100000.")
    max_iteraciones = int(iteraciones_numericas)

    # El Teorema del Valor Intermedio requiere valores definidos y signos opuestos en los extremos.
    fa = funcion.evaluar(a)
    fb = funcion.evaluar(b)
    if fa == 0:
        return ResultadoBiseccion(a, None, (), True, "Raíz exacta en el extremo a.", "exacto")
    if fb == 0:
        return ResultadoBiseccion(b, None, (), True, "Raíz exacta en el extremo b.", "exacto")
    if _signo(fa) == _signo(fb):
        raise ValueError("No hay cambio de signo entre f(a) y f(b); no se garantiza una raíz en el intervalo.")

    filas = []
    anterior = None
    criterio = "error relativo porcentual"
    for numero in range(1, max_iteraciones + 1):
        # Forma el punto medio sin redondear; estos valores internos alimentan toda la tabla.
        c = a + (b - a) / 2
        fc = funcion.evaluar(c)
        # Comparar signos evita multiplicar f(a) por f(c) y desbordar números grandes.
        producto_signo = "0" if fc == 0 else "+" if _signo(fa) == _signo(fc) else "−"

        error = None
        criterio_fila = "error relativo porcentual"
        if anterior is not None:
            if c != 0:
                error = abs((c - anterior) / c) * 100
            else:
                # Si el nuevo punto es cero, usa el ancho del intervalo como error relativo alternativo.
                escala = max(abs(a), abs(b), 1.0)
                error = abs(b - a) / escala * 100
                criterio_fila = "ancho relativo del intervalo (alternativo para c = 0)"

        # Conserva el subintervalo cuyo producto de signos es negativo.
        if fc == 0:
            modificado, nuevo_a, nuevo_b = "Ninguno (raíz exacta)", a, b
        elif producto_signo == "−":
            modificado, nuevo_a, nuevo_b = "b", a, c
        else:
            modificado, nuevo_a, nuevo_b = "a", c, b

        filas.append(IteracionBiseccion(
            numero, a, b, c, fa, fb, fc, producto_signo, error,
            modificado, nuevo_a, nuevo_b, criterio_fila,
        ))

        if fc == 0:
            return ResultadoBiseccion(c, error, tuple(filas), True, "Se encontró una raíz exacta.", criterio_fila)
        # La guía exige que Ea sea estrictamente menor que la tolerancia permitida.
        if error is not None and error < error_permitido:
            return ResultadoBiseccion(c, error, tuple(filas), True, "Se alcanzó el error permitido.", criterio_fila)

        a, b = nuevo_a, nuevo_b
        if modificado == "a":
            # Reutiliza f(c) como nuevo f(a) en la siguiente iteración.
            fa = fc
        elif modificado == "b":
            # Reutiliza f(c) como nuevo f(b) en la siguiente iteración.
            fb = fc
        anterior = c
        criterio = criterio_fila

    return ResultadoBiseccion(
        filas[-1].c, filas[-1].error_relativo, tuple(filas), False,
        f"No se alcanzó el error permitido en {max_iteraciones} iteraciones.", criterio,
    )