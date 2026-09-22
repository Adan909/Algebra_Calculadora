# modelo/conversiones.py

def decimal_a_base(numero_decimal, base):
    """
    Convierte un número decimal a la base especificada (2, 8 o 16)
    utilizando el algoritmo de divisiones sucesivas.
    
    Retorna una tupla: (cadena_resultado, cadena_proceso)
    """
    if numero_decimal == 0:
        return "0", "0 / {} = 0, residuo 0\nResultado: 0".format(base)

    if numero_decimal < 0:
        signo = "-"
        numero = abs(numero_decimal)
    else:
        signo = ""
        numero = numero_decimal

    residuos = []
    proceso = []
    actual = numero

    hex_chars = "0123456789ABCDEF"

    while actual > 0:
        cociente = actual // base
        residuo = actual % base
        
        char_residuo = hex_chars[residuo] if base == 16 else str(residuo)
        residuos.append(char_residuo)
        
        paso = f"  {actual} / {base} = {cociente}, residuo {char_residuo}"
        proceso.append(paso)
        
        actual = cociente

    residuos.reverse()
    resultado = signo + "".join(residuos)
    
    texto_proceso = "\n".join(proceso)
    texto_proceso += f"\nLeyendo los residuos de abajo hacia arriba: {resultado}"

    return resultado, texto_proceso

def base_a_decimal(cadena_numero, base):
    """
    Convierte una cadena que representa un número en una base dada (2, 8 o 16)
    a su equivalente decimal.
    
    Retorna una tupla: (valor_decimal, cadena_proceso)
    """
    cadena = cadena_numero.strip().upper()
    if not cadena:
        raise ValueError("La cadena está vacía.")
        
    signo = 1
    if cadena.startswith("-"):
        signo = -1
        cadena = cadena[1:]
    elif cadena.startswith("+"):
        cadena = cadena[1:]

    # Quitar posibles prefijos 0b, 0o, 0x
    if base == 2 and cadena.startswith("0B"):
        cadena = cadena[2:]
    elif base == 8 and cadena.startswith("0O"):
        cadena = cadena[2:]
    elif base == 16 and cadena.startswith("0X"):
        cadena = cadena[2:]

    if not cadena:
        raise ValueError("Número no válido.")

    hex_chars = "0123456789ABCDEF"
    
    decimal = 0
    longitud = len(cadena)
    
    partes_combinacion = []
    
    for i, char in enumerate(cadena):
        potencia = longitud - 1 - i
        
        if base == 16:
            if char not in hex_chars:
                raise ValueError(f"Dígito inválido '{char}' para base 16.")
            valor_digito = hex_chars.index(char)
        else:
            if not char.isdigit():
                raise ValueError(f"Dígito inválido '{char}' para base {base}.")
            valor_digito = int(char)
            if valor_digito >= base:
                raise ValueError(f"Dígito '{char}' no permitido en base {base}.")
                
        termino_valor = valor_digito * (base ** potencia)
        decimal += termino_valor
        
        partes_combinacion.append(f"{valor_digito} * {base}^{potencia}")
        
    decimal *= signo
    
    # Formatear el proceso
    texto_proceso = "Combinación lineal:\n"
    texto_proceso += " + ".join(partes_combinacion)
    
    valores_evaluados = []
    for i, char in enumerate(cadena):
        potencia = longitud - 1 - i
        val = (hex_chars.index(char) if base == 16 else int(char)) * (base ** potencia)
        valores_evaluados.append(str(val))
        
    texto_proceso += f"\n= {' + '.join(valores_evaluados)}"
    if signo == -1:
        texto_proceso += f"\n= -({sum(int(v) for v in valores_evaluados)})"
    texto_proceso += f"\n= {decimal}"

    return decimal, texto_proceso
