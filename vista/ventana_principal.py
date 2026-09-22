import tkinter as tk
from tkinter import ttk, messagebox
from vista.componentes import ScrollableFrame

class VentanaPrincipal:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Calculadora de Álgebra Lineal MVC")
        self.root.geometry("1000x800")
        
        self.controlador = controlador
        
        # Estilo general moderno
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        BG_COLOR = "#f4f4f9"
        FG_COLOR = "#333333"
        ACCENT_COLOR = "#4a90e2"
        FONT_MAIN = ("Segoe UI", 10)
        FONT_TITLE = ("Segoe UI", 12, "bold")
        
        self.root.configure(bg=BG_COLOR)
        self.style.configure(".", background=BG_COLOR, foreground=FG_COLOR, font=FONT_MAIN)
        self.style.configure("TLabelFrame", background=BG_COLOR, font=FONT_TITLE)
        self.style.configure("TLabelFrame.Label", font=FONT_TITLE, foreground=ACCENT_COLOR)
        self.style.configure("TButton", background=ACCENT_COLOR, foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("TButton", background=[("active", "#357abd")])
        self.style.configure("TNotebook", background=BG_COLOR)
        self.style.configure("TNotebook.Tab", font=FONT_MAIN, padding=[10, 5])
        
        # Contenedor Principal es ahora un Notebook
        self.notebook_principal = ttk.Notebook(self.root)
        self.notebook_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas Principales
        self.tab_matrices_gauss = ttk.Frame(self.notebook_principal, padding="10")
        self.notebook_principal.add(self.tab_matrices_gauss, text="Sistemas de Ecuaciones (Gauss)")

        self.tab_vectoriales = ttk.Frame(self.notebook_principal, padding="10")
        self.notebook_principal.add(self.tab_vectoriales, text="Vectores y Matrices")

        self.tab_conversiones = ttk.Frame(self.notebook_principal, padding="10")
        self.notebook_principal.add(self.tab_conversiones, text="Conversiones de Base")

        self._construir_pestaña_gauss()
        self._construir_pestaña_vectoriales()
        self._construir_pestaña_conversiones()

    # ==========================================
    # PESTAÑA 1: SISTEMAS DE ECUACIONES (GAUSS)
    # ==========================================
    def _construir_pestaña_gauss(self):
        # Panel Config
        frame_config = ttk.LabelFrame(self.tab_matrices_gauss, text="Dimensiones del Sistema", padding="10")
        frame_config.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame_config, text="Filas (m):").grid(row=0, column=0, padx=5, pady=5)
        self.spin_m = ttk.Spinbox(frame_config, from_=1, to=10, width=5)
        self.spin_m.set(3)
        self.spin_m.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_config, text="Columnas (n):").grid(row=0, column=2, padx=5, pady=5)
        self.spin_n = ttk.Spinbox(frame_config, from_=1, to=10, width=5)
        self.spin_n.set(3)
        self.spin_n.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_generar = ttk.Button(frame_config, text="Generar Cuadrícula", command=self.controlador.generar_cuadricula)
        self.btn_generar.grid(row=0, column=4, padx=20, pady=5)

        ttk.Label(frame_config, text="Método:").grid(row=0, column=5, padx=(5, 2), pady=5)
        self.metodo = tk.StringVar(value="Gauss")
        self.selector_metodo = ttk.Combobox(
            frame_config, textvariable=self.metodo,
            values=("Gauss", "Gauss-Jordan"), state="readonly", width=14
        )
        self.selector_metodo.grid(row=0, column=6, padx=5, pady=5)
        
        frame_ejemplos = ttk.Frame(frame_config)
        frame_ejemplos.grid(row=1, column=0, columnspan=7, pady=10)
        ttk.Label(frame_ejemplos, text="Cargar Ejemplo:", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Solución Única", command=lambda: self.controlador.cargar_ejemplo("unica")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Infinitas Soluciones", command=lambda: self.controlador.cargar_ejemplo("infinitas")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Sin Solución", command=lambda: self.controlador.cargar_ejemplo("inconsistente")).pack(side=tk.LEFT, padx=5)

        # Panel Matriz
        self.frame_matriz_outer = ttk.LabelFrame(self.tab_matrices_gauss, text="Ingreso de Coeficientes", padding="10")
        self.frame_matriz_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.scroll_matriz = ScrollableFrame(self.frame_matriz_outer)
        self.scroll_matriz.pack(fill=tk.BOTH, expand=True)
        self.matriz_entries = []
        self.vector_entries = []
        
        self.btn_resolver = ttk.Button(self.frame_matriz_outer, text="Resolver Sistema", state=tk.DISABLED, command=self.controlador.resolver_sistema)
        self.btn_resolver.pack(pady=10)

        # Panel Resultados
        frame_resultados = ttk.Notebook(self.tab_matrices_gauss)
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        
        self.tab_resumen = ttk.Frame(frame_resultados, padding="10")
        frame_resultados.add(self.tab_resumen, text="Resumen de Solución")
        self.lbl_clasificacion = ttk.Label(self.tab_resumen, text="Clasificación: -", font=("Segoe UI", 12, "bold"), foreground="#d9534f")
        self.lbl_clasificacion.pack(anchor="w", pady=10)
        self.txt_solucion = tk.Text(self.tab_resumen, height=6, state=tk.DISABLED, bg="#ffffff", font=("Consolas", 11), relief=tk.FLAT, borderwidth=1)
        self.txt_solucion.pack(fill=tk.BOTH, expand=True, pady=5)
        self.lbl_verificacion = ttk.Label(self.tab_resumen, text="Verificación: -", font=("Segoe UI", 11, "bold"))
        self.lbl_verificacion.pack(anchor="w", pady=5)
        self.txt_verificacion = tk.Text(self.tab_resumen, height=6, state=tk.DISABLED, bg="#ffffff", font=("Consolas", 11), relief=tk.FLAT, borderwidth=1)
        self.txt_verificacion.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tab_historial = ttk.Frame(frame_resultados, padding="10")
        frame_resultados.add(self.tab_historial, text="Historial Paso a Paso")
        self.txt_historial = tk.Text(self.tab_historial, wrap=tk.NONE, state=tk.DISABLED, font=("Consolas", 11), bg="#1e1e1e", fg="#d4d4d4", relief=tk.FLAT)
        scroll_y = ttk.Scrollbar(self.tab_historial, orient="vertical", command=self.txt_historial.yview)
        scroll_x = ttk.Scrollbar(self.tab_historial, orient="horizontal", command=self.txt_historial.xview)
        self.txt_historial.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.txt_historial.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.tab_historial.grid_rowconfigure(0, weight=1)
        self.tab_historial.grid_columnconfigure(0, weight=1)

    def construir_cuadricula(self, m, n):
        for widget in self.scroll_matriz.scrollable_frame.winfo_children():
            widget.destroy()
        self.matriz_entries = []
        self.vector_entries = []
        
        ttk.Label(self.scroll_matriz.scrollable_frame, text="Matriz A").grid(row=0, column=0, columnspan=n, pady=(0, 5))
        ttk.Label(self.scroll_matriz.scrollable_frame, text="Vector b").grid(row=0, column=n, padx=(15, 0), pady=(0, 5))
        
        for i in range(m):
            fila_entries = []
            for j in range(n):
                entry = ttk.Entry(self.scroll_matriz.scrollable_frame, width=8, font=("Consolas", 11), justify="center")
                entry.grid(row=i+1, column=j, padx=2, pady=5)
                entry.insert(0, "0")
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)
            
            entry_b = ttk.Entry(self.scroll_matriz.scrollable_frame, width=8, font=("Consolas", 11, "bold"), justify="center")
            entry_b.grid(row=i+1, column=n, padx=(15, 0), pady=5)
            entry_b.insert(0, "0")
            self.vector_entries.append(entry_b)
            
        self.btn_resolver.config(state=tk.NORMAL)

    def actualizar_resumen(self, clasificacion, solucion_texto, verificacion_texto):
        self.lbl_clasificacion.config(text=f"Clasificación: {clasificacion}")
        self.txt_solucion.config(state=tk.NORMAL)
        self.txt_solucion.delete(1.0, tk.END)
        self.txt_solucion.insert(tk.END, solucion_texto)
        self.txt_solucion.config(state=tk.DISABLED)
        self.txt_verificacion.config(state=tk.NORMAL)
        self.txt_verificacion.delete(1.0, tk.END)
        self.txt_verificacion.insert(tk.END, verificacion_texto)
        self.txt_verificacion.config(state=tk.DISABLED)

    def actualizar_historial(self, historial_texto):
        self.txt_historial.config(state=tk.NORMAL)
        self.txt_historial.delete(1.0, tk.END)
        self.txt_historial.insert(tk.END, historial_texto)
        self.txt_historial.config(state=tk.DISABLED)


    # ==========================================
    # PESTAÑA 2: VECTORIALES Y MATRICIALES
    # ==========================================
    def _construir_pestaña_vectoriales(self):
        notebook_vectores = ttk.Notebook(self.tab_vectoriales)
        notebook_vectores.pack(fill=tk.BOTH, expand=True)
        
        # --- Sub-Pestaña Vectores ---
        tab_vec = ttk.Frame(notebook_vectores, padding="10")
        notebook_vectores.add(tab_vec, text="Vectores (Rn)")
        
        frame_config_v = ttk.LabelFrame(tab_vec, text="Configuración", padding="10")
        frame_config_v.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame_config_v, text="Dimensión (n):").pack(side=tk.LEFT, padx=5)
        self.spin_dim_v = ttk.Spinbox(frame_config_v, from_=1, to=10, width=5)
        self.spin_dim_v.set(3)
        self.spin_dim_v.pack(side=tk.LEFT, padx=5)
        ttk.Label(frame_config_v, text="Vectores (k):").pack(side=tk.LEFT, padx=5)
        self.spin_cant_v = ttk.Spinbox(frame_config_v, from_=1, to=10, width=5)
        self.spin_cant_v.set(2)
        self.spin_cant_v.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_config_v, text="Generar", command=self.controlador.generar_vectores).pack(side=tk.LEFT, padx=20)
        ttk.Label(frame_config_v, text="Escalar Mult.:").pack(side=tk.LEFT, padx=5)
        self.entrada_escalar_vector = ttk.Entry(frame_config_v, width=5)
        self.entrada_escalar_vector.insert(0, "1")
        self.entrada_escalar_vector.pack(side=tk.LEFT, padx=5)
        
        self.scroll_vectores = ScrollableFrame(tab_vec)
        self.scroll_vectores.pack(fill=tk.BOTH, expand=True, pady=10)
        self.vec_entries = []
        self.vec_b_entries = []
        
        ttk.Button(tab_vec, text="Calcular Operaciones y Combinación Lineal", command=self.controlador.operar_vectores).pack(pady=5)
        self.txt_res_vectores = tk.Text(tab_vec, height=10, state=tk.DISABLED, font=("Consolas", 11))
        self.txt_res_vectores.pack(fill=tk.X, pady=5)

        # --- Sub-Pestaña Matrices ---
        tab_mat = ttk.Frame(notebook_vectores, padding="10")
        notebook_vectores.add(tab_mat, text="Operaciones de Matrices")
        
        frame_config_m = ttk.LabelFrame(tab_mat, text="Dimensiones", padding="10")
        frame_config_m.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame_config_m, text="Matriz A (FilxCol):").pack(side=tk.LEFT, padx=2)
        self.spin_fa = ttk.Spinbox(frame_config_m, from_=1, to=10, width=4)
        self.spin_fa.set(2)
        self.spin_fa.pack(side=tk.LEFT, padx=2)
        self.spin_ca = ttk.Spinbox(frame_config_m, from_=1, to=10, width=4)
        self.spin_ca.set(2)
        self.spin_ca.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(frame_config_m, text="Matriz B (FilxCol):").pack(side=tk.LEFT, padx=(15, 2))
        self.spin_fb = ttk.Spinbox(frame_config_m, from_=1, to=10, width=4)
        self.spin_fb.set(2)
        self.spin_fb.pack(side=tk.LEFT, padx=2)
        self.spin_cb = ttk.Spinbox(frame_config_m, from_=1, to=10, width=4)
        self.spin_cb.set(2)
        self.spin_cb.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(frame_config_m, text="Generar Matrices", command=self.controlador.generar_matrices_ops).pack(side=tk.LEFT, padx=15)
        
        self.scroll_matrices_ops = ScrollableFrame(tab_mat)
        self.scroll_matrices_ops.pack(fill=tk.BOTH, expand=True, pady=10)
        self.mat_entries_a = []
        self.mat_entries_b = []
        
        frame_ctrl_m = ttk.Frame(tab_mat)
        frame_ctrl_m.pack(fill=tk.X, pady=5)
        ttk.Button(frame_ctrl_m, text="A + B", command=lambda: self.controlador.operar_matrices("suma")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ctrl_m, text="A - B", command=lambda: self.controlador.operar_matrices("resta")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ctrl_m, text="A × B", command=lambda: self.controlador.operar_matrices("multiplicacion")).pack(side=tk.LEFT, padx=5)
        ttk.Label(frame_ctrl_m, text="Escalar (c):").pack(side=tk.LEFT, padx=(20, 5))
        self.entrada_escalar_mat = ttk.Entry(frame_ctrl_m, width=5)
        self.entrada_escalar_mat.insert(0, "2")
        self.entrada_escalar_mat.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ctrl_m, text="c × A", command=lambda: self.controlador.operar_matrices("escalar")).pack(side=tk.LEFT, padx=5)
        
        self.txt_res_matrices = tk.Text(tab_mat, height=10, state=tk.DISABLED, font=("Consolas", 11))
        self.txt_res_matrices.pack(fill=tk.X, pady=5)

    def construir_vectores(self, n, k):
        for widget in self.scroll_vectores.scrollable_frame.winfo_children():
            widget.destroy()
        self.vec_entries = []
        self.vec_b_entries = []
        
        for i in range(k):
            ttk.Label(self.scroll_vectores.scrollable_frame, text=f"v{i+1}:").grid(row=i, column=0, padx=5, pady=5)
            fila_entries = []
            for j in range(n):
                entry = ttk.Entry(self.scroll_vectores.scrollable_frame, width=6, justify="center")
                entry.grid(row=i, column=j+1, padx=2, pady=5)
                entry.insert(0, "0")
                fila_entries.append(entry)
            self.vec_entries.append(fila_entries)
            
        ttk.Label(self.scroll_vectores.scrollable_frame, text="b:", font=("Segoe UI", 10, "bold")).grid(row=k, column=0, padx=5, pady=15)
        for j in range(n):
            entry_b = ttk.Entry(self.scroll_vectores.scrollable_frame, width=6, justify="center")
            entry_b.grid(row=k, column=j+1, padx=2, pady=15)
            entry_b.insert(0, "0")
            self.vec_b_entries.append(entry_b)

    def mostrar_resultado_vectores(self, texto):
        self.txt_res_vectores.config(state=tk.NORMAL)
        self.txt_res_vectores.delete(1.0, tk.END)
        self.txt_res_vectores.insert(tk.END, texto)
        self.txt_res_vectores.config(state=tk.DISABLED)

    def construir_matrices_ops(self, m_a, n_a, m_b, n_b):
        for widget in self.scroll_matrices_ops.scrollable_frame.winfo_children():
            widget.destroy()
        self.mat_entries_a = []
        self.mat_entries_b = []
        
        ttk.Label(self.scroll_matrices_ops.scrollable_frame, text="Matriz A", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=n_a, pady=5)
        for i in range(m_a):
            fila = []
            for j in range(n_a):
                entry = ttk.Entry(self.scroll_matrices_ops.scrollable_frame, width=6, justify="center")
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.mat_entries_a.append(fila)
            
        offset_col = n_a + 2
        ttk.Label(self.scroll_matrices_ops.scrollable_frame, text="Matriz B", font=("Segoe UI", 10, "bold")).grid(row=0, column=offset_col, columnspan=n_b, pady=5)
        for i in range(m_b):
            fila = []
            for j in range(n_b):
                entry = ttk.Entry(self.scroll_matrices_ops.scrollable_frame, width=6, justify="center")
                entry.grid(row=i+1, column=j+offset_col, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.mat_entries_b.append(fila)

    def mostrar_resultado_matrices(self, texto):
        self.txt_res_matrices.config(state=tk.NORMAL)
        self.txt_res_matrices.delete(1.0, tk.END)
        self.txt_res_matrices.insert(tk.END, texto)
        self.txt_res_matrices.config(state=tk.DISABLED)

    # ==========================================
    # PESTAÑA 3: CONVERSIONES
    # ==========================================
    def _construir_pestaña_conversiones(self):
        # A Decimal
        frame_a_decimal = ttk.LabelFrame(self.tab_conversiones, text="Conversión hacia Decimal (Muestra la Combinación Lineal)", padding="10")
        frame_a_decimal.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_a_decimal, text="Número original:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_conv_origen = ttk.Entry(frame_a_decimal, width=15)
        self.entry_conv_origen.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_a_decimal, text="Base de origen:").grid(row=0, column=2, padx=5, pady=5)
        self.base_origen = tk.StringVar(value="Binario")
        ttk.Combobox(frame_a_decimal, textvariable=self.base_origen, values=("Binario", "Octal", "Hexadecimal"), state="readonly", width=12).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_a_decimal, text="Convertir a Decimal", command=self.controlador.convertir_a_decimal).grid(row=0, column=4, padx=15, pady=5)

        # Desde Decimal
        frame_desde_decimal = ttk.LabelFrame(self.tab_conversiones, text="Conversión desde Decimal", padding="10")
        frame_desde_decimal.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_desde_decimal, text="Número decimal:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_conv_decimal = ttk.Entry(frame_desde_decimal, width=15)
        self.entry_conv_decimal.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_desde_decimal, text="Base de destino:").grid(row=0, column=2, padx=5, pady=5)
        self.base_destino = tk.StringVar(value="Binario")
        ttk.Combobox(frame_desde_decimal, textvariable=self.base_destino, values=("Binario", "Octal", "Hexadecimal"), state="readonly", width=12).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_desde_decimal, text="Convertir", command=self.controlador.convertir_desde_decimal).grid(row=0, column=4, padx=15, pady=5)

        # Resultados de conversiones
        ttk.Label(self.tab_conversiones, text="Resultados y Procedimiento:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=5)
        self.txt_resultados_conv = tk.Text(self.tab_conversiones, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", font=("Consolas", 11), relief=tk.FLAT, borderwidth=1)
        self.txt_resultados_conv.pack(fill=tk.BOTH, expand=True)

    def mostrar_resultado_conversion(self, texto):
        self.txt_resultados_conv.config(state=tk.NORMAL)
        self.txt_resultados_conv.delete(1.0, tk.END)
        self.txt_resultados_conv.insert(tk.END, texto)
        self.txt_resultados_conv.config(state=tk.DISABLED)

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

