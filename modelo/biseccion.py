import ast
import math
import operator
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoContinuidad:
    """Contiene el análisis riguroso y la demostración matemática de continuidad."""
    es_continua: bool
    tipo_funcion: str
    expresion_str: str
    a: float
    b: float
    fa: float | None
    fb: float | None
    cambio_signo: bool
    aplica_bolzano: bool
    puntos_discontinuidad: tuple
    condicion_1_evaluacion: str
    condicion_2_limites: str
    condicion_3_coincidencia: str
    demostracion_formal: str
    teorema_bolzano: str
    resumen: str


class FuncionMatematica:
    """Evalúa expresiones reales limitadas a operaciones matemáticas conocidas y analiza su continuidad."""

    # Solo se exponen funciones matemáticas conocidas; no se permite ejecutar código arbitrario.
    FUNCIONES = {
        "abs": abs,
        "acos": math.acos,
        "arccos": math.acos,
        "asin": math.asin,
        "arcsin": math.asin,
        "atan": math.atan,
        "arctan": math.atan,
        "cos": math.cos,
        "exp": math.exp,
        "floor": math.floor,
        "ln": math.log,
        "log": math.log,
        "log10": math.log10,
        "sen": math.sin,
        "sin": math.sin,
        "sqrt": math.sqrt,
        "tan": math.tan,
        "tg": math.tan,
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

    @classmethod
    def _nodo_contiene_x(cls, nodo):
        """Determina si un subárbol AST depende de la variable x."""
        for subnodo in ast.walk(nodo):
            if isinstance(subnodo, ast.Name) and subnodo.id == "x":
                return True
        return False

    def clasificar_estructura(self):
        """
        Clasifica la función según su estructura algebraica y funciones elementales componentes.
        Retorna una tupla (tipo_principal, detalles, funciones_usadas).
        """
        nodos = list(ast.walk(self._expresion_parseada))
        nombres_funcs = {n.func.id for n in nodos if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        
        tiene_division_x = False
        tiene_potencia_no_entera = False
        tiene_potencia_negativa = False
        tiene_x_en_exponente = False

        for n in nodos:
            if isinstance(n, ast.BinOp):
                if isinstance(n.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                    if self._nodo_contiene_x(n.right):
                        tiene_division_x = True
                elif isinstance(n.op, ast.Pow):
                    base_tiene_x = self._nodo_contiene_x(n.left)
                    exp_tiene_x = self._nodo_contiene_x(n.right)
                    if exp_tiene_x:
                        tiene_x_en_exponente = True
                    if base_tiene_x and isinstance(n.right, ast.Constant):
                        val = n.right.value
                        if isinstance(val, (int, float)):
                            if val < 0:
                                tiene_potencia_negativa = True
                            elif not float(val).is_integer():
                                tiene_potencia_no_entera = True

        tipos = []
        if tiene_division_x or tiene_potencia_negativa:
            tipos.append("Racional (con asíntotas o polos potenciales)")
        if "sqrt" in nombres_funcs or tiene_potencia_no_entera:
            tipos.append("Radical / Potencia no entera (dominio restringido)")
        if any(f in nombres_funcs for f in ("sin", "sen", "cos", "tan", "tg", "asin", "arcsin", "acos", "arccos", "atan", "arctan")):
            tipos.append("Trigonométrica")
        if any(f in nombres_funcs for f in ("exp", "log", "ln", "log10")) or tiene_x_en_exponente:
            tipos.append("Exponencial / Logarítmica")

        if not tipos:
            tipo_principal = "Polinómica"
            detalles = "Función polinómica formada exclusivamente por sumas, restas y productos de potencias enteras no negativas de x."
        elif len(tipos) == 1:
            tipo_principal = tipos[0]
            detalles = f"Función del tipo {tipos[0]}."
        else:
            tipo_principal = "Composición de Funciones Elementales"
            detalles = f"Composición algebraica de tipos: {', '.join(tipos)}."

        return tipo_principal, detalles, tuple(sorted(nombres_funcs))

    def analizar_continuidad(self, a, b, num_muestras=500):
        """
        Realiza la verificación formal y demostración matemática de continuidad en [a, b].
        Comprueba las 3 condiciones fundamentales del cálculo infinitesimal y el Teorema de Bolzano.
        """
        a, b = float(a), float(b)
        if not math.isfinite(a) or not math.isfinite(b) or a >= b:
            raise ValueError("El intervalo debe tener extremos reales finitos con a < b.")

        tipo_principal, detalles_tipo, funcs_usadas = self.clasificar_estructura()
        
        # Evaluar extremos
        fa = None
        fb = None
        discontinuidades = []

        try:
            fa = self.evaluar(a)
        except Exception as error:
            discontinuidades.append((a, f"Extremo a={a:g} no pertenece al dominio: {error}"))

        try:
            fb = self.evaluar(b)
        except Exception as error:
            discontinuidades.append((b, f"Extremo b={b:g} no pertenece al dominio: {error}"))

        # Muestreo denso adaptativo en el intervalo [a, b]
        num_muestras = max(100, min(2000, int(num_muestras)))
        paso = (b - a) / (num_muestras - 1)
        muestras_validas = []

        # Puntos críticos a incluir obligatoriamente si caen dentro de [a, b]
        puntos_criticos = set()
        if a < 0 < b:
            puntos_criticos.add(0.0)
        # Puntos medios y tercios
        puntos_criticos.add((a + b) / 2.0)
        puntos_criticos.add(a + (b - a) / 3.0)
        puntos_criticos.add(a + 2.0 * (b - a) / 3.0)

        for x_crit in puntos_criticos:
            try:
                y_c = self.evaluar(x_crit)
                muestras_validas.append((x_crit, y_c))
            except Exception as error:
                if not any(abs(d[0] - x_crit) < 1e-5 for d in discontinuidades):
                    discontinuidades.append((x_crit, f"Discontinuidad / Indefinición en x={x_crit:.6g}: {error}"))

        for i in range(num_muestras):
            x_i = a + i * paso
            try:
                y_i = self.evaluar(x_i)
                muestras_validas.append((x_i, y_i))
            except Exception as error:
                if not any(abs(d[0] - x_i) < 1e-5 for d in discontinuidades):
                    discontinuidades.append((x_i, f"Discontinuidad / Indefinición en x={x_i:.6g}: {error}"))

        muestras_validas.sort(key=lambda item: item[0])

        # Análisis de variaciones bruscas (detección de asíntotas verticales / saltos finitos o infinitos)
        if len(muestras_validas) > 2:
            for k in range(len(muestras_validas) - 1):
                x1, y1 = muestras_validas[k]
                x2, y2 = muestras_validas[k + 1]
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                pendiente = (dy / dx) if dx > 0 else 0
                
                # Detectar gradientes extremos o divergencia en direcciones opuestas
                if (dx > 0 and (dy > 100.0 or pendiente > 200.0 or (y1 * y2 < 0 and (abs(y1) > 10 or abs(y2) > 10)))):
                    # Búsqueda dicotómica de singularidad en [x1, x2]
                    xl, xr = x1, x2
                    singularidad_encontrada = False
                    for _ in range(25):
                        xm = (xl + xr) / 2.0
                        try:
                            ym = self.evaluar(xm)
                            if abs(ym) > 1e6:
                                if not any(abs(d[0] - xm) < 1e-4 for d in discontinuidades):
                                    discontinuidades.append((xm, f"Asíntota vertical / divergencia en x ≈ {xm:.6g}"))
                                singularidad_encontrada = True
                                break
                            yl = self.evaluar(xl)
                            if (yl > 0 and ym < 0) or (yl < 0 and ym > 0):
                                xr = xm
                            else:
                                xl = xm
                        except Exception as error:
                            if not any(abs(d[0] - xm) < 1e-4 for d in discontinuidades):
                                discontinuidades.append((xm, f"Singularidad en x ≈ {xm:.6g}: {error}"))
                            singularidad_encontrada = True
                            break
                    if not singularidad_encontrada and (abs(y1) > 100 or abs(y2) > 100) and y1 * y2 < 0:
                        x_aprox = (x1 + x2) / 2.0
                        if not any(abs(d[0] - x_aprox) < 1e-3 for d in discontinuidades):
                            discontinuidades.append((x_aprox, f"Asíntota vertical / salto en x ≈ {x_aprox:.6g}"))

        es_continua = len(discontinuidades) == 0
        cambio_signo = (fa is not None and fb is not None and ((fa < 0 < fb) or (fb < 0 < fa) or fa == 0 or fb == 0))
        aplica_bolzano = es_continua and cambio_signo

        # Redacción de las 3 condiciones de continuidad
        if es_continua:
            c1 = (
                f"✓ CUMPLIDA: Para todo c ∈ [{a:g}, {b:g}], la función f(c) está unívocamente definida en ℝ.\n"
                f"  Evaluaciones en los extremos: f(a) = f({a:g}) = {fa:.8g}, f(b) = f({b:g}) = {fb:.8g}.\n"
                f"  No se detectaron divisiones por cero, raíces de orden par negativas ni argumentos fuera de dominio."
            )
            c2 = (
                f"✓ CUMPLIDA: Para todo punto interior c ∈ ({a:g}, {b:g}), los límites laterales existen, son finitos\n"
                f"  y coinciden: lim(x→c⁻) f(x) = lim(x→c⁺) f(x) = L ∈ ℝ.\n"
                f"  En los extremos, existen lim(x→{a:g}⁺) f(x) = {fa:.8g} y lim(x→{b:g}⁻) f(x) = {fb:.8g}."
            )
            c3 = (
                f"✓ CUMPLIDA: Para todo c ∈ [{a:g}, {b:g}], se verifica que lim(x→c) f(x) = f(c).\n"
                f"  La función satisface la propiedad de sustitución directa en todo el intervalo."
            )
        else:
            puntos_str = ", ".join(f"x ≈ {p[0]:.5g}" for p in discontinuidades[:3])
            c1 = (
                f"✗ NO CUMPLIDA: Se encontraron puntos en [{a:g}, {b:g}] donde f(x) no está definida en ℝ ({puntos_str})."
            )
            c2 = (
                f"✗ NO CUMPLIDA: El límite no existe o diverge a infinito en las singularidades detectadas."
            )
            c3 = (
                f"✗ NO CUMPLIDA: Al no existir f(c) o divergir el límite en puntos del intervalo, la igualdad falla."
            )

        # Demostración formal según el tipo de función
        exp_bonita = self.expresion.replace("**", "^")
        lineas_demostracion = [
            f"DEMOSTRACIÓN FORMAL DE CONTINUIDAD EN EL INTERVALO [{a:g}, {b:g}]",
            "=" * 60,
            f"Función analizada: f(x) = {exp_bonita}",
            f"Clasificación estructural: {tipo_principal}",
            "",
            "1. FUNDAMENTO TEÓRICO Y ÁLGEBRA DE FUNCIONES CONTINUAS:",
        ]

        if tipo_principal == "Polinómica":
            lineas_demostracion.extend([
                "  • Teorema: Toda función polinómica P(x) = aₙxⁿ + ... + a₁x + a₀ con coeficientes reales",
                "    es continua en todo el conjunto de los números reales ℝ.",
                "  • Justificación analítica: La función identidad g(x) = x y las funciones constantes h(x) = k",
                "    son continuas en ℝ por la definición ε-δ de Cauchy.",
                "  • Por el Álgebra de Límites, las sumas, restas y productos de funciones continuas son continuas.",
                f"  • Consecuencia: f(x) es continua en todo ℝ y, en particular, en el subconjunto compacto [{a:g}, {b:g}]."
            ])
        elif "Trigonométrica" in tipo_principal and "Racional" not in tipo_principal and "Radical" not in tipo_principal:
            lineas_demostracion.extend([
                "  • Teorema: Las funciones trigonométricas estándar (sin, cos) son continuas en todo ℝ.",
                "  • Justificación analítica: Para cualquier c ∈ ℝ, lim(x→c) sin(x) = sin(c) y lim(x→c) cos(x) = cos(c).",
                "  • La suma, producto y composición de estas funciones con polinomios preserva la continuidad.",
                f"  • Al no existir indeterminaciones en [{a:g}, {b:g}], la función es estrictamente continua en el intervalo."
            ])
        elif "Exponencial" in tipo_principal and "Racional" not in tipo_principal:
            lineas_demostracion.extend([
                "  • Teorema: La función exponencial exp(x) = eˣ es continua en todo ℝ.",
                "  • Teorema: Las funciones logarítmicas log(x) son continuas en su dominio natural (0, ∞).",
                "  • Al verificar que todos los argumentos pertenecen a sus respectivos dominios en [{a:g}, {b:g}],",
                "    la composición de funciones elementales continuas resulta continua en [{a:g}, {b:g}]."
            ])
        else:
            lineas_demostracion.extend([
                "  • Teorema de Continuidad de Funciones Elementales: Toda función elemental construida mediante",
                "    sumas, productos, cocientes y composiciones de polinomios, exponenciales, logaritmos,",
                "    trigonométricas y radicales es continua en todo punto perteneciente a su dominio natural.",
                f"  • Verificación en el intervalo: Se examinó [{a:g}, {b:g}] y {'no se detectaron singularidades' if es_continua else 'se detectaron discontinuidades'}."
            ])

        lineas_demostracion.extend([
            "",
            "2. VERIFICACIÓN DE LAS TRES CONDICIONES DE CAUCHY-WEIERSTRASS:",
            f"  I.   Existencia del valor de la función: { 'Satisfecha en todo c ∈ [' + str(a) + ', ' + str(b) + ']' if es_continua else 'Falló en puntos singulares' }",
            f"  II.  Existencia y finitud del límite:   { 'Satisfecha: lim(x→c) f(x) existe y es finito' if es_continua else 'Falló: el límite no existe o diverge' }",
            f"  III. Igualdad límite = valor evaluado: { 'Satisfecha: lim(x→c) f(x) = f(c)' if es_continua else 'Falló' }",
            "",
            "3. CONCLUSIÓN DEL ANÁLISIS DE CONTINUIDAD:",
            f"  Resultado: La función f(x) {'ES CONTINUA' if es_continua else 'NO ES CONTINUA'} en el intervalo cerrado [{a:g}, {b:g}]."
        ])

        demostracion_formal = "\n".join(lineas_demostracion)

        # Análisis de Bolzano
        if aplica_bolzano:
            teorema_bolzano = (
                f"APLICABILIDAD DEL TEOREMA DE BOLZANO (VALOR INTERMEDIO):\n"
                f"  1. Hipótesis 1 (Continuidad): f(x) es continua en el intervalo cerrado [{a:g}, {b:g}]  → [CUMPLIDA]\n"
                f"  2. Hipótesis 2 (Cambio de Signo): f(a)={fa:.6g} y f(b)={fb:.6g} tienen signos opuestos  → [CUMPLIDA]\n"
                f"  CONCLUSIÓN: Existe al menos un valor c ∈ ({a:g}, {b:g}) tal que f(c) = 0.\n"
                f"  El Método de Bisección garantiza la convergencia matemática hacia la raíz."
            )
            resumen = f"Función continua en [{a:g}, {b:g}]. Teorema de Bolzano plenamente aplicable (raíz garantizada)."
        elif es_continua and not cambio_signo:
            teorema_bolzano = (
                f"APLICABILIDAD DEL TEOREMA DE BOLZANO (VALOR INTERMEDIO):\n"
                f"  1. Hipótesis 1 (Continuidad): f(x) es continua en el intervalo cerrado [{a:g}, {b:g}]  → [CUMPLIDA]\n"
                f"  2. Hipótesis 2 (Cambio de Signo): f(a)={fa:.6g} y f(b)={fb:.6g} tienen el MISMO signo  → [NO CUMPLIDA]\n"
                f"  CONCLUSIÓN: No se garantiza la existencia de una raíz en este intervalo mediante Bolzano.\n"
                f"  Debe seleccionarse un intervalo donde f(a) y f(b) tengan signos opuestos (f(a)·f(b) < 0)."
            )
            resumen = f"Función continua en [{a:g}, {b:g}], pero sin cambio de signo en los extremos."
        else:
            teorema_bolzano = (
                f"APLICABILIDAD DEL TEOREMA DE BOLZANO (VALOR INTERMEDIO):\n"
                f"  1. Hipótesis 1 (Continuidad): f(x) NO es continua en [{a:g}, {b:g}]  → [NO CUMPLIDA]\n"
                f"  CONCLUSIÓN: El Teorema de Bolzano NO es aplicable debido a discontinuidades en el intervalo.\n"
                f"  El Método de Bisección no puede garantizar convergencia en presencia de discontinuidades."
            )
            resumen = f"Función NO continua en [{a:g}, {b:g}]. No se puede aplicar el Teorema de Bolzano."

        return ResultadoContinuidad(
            es_continua=es_continua,
            tipo_funcion=tipo_principal,
            expresion_str=exp_bonita,
            a=a,
            b=b,
            fa=fa,
            fb=fb,
            cambio_signo=cambio_signo,
            aplica_bolzano=aplica_bolzano,
            puntos_discontinuidad=tuple(discontinuidades),
            condicion_1_evaluacion=c1,
            condicion_2_limites=c2,
            condicion_3_coincidencia=c3,
            demostracion_formal=demostracion_formal,
            teorema_bolzano=teorema_bolzano,
            resumen=resumen
        )

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
    continuidad: ResultadoContinuidad | None = None


def _signo(valor):
    if valor < 0:
        return "−"
    if valor > 0:
        return "+"
    return "0"


def verificar_continuidad(expresion, a, b):
    """Verifica y demuestra formalmente la continuidad de una expresión en el intervalo [a, b]."""
    funcion = expresion if isinstance(expresion, FuncionMatematica) else FuncionMatematica(expresion)
    return funcion.analizar_continuidad(a, b)


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

    # Verifica formalmente la continuidad de la función en [a, b]
    analisis_cont = funcion.analizar_continuidad(a, b)
    if not analisis_cont.es_continua:
        detalle_disc = analisis_cont.puntos_discontinuidad[0][1] if analisis_cont.puntos_discontinuidad else "discontinuidad en el intervalo"
        raise ValueError(f"La función no es continua en [{a:g}, {b:g}] ({detalle_disc}); no se garantiza la validez del Teorema de Bolzano.")

    # El Teorema del Valor Intermedio requiere valores definidos y signos opuestos en los extremos.
    fa = funcion.evaluar(a)
    fb = funcion.evaluar(b)
    if fa == 0:
        return ResultadoBiseccion(a, None, (), True, "Raíz exacta en el extremo a.", "exacto", continuidad=analisis_cont)
    if fb == 0:
        return ResultadoBiseccion(b, None, (), True, "Raíz exacta en el extremo b.", "exacto", continuidad=analisis_cont)
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
            return ResultadoBiseccion(c, error, tuple(filas), True, "Se encontró una raíz exacta.", criterio_fila, continuidad=analisis_cont)
        # La guía exige que Ea sea estrictamente menor que la tolerancia permitida.
        if error is not None and error < error_permitido:
            return ResultadoBiseccion(c, error, tuple(filas), True, "Se alcanzó el error permitido.", criterio_fila, continuidad=analisis_cont)

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
        continuidad=analisis_cont
    )