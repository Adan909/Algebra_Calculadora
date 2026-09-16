import tkinter as tk
from tkinter import ttk, messagebox
from vista.componentes import ScrollableFrame

class VentanaPrincipal:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Calculadora de Eliminación Gaussiana MVC")
        self.root.geometry("900x700")
        
        self.controlador = controlador
        
        # Estilo general moderno
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configurar colores y fuentes
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
        
        # Contenedor Principal
        self.main_container = ttk.Frame(self.root, padding="15")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self._crear_panel_configuracion()
        self._crear_panel_matriz()
        self._crear_panel_resultados()
        
    def _crear_panel_configuracion(self):
        frame_config = ttk.LabelFrame(self.main_container, text="Dimensiones del Sistema", padding="10")
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
            frame_config,
            textvariable=self.metodo,
            values=("Gauss", "Gauss-Jordan"),
            state="readonly",
            width=14
        )
        self.selector_metodo.grid(row=0, column=6, padx=5, pady=5)
        
        # Botones de ejemplos
        frame_ejemplos = ttk.Frame(frame_config)
        frame_ejemplos.grid(row=1, column=0, columnspan=5, pady=10)
        
        ttk.Label(frame_ejemplos, text="Cargar Ejemplo:", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Solución Única", command=lambda: self.controlador.cargar_ejemplo("unica")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Infinitas Soluciones", command=lambda: self.controlador.cargar_ejemplo("infinitas")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ejemplos, text="Sin Solución", command=lambda: self.controlador.cargar_ejemplo("inconsistente")).pack(side=tk.LEFT, padx=5)

        frame_conversion = ttk.Frame(frame_config)
        frame_conversion.grid(row=2, column=0, columnspan=7, pady=(5, 0))
        ttk.Label(frame_conversion, text="Base de entrada:").pack(side=tk.LEFT, padx=5)
        self.base_entrada = tk.StringVar(value="Decimal")
        self.selector_base = ttk.Combobox(
            frame_conversion,
            textvariable=self.base_entrada,
            values=("Decimal", "Binario", "Octal", "Hexadecimal"),
            state="readonly",
            width=12
        )
        self.selector_base.pack(side=tk.LEFT, padx=5)
        self.entrada_conversion = ttk.Entry(frame_conversion, width=14, justify="center")
        self.entrada_conversion.pack(side=tk.LEFT, padx=5)
        ttk.Button(
            frame_conversion,
            text="Convertir",
            command=self.controlador.convertir_numero
        ).pack(side=tk.LEFT, padx=5)

    def _crear_panel_matriz(self):
        self.frame_matriz_outer = ttk.LabelFrame(self.main_container, text="Ingreso de Coeficientes", padding="10")
        self.frame_matriz_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Usar el ScrollableFrame para la matriz en caso de que sea grande
        self.scroll_matriz = ScrollableFrame(self.frame_matriz_outer)
        self.scroll_matriz.pack(fill=tk.BOTH, expand=True)
        
        self.matriz_entries = []
        self.vector_entries = []
        
        self.btn_resolver = ttk.Button(self.frame_matriz_outer, text="Resolver Sistema", state=tk.DISABLED, command=self.controlador.resolver_sistema)
        self.btn_resolver.pack(pady=10)

    def _crear_panel_resultados(self):
        frame_resultados = ttk.Notebook(self.main_container)
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        self.frame_resultados = frame_resultados
        
        # Pestaña de Resumen y Clasificación
        self.tab_resumen = ttk.Frame(frame_resultados, padding="10")
        frame_resultados.add(self.tab_resumen, text="Resumen de Solución")
        
        self.lbl_clasificacion = ttk.Label(self.tab_resumen, text="Clasificación: -", font=("Segoe UI", 12, "bold"), foreground="#d9534f")
        self.lbl_clasificacion.pack(anchor="w", pady=10)
        
        self.txt_solucion = tk.Text(self.tab_resumen, height=8, state=tk.DISABLED, bg="#ffffff", font=("Consolas", 11), relief=tk.FLAT, borderwidth=1)
        self.txt_solucion.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.lbl_verificacion = ttk.Label(self.tab_resumen, text="Verificación: -", font=("Segoe UI", 11, "bold"))
        self.lbl_verificacion.pack(anchor="w", pady=5)
        
        self.txt_verificacion = tk.Text(self.tab_resumen, height=8, state=tk.DISABLED, bg="#ffffff", font=("Consolas", 11), relief=tk.FLAT, borderwidth=1)
        self.txt_verificacion.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tab_conversiones = ttk.Frame(frame_resultados, padding="10")
        frame_resultados.add(self.tab_conversiones, text="Conversiones")
        self.txt_conversiones = tk.Text(
            self.tab_conversiones,
            height=8,
            state=tk.DISABLED,
            bg="#ffffff",
            font=("Consolas", 11),
            relief=tk.FLAT,
            borderwidth=1
        )
        self.txt_conversiones.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña del Historial Paso a Paso
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
        # Limpiar entradas anteriores
        for widget in self.scroll_matriz.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.matriz_entries = []
        self.vector_entries = []
        
        # Títulos
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
            
            # Vector b
            entry_b = ttk.Entry(self.scroll_matriz.scrollable_frame, width=8, font=("Consolas", 11, "bold"), justify="center")
            entry_b.grid(row=i+1, column=n, padx=(15, 0), pady=5)
            entry_b.insert(0, "0")
            self.vector_entries.append(entry_b)
            
        self.btn_resolver.config(state=tk.NORMAL)
        
    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)
        
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

    def actualizar_conversiones(self, conversiones_texto):
        self.txt_conversiones.config(state=tk.NORMAL)
        self.txt_conversiones.delete(1.0, tk.END)
        self.txt_conversiones.insert(tk.END, conversiones_texto)
        self.txt_conversiones.config(state=tk.DISABLED)
        self.frame_resultados.select(self.tab_conversiones)
        
    def actualizar_historial(self, historial_texto):
        self.txt_historial.config(state=tk.NORMAL)
        self.txt_historial.delete(1.0, tk.END)
        self.txt_historial.insert(tk.END, historial_texto)
        self.txt_historial.config(state=tk.DISABLED)
