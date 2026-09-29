# modelo/romanos.py
import re
from fractions import Fraction

# Mapeo de valores de símbolos romanos individuales
VALORES_ROMANOS = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

# Tabla de descomposición para conversión de Arábigo a Romano
TABLA_ARABIGO_A_ROMANO = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I")
]

# Expresión regular estándar para números romanos válidos entre 1 y 3999
REGEX_ROMANO_ESTRICTO = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",
    re.IGNORECASE
)

def validar_romano(cadena):
    """
    Valida si una cadena de texto es un número romano clásico válido (1 a 3999).
    Lanza ValueError con explicación clara si no es válido.
    """
    texto = cadena.strip().upper()
    if not texto:
        raise ValueError("El número romano no puede estar vacío.")

    # Verificar caracteres no reconocidos
    caracteres_invalidos = [c for c in texto if c not in VALORES_ROMANOS]
    if caracteres_invalidos:
        raise ValueError(f"Caracteres no válidos para números romanos: {', '.join(set(caracteres_invalidos))}. Use solo I, V, X, L, C, D, M.")

    if not REGEX_ROMANO_ESTRICTO.match(texto):
        # Explicar razones comunes de fallo
        if "IIII" in texto or "XXXX" in texto or "CCCC" in texto or "MMMM" in texto:
            raise ValueError(f"'{texto}' es inválido: Los símbolos I, X, C, M no pueden repetirse más de 3 veces consecutivas.")
        if "VV" in texto or "LL" in texto or "DD" in texto:
            raise ValueError(f"'{texto}' es inválido: Los símbolos V, L, D no pueden repetirse.")
        raise ValueError(f"'{texto}' no sigue las reglas gramaticales estándar de la numeración romana.")

    return texto

def romano_a_arabigo(cadena):
    """
    Convierte un número romano a un entero normal (arábigo).
    Retorna una tupla: (valor_entero, texto_explicacion_paso_a_paso)
    """
    romano = validar_romano(cadena)
    
    pasos = []
    total = 0
    i = 0
    n = len(romano)
    
    pasos.append(f"Análisis del número romano '{romano}':")
    
    while i < n:
        actual = romano[i]
        val_actual = VALORES_ROMANOS[actual]
        
        if i + 1 < n:
            siguiente = romano[i + 1]
            val_siguiente = VALORES_ROMANOS[siguiente]
            
            # Caso sustractivo: símbolo menor antes de uno mayor
            if val_actual < val_siguiente:
                diferencia = val_siguiente - val_actual
                pasos.append(f"  • Par sustractivo '{actual}{siguiente}': {siguiente} ({val_siguiente}) - {actual} ({val_actual}) = {diferencia}")
                total += diferencia
                i += 2
                continue
        
        # Caso aditivo regular
        pasos.append(f"  • Símbolo aditivo '{actual}': +{val_actual}")
        total += val_actual
        i += 1
        
    pasos.append(f"  -> Total arábigo = {total}")
    return total, "\n".join(pasos)

