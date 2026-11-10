class IteracionRF:
    """Clase para almacenar los datos de cada iteración y pasarlos a la tabla de la vista."""
    def __init__(self, numero, a, b, c, fa, fb, fc, signo_producto, extremo_modificado, nuevo_a, nuevo_b, error_relativo, criterio_error="error relativo porcentual"):
        self.numero = numero
        self.a = a
        self.b = b
        self.c = c
        self.fa = fa
        self.fb = fb
        self.fc = fc
        self.signo_producto = signo_producto
        self.extremo_modificado = extremo_modificado
        self.nuevo_a = nuevo_a
        self.nuevo_b = nuevo_b
        self.error_relativo = error_relativo
        self.criterio_error = criterio_error

class ResultadoRF:
    """Clase para encapsular el resultado final y enviarlo a la vista."""
    def __init__(self, raiz, error_final, convergio, iteraciones, motivo=""):
        self.raiz = raiz
        self.error_final = error_final
        self.convergio = convergio
        self.iteraciones = iteraciones
        self.motivo = motivo
        self.continuidad = None  # Se llenará desde el controlador si se analiza

def calcular_regula_falsi(funcion, a, b, error_esperado, max_iter):
    iteraciones = []
    
    # 1. Corrección: Usar .evaluar() en lugar de llamar al objeto directamente
    fa = funcion.evaluar(a)
    fb = funcion.evaluar(b)
    
    if fa * fb > 0:
        raise ValueError("La función no cambia de signo en el intervalo [a, b]. f(a) y f(b) tienen el mismo signo.")
        
    error_aprox = 100.0
    c_anterior = 0
    c = 0
    convergio = False
    
    for i in range(1, max_iter + 1):
        fa = funcion.evaluar(a)
        fb = funcion.evaluar(b)
        
        # Fórmula de Falsa Posición
        c = b - (fb * (a - b)) / (fa - fb)
        fc = funcion.evaluar(c)
        
        if i > 1:
            if c != 0:
                error_aprox = abs((c - c_anterior) / c) * 100
            else:
                error_aprox = 0.0
                
        signo_prod = "< 0" if (fa * fc) < 0 else "> 0" if (fa * fc) > 0 else "= 0"
        
        # Lógica de reemplazo de intervalos
        nuevo_a, nuevo_b = a, b
        extremo_mod = ""
        
        if fa * fc < 0:
            nuevo_b = c
            extremo_mod = "b (xu)"
        elif fa * fc > 0:
            nuevo_a = c
            extremo_mod = "a (xl)"
        else:
            extremo_mod = "Raíz exacta encontrada"
            
        iteracion = IteracionRF(
            numero=i, a=a, b=b, c=c, 
            fa=fa, fb=fb, fc=fc,
            signo_producto=signo_prod, extremo_modificado=extremo_mod,
            nuevo_a=nuevo_a, nuevo_b=nuevo_b, 
            error_relativo=error_aprox if i > 1 else None
        )
        iteraciones.append(iteracion)
        
        if error_aprox < error_esperado or fc == 0:
            convergio = True
            break
            
        a, b = nuevo_a, nuevo_b
        c_anterior = c
        
    motivo = "Raíz encontrada con el error deseado." if convergio else "Se alcanzó el número máximo de iteraciones sin lograr la tolerancia."
    return ResultadoRF(raiz=c, error_final=error_aprox if i > 1 else None, convergio=convergio, iteraciones=iteraciones, motivo=motivo)