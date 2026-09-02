from vista.ventana_principal import VentanaPrincipal
from modelo.solucionador import SolucionadorGauss, SolucionadorGaussJordan
from modelo.matriz import formatear_fraccion, formatear_matriz

class Controlador:
    def __init__(self, root):
        self.vista = VentanaPrincipal(root, self)
        
    def generar_cuadricula(self):
        try:
            m = int(self.vista.spin_m.get())
            n = int(self.vista.spin_n.get())
            
            if not (1 <= m <= 10) or not (1 <= n <= 10):
                self.vista.mostrar_error("Error", "Las dimensiones m y n deben estar entre 1 y 10.")
                return
                
            self.vista.construir_cuadricula(m, n)
            
        except ValueError:
            self.vista.mostrar_error("Error de entrada", "Por favor, ingrese valores enteros válidos para m y n.")
            
    def cargar_ejemplo(self, tipo):
        if tipo == "unica":
            # 3x3 consistente determinado
            A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
            b = [8, -11, -3]
        elif tipo == "infinitas":
            # 3x3 consistente indeterminado
            A = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
            b = [1, 2, 3]
        elif tipo == "inconsistente":
            # 3x3 inconsistente
            A = [[1, 2, 3], [1, 2, 3], [2, 1, 1]]
            b = [4, 5, 1]
            
        m = len(A)
        n = len(A[0])
        self.vista.spin_m.set(m)
        self.vista.spin_n.set(n)
        self.vista.construir_cuadricula(m, n)
        
        for i in range(m):
            for j in range(n):
                self.vista.matriz_entries[i][j].delete(0, 'end')
                self.vista.matriz_entries[i][j].insert(0, str(A[i][j]))
            self.vista.vector_entries[i].delete(0, 'end')
            self.vista.vector_entries[i].insert(0, str(b[i]))

    def resolver_sistema(self):
        try:
            m = len(self.vista.matriz_entries)
            n = len(self.vista.matriz_entries[0])
            
            from fractions import Fraction
            A = []
            for i in range(m):
                fila = []
                for j in range(n):
                    val = Fraction(self.vista.matriz_entries[i][j].get())
                    fila.append(val)
                A.append(fila)
                
            b = []
            for i in range(m):
                val = Fraction(self.vista.vector_entries[i].get())
                b.append(val)
                
        except ValueError:
            self.vista.mostrar_error("Error de Valor", "Todos los coeficientes deben ser números reales válidos.")
            return

        # Instanciar modelo y ejecutar lógica
        if self.vista.metodo.get() == "Gauss-Jordan":
            solucionador = SolucionadorGaussJordan(A, b)
        else:
            solucionador = SolucionadorGauss(A, b)
        solucionador.resolver()
        
        # Extraer y formatear datos del modelo
        clasificacion = solucionador.clasificacion
        
        texto_sol = ""
        texto_ver = ""
        
        if solucionador.es_valido:
            texto_sol = "Vector de Solución:\n"
            for i, val in enumerate(solucionador.solucion):
                texto_sol += f"x{i+1} = {formatear_fraccion(val)}\n"
                
            errores = solucionador.verificar()
            if errores:
                texto_ver = "Verificación (Ecuaciones originales):\n"
                for i, (calc, orig, err) in enumerate(errores):
                    texto_ver += f"Eq {i+1}: valor calculado = {formatear_fraccion(calc)}, valor original = {formatear_fraccion(orig)} | Error abs: {formatear_fraccion(err)}\n"
        else:
            texto_sol = "No hay una solución única."
            texto_ver = "Verificación no aplicable."
            
        self.vista.actualizar_resumen(clasificacion, texto_sol, texto_ver)
        
        # Formatear historial
        texto_historial = ""
        for paso, (mensaje, matriz) in enumerate(solucionador.historial):
            texto_historial += f"--- Paso {paso}: {mensaje} ---\n"
            texto_historial += formatear_matriz(matriz)
            texto_historial += "\n"
            
        self.vista.actualizar_historial(texto_historial)