def arabigo_a_romano(numero):
    """
    Convierte un número entero arábigo (1 a 3999) a su equivalente en número romano.
    Retorna una tupla: (cadena_romano, texto_explicacion)
    Si el número no es representable (<= 0 o > 3999), retorna (None, texto_explicacion).
    """
    if numero == 0:
        return "N/A", "El número 0 no tiene representación en el sistema de numeración romano clásico (los romanos utilizaban términos verbales como 'nulla' o simplemente no lo consideraban un número)."
        
    if numero < 0:
        return "N/A", f"El número {numero} es negativo. El sistema de numeración romano clásico no contempla valores negativos."
        
    if numero > 3999:
        return "N/A", f"El número {numero} excede el rango tradicional (1 - 3999). Para valores mayores o iguales a 4000, los romanos empleaban una barra horizontal superior (vinculum) multiplicativa."
        
    descomposicion = []
    romano = []
    resto = numero
    
    # Desglose posicional: Millares, Centenas, Decenas, Unidades
    millares = (numero // 1000) * 1000
    centenas = ((numero % 1000) // 100) * 100
    decenas = ((numero % 100) // 10) * 10
    unidades = numero % 10
    
    partes = []
    if millares > 0:
        partes.append((millares, "millares"))
    if centenas > 0:
        partes.append((centenas, "centenas"))
    if decenas > 0:
        partes.append((decenas, "decenas"))
    if unidades > 0:
        partes.append((unidades, "unidades"))
        
    descomposicion.append(f"Descomposición de {numero}:")
    for valor, desc in partes:
        # Encontrar la representación romana de esta parte
        temp = valor
        rom_parte = ""
        for v, s in TABLA_ARABIGO_A_ROMANO:
            while temp >= v and v >= (1000 if desc == "millares" else 100 if desc == "centenas" else 10 if desc == "decenas" else 1):
                rom_parte += s
                temp -= v
        descomposicion.append(f"  • {desc.capitalize()} ({valor}): {rom_parte}")
        romano.append(rom_parte)
        
    resultado_romano = "".join(romano)
    descomposicion.append(f"  -> Unión de componentes = {resultado_romano}")
    return resultado_romano, "\n".join(descomposicion)

def operar_lista_romanos(lista_romanos, operacion):
    """
    Realiza una operación (+, -, *, /) sobre una lista de 2 o más números romanos.
    
    Retorna un diccionario con:
    - 'exito': bool
    - 'error': str (si exito es False)
    - 'desglose_operandos': str
    - 'proceso_normal': str
    - 'proceso_romano': str
    - 'resultado_normal': int o float o Fraction
    - 'resultado_romano': str
    """
    if len(lista_romanos) < 2:
        return {
            'exito': False,
            'error': "Debe proporcionar al menos dos (2) números romanos para operar."
        }
        
    # 1. Convertir y desglosar cada operando
    desglose_operandos = []
    valores_arabigos = []
    romanos_limpios = []
    
    for idx, raw in enumerate(lista_romanos):
        try:
            val, texto_paso = romano_a_arabigo(raw)
            romanos_limpios.append(validar_romano(raw))
            valores_arabigos.append(val)
            desglose_operandos.append(f"[Número {idx + 1}]: {raw.strip().upper()} = {val}\n{texto_paso}\n")
        except ValueError as e:
            return {
                'exito': False,
                'error': f"Error en el operando #{idx + 1} ('{raw}'): {str(e)}"
            }

    # 2. Proceso aritmético en números normales y en números romanos
    proceso_normal_lineas = []
    proceso_romano_lineas = []
    
    nombres_ops = {
        '+': ("Suma", "+", "+"),
        '-': ("Resta", "-", "-"),
        '*': ("Multiplicación", "×", "×"),
        '/': ("División", "÷", "÷")
    }
    
    if operacion not in nombres_ops:
        return {
            'exito': False,
            'error': f"Operación no soportada: '{operacion}'. Use '+', '-', '*', '/'."
        }
        
    nombre_op, signo_norm, signo_rom = nombres_ops[operacion]
    
    proceso_normal_lineas.append(f"Operación: {nombre_op}")
    proceso_romano_lineas.append(f"Operación: {nombre_op}")
    
    # Expresión general
    exp_normal = f" {signo_norm} ".join(str(v) for v in valores_arabigos)
    exp_romana = f" {signo_rom} ".join(romanos_limpios)
    proceso_normal_lineas.append(f"Expresión numérica: {exp_normal}\n")
    proceso_romano_lineas.append(f"Expresión en romanos: {exp_romana}\n")
    
    acum_normal = valores_arabigos[0]
    acum_romano = romanos_limpios[0]
    
    proceso_normal_lineas.append("Paso a paso aritmético:")
    proceso_romano_lineas.append("Paso a paso en números romanos:")
    
    es_division = (operacion == '/')
    
    for i in range(1, len(valores_arabigos)):
        val_sig = valores_arabigos[i]
        rom_sig = romanos_limpios[i]
        
        ant_normal = acum_normal
        ant_romano = acum_romano
        
        if operacion == '+':
            acum_normal = ant_normal + val_sig
            res_rom, _ = arabigo_a_romano(acum_normal)
            acum_romano = res_rom
            proceso_normal_lineas.append(f"  Paso {i}: {ant_normal} + {val_sig} = {acum_normal}")
            proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} + {rom_sig} = {acum_romano}  (en normales: {ant_normal} + {val_sig} = {acum_normal})")
            
        elif operacion == '-':
            acum_normal = ant_normal - val_sig
            res_rom, expl_rom = arabigo_a_romano(acum_normal)
            acum_romano = res_rom
            proceso_normal_lineas.append(f"  Paso {i}: {ant_normal} - {val_sig} = {acum_normal}")
            if res_rom != "N/A":
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} - {rom_sig} = {acum_romano}  (en normales: {ant_normal} - {val_sig} = {acum_normal})")
            else:
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} - {rom_sig} = {acum_normal} [Sin representación romana directa: {expl_rom}]")
                
        elif operacion == '*':
            acum_normal = ant_normal * val_sig
            res_rom, expl_rom = arabigo_a_romano(acum_normal)
            acum_romano = res_rom
            proceso_normal_lineas.append(f"  Paso {i}: {ant_normal} × {val_sig} = {acum_normal}")
            if res_rom != "N/A":
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} × {rom_sig} = {acum_romano}  (en normales: {ant_normal} × {val_sig} = {acum_normal})")
            else:
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} × {rom_sig} = {acum_normal} [{expl_rom}]")
                
        elif operacion == '/':
            if val_sig == 0:
                return {'exito': False, 'error': f"División por cero en el paso {i}."}
            
            # En división tratamos cociente entero y residuo
            cociente = ant_normal // val_sig
            residuo = ant_normal % val_sig
            exacto = ant_normal / val_sig
            
            cociente_rom, _ = arabigo_a_romano(cociente)
            residuo_rom, _ = arabigo_a_romano(residuo)
            
            if residuo == 0:
                proceso_normal_lineas.append(f"  Paso {i}: {ant_normal} ÷ {val_sig} = {cociente} (División exacta)")
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} ÷ {rom_sig} = {cociente_rom} (División exacta)")
            else:
                proceso_normal_lineas.append(f"  Paso {i}: {ant_normal} ÷ {val_sig} = {cociente} con residuo {residuo} (Decimal exacto: {exacto:.4g})")
                proceso_romano_lineas.append(f"  Paso {i}: {ant_romano} ÷ {rom_sig} = Cociente {cociente_rom} ({cociente}) con Residuo {residuo_rom} ({residuo})")
                
            acum_normal = cociente  # Continuamos con el cociente entero para siguientes divisiones
            acum_romano = cociente_rom

    # Resultado final
    resultado_normal = acum_normal
    res_final_romano, expl_final_romano = arabigo_a_romano(resultado_normal)
    
    proceso_normal_lineas.append(f"\n-> Resultado Final Normal (Arábigo): {resultado_normal}")
    
    proceso_romano_lineas.append(f"\n-> Resultado Final Romano: {res_final_romano}")
    proceso_romano_lineas.append("\nProcedimiento de composición del resultado a número romano:")
    proceso_romano_lineas.append(expl_final_romano)

    return {
        'exito': True,
        'desglose_operandos': "\n".join(desglose_operandos),
        'proceso_normal': "\n".join(proceso_normal_lineas),
        'proceso_romano': "\n".join(proceso_romano_lineas),
        'resultado_normal': resultado_normal,
        'resultado_romano': res_final_romano
    }

