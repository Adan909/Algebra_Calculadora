import tkinter as tk
from tkinter import ttk
from vista.componentes import ScrollableFrame

class VentanaOperaciones(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.title("Operaciones Vectoriales y Matriciales")
        self.geometry("850x650")
        self.controlador = controlador
        self.configure(bg="#f4f4f9")
        
        # Notebook principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self._crear_pestana_vectores()
        self._crear_pestana_matrices()

    def _crear_pestana_vectores(self):
        tab_vectores = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_vectores, text="Vectores (Rn)")
        
        # Panel de configuración
        frame_config = ttk.LabelFrame(tab_vectores, text="Configuración de Vectores", padding="10")
        frame_config.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame_config, text="Dimensión (n):").pack(side=tk.LEFT, padx=5)
        self.spin_dimension_vector = ttk.Spinbox(frame_config, from_=1, to=10, width=5)
        self.spin_dimension_vector.set(3)
        self.spin_dimension_vector.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_config, text="Cantidad de Vectores (k):").pack(side=tk.LEFT, padx=5)
        self.spin_cantidad_vectores = ttk.Spinbox(frame_config, from_=1, to=10, width=5)
        self.spin_cantidad_vectores.set(2)
        self.spin_cantidad_vectores.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_config, text="Generar Entradas", command=self.controlador.generar_vectores).pack(side=tk.LEFT, padx=20)
        
        ttk.Label(frame_config, text="Escalar para Mult.:").pack(side=tk.LEFT, padx=5)
        self.entrada_escalar_vector = ttk.Entry(frame_config, width=5)
        self.entrada_escalar_vector.insert(0, "1")
        self.entrada_escalar_vector.pack(side=tk.LEFT, padx=5)
        
        # Área dinámica
        self.scroll_vectores = ScrollableFrame(tab_vectores)
        self.scroll_vectores.pack(fill=tk.BOTH, expand=True, pady=10)
        self.vector_entries = []
        self.vector_b_entries = []
        
        # Botón y resultados
        ttk.Button(tab_vectores, text="Calcular Operaciones y Combinación Lineal", command=self.controlador.operar_vectores).pack(pady=5)
        self.txt_resultados_vectores = tk.Text(tab_vectores, height=12, state=tk.DISABLED, font=("Consolas", 11))
        self.txt_resultados_vectores.pack(fill=tk.X, pady=5)

    def _crear_pestana_matrices(self):
        tab_matrices = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_matrices, text="Operaciones Matriciales")
        
        frame_config = ttk.LabelFrame(tab_matrices, text="Dimensiones", padding="10")
        frame_config.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame_config, text="Matriz A -> Filas:").pack(side=tk.LEFT, padx=2)
        self.spin_filas_a = ttk.Spinbox(frame_config, from_=1, to=10, width=4)
        self.spin_filas_a.set(2)
        self.spin_filas_a.pack(side=tk.LEFT, padx=2)
        ttk.Label(frame_config, text="Cols:").pack(side=tk.LEFT, padx=2)
        self.spin_columnas_a = ttk.Spinbox(frame_config, from_=1, to=10, width=4)
        self.spin_columnas_a.set(2)
        self.spin_columnas_a.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(frame_config, text="Matriz B -> Filas:").pack(side=tk.LEFT, padx=2)
        self.spin_filas_b = ttk.Spinbox(frame_config, from_=1, to=10, width=4)
        self.spin_filas_b.set(2)
        self.spin_filas_b.pack(side=tk.LEFT, padx=2)
        ttk.Label(frame_config, text="Cols:").pack(side=tk.LEFT, padx=2)
        self.spin_columnas_b = ttk.Spinbox(frame_config, from_=1, to=10, width=4)
        self.spin_columnas_b.set(2)
        self.spin_columnas_b.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(frame_config, text="Generar Matrices", command=self.controlador.generar_matrices).pack(side=tk.LEFT, padx=10)
        
        # Área dinámica
        self.scroll_matrices = ScrollableFrame(tab_matrices)
        self.scroll_matrices.pack(fill=tk.BOTH, expand=True, pady=10)
        self.matriz_entries_a = []
        self.matriz_entries_b = []
        
        # Controles de operación
        frame_controles = ttk.Frame(tab_matrices)
        frame_controles.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_controles, text="A + B", command=lambda: self.controlador.operar_matrices("suma")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="A - B", command=lambda: self.controlador.operar_matrices("resta")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="A × B", command=lambda: self.controlador.operar_matrices("multiplicacion")).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_controles, text="Escalar (c):").pack(side=tk.LEFT, padx=(20, 5))
        self.entrada_escalar = ttk.Entry(frame_controles, width=5)
        self.entrada_escalar.insert(0, "2")
        self.entrada_escalar.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="c × A", command=lambda: self.controlador.operar_matrices("escalar")).pack(side=tk.LEFT, padx=5)
        
        self.txt_resultados_matrices = tk.Text(tab_matrices, height=12, state=tk.DISABLED, font=("Consolas", 11))
        self.txt_resultados_matrices.pack(fill=tk.X, pady=5)

    def construir_vectores(self, n, k):
        for widget in self.scroll_vectores.scrollable_frame.winfo_children():
            widget.destroy()
        self.vector_entries = []
        self.vector_b_entries = []
        
        for i in range(k):
            ttk.Label(self.scroll_vectores.scrollable_frame, text=f"v{i+1}:").grid(row=i, column=0, padx=5, pady=5)
            fila_entries = []
            for j in range(n):
                entry = ttk.Entry(self.scroll_vectores.scrollable_frame, width=6, justify="center")
                entry.grid(row=i, column=j+1, padx=2, pady=5)
                entry.insert(0, "0")
                fila_entries.append(entry)
            self.vector_entries.append(fila_entries)
            
        ttk.Label(self.scroll_vectores.scrollable_frame, text="b:", font=("Segoe UI", 10, "bold")).grid(row=k, column=0, padx=5, pady=15)
        for j in range(n):
            entry_b = ttk.Entry(self.scroll_vectores.scrollable_frame, width=6, justify="center")
            entry_b.grid(row=k, column=j+1, padx=2, pady=15)
            entry_b.insert(0, "0")
            self.vector_b_entries.append(entry_b)

    def mostrar_resultado_vectores(self, texto):
        self.txt_resultados_vectores.config(state=tk.NORMAL)
        self.txt_resultados_vectores.delete(1.0, tk.END)
        self.txt_resultados_vectores.insert(tk.END, texto)
        self.txt_resultados_vectores.config(state=tk.DISABLED)

    def construir_matrices(self, m_a, n_a, m_b, n_b):
        for widget in self.scroll_matrices.scrollable_frame.winfo_children():
            widget.destroy()
        self.matriz_entries_a = []
        self.matriz_entries_b = []
        
        ttk.Label(self.scroll_matrices.scrollable_frame, text="Matriz A", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=n_a, pady=5)
        for i in range(m_a):
            fila = []
            for j in range(n_a):
                entry = ttk.Entry(self.scroll_matrices.scrollable_frame, width=6, justify="center")
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.matriz_entries_a.append(fila)
            
        offset_col = n_a + 2
        ttk.Label(self.scroll_matrices.scrollable_frame, text="Matriz B", font=("Segoe UI", 10, "bold")).grid(row=0, column=offset_col, columnspan=n_b, pady=5)
        for i in range(m_b):
            fila = []
            for j in range(n_b):
                entry = ttk.Entry(self.scroll_matrices.scrollable_frame, width=6, justify="center")
                entry.grid(row=i+1, column=j+offset_col, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.matriz_entries_b.append(fila)

    def mostrar_resultado_matrices(self, texto):
        self.txt_resultados_matrices.config(state=tk.NORMAL)
        self.txt_resultados_matrices.delete(1.0, tk.END)
        self.txt_resultados_matrices.insert(tk.END, texto)
        self.txt_resultados_matrices.config(state=tk.DISABLED)