def evaluar_expresion_romana(expresion):
    """
    Evalúa una expresión libre con números romanos y operadores (+, -, *, /).
    Ejemplo: 'XX + IV * II' o '(XIV - IV) * III'
    
    Muestra la traducción término a término, el orden de operaciones
    y el resultado tanto en arábigos como en romanos.
    """
    exp_limpia = expresion.strip()
    if not exp_limpia:
        return {'exito': False, 'error': "La expresión no puede estar vacía."}
        
    # Tokenizar números romanos, operadores y paréntesis
    tokens = re.findall(r'[A-Za-z]+|[+\-*/()]|\d+', exp_limpia)
    
    if not tokens:
        return {'exito': False, 'error': "Expresión vacía o no válida."}
        
    desglose_operandos = []
    tokens_arabigos = []
    
    vistos = {}
    
    for t in tokens:
        if t in "+-*/()":
            tokens_arabigos.append(t)
        elif t.isdigit():
            tokens_arabigos.append(t)
            desglose_operandos.append(f"Número arábigo detectado: {t}")
        else:
            # Debe ser romano
            try:
                val, expl = romano_a_arabigo(t)
                tokens_arabigos.append(str(val))
                if t.upper() not in vistos:
                    vistos[t.upper()] = val
                    desglose_operandos.append(f"Romano '{t.upper()}' = {val}\n{expl}\n")
            except ValueError as e:
                return {'exito': False, 'error': f"Símbolo no válido en expresión '{t}': {str(e)}"}
                
    exp_arabiga = " ".join(tokens_arabigos)
    
    # Evaluar de forma segura
    try:
        # Solo permitimos números, operadores y paréntesis
        if not re.match(r'^[\d\s+\-*/()]+$', exp_arabiga):
            return {'exito': False, 'error': "Expresión con caracteres no permitidos."}
        
        # Calcular resultado numérico usando Python
        # Para evitar división por cero o errores de sintaxis
        resultado_normal = eval(exp_arabiga, {"__builtins__": None}, {})
        
        if isinstance(resultado_normal, float) and resultado_normal.is_integer():
            resultado_normal = int(resultado_normal)
            
    except ZeroDivisionError:
        return {'exito': False, 'error': "Error matemático: División por cero."}
    except Exception as e:
        return {'exito': False, 'error': f"Sintaxis inválida en la expresión: {str(e)}"}
        
    res_romano, expl_romano = arabigo_a_romano(int(resultado_normal) if isinstance(resultado_normal, (int, float)) and resultado_normal > 0 else 0)
    if isinstance(resultado_normal, (int, float)) and (resultado_normal <= 0 or resultado_normal > 3999):
        res_romano, expl_romano = arabigo_a_romano(int(resultado_normal))
        
    proceso_normal = [
        f"Expresión original (Romana): {exp_limpia}",
        f"Expresión traducida (Normal): {exp_arabiga}",
        f"Evaluación respetando jerarquía de operaciones: {resultado_normal}"
    ]
    
    proceso_romano = [
        f"Resultado numérico obtenido: {resultado_normal}",
        f"Resultado en número romano: {res_romano}",
        "\nExplicación de la conversión:",
        expl_romano
    ]
    
    return {
        'exito': True,
        'desglose_operandos': "\n".join(desglose_operandos),
        'proceso_normal': "\n".join(proceso_normal),
        'proceso_romano': "\n".join(proceso_romano),
        'resultado_normal': resultado_normal,
        'resultado_romano': res_romano
    }
