"""
Ventana Principal de 'Algebra Computation Engine'.
Implementa una interfaz moderna en Tema Claro (Light Mode), ergonómica, accesible
y con un flujo de trabajo optimizado para herramientas científicas y educativas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from fractions import Fraction

import vista.tema as tema
from vista.tema import (
    BG_WINDOW, BG_CARD, BG_SECONDARY, BG_HOVER, BG_ACTIVE,
    BORDER_SUBTLE, BORDER_FOCUS, BORDER_ERROR,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ON_ACCENT, TEXT_ON_SEC,
    ACCENT_PRIMARY, ACCENT_HOVER, ACCENT_ACTIVE, ACCENT_SOFT, ACCENT_BORDER,
    SUCCESS_BG, SUCCESS_TEXT, SUCCESS_BORDER,
    WARNING_BG, WARNING_TEXT, WARNING_BORDER,
    ERROR_BG, ERROR_TEXT, ERROR_BORDER,
    INFO_BG, INFO_TEXT, INFO_BORDER,
    PAD_XS, PAD_SM, PAD_MD, PAD_LG, PAD_XL,
    FONT_TITLE_LG, FONT_TITLE, FONT_HEADING, FONT_SUBHEAD,
    FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_SMALL_BOLD, FONT_MICRO,
    FONT_MONO, FONT_MONO_BOLD, FONT_MONO_SM, FONT_MONO_LG, FONT_MATRIX
)
from vista.componentes import (
    BotonPrimario, BotonSecundario, BotonFantasma,
    Tarjeta, SpinboxNumerico, ControlSegmentado, ChipSistema,
    BadgeEstado, Tooltip, EstadoVacio, CeldaMatriz, ScrollableFrame,
    InterruptorTema
)


class VentanaPrincipal:
    """
    Consola interactiva de Álgebra Lineal y Métodos Numéricos.
    Diseñada en Tema Claro con patrón MVC y componentes ergonómicos.
    """
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self._op_count = 0
        self._root_fullscreen = False

        self.root.title("Algebra Computation Engine")
        self.root.geometry("1280x880")
        self.root.minsize(1040, 720)
        self.root.configure(bg=BG_WINDOW)

        # Configuración del contenedor con scroll global
        self._scroll_canvas = tk.Canvas(
            self.root, bg=BG_WINDOW, highlightthickness=0, borderwidth=0
        )
        self._scrollbar_vertical = ttk.Scrollbar(
            self.root, orient="vertical", command=self._scroll_canvas.yview
        )
        self._scroll_canvas.configure(yscrollcommand=self._scrollbar_vertical.set)
        
        self._scroll_canvas.grid(row=0, column=0, sticky="nsew")
        self._scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self._contenido_scroll = tk.Frame(self._scroll_canvas, bg=BG_WINDOW)
        self._ventana_scroll = self._scroll_canvas.create_window(
            (0, 0), window=self._contenido_scroll, anchor="nw"
        )
        
        self._contenido_scroll.bind("<Configure>", self._actualizar_region_scroll)
        self._scroll_canvas.bind("<Configure>", self._ajustar_contenido_scroll)
        self.root.bind("<F11>", self._toggle_root_fullscreen)

        # Historial de estados de matriz para función deshacer
        self._historial_matrices = []

        # Inicialización de estilos y capas visuales
        self._configurar_estilos_ttk()
        self._construir_header()
        self._construir_footer()
        self._construir_cuerpo()
        self._iniciar_reloj()

    def _actualizar_region_scroll(self, _event=None):
        self._scroll_canvas.configure(scrollregion=self._scroll_canvas.bbox("all"))

    def _ajustar_contenido_scroll(self, event):
        alto = max(event.height, self._contenido_scroll.winfo_reqheight())
        self._scroll_canvas.itemconfigure(
            self._ventana_scroll, width=event.width, height=alto
        )

    # ==========================================================================
    # ESTILOS GLOBALES TTK (TEMA CLAM PERSONALIZADO)
    # ==========================================================================
    def _configurar_estilos_ttk(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure(".", background=BG_CARD, foreground=TEXT_PRIMARY, font=FONT_BODY)
        s.configure("TFrame", background=BG_CARD)

        # Botón primario TTK
        s.configure("P.TButton",
            background=ACCENT_PRIMARY, foreground=TEXT_ON_ACCENT,
            bordercolor=BORDER_SUBTLE, borderwidth=1,
            relief="flat", font=FONT_SUBHEAD, padding=(14, 7))
        s.map("P.TButton",
            background=[("active", ACCENT_HOVER), ("disabled", BG_SECONDARY)],
            foreground=[("active", TEXT_ON_ACCENT), ("disabled", TEXT_MUTED)])

        # Botón secundario TTK
        s.configure("S.TButton",
            background=BG_CARD, foreground=TEXT_PRIMARY,
            bordercolor=BORDER_SUBTLE, borderwidth=1,
            relief="flat", font=FONT_BODY, padding=(10, 5))
        s.map("S.TButton",
            background=[("active", BG_HOVER)],
            foreground=[("active", TEXT_PRIMARY)],
            bordercolor=[("active", ACCENT_PRIMARY)])

        # Notebooks internos
        s.configure("Sub.TNotebook", background=BG_CARD, borderwidth=0, tabmargins=[0, 0, 0, 0])
        s.configure("Sub.TNotebook.Tab",
            background=BG_SECONDARY, foreground=TEXT_SECONDARY,
            padding=[16, 7], font=FONT_SMALL_BOLD, borderwidth=0)
        s.map("Sub.TNotebook.Tab",
            background=[("selected", BG_CARD), ("active", BG_HOVER)],
            foreground=[("selected", ACCENT_PRIMARY), ("active", TEXT_PRIMARY)])

        # Combobox
        s.configure("TCombobox",
            fieldbackground=BG_CARD, background=BG_SECONDARY,
            foreground=TEXT_PRIMARY, arrowcolor=ACCENT_PRIMARY,
            bordercolor=BORDER_SUBTLE, insertcolor=ACCENT_PRIMARY, padding=(6, 5))
        s.map("TCombobox",
            fieldbackground=[("readonly", BG_CARD)],
            foreground=[("readonly", TEXT_PRIMARY)],
            bordercolor=[("focus", ACCENT_PRIMARY)])

        # Spinbox
        s.configure("TSpinbox",
            fieldbackground=BG_CARD, background=BG_SECONDARY,
            foreground=TEXT_PRIMARY, arrowcolor=ACCENT_PRIMARY,
            bordercolor=BORDER_SUBTLE, insertcolor=ACCENT_PRIMARY, padding=(6, 4))
        s.map("TSpinbox", bordercolor=[("focus", ACCENT_PRIMARY)])

        # Scrollbars
        s.configure("TScrollbar",
            background=BG_SECONDARY, troughcolor=BG_WINDOW,
            bordercolor=BORDER_SUBTLE, arrowcolor=TEXT_MUTED,
            relief="flat", gripcount=0)
        s.map("TScrollbar", background=[("active", ACCENT_SOFT)])

        # Treeview (para Bisección)
        s.configure("Treeview",
            background=BG_CARD, fieldbackground=BG_CARD, foreground=TEXT_PRIMARY,
            bordercolor=BORDER_SUBTLE, rowheight=26, font=FONT_MONO_SM)
        s.configure("Treeview.Heading",
            background=BG_SECONDARY, foreground=TEXT_PRIMARY,
            bordercolor=BORDER_SUBTLE, font=FONT_SMALL_BOLD, padding=(6, 5))
        s.map("Treeview",
            background=[("selected", ACCENT_SOFT)],
            foreground=[("selected", ACCENT_PRIMARY)])

    # ==========================================================================
    # ENCABEZADO (HEADER COMPACTO EN TEMA CLARO)
    # ==========================================================================
    def _construir_header(self):
        header_bar = tk.Frame(self._contenido_scroll, bg=BG_CARD, height=54)
        header_bar.pack(fill=tk.X, side=tk.TOP)
        header_bar.pack_propagate(False)

        # Lado izquierdo: Identidad de la aplicación
        left_box = tk.Frame(header_bar, bg=BG_CARD)
        left_box.pack(side=tk.LEFT, fill=tk.Y, padx=(18, 10))

        lbl_logo = tk.Label(
            left_box, text="⚡ ALGEBRA ENGINE",
            font=FONT_TITLE, bg=BG_CARD, fg=TEXT_PRIMARY
        )
        lbl_logo.pack(side=tk.LEFT, pady=12)
        Tooltip(lbl_logo, "Motor de Álgebra Lineal & Métodos Numéricos\nPrecisión Racional Exacta con fracciones continuas")

        # Centro: Control segmentado de navegación entre módulos
        center_box = tk.Frame(header_bar, bg=BG_CARD)
        center_box.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.modulos = [
            "Gauss-Jordan",
            "Vectorial & Matrices",
            "Conversión de Bases",
            "Números Romanos",
            "Método de Bisección"
        ]
        self.nav_segmentada = ControlSegmentado(
            center_box, self.modulos, comando=self._al_cambiar_modulo, initial_index=0
        )
        self.nav_segmentada.pack(side=tk.LEFT, pady=10)

        # Lado derecho: Reloj discreto, interruptor de modo oscuro y estado
        right_box = tk.Frame(header_bar, bg=BG_CARD)
        right_box.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 18))

        self.sw_tema = InterruptorTema(
            right_box, es_oscuro=tema.es_oscuro(), comando=self.alternar_tema
        )
        self.sw_tema.pack(side=tk.RIGHT, pady=10, padx=(12, 0))

        self.lbl_clock = tk.Label(
            right_box, text="--:--:--",
            font=FONT_MONO_BOLD, bg=BG_CARD, fg=TEXT_SECONDARY
        )
        self.lbl_clock.pack(side=tk.RIGHT, pady=16)
        Tooltip(self.lbl_clock, "Hora local del sistema")

        # Borde inferior fino de separación
        tk.Frame(self._contenido_scroll, bg=BORDER_SUBTLE, height=1).pack(fill=tk.X, side=tk.TOP)

    def _al_cambiar_modulo(self, index, nombre):
        if hasattr(self, "nb_main"):
            self.nb_main.select(index)

    # ==========================================================================
    # GESTIÓN Y CONMUTACIÓN DINÁMICA DE TEMA (CLARO / OSCURO)
    # ==========================================================================
    def alternar_tema(self):
        """
        Alterna el tema visual de la aplicación entre Claro y Oscuro, preservando
        íntegramente el estado de todas las entradas, resultados y navegación activa.
        """
        estado = self._guardar_estado()
        nuevo_tema = tema.alternar_tema()

        # Sincronizar variables de módulo en ventana_principal
        import sys
        mod = sys.modules[__name__]
        for k, v in tema.PALETAS[nuevo_tema].items():
            setattr(mod, k, v)

        self._reconstruir_ui()
        self._restaurar_estado(estado)

    def _reconstruir_ui(self):
        """
        Reconfigura el lienzo global y reconstruye los componentes visuales con la paleta activa.
        """
        self.root.configure(bg=BG_WINDOW)
        self._scroll_canvas.configure(bg=BG_WINDOW)
        self._contenido_scroll.configure(bg=BG_WINDOW)

        for child in self._contenido_scroll.winfo_children():
            child.destroy()

        self._configurar_estilos_ttk()
        self._construir_header()
        self._construir_footer()
        self._construir_cuerpo()

    def _guardar_estado(self):
        """
        Captura el estado completo de los módulos para su restauración fiel tras el cambio de tema.
        """
        estado = {}
        try:
            estado["tab_idx"] = self.nav_segmentada.seleccionado if hasattr(self, "nav_segmentada") else 0
            estado["op_count"] = self._op_count

            # Gauss
            estado["gauss_m"] = self.spin_m.get_int() if hasattr(self, "spin_m") else 3
            estado["gauss_n"] = self.spin_n.get_int() if hasattr(self, "spin_n") else 3
            estado["gauss_metodo"] = self.metodo.get() if hasattr(self, "metodo") else "Gauss"
            estado["gauss_mat"] = [[e.get() for e in fila] for fila in getattr(self, "matriz_entries", [])]
            estado["gauss_vec"] = [e.get() for e in getattr(self, "vector_entries", [])]
            estado["gauss_sol"] = self.txt_solucion.get("1.0", tk.END).strip() if hasattr(self, "txt_solucion") else ""
            estado["gauss_hist"] = self.txt_historial.get("1.0", tk.END).strip() if hasattr(self, "txt_historial") else ""
            estado["gauss_badge_texto"] = self.badge_clasificacion.lbl_text.cget("text") if hasattr(self, "badge_clasificacion") else ""
            estado["gauss_badge_tipo"] = getattr(self.badge_clasificacion, "_tipo", "info") if hasattr(self, "badge_clasificacion") else "info"
            estado["gauss_tab_res"] = self.nb_gauss_res.index("current") if hasattr(self, "nb_gauss_res") else 0

            # Vectorial & Matrices
            estado["vec_dim"] = self.spin_dim_v.get_int() if hasattr(self, "spin_dim_v") else 3
            estado["vec_cant"] = self.spin_cant_v.get_int() if hasattr(self, "spin_cant_v") else 2
            estado["vec_entries"] = [[e.get() for e in fila] for fila in getattr(self, "vec_entries", [])]
            estado["vec_b_entries"] = [e.get() for e in getattr(self, "vec_b_entries", [])]
            estado["mat_fa"] = self.spin_filas_a.get_int() if hasattr(self, "spin_filas_a") else 2
            estado["mat_ca"] = self.spin_cols_a.get_int() if hasattr(self, "spin_cols_a") else 2
            estado["mat_fb"] = self.spin_filas_b.get_int() if hasattr(self, "spin_filas_b") else 2
            estado["mat_cb"] = self.spin_cols_b.get_int() if hasattr(self, "spin_cols_b") else 2
            estado["mat_a_entries"] = [[e.get() for e in fila] for fila in getattr(self, "mat_a_entries", [])]
            estado["mat_b_entries"] = [[e.get() for e in fila] for fila in getattr(self, "mat_b_entries", [])]
            estado["mat_escalar"] = self.escalar_entry.get() if hasattr(self, "escalar_entry") else "1"
            estado["vec_res"] = self.txt_resultado_vec.get("1.0", tk.END).strip() if hasattr(self, "txt_resultado_vec") else ""
            estado["mat_res"] = self.txt_resultado_mat.get("1.0", tk.END).strip() if hasattr(self, "txt_resultado_mat") else ""
            estado["tab_vectorial_idx"] = self.nb_vectorial.index("current") if hasattr(self, "nb_vectorial") else 0

            # Conversiones
            estado["conv_num"] = self.conv_numero.get() if hasattr(self, "conv_numero") else ""
            estado["conv_orig"] = self.conv_base_origen.get() if hasattr(self, "conv_base_origen") else "10"
            estado["conv_dest"] = self.conv_base_destino.get() if hasattr(self, "conv_base_destino") else "2"
            estado["conv_res"] = self.txt_resultado_conv.get("1.0", tk.END).strip() if hasattr(self, "txt_resultado_conv") else ""

            # Romanos
            estado["rom_modo"] = self.romanos_modo.get() if hasattr(self, "romanos_modo") else "directa"
            estado["rom_entrada"] = self.romanos_entrada.get() if hasattr(self, "romanos_entrada") else ""
            estado["rom_op"] = self.romanos_op_combo.get() if hasattr(self, "romanos_op_combo") else "suma"
            estado["rom_cant"] = self.spin_cant_rom.get_int() if hasattr(self, "spin_cant_rom") else 2
            estado["rom_lista"] = [e.get() for e in getattr(self, "romanos_lista_entries", [])]
            estado["rom_res"] = self.txt_resultado_romanos.get("1.0", tk.END).strip() if hasattr(self, "txt_resultado_romanos") else ""

            # Bisección
            estado["bis_func"] = self.biseccion_funcion.get() if hasattr(self, "biseccion_funcion") else ""
            estado["bis_a"] = self.biseccion_a.get() if hasattr(self, "biseccion_a") else ""
            estado["bis_b"] = self.biseccion_b.get() if hasattr(self, "biseccion_b") else ""
            estado["bis_err"] = self.biseccion_error.get() if hasattr(self, "biseccion_error") else ""
            estado["bis_max"] = self.biseccion_max_iter.get() if hasattr(self, "biseccion_max_iter") else ""
            estado["bis_res"] = getattr(self, "_resultado_biseccion", None)
            estado["bis_func_obj"] = getattr(self, "_funcion_grafica_biseccion", None)
        except Exception:
            pass
        return estado

    def _restaurar_estado(self, estado):
        """
        Restaura fielmente los valores, cuadrículas y resultados guardados.
        """
        if not estado:
            return
        try:
            self._op_count = estado.get("op_count", 0)
            if hasattr(self, "lbl_op_count"):
                self.lbl_op_count.config(text=f"OPS: {self._op_count}")

            # Restaurar Gauss
            m = estado.get("gauss_m", 3)
            n = estado.get("gauss_n", 3)
            self.spin_m.set(m)
            self.spin_n.set(n)
            self.metodo.set(estado.get("gauss_metodo", "Gauss"))
            self.construir_cuadricula(m, n)
            mat_vals = estado.get("gauss_mat", [])
            for i, fila in enumerate(self.matriz_entries):
                for j, entry in enumerate(fila):
                    if i < len(mat_vals) and j < len(mat_vals[i]):
                        entry.delete(0, tk.END)
                        entry.insert(0, mat_vals[i][j])
            vec_vals = estado.get("gauss_vec", [])
            for i, entry in enumerate(self.vector_entries):
                if i < len(vec_vals):
                    entry.delete(0, tk.END)
                    entry.insert(0, vec_vals[i])

            sol_txt = estado.get("gauss_sol", "")
            hist_txt = estado.get("gauss_hist", "")
            badge_txt = estado.get("gauss_badge_texto", "")
            badge_tipo = estado.get("gauss_badge_tipo", "info")
            if sol_txt or hist_txt:
                self.actualizar_resumen(badge_txt or "SISTEMA PROCESADO", sol_txt, "")
                if hist_txt:
                    self.actualizar_historial(hist_txt)
                if badge_txt and hasattr(self, "badge_clasificacion"):
                    self.badge_clasificacion.actualizar(badge_txt, badge_tipo)

            if hasattr(self, "nb_gauss_res"):
                self.nb_gauss_res.select(estado.get("gauss_tab_res", 0))

            # Restaurar Vectorial & Matrices
            v_dim = estado.get("vec_dim", 3)
            v_cant = estado.get("vec_cant", 2)
            self.spin_dim_v.set(v_dim)
            self.spin_cant_v.set(v_cant)
            self.construir_vectores(v_dim, v_cant)
            for i, fila in enumerate(self.vec_entries):
                for j, entry in enumerate(fila):
                    if i < len(estado.get("vec_entries", [])) and j < len(estado["vec_entries"][i]):
                        entry.delete(0, tk.END)
                        entry.insert(0, estado["vec_entries"][i][j])
            for i, entry in enumerate(self.vec_b_entries):
                if i < len(estado.get("vec_b_entries", [])):
                    entry.delete(0, tk.END)
                    entry.insert(0, estado["vec_b_entries"][i])

            fa = estado.get("mat_fa", 2)
            ca = estado.get("mat_ca", 2)
            fb = estado.get("mat_fb", 2)
            cb = estado.get("mat_cb", 2)
            self.spin_filas_a.set(fa)
            self.spin_cols_a.set(ca)
            self.spin_filas_b.set(fb)
            self.spin_cols_b.set(cb)
            self.construir_matrices_ops(fa, ca, fb, cb)
            for i, fila in enumerate(self.mat_a_entries):
                for j, entry in enumerate(fila):
                    if i < len(estado.get("mat_a_entries", [])) and j < len(estado["mat_a_entries"][i]):
                        entry.delete(0, tk.END)
                        entry.insert(0, estado["mat_a_entries"][i][j])
            for i, fila in enumerate(self.mat_b_entries):
                for j, entry in enumerate(fila):
                    if i < len(estado.get("mat_b_entries", [])) and j < len(estado["mat_b_entries"][i]):
                        entry.delete(0, tk.END)
                        entry.insert(0, estado["mat_b_entries"][i][j])
            self.escalar_entry.delete(0, tk.END)
            self.escalar_entry.insert(0, estado.get("mat_escalar", "1"))

            if estado.get("vec_res"):
                self.mostrar_resultado_vectorial(estado["vec_res"])
            if estado.get("mat_res"):
                self.mostrar_resultado_matricial(estado["mat_res"])
            if hasattr(self, "nb_vectorial"):
                self.nb_vectorial.select(estado.get("tab_vectorial_idx", 0))

            # Restaurar Conversiones
            self.conv_numero.delete(0, tk.END)
            self.conv_numero.insert(0, estado.get("conv_num", ""))
            self.conv_base_origen.set(estado.get("conv_orig", "10"))
            self.conv_base_destino.set(estado.get("conv_dest", "2"))
            if estado.get("conv_res"):
                self.mostrar_resultado_conversion(estado["conv_res"])

            # Restaurar Romanos
            self.romanos_modo.set(estado.get("rom_modo", "directa"))
            self._alternar_modo_romanos()
            self.romanos_entrada.delete(0, tk.END)
            self.romanos_entrada.insert(0, estado.get("rom_entrada", ""))
            self.romanos_op_combo.set(estado.get("rom_op", "suma"))
            self.spin_cant_rom.set(estado.get("rom_cant", 2))
            self.construir_campos_romanos_operacion(estado.get("rom_cant", 2))
            for i, entry in enumerate(self.romanos_lista_entries):
                if i < len(estado.get("rom_lista", [])):
                    entry.delete(0, tk.END)
                    entry.insert(0, estado["rom_lista"][i])
            if estado.get("rom_res"):
                self.mostrar_resultado_romanos(estado["rom_res"])

            # Restaurar Bisección
            self.biseccion_funcion.delete(0, tk.END)
            self.biseccion_funcion.insert(0, estado.get("bis_func", ""))
            self.biseccion_a.delete(0, tk.END)
            self.biseccion_a.insert(0, estado.get("bis_a", ""))
            self.biseccion_b.delete(0, tk.END)
            self.biseccion_b.insert(0, estado.get("bis_b", ""))
            self.biseccion_error.delete(0, tk.END)
            self.biseccion_error.insert(0, estado.get("bis_err", ""))
            self.biseccion_max_iter.delete(0, tk.END)
            self.biseccion_max_iter.insert(0, estado.get("bis_max", ""))
            if estado.get("bis_res") and estado.get("bis_func_obj"):
                self.mostrar_resultado_biseccion(estado["bis_res"], estado["bis_func_obj"])

            # Seleccionar pestaña principal
            tab_idx = estado.get("tab_idx", 0)
            if hasattr(self, "nav_segmentada"):
                self.nav_segmentada.seleccionar(tab_idx)
            if hasattr(self, "nb_main"):
                self.nb_main.select(tab_idx)
        except Exception:
            pass

    # ==========================================================================
    # PIE DE PÁGINA (FOOTER MÍNIMO)
    # ==========================================================================
    def _construir_footer(self):
        tk.Frame(self._contenido_scroll, bg=BORDER_SUBTLE, height=1).pack(fill=tk.X, side=tk.BOTTOM)

        foot = tk.Frame(self._contenido_scroll, bg=BG_CARD, height=28)
        foot.pack(fill=tk.X, side=tk.BOTTOM)
        foot.pack_propagate(False)

        # Indicador de estado activo
        tk.Frame(foot, bg=SUCCESS_TEXT, width=8, height=8).pack(side=tk.LEFT, padx=(16, 6), pady=10)
        tk.Label(
            foot, text="Motor Activo",
            font=FONT_MICRO, bg=BG_CARD, fg=TEXT_SECONDARY
        ).pack(side=tk.LEFT, pady=6)

        self.lbl_op_count = tk.Label(
            foot, text="OPS: 0",
            font=FONT_MONO_SM, bg=BG_CARD, fg=TEXT_MUTED
        )
        self.lbl_op_count.pack(side=tk.RIGHT, padx=16)

    # ==========================================================================
    # CUERPO PRINCIPAL (NOTEBOOK MULTIMÓDULO)
    # ==========================================================================
    def _construir_cuerpo(self):
        container = tk.Frame(self._contenido_scroll, bg=BG_WINDOW)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # Ocultamos la barra nativa de pestañas de ttk para usar nuestro ControlSegmentado
        s = ttk.Style()
        s.layout("Hidden.TNotebook.Tab", [])
        self.nb_main = ttk.Notebook(container, style="Hidden.TNotebook")
        self.nb_main.pack(fill=tk.BOTH, expand=True)

        self.tab_gauss     = tk.Frame(self.nb_main, bg=BG_WINDOW)
        self.tab_vectorial = tk.Frame(self.nb_main, bg=BG_WINDOW)
        self.tab_conv      = tk.Frame(self.nb_main, bg=BG_WINDOW)
        self.tab_romanos   = tk.Frame(self.nb_main, bg=BG_WINDOW)
        self.tab_biseccion = tk.Frame(self.nb_main, bg=BG_WINDOW)

        self.nb_main.add(self.tab_gauss,     text="Gauss-Jordan")
        self.nb_main.add(self.tab_vectorial, text="Vectorial & Matrices")
        self.nb_main.add(self.tab_conv,      text="Conversión de Bases")
        self.nb_main.add(self.tab_romanos,   text="Números Romanos")
        self.nb_main.add(self.tab_biseccion, text="Método de Bisección")

        self._build_gauss()
        self._build_vectorial()
        self._build_conv()
        self._build_romanos()
        self._build_biseccion()

    # ==========================================================================
    # HELPERS Y CONSOLA DE PANTALLA COMPLETA
    # ==========================================================================
    def _crear_consola(self, parent, height=12, wrap=tk.WORD, **kwargs):
        txt = tk.Text(
            parent, height=height, font=FONT_MONO,
            bg=BG_CARD, fg=TEXT_PRIMARY, spacing1=2, spacing3=2,
            insertbackground=ACCENT_PRIMARY,
            selectbackground=ACCENT_SOFT, selectforeground=ACCENT_PRIMARY,
            relief="flat", bd=0, padx=10, pady=8,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, highlightcolor=ACCENT_PRIMARY,
            state=tk.DISABLED, wrap=wrap, **kwargs
        )
        return txt

    def _conectar_consola_fullscreen(self, widget_text, titulo, bar_derecha=None, proveedor_texto=None):
        target = proveedor_texto if proveedor_texto is not None else widget_text

        if bar_derecha is not None:
            btn_fs = BotonFantasma(
                bar_derecha, text="⛶ Pantalla Completa",
                command=lambda: self.abrir_consola_fullscreen(titulo, target)
            )
            btn_fs.pack(side=tk.RIGHT, padx=4)
            Tooltip(btn_fs, "Abrir visor expandido con zoom y portapapeles")

        widget_text.bind(
            "<Double-Button-1>",
            lambda e: self.abrir_consola_fullscreen(titulo, target)
        )

        menu = tk.Menu(widget_text, tearoff=0, bg=BG_CARD, fg=TEXT_PRIMARY,
                       activebackground=BG_SECONDARY, activeforeground=TEXT_PRIMARY,
                       font=FONT_BODY, bd=1, relief="solid")
        menu.add_command(
            label="  ⛶  Pantalla Completa",
            command=lambda: self.abrir_consola_fullscreen(titulo, target)
        )
        menu.add_separator()
        def copiar():
            texto = widget_text.get("1.0", tk.END).strip()
            if texto:
                self.copiar_al_portapapeles(texto)
        menu.add_command(label="  📋  Copiar Todo", command=copiar)

        def popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        widget_text.bind("<Button-3>", popup)

    def abrir_consola_fullscreen(self, titulo, widget_origen):
        ventana_fs = tk.Toplevel(self.root)
        ventana_fs.title(f"Visor de Resultados · {titulo}")
        ventana_fs.configure(bg=BG_WINDOW)

        try:
            ventana_fs.attributes("-fullscreen", True)
            es_fullscreen = [True]
        except Exception:
            es_fullscreen = [False]

        tamano_fuente = [12]

        def actualizar_fuente():
            txt_fs.config(font=(FONT_MONO[0], tamano_fuente[0]))

        def zoom_in(event=None):
            if tamano_fuente[0] < 26:
                tamano_fuente[0] += 1
                actualizar_fuente()

        def zoom_out(event=None):
            if tamano_fuente[0] > 8:
                tamano_fuente[0] -= 1
                actualizar_fuente()

        def toggle_fullscreen(event=None):
            es_fullscreen[0] = not es_fullscreen[0]
            try:
                ventana_fs.attributes("-fullscreen", es_fullscreen[0])
            except Exception:
                pass
            btn_toggle_fs.config(
                text=" 🗗 Restaurar (F11) " if es_fullscreen[0] else " ⛶ Pantalla Completa (F11) "
            )

        def copiar_todo(event=None):
            contenido = txt_fs.get("1.0", tk.END).strip()
            if contenido:
                self.copiar_al_portapapeles(contenido)
                lbl_copiado.config(text="✔ Copiado al portapapeles")
                ventana_fs.after(2000, lambda: lbl_copiado.config(text=""))

        def recargar_contenido(event=None):
            txt_fs.config(state=tk.NORMAL)
            txt_fs.delete("1.0", tk.END)
            if hasattr(widget_origen, "get"):
                texto = widget_origen.get("1.0", tk.END).strip()
            elif callable(widget_origen):
                texto = str(widget_origen()).strip()
            else:
                texto = str(widget_origen).strip()
            if not texto:
                texto = "[ No se ha generado ningún resultado aún ]"
            txt_fs.insert(tk.END, texto)
            txt_fs.config(state=tk.NORMAL)

        # Barra superior del visor
        top_bar = tk.Frame(ventana_fs, bg=BG_CARD, height=48, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        left_box = tk.Frame(top_bar, bg=BG_CARD)
        left_box.pack(side=tk.LEFT, fill=tk.Y, padx=16)

        tk.Label(
            left_box, text=f"⛶ {titulo}",
            font=FONT_HEADING, bg=BG_CARD, fg=TEXT_PRIMARY
        ).pack(side=tk.LEFT, pady=12)

        lbl_copiado = tk.Label(
            left_box, text="", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=SUCCESS_TEXT
        )
        lbl_copiado.pack(side=tk.LEFT, padx=16)

        right_box = tk.Frame(top_bar, bg=BG_CARD)
        right_box.pack(side=tk.RIGHT, fill=tk.Y, padx=12)

        BotonSecundario(right_box, text="A −", command=zoom_out, font=FONT_MONO_BOLD, padx=8, pady=4).pack(side=tk.LEFT, padx=2, pady=8)
        BotonSecundario(right_box, text="A +", command=zoom_in, font=FONT_MONO_BOLD, padx=8, pady=4).pack(side=tk.LEFT, padx=2, pady=8)
        BotonPrimario(right_box, text="📋 Copiar", command=copiar_todo, font=FONT_SMALL_BOLD, padx=10, pady=4).pack(side=tk.LEFT, padx=4, pady=8)

        btn_toggle_fs = BotonSecundario(right_box, text="🗗 Restaurar (F11)", command=toggle_fullscreen, font=FONT_SMALL, padx=8, pady=4)
        btn_toggle_fs.pack(side=tk.LEFT, padx=4, pady=8)

        BotonSecundario(right_box, text="✕ Cerrar (Esc)", command=ventana_fs.destroy, font=FONT_SMALL_BOLD, padx=10, pady=4).pack(side=tk.LEFT, padx=(4, 0), pady=8)

        body_frame = tk.Frame(ventana_fs, bg=BG_WINDOW, padx=16, pady=14)
        body_frame.pack(fill=tk.BOTH, expand=True)

        txt_fs = tk.Text(
            body_frame, font=(FONT_MONO[0], tamano_fuente[0]),
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=ACCENT_PRIMARY,
            selectbackground=ACCENT_SOFT, selectforeground=ACCENT_PRIMARY,
            relief="flat", bd=0, wrap=tk.NONE,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE
        )
        sc_y = ttk.Scrollbar(body_frame, orient="vertical", command=txt_fs.yview)
        sc_x = ttk.Scrollbar(body_frame, orient="horizontal", command=txt_fs.xview)
        txt_fs.configure(yscrollcommand=sc_y.set, xscrollcommand=sc_x.set)

        txt_fs.grid(row=0, column=0, sticky="nsew")
        sc_y.grid(row=0, column=1, sticky="ns")
        sc_x.grid(row=1, column=0, sticky="ew")

        body_frame.grid_rowconfigure(0, weight=1)
        body_frame.grid_columnconfigure(0, weight=1)

        recargar_contenido()

        ventana_fs.bind("<Escape>", lambda e: ventana_fs.destroy())
        ventana_fs.bind("<F11>", toggle_fullscreen)
        ventana_fs.bind("<Control-plus>", zoom_in)
        ventana_fs.bind("<Control-minus>", zoom_out)
        ventana_fs.bind("<Control-equal>", zoom_in)
        ventana_fs.focus_set()

    def copiar_al_portapapeles(self, texto):
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)

    def _write(self, widget, texto):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, texto)
        widget.config(state=tk.DISABLED)

    def _ops(self):
        self._op_count += 1
        self.lbl_op_count.config(text=f"OPS: {self._op_count}")

    def _iniciar_reloj(self):
        try:
            if hasattr(self, "lbl_clock") and self.lbl_clock.winfo_exists():
                self.lbl_clock.config(text=time.strftime("%H:%M:%S"))
        except Exception:
            pass
        self.root.after(1000, self._iniciar_reloj)

    def _toggle_root_fullscreen(self, event=None):
        self._root_fullscreen = not getattr(self, "_root_fullscreen", False)
        try:
            self.root.attributes("-fullscreen", self._root_fullscreen)
        except Exception:
            pass

    # ==========================================================================
    # MÓDULO 1 — GAUSS-JORDAN (REDIEÑO COMPLETO EN TEMA CLARO)
    # ==========================================================================
    def _build_gauss(self):
        parent = self.tab_gauss

        # ── Barra de Indicador de 3 Pasos ─────────────────────────────────────
        pasos_bar = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        pasos_bar.pack(fill=tk.X, pady=(0, 10))

        self.step_labels = []
        pasos_info = [
            ("1", "Configurar Dimensiones", "Define m ecuaciones × n incógnitas"),
            ("2", "Ingresar Matriz [A | b]", "Celdas numéricas con fracciones exactas"),
            ("3", "Resolver & Diagnóstico", "Eliminación, clasificación y verificación")
        ]

        for i, (num, titulo, desc) in enumerate(pasos_info):
            s_frame = tk.Frame(pasos_bar, bg=BG_CARD, padx=12, pady=6)
            s_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

            circulo = tk.Label(
                s_frame, text=num, font=FONT_SMALL_BOLD,
                bg=ACCENT_PRIMARY if i == 0 else BG_SECONDARY,
                fg=TEXT_ON_ACCENT if i == 0 else TEXT_SECONDARY,
                width=2, height=1
            )
            circulo.pack(side=tk.LEFT, padx=(0, 8))

            info_box = tk.Frame(s_frame, bg=BG_CARD)
            info_box.pack(side=tk.LEFT)

            lbl_t = tk.Label(info_box, text=titulo, font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY)
            lbl_t.pack(anchor="w")
            lbl_d = tk.Label(info_box, text=desc, font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED)
            lbl_d.pack(anchor="w")

            self.step_labels.append((circulo, lbl_t))

            if i < 2:
                tk.Label(pasos_bar, text="→", font=FONT_SUBHEAD, bg=BG_CARD, fg=BORDER_SUBTLE).pack(side=tk.LEFT)

        # ── Layout de Dos Columnas (Izquierda: Config + Matriz / Derecha: Resultados) ──
        cols_frame = tk.Frame(parent, bg=BG_WINDOW)
        cols_frame.pack(fill=tk.BOTH, expand=True)

        col_izq = tk.Frame(cols_frame, bg=BG_WINDOW)
        col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        col_der = tk.Frame(cols_frame, bg=BG_WINDOW)
        col_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # ── TARJETA: Parámetros del Sistema ───────────────────────────────────
        tarjeta_cfg = Tarjeta(col_izq, titulo="Parámetros del Sistema", subtitulo="Selección de dimensiones y algoritmo de solución")
        tarjeta_cfg.pack(fill=tk.X, pady=(0, 8))

        row_cfg = tk.Frame(tarjeta_cfg.contenido, bg=BG_CARD)
        row_cfg.pack(fill=tk.X)

        # Spinbox Filas m
        tk.Label(row_cfg, text="Filas (m):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_m = SpinboxNumerico(row_cfg, min_val=1, max_val=10, initial_val=3, on_change=self._al_cambiar_dimensiones)
        self.spin_m.pack(side=tk.LEFT, padx=(0, 12))

        # Spinbox Columnas n
        tk.Label(row_cfg, text="Columnas (n):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_n = SpinboxNumerico(row_cfg, min_val=1, max_val=10, initial_val=3, on_change=self._al_cambiar_dimensiones)
        self.spin_n.pack(side=tk.LEFT, padx=(0, 14))

        # Selector de Método
        tk.Label(row_cfg, text="Algoritmo:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.metodo = tk.StringVar(value="Gauss")
        self.selector_metodo = ttk.Combobox(
            row_cfg, textvariable=self.metodo,
            values=("Gauss", "Gauss-Jordan", "Factorización LU"),
            state="readonly", width=16
        )
        self.selector_metodo.pack(side=tk.LEFT, padx=(0, 10))

        BotonSecundario(row_cfg, text="Regenerar", command=self.controlador.generar_cuadricula, font=FONT_SMALL_BOLD).pack(side=tk.LEFT)

        # ── TARJETA: Sistemas Precargados (Chips Semánticos) ───────────────────
        tarjeta_presets = Tarjeta(col_izq, titulo="Sistemas Precargados", subtitulo="Prueba configuraciones y tipos de solución predefinidos")
        tarjeta_presets.pack(fill=tk.X, pady=(0, 8))

        chips_frame = tk.Frame(tarjeta_presets.contenido, bg=BG_CARD)
        chips_frame.pack(fill=tk.X)

        presets = [
            ("Solución Única", "Sistema compatible determinado", "success", "unica"),
            ("Factorización LU", "Descomposición A = LU", "accent", "lu"),
            ("Infinitas Soluciones", "Compatible indeterminado", "warning", "infinitas"),
            ("Inconsistente", "Sin solución en R^n", "error", "inconsistente"),
            ("Inversa Matriz", "Cálculo A⁻¹", "info", "inversa"),
        ]

        for tit, desc, tipo_col, tipo_key in presets:
            chip = ChipSistema(
                chips_frame, titulo=tit, descripcion=desc, tipo_color=tipo_col,
                comando=lambda t=tipo_key: self.controlador.cargar_ejemplo(t)
            )
            chip.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

        # ── TARJETA: Matriz Aumentada [A | b] ─────────────────────────────────
        tarjeta_matriz = Tarjeta(col_izq, titulo="Matriz Aumentada [ A | b ]", subtitulo="Navega con Tab / Flechas. Se aceptan fracciones (ej: 1/2, -3/4)")
        tarjeta_matriz.pack(fill=tk.BOTH, expand=True)

        self.scroll_matriz = ScrollableFrame(tarjeta_matriz.contenido, bg_color=BG_CARD)
        self.scroll_matriz.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.matriz_entries = []
        self.vector_entries = []

        # Botón Principal de Resolución Destacado
        btn_box = tk.Frame(tarjeta_matriz.contenido, bg=BG_CARD)
        btn_box.pack(fill=tk.X, pady=(4, 0))

        self.btn_resolver = BotonPrimario(
            btn_box, text="⚡ RESOLVER SISTEMA", shortcut="Ctrl + Enter",
            command=self.controlador.resolver_sistema, font=FONT_TITLE,
            padx=20, pady=10
        )
        self.btn_resolver.pack(fill=tk.X)
        self.root.bind("<Control-Return>", lambda e: self.controlador.resolver_sistema())
        self.root.bind("<Control-KP_Enter>", lambda e: self.controlador.resolver_sistema())

        # ── COLUMNA DERECHA: RESULTADOS Y DIAGNÓSTICO ──────────────────────────
        tarjeta_res = Tarjeta(col_der, titulo="Resultados del Análisis", subtitulo="Diagnóstico matemático e historial de pivoteo")
        tarjeta_res.pack(fill=tk.BOTH, expand=True)

        self.nb_gauss_res = ttk.Notebook(tarjeta_res.contenido, style="Sub.TNotebook")
        self.nb_gauss_res.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Diagnóstico & Solución
        t_diag = tk.Frame(self.nb_gauss_res, bg=BG_CARD, padx=12, pady=10)
        self.nb_gauss_res.add(t_diag, text="  Diagnóstico & Solución  ")

        # Badge Grande de Clasificación
        self.badge_clasificacion = BadgeEstado(t_diag, text="SIN CALCULAR AÚN", tipo="neutral")
        self.badge_clasificacion.pack(anchor="w", pady=(0, 10))

        cols_diag = tk.Frame(t_diag, bg=BG_CARD)
        cols_diag.pack(fill=tk.BOTH, expand=True)

        # Vector Solución
        box_sol = tk.Frame(cols_diag, bg=BG_CARD)
        box_sol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(box_sol, text="Vector Solución:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 4))
        self.txt_solucion = self._crear_consola(box_sol, height=9)
        self.txt_solucion.pack(fill=tk.BOTH, expand=True)

        # Comprobación de Ecuaciones
        box_ver = tk.Frame(cols_diag, bg=BG_CARD)
        box_ver.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(box_ver, text="Comprobación en Ecuaciones:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 4))
        self.txt_verificacion = self._crear_consola(box_ver, height=9)
        self.txt_verificacion.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Historial de Pivoteo
        t_hist = tk.Frame(self.nb_gauss_res, bg=BG_CARD, padx=10, pady=8)
        self.nb_gauss_res.add(t_hist, text="  Historial de Pivoteo Paso a Paso  ")

        bar_h = tk.Frame(t_hist, bg=BG_CARD)
        bar_h.pack(fill=tk.X, pady=(0, 4))
        tk.Label(bar_h, text="Transformaciones elementales de fila:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_SECONDARY).pack(side=tk.LEFT)

        frame_txt_h = tk.Frame(t_hist, bg=BG_CARD)
        frame_txt_h.pack(fill=tk.BOTH, expand=True)

        self.txt_historial = self._crear_consola(frame_txt_h, height=18, wrap=tk.NONE)
        sc_hy = ttk.Scrollbar(frame_txt_h, orient="vertical", command=self.txt_historial.yview)
        sc_hx = ttk.Scrollbar(frame_txt_h, orient="horizontal", command=self.txt_historial.xview)
        self.txt_historial.configure(yscrollcommand=sc_hy.set, xscrollcommand=sc_hx.set)

        self.txt_historial.grid(row=0, column=0, sticky="nsew")
        sc_hy.grid(row=0, column=1, sticky="ns")
        sc_hx.grid(row=1, column=0, sticky="ew")
        frame_txt_h.grid_rowconfigure(0, weight=1)
        frame_txt_h.grid_columnconfigure(0, weight=1)

        self._conectar_consola_fullscreen(self.txt_historial, "Historial de Pivoteo Gauss-Jordan", bar_h)

        # ── Barra de Acciones Rápidas (Abajo en la tarjeta de resultados) ─────
        acciones_bar = tk.Frame(tarjeta_res.contenido, bg=BG_CARD)
        acciones_bar.pack(fill=tk.X, pady=(8, 0))

        btn_copiar = BotonSecundario(
            acciones_bar, text="📋 Copiar Resultado", font=FONT_SMALL_BOLD,
            command=lambda: self.copiar_al_portapapeles(self._obtener_resumen_gauss_texto())
        )
        btn_copiar.pack(side=tk.LEFT, padx=(0, 6))
        Tooltip(btn_copiar, "Copia el vector solución y comprobación al portapapeles")

        btn_limpiar = BotonSecundario(
            acciones_bar, text="🧹 Limpiar Matriz", font=FONT_SMALL_BOLD,
            command=self.limpiar_campos
        )
        btn_limpiar.pack(side=tk.LEFT, padx=6)
        Tooltip(btn_limpiar, "Restablece todos los coeficientes a 0")

        btn_deshacer = BotonSecundario(
            acciones_bar, text="↩ Deshacer", font=FONT_SMALL_BOLD,
            command=self.deshacer_cambio
        )
        btn_deshacer.pack(side=tk.LEFT, padx=6)
        Tooltip(btn_deshacer, "Restaura el estado previo de la matriz")

        btn_fs = BotonSecundario(
            acciones_bar, text="⛶ Pantalla Completa", font=FONT_SMALL_BOLD,
            command=lambda: self.abrir_consola_fullscreen("Informe Completo Gauss-Jordan", self._obtener_resumen_gauss_texto)
        )
        btn_fs.pack(side=tk.RIGHT)
        Tooltip(btn_fs, "Abre los resultados en pantalla completa para proyectar")

        # Construir matriz inicial de 3x3
        self.construir_cuadricula(3, 3)

    def _al_cambiar_dimensiones(self, _val=None):
        try:
            m = int(self.spin_m.get())
            n = int(self.spin_n.get())
            # Conservar valores actuales si existen
            valores_anteriores = []
            if self.matriz_entries:
                for fila in self.matriz_entries:
                    valores_anteriores.append([e.get() for e in fila])
            vec_anterior = [e.get() for e in self.vector_entries] if self.vector_entries else []

            self.construir_cuadricula(m, n)

            # Restaurar valores donde coincidan dimensiones
            for i in range(min(m, len(valores_anteriores))):
                for j in range(min(n, len(valores_anteriores[i]))):
                    self.matriz_entries[i][j].delete(0, tk.END)
                    self.matriz_entries[i][j].insert(0, valores_anteriores[i][j])
            for i in range(min(m, len(vec_anterior))):
                self.vector_entries[i].delete(0, tk.END)
                self.vector_entries[i].insert(0, vec_anterior[i])
        except Exception:
            pass

    def construir_cuadricula(self, m, n):
        # Guardar estado para deshacer
        if self.matriz_entries:
            estado = {
                "A": [[e.get() for e in fila] for fila in self.matriz_entries],
                "b": [e.get() for e in self.vector_entries]
            }
            self._historial_matrices.append(estado)
            if len(self._historial_matrices) > 10:
                self._historial_matrices.pop(0)

        for w in self.scroll_matriz.scrollable_frame.winfo_children():
            w.destroy()

        self.matriz_entries = []
        self.vector_entries = []
        c = self.scroll_matriz.scrollable_frame

        # Encabezados de Columna (x₁, x₂, ... | b)
        for j in range(n):
            tk.Label(
                c, text=f"x{j+1}", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_SECONDARY
            ).grid(row=0, column=j+1, padx=3, pady=(0, 6))

        # Separador visual entre A y b
        tk.Label(c, text="│", font=FONT_MONO_BOLD, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=0, column=n+1, padx=4)

        lbl_b = tk.Label(c, text="b", font=FONT_SMALL_BOLD, bg=ACCENT_SOFT, fg=ACCENT_PRIMARY, padx=8)
        lbl_b.grid(row=0, column=n+2, padx=3, pady=(0, 6))

        # Celdas numéricas
        for i in range(m):
            tk.Label(
                c, text=f"E{i+1}", font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED
            ).grid(row=i+1, column=0, padx=(0, 6))

            fila = []
            for j in range(n):
                celda = CeldaMatriz(c, valor_inicial="0", es_columna_b=False)
                celda.grid(row=i+1, column=j+1, padx=2, pady=2)
                self._conectar_navegacion_celdas(celda, i, j, m, n)
                fila.append(celda)
            self.matriz_entries.append(fila)

            tk.Label(c, text="│", font=FONT_MONO_BOLD, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=i+1, column=n+1, padx=4)

            celda_b = CeldaMatriz(c, valor_inicial="0", es_columna_b=True)
            celda_b.grid(row=i+1, column=n+2, padx=2, pady=2)
            self._conectar_navegacion_celdas(celda_b, i, n, m, n)
            self.vector_entries.append(celda_b)

        self._actualizar_paso_activo(1)

    def _conectar_navegacion_celdas(self, entry, row, col, max_r, max_c):
        def on_down(event):
            if row + 1 < max_r:
                if col < max_c:
                    self.matriz_entries[row + 1][col].focus_set()
                else:
                    self.vector_entries[row + 1].focus_set()

        def on_up(event):
            if row - 1 >= 0:
                if col < max_c:
                    self.matriz_entries[row - 1][col].focus_set()
                else:
                    self.vector_entries[row - 1].focus_set()

        def on_right(event):
            if col + 1 < max_c:
                self.matriz_entries[row][col + 1].focus_set()
            elif col + 1 == max_c:
                self.vector_entries[row].focus_set()

        def on_left(event):
            if col == max_c:
                self.matriz_entries[row][max_c - 1].focus_set()
            elif col - 1 >= 0:
                self.matriz_entries[row][col - 1].focus_set()

        entry.bind("<Down>", on_down)
        entry.bind("<Up>", on_up)
        entry.bind("<Right>", on_right)
        entry.bind("<Left>", on_left)

    def _actualizar_paso_activo(self, paso):
        for idx, (circ, lbl) in enumerate(self.step_labels):
            if idx + 1 < paso:
                circ.configure(bg=SUCCESS_BG, fg=SUCCESS_TEXT, text="✓")
                lbl.configure(fg=TEXT_PRIMARY)
            elif idx + 1 == paso:
                circ.configure(bg=ACCENT_PRIMARY, fg=TEXT_ON_ACCENT, text=str(idx + 1))
                lbl.configure(fg=ACCENT_PRIMARY)
            else:
                circ.configure(bg=BG_SECONDARY, fg=TEXT_MUTED, text=str(idx + 1))
                lbl.configure(fg=TEXT_MUTED)

    def actualizar_resumen(self, clasificacion, solucion_texto, verificacion_texto):
        es_unica = "Única" in clasificacion
        es_inf   = "Infinitas" in clasificacion
        tipo_b = "success" if es_unica else ("warning" if es_inf else "error")

        self.badge_clasificacion.set_estado(clasificacion.upper(), tipo=tipo_b)
        self._write(self.txt_solucion, solucion_texto)
        self._write(self.txt_verificacion, verificacion_texto)
        self._actualizar_paso_activo(3)
        self._ops()

    def actualizar_historial(self, h):
        self._write(self.txt_historial, h)

    def limpiar_campos(self):
        for fila in self.matriz_entries:
            for e in fila:
                e.delete(0, tk.END)
                e.insert(0, "0")
        for eb in self.vector_entries:
            eb.delete(0, tk.END)
            eb.insert(0, "0")
        self.badge_clasificacion.set_estado("MATRIZ REINICIADA", tipo="neutral")
        self._write(self.txt_solucion, "")
        self._write(self.txt_verificacion, "")
        self._write(self.txt_historial, "")
        self._actualizar_paso_activo(2)

    def deshacer_cambio(self):
        if self._historial_matrices:
            ant = self._historial_matrices.pop()
            A = ant["A"]
            b = ant["b"]
            m, n = len(A), len(A[0])
            self.spin_m.set(m)
            self.spin_n.set(n)
            self.construir_cuadricula(m, n)
            for i in range(m):
                for j in range(n):
                    self.matriz_entries[i][j].delete(0, tk.END)
                    self.matriz_entries[i][j].insert(0, str(A[i][j]))
                self.vector_entries[i].delete(0, tk.END)
                self.vector_entries[i].insert(0, str(b[i]))

    def _obtener_resumen_gauss_texto(self):
        clasif = self.badge_clasificacion.lbl.cget("text")
        sol = self.txt_solucion.get("1.0", tk.END).strip()
        ver = self.txt_verificacion.get("1.0", tk.END).strip()
        hist = self.txt_historial.get("1.0", tk.END).strip()

        lineas = [
            "=" * 70,
            f"  DIAGNÓSTICO: {clasif.strip()}",
            "=" * 70 + "\n",
            "── VECTOR SOLUCIÓN ───────────────────────────────────────────────────",
            sol if sol else "[ Sin solución calculada ]",
            "\n── COMPROBACIÓN EN ECUACIONES ────────────────────────────────────────",
            ver if ver else "[ Sin comprobación calculada ]"
        ]
        if hist:
            lineas.extend([
                "\n── HISTORIAL DE PIVOTEO PASO A PASO ──────────────────────────────────",
                hist
            ])
        return "\n".join(lineas)

    # ==========================================================================
    # MÓDULO 2 — VECTORIAL & MATRICES
    # ==========================================================================
    def _build_vectorial(self):
        parent = self.tab_vectorial
        self.nb_vectorial = ttk.Notebook(parent, style="Sub.TNotebook")
        self.nb_vectorial.pack(fill=tk.BOTH, expand=True)

        # ── SUB-TAB: Vectores en R^n ──────────────────────────────────────────
        tv = tk.Frame(self.nb_vectorial, bg=BG_WINDOW)
        self.nb_vectorial.add(tv, text="  Vectores en R^n  ")

        cols_v = tk.Frame(tv, bg=BG_WINDOW)
        cols_v.pack(fill=tk.BOTH, expand=True, pady=6)

        v_izq = tk.Frame(cols_v, bg=BG_WINDOW)
        v_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        v_der = tk.Frame(cols_v, bg=BG_WINDOW)
        v_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # Tarjeta Config Vectores
        t_vcfg = Tarjeta(v_izq, titulo="Parámetros de Vectores", subtitulo="Suma, resta, ponderación y combinación lineal")
        t_vcfg.pack(fill=tk.X, pady=(0, 8))

        row_v = tk.Frame(t_vcfg.contenido, bg=BG_CARD)
        row_v.pack(fill=tk.X)

        tk.Label(row_v, text="Dimensión (n):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_dim_v = SpinboxNumerico(row_v, min_val=1, max_val=10, initial_val=3)
        self.spin_dim_v.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row_v, text="Cantidad (k):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_cant_v = SpinboxNumerico(row_v, min_val=1, max_val=10, initial_val=2)
        self.spin_cant_v.pack(side=tk.LEFT, padx=(0, 10))

        BotonSecundario(row_v, text="Generar", command=self.controlador.generar_vectores, font=FONT_SMALL_BOLD).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(row_v, text="Escalar c:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.entrada_escalar_vector = CeldaMatriz(row_v, valor_inicial="1", width=5)
        self.entrada_escalar_vector.pack(side=tk.LEFT)

        # Tarjeta Entradas de Vectores
        t_vinp = Tarjeta(v_izq, titulo="Componentes de los Vectores", subtitulo="Ingresa los valores de v₁...vk y el vector objetivo b")
        t_vinp.pack(fill=tk.BOTH, expand=True)

        self.scroll_vectores = ScrollableFrame(t_vinp.contenido, bg_color=BG_CARD)
        self.scroll_vectores.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.vec_entries = []
        self.vec_b_entries = []

        BotonPrimario(
            t_vinp.contenido, text="▶ Calcular Operaciones y Combinación Lineal",
            command=self.controlador.operar_vectores, font=FONT_HEADING
        ).pack(fill=tk.X)

        # Tarjeta Resultados Vectores
        t_vres = Tarjeta(v_der, titulo="Resultados Vectoriales", subtitulo="Operaciones algebraicas y dependencia lineal")
        t_vres.pack(fill=tk.BOTH, expand=True)

        frame_txt_v = tk.Frame(t_vres.contenido, bg=BG_CARD)
        frame_txt_v.pack(fill=tk.BOTH, expand=True)

        self.txt_res_vectores = self._crear_consola(frame_txt_v, height=18)
        sc_vy = ttk.Scrollbar(frame_txt_v, orient="vertical", command=self.txt_res_vectores.yview)
        self.txt_res_vectores.configure(yscrollcommand=sc_vy.set)
        self.txt_res_vectores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_vy.pack(side=tk.RIGHT, fill=tk.Y)

        self._conectar_consola_fullscreen(self.txt_res_vectores, "Operaciones Vectoriales")

        # ── SUB-TAB: Álgebra Matricial ────────────────────────────────────────
        tm = tk.Frame(self.nb_vectorial, bg=BG_WINDOW)
        self.tab_sub_matrices = tm
        self.nb_vectorial.add(tm, text="  Álgebra Matricial (A+B, A×B, A⁻¹, LU)  ")

        cols_m = tk.Frame(tm, bg=BG_WINDOW)
        cols_m.pack(fill=tk.BOTH, expand=True, pady=6)

        m_izq = tk.Frame(cols_m, bg=BG_WINDOW)
        m_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        m_der = tk.Frame(cols_m, bg=BG_WINDOW)
        m_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # Tarjeta Dimensiones Matrices
        t_mcfg = Tarjeta(m_izq, titulo="Dimensiones y Presets", subtitulo="Configura filas y columnas de las matrices A y B")
        t_mcfg.pack(fill=tk.X, pady=(0, 8))

        row_m1 = tk.Frame(t_mcfg.contenido, bg=BG_CARD)
        row_m1.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row_m1, text="Matriz A (f × c):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_fa = SpinboxNumerico(row_m1, min_val=1, max_val=10, initial_val=2, width=3); self.spin_fa.pack(side=tk.LEFT, padx=2)
        self.spin_ca = SpinboxNumerico(row_m1, min_val=1, max_val=10, initial_val=2, width=3); self.spin_ca.pack(side=tk.LEFT, padx=(2, 12))

        tk.Label(row_m1, text="Matriz B (f × c):", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_fb = SpinboxNumerico(row_m1, min_val=1, max_val=10, initial_val=2, width=3); self.spin_fb.pack(side=tk.LEFT, padx=2)
        self.spin_cb = SpinboxNumerico(row_m1, min_val=1, max_val=10, initial_val=2, width=3); self.spin_cb.pack(side=tk.LEFT, padx=(2, 12))

        BotonSecundario(row_m1, text="Generar", command=self.controlador.generar_matrices_ops, font=FONT_SMALL_BOLD).pack(side=tk.LEFT)

        # Presets para Matrices
        row_mej = tk.Frame(t_mcfg.contenido, bg=BG_CARD)
        row_mej.pack(fill=tk.X)
        tk.Label(row_mej, text="Presets:", font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED).pack(side=tk.LEFT, padx=(0, 6))
        for lbl, tipo in [("Inv 2×2", "inv_2x2"), ("Inv 3×3", "inv_3x3"), ("Singular", "inv_singular"), ("LU 3×3", "lu_3x3"), ("LU Pivot", "lu_pivoteo")]:
            BotonFantasma(row_mej, text=lbl, command=lambda t=tipo: self.controlador.cargar_ejemplo_matrices(t)).pack(side=tk.LEFT, padx=2)

        # Tarjeta Celdas Matrices A y B
        t_minp = Tarjeta(m_izq, titulo="Matrices A y B", subtitulo="Ingresa los coeficientes numéricos")
        t_minp.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.scroll_matrices_ops = ScrollableFrame(t_minp.contenido, bg_color=BG_CARD)
        self.scroll_matrices_ops.pack(fill=tk.BOTH, expand=True)
        self.mat_entries_a = []
        self.mat_entries_b = []

        # Tarjeta Operaciones Matriciales
        t_mops = Tarjeta(m_izq, titulo="Operaciones Disponibles", subtitulo="Aritmética, inversión, descomposición LU y determinantes")
        t_mops.pack(fill=tk.X)

        row_op1 = tk.Frame(t_mops.contenido, bg=BG_CARD)
        row_op1.pack(fill=tk.X, pady=(0, 6))

        for txt, op in [("A + B", "suma"), ("A − B", "resta"), ("A × B", "multiplicacion")]:
            BotonPrimario(row_op1, text=txt, command=lambda o=op: self.controlador.operar_matrices(o), font=FONT_SMALL_BOLD, padx=8, pady=4).pack(side=tk.LEFT, padx=2)

        tk.Label(row_op1, text="Escalar c:", font=FONT_SMALL, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(10, 4))
        self.entrada_escalar_mat = CeldaMatriz(row_op1, valor_inicial="2", width=4)
        self.entrada_escalar_mat.pack(side=tk.LEFT, padx=(0, 4))
        BotonSecundario(row_op1, text="c × A", command=lambda: self.controlador.operar_matrices("escalar"), font=FONT_SMALL_BOLD, padx=8, pady=4).pack(side=tk.LEFT)

        row_op2 = tk.Frame(t_mops.contenido, bg=BG_CARD)
        row_op2.pack(fill=tk.X)

        BotonSecundario(row_op2, text="A⁻¹ (Inversa A)", command=lambda: self.controlador.operar_matrices("inversa_a"), font=FONT_SMALL_BOLD, padx=6, pady=4).pack(side=tk.LEFT, padx=2)
        BotonSecundario(row_op2, text="B⁻¹ (Inversa B)", command=lambda: self.controlador.operar_matrices("inversa_b"), font=FONT_SMALL_BOLD, padx=6, pady=4).pack(side=tk.LEFT, padx=2)
        BotonSecundario(row_op2, text="LU (Matriz A)", command=lambda: self.controlador.operar_matrices("lu_a"), font=FONT_SMALL_BOLD, padx=6, pady=4).pack(side=tk.LEFT, padx=2)
        BotonSecundario(row_op2, text="det(A) Sarrus", command=lambda: self.controlador.operar_matrices("determinante_sarrus"), font=FONT_SMALL_BOLD, padx=6, pady=4).pack(side=tk.LEFT, padx=2)
        BotonSecundario(row_op2, text="det(A) Cofact.", command=lambda: self.controlador.operar_matrices("determinante_cofactores"), font=FONT_SMALL_BOLD, padx=6, pady=4).pack(side=tk.LEFT, padx=2)

        # Tarjeta Resultados Matrices
        t_mres = Tarjeta(m_der, titulo="Resultados del Cálculo Matricial", subtitulo="Matrices resultantes y desglose analítico paso a paso")
        t_mres.pack(fill=tk.BOTH, expand=True)

        frame_txt_m = tk.Frame(t_mres.contenido, bg=BG_CARD)
        frame_txt_m.pack(fill=tk.BOTH, expand=True)

        self.txt_res_matrices = self._crear_consola(frame_txt_m, height=20, wrap=tk.NONE)
        sc_my = ttk.Scrollbar(frame_txt_m, orient="vertical", command=self.txt_res_matrices.yview)
        sc_mx = ttk.Scrollbar(frame_txt_m, orient="horizontal", command=self.txt_res_matrices.xview)
        self.txt_res_matrices.configure(yscrollcommand=sc_my.set, xscrollcommand=sc_mx.set)

        self.txt_res_matrices.grid(row=0, column=0, sticky="nsew")
        sc_my.grid(row=0, column=1, sticky="ns")
        sc_mx.grid(row=1, column=0, sticky="ew")
        frame_txt_m.grid_rowconfigure(0, weight=1)
        frame_txt_m.grid_columnconfigure(0, weight=1)

        self._conectar_consola_fullscreen(self.txt_res_matrices, "Álgebra Matricial")

        # Inicialización de vectores y matrices
        self.construir_vectores(3, 2)
        self.construir_matrices_ops(2, 2, 2, 2)

    def construir_vectores(self, n, k):
        for w in self.scroll_vectores.scrollable_frame.winfo_children():
            w.destroy()
        self.vec_entries = []
        self.vec_b_entries = []
        c = self.scroll_vectores.scrollable_frame

        for i in range(k):
            tk.Label(c, text=f"v{i+1} =", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).grid(row=i, column=0, padx=6, pady=4)
            tk.Label(c, text="(", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=i, column=1)
            fila = []
            for j in range(n):
                celda = CeldaMatriz(c, valor_inicial="0", width=6)
                celda.grid(row=i, column=j+2, padx=2, pady=4)
                fila.append(celda)
            self.vec_entries.append(fila)
            tk.Label(c, text=")", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=i, column=n+2)

        tk.Label(c, text="b =", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=k, column=0, padx=6, pady=8)
        tk.Label(c, text="(", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=k, column=1, pady=8)
        for j in range(n):
            celda_b = CeldaMatriz(c, valor_inicial="0", width=6, es_columna_b=True)
            celda_b.grid(row=k, column=j+2, padx=2, pady=8)
            self.vec_b_entries.append(celda_b)
        tk.Label(c, text=")", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=k, column=n+2, pady=8)

    def mostrar_resultado_vectores(self, t):
        self._write(self.txt_res_vectores, t)
        self._ops()

    def construir_matrices_ops(self, m_a, n_a, m_b, n_b):
        for w in self.scroll_matrices_ops.scrollable_frame.winfo_children():
            w.destroy()
        self.mat_entries_a = []
        self.mat_entries_b = []
        c = self.scroll_matrices_ops.scrollable_frame

        # Matriz A
        tk.Label(c, text=f"Matriz A ({m_a}×{n_a})", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=0, column=0, columnspan=n_a+2, pady=(0, 4))
        for i in range(m_a):
            tk.Label(c, text="[", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=i+1, column=0)
            fila = []
            for j in range(n_a):
                celda = CeldaMatriz(c, valor_inicial="0", width=6)
                celda.grid(row=i+1, column=j+1, padx=2, pady=2)
                fila.append(celda)
            self.mat_entries_a.append(fila)
            tk.Label(c, text="]", font=FONT_MONO_LG, bg=BG_CARD, fg=ACCENT_PRIMARY).grid(row=i+1, column=n_a+1)

        off = n_a + 3
        # Matriz B
        tk.Label(c, text=f"Matriz B ({m_b}×{n_b})", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_SECONDARY).grid(row=0, column=off, columnspan=n_b+2, pady=(0, 4))
        for i in range(m_b):
            tk.Label(c, text="[", font=FONT_MONO_LG, bg=BG_CARD, fg=TEXT_SECONDARY).grid(row=i+1, column=off)
            fila = []
            for j in range(n_b):
                celda = CeldaMatriz(c, valor_inicial="0", width=6)
                celda.grid(row=i+1, column=j+off+1, padx=2, pady=2)
                fila.append(celda)
            self.mat_entries_b.append(fila)
            tk.Label(c, text="]", font=FONT_MONO_LG, bg=BG_CARD, fg=TEXT_SECONDARY).grid(row=i+1, column=n_b+off+1)

    def mostrar_resultado_matrices(self, t):
        self._write(self.txt_res_matrices, t)
        self._ops()

    # ==========================================================================
    # MÓDULO 3 — CONVERSIÓN DE BASES
    # ==========================================================================
    def _build_conv(self):
        parent = self.tab_conv

        cols = tk.Frame(parent, bg=BG_WINDOW)
        cols.pack(fill=tk.BOTH, expand=True)

        col_l = tk.Frame(cols, bg=BG_WINDOW)
        col_l.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        col_r = tk.Frame(cols, bg=BG_WINDOW)
        col_r.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # Tarjeta 1: Hacia Decimal
        t_hacia = Tarjeta(col_l, titulo="Hacia Decimal", subtitulo="Descomposición polinómica con base radix")
        t_hacia.pack(fill=tk.X, pady=(0, 10))

        row1 = tk.Frame(t_hacia.contenido, bg=BG_CARD)
        row1.pack(fill=tk.X, pady=(0, 8))

        tk.Label(row1, text="Número Original:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_conv_origen = CeldaMatriz(row1, valor_inicial="101101", width=14)
        self.entry_conv_origen.pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(row1, text="Base Radix:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 6))
        self.base_origen = tk.StringVar(value="Binario")
        ttk.Combobox(row1, textvariable=self.base_origen, values=("Binario", "Octal", "Hexadecimal"), state="readonly", width=12).pack(side=tk.LEFT)

        BotonPrimario(
            t_hacia.contenido, text="Convertir a Decimal",
            command=self.controlador.convertir_a_decimal, font=FONT_SMALL_BOLD
        ).pack(fill=tk.X)

        # Tarjeta 2: Desde Decimal
        t_desde = Tarjeta(col_l, titulo="Desde Decimal", subtitulo="Conversión mediante divisiones sucesivas")
        t_desde.pack(fill=tk.X)

        row2 = tk.Frame(t_desde.contenido, bg=BG_CARD)
        row2.pack(fill=tk.X, pady=(0, 8))

        tk.Label(row2, text="Entero Decimal:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_conv_decimal = CeldaMatriz(row2, valor_inicial="45", width=14)
        self.entry_conv_decimal.pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(row2, text="Base Destino:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 6))
        self.base_destino = tk.StringVar(value="Hexadecimal")
        ttk.Combobox(row2, textvariable=self.base_destino, values=("Binario", "Octal", "Hexadecimal"), state="readonly", width=12).pack(side=tk.LEFT)

        BotonPrimario(
            t_desde.contenido, text="Convertir a Base Destino",
            command=self.controlador.convertir_desde_decimal, font=FONT_SMALL_BOLD
        ).pack(fill=tk.X)

        # Tarjeta Derecha: Consola de Desglose
        t_res = Tarjeta(col_r, titulo="Desglose y Procedimiento de Conversión", subtitulo="Pasos detallados de la conversión matemática")
        t_res.pack(fill=tk.BOTH, expand=True)

        frame_txt_c = tk.Frame(t_res.contenido, bg=BG_CARD)
        frame_txt_c.pack(fill=tk.BOTH, expand=True)

        self.txt_resultados_conv = self._crear_consola(frame_txt_c, height=20, wrap=tk.WORD)
        sc_cy = ttk.Scrollbar(frame_txt_c, orient="vertical", command=self.txt_resultados_conv.yview)
        self.txt_resultados_conv.configure(yscrollcommand=sc_cy.set)
        self.txt_resultados_conv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_cy.pack(side=tk.RIGHT, fill=tk.Y)

        self._conectar_consola_fullscreen(self.txt_resultados_conv, "Conversión de Bases Numéricas")

    def mostrar_resultado_conversion(self, t):
        self._write(self.txt_resultados_conv, t)
        self._ops()

    # ==========================================================================
    # MÓDULO 4 — NÚMEROS ROMANOS
    # ==========================================================================
    def _build_romanos(self):
        parent = self.tab_romanos

        cols = tk.Frame(parent, bg=BG_WINDOW)
        cols.pack(fill=tk.BOTH, expand=True)

        col_l = tk.Frame(cols, bg=BG_WINDOW)
        col_l.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        col_r = tk.Frame(cols, bg=BG_WINDOW)
        col_r.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # Tarjeta Configuración Romanos
        t_rcfg = Tarjeta(col_l, titulo="Aritmética y Conversión Romana", subtitulo="Configura operandos y la operación a ejecutar")
        t_rcfg.pack(fill=tk.X, pady=(0, 8))

        row1 = tk.Frame(t_rcfg.contenido, bg=BG_CARD)
        row1.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row1, text="Operandos:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_cant_romanos = SpinboxNumerico(row1, min_val=2, max_val=10, initial_val=2, width=3)
        self.spin_cant_romanos.pack(side=tk.LEFT, padx=(0, 10))

        BotonSecundario(row1, text="Generar", command=self.controlador.generar_campos_romanos, font=FONT_SMALL_BOLD).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(row1, text="Operación:", font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))
        self.op_romanos = tk.StringVar(value="Suma (+)")
        self.combo_op_romanos = ttk.Combobox(
            row1, textvariable=self.op_romanos,
            values=("Suma (+)", "Resta (-)", "Multiplicación (×)", "División (÷)"),
            state="readonly", width=16
        )
        self.combo_op_romanos.pack(side=tk.LEFT)

        # Presets
        row_rej = tk.Frame(t_rcfg.contenido, bg=BG_CARD)
        row_rej.pack(fill=tk.X)
        tk.Label(row_rej, text="Ejemplos:", font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED).pack(side=tk.LEFT, padx=(0, 6))
        for lbl, tipo in [("Suma (3)", "suma3"), ("Multiplicación", "mult"), ("División", "div"), ("Resta (3)", "resta3")]:
            BotonFantasma(row_rej, text=lbl, command=lambda t=tipo: self.controlador.cargar_ejemplo_romanos(t)).pack(side=tk.LEFT, padx=2)

        # Tarjeta Operandos Dinámicos
        t_rinp = Tarjeta(col_l, titulo="Valores de los Operandos", subtitulo="Ingresa números romanos estándar (ej: X, XIV, MMXXIV)")
        t_rinp.pack(fill=tk.BOTH, expand=True)

        self.scroll_romanos = ScrollableFrame(t_rinp.contenido, bg_color=BG_CARD)
        self.scroll_romanos.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.romanos_entries = []

        BotonPrimario(
            t_rinp.contenido, text="⚡ CALCULAR RESULTADO",
            command=self.controlador.calcular_operacion_romanos, font=FONT_HEADING
        ).pack(fill=tk.X)

        # Tarjeta Resultados Romanos
        t_rres = Tarjeta(col_r, titulo="Resultados de la Operación", subtitulo="Equivalencia en números romanos y arábigos con desglose")
        t_rres.pack(fill=tk.BOTH, expand=True)

        nb_r = ttk.Notebook(t_rres.contenido, style="Sub.TNotebook")
        nb_r.pack(fill=tk.BOTH, expand=True)

        self.tab_res_romanos  = tk.Frame(nb_r, bg=BG_CARD, padx=16, pady=20)
        self.tab_res_normales = tk.Frame(nb_r, bg=BG_CARD, padx=16, pady=20)
        self.tab_res_desglose = tk.Frame(nb_r, bg=BG_CARD, padx=10, pady=8)

        nb_r.add(self.tab_res_romanos,  text="  Sistema Romano  ")
        nb_r.add(self.tab_res_normales, text="  Sistema Arábigo  ")
        nb_r.add(self.tab_res_desglose, text="  Procedimiento Detallado  ")

        self.lbl_res_romano = tk.Label(
            self.tab_res_romanos, text="—", font=("Consolas", 24, "bold"),
            bg=BG_CARD, fg=ACCENT_PRIMARY, anchor="center"
        )
        self.lbl_res_romano.pack(fill=tk.BOTH, expand=True)

        self.lbl_res_normal = tk.Label(
            self.tab_res_normales, text="—", font=("Consolas", 24, "bold"),
            bg=BG_CARD, fg=TEXT_PRIMARY, anchor="center"
        )
        self.lbl_res_normal.pack(fill=tk.BOTH, expand=True)

        frame_txt_rom = tk.Frame(self.tab_res_desglose, bg=BG_CARD)
        frame_txt_rom.pack(fill=tk.BOTH, expand=True)

        self.txt_rom_desglose = self._crear_consola(frame_txt_rom, height=16, wrap=tk.WORD)
        sc_rom = ttk.Scrollbar(frame_txt_rom, orient="vertical", command=self.txt_rom_desglose.yview)
        self.txt_rom_desglose.configure(yscrollcommand=sc_rom.set)
        self.txt_rom_desglose.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_rom.pack(side=tk.RIGHT, fill=tk.Y)

        self._conectar_consola_fullscreen(self.txt_rom_desglose, "Procedimiento Números Romanos")

        self.construir_campos_romanos(2)

    def construir_campos_romanos(self, cantidad):
        for w in self.scroll_romanos.scrollable_frame.winfo_children():
            w.destroy()
        self.romanos_entries = []
        c = self.scroll_romanos.scrollable_frame

        for i in range(cantidad):
            f = tk.Frame(c, bg=BG_CARD, padx=6, pady=4)
            f.pack(side=tk.LEFT, padx=6)
            tk.Label(f, text=f"Op. #{i+1}", font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
            e = CeldaMatriz(f, valor_inicial="X" if i == 0 else "V" if i == 1 else "I", width=10)
            e.pack(pady=2)
            self.romanos_entries.append(e)

    def mostrar_resultados_romanos(self, resultado_dict):
        res_romano  = resultado_dict.get('resultado_romano', '?')
        res_normal  = resultado_dict.get('resultado_normal', '?')
        desglose    = resultado_dict.get('desglose_operandos', '').strip()
        proc_n      = resultado_dict.get('proceso_normal', '').strip()

        mapa_ops = {
            "Suma (+)": "+", "Resta (-)": "−", "Multiplicación (×)": "×", "División (÷)": "÷"
        }
        signo = mapa_ops.get(self.op_romanos.get(), "?")
        operandos_r = [e.get().strip().upper() for e in self.romanos_entries]

        if len(operandos_r) >= 2:
            ec_romano = f"{(' ' + signo + ' ').join(operandos_r)}  =  {res_romano}"
        else:
            ec_romano = f"{operandos_r[0]}  =  {res_romano}"

        ec_normal = str(res_normal)
        for linea in proc_n.splitlines():
            if "Expresión" in linea and ":" in linea:
                expr_n = linea.split(":", 1)[1].strip()
                ec_normal = f"{expr_n}  =  {res_normal}"
                break
            if "traducida" in linea and ":" in linea:
                expr_n = linea.split(":", 1)[1].strip()
                ec_normal = f"{expr_n}  =  {res_normal}"
                break

        self.lbl_res_romano.config(text=ec_romano)
        self.lbl_res_normal.config(text=ec_normal)
        self._write(self.txt_rom_desglose, desglose)
        self._ops()

    # ==========================================================================
    # MÓDULO 5 — MÉTODO DE BISECCIÓN
    # ==========================================================================
    def _build_biseccion(self):
        parent = self.tab_biseccion

        # Tarjeta Parámetros Bisección
        t_bcfg = Tarjeta(parent, titulo="Método de Bisección · Búsqueda de Raíces", subtitulo="Teorema del Valor Intermedio en funciones continuas")
        t_bcfg.pack(fill=tk.X, pady=(0, 8))

        fields = tk.Frame(t_bcfg.contenido, bg=BG_CARD)
        fields.pack(fill=tk.X, pady=(0, 6))

        specs = (
            ("Función f(x):", "biseccion_funcion", "x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10", 32),
            ("Extremo a:", "biseccion_a", "0.55", 9),
            ("Extremo b:", "biseccion_b", "1.1", 9),
            ("Error (%) :", "biseccion_error", "1", 8),
            ("Máx. Iter:", "biseccion_max_iter", "100", 8),
        )

        for columna, (label, atributo, inicial, ancho) in enumerate(specs):
            cell = tk.Frame(fields, bg=BG_CARD)
            cell.grid(row=0, column=columna, sticky="ew", padx=(0, 10))
            tk.Label(cell, text=label, font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 2))
            if atributo == "biseccion_max_iter":
                entry = SpinboxNumerico(cell, min_val=1, max_val=100000, initial_val=int(inicial), width=ancho)
            else:
                entry = CeldaMatriz(cell, valor_inicial=inicial, width=ancho)
            entry.pack(fill=tk.X)
            setattr(self, atributo, entry)
            fields.grid_columnconfigure(columna, weight=3 if columna == 0 else 1)

        actions = tk.Frame(t_bcfg.contenido, bg=BG_CARD)
        actions.pack(fill=tk.X, pady=(4, 0))

        BotonPrimario(actions, text="⚡ CALCULAR RAÍZ", command=self.controlador.calcular_biseccion, font=FONT_SMALL_BOLD).pack(side=tk.LEFT, padx=(0, 6))
        BotonSecundario(actions, text="🧹 Limpiar", command=self.controlador.limpiar_biseccion, font=FONT_SMALL_BOLD).pack(side=tk.LEFT, padx=6)
        BotonSecundario(actions, text="★ Ejemplo del Profesor", command=self.controlador.cargar_ejemplo_biseccion, font=FONT_SMALL_BOLD).pack(side=tk.LEFT, padx=6)
        tk.Label(actions, text="Funciones soportadas: sin, cos, tan, sqrt, log, exp, potencias (^)", font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED).pack(side=tk.RIGHT)

        # Fila de Métricas / Resumen
        summary = tk.Frame(parent, bg=BG_WINDOW)
        summary.pack(fill=tk.X, pady=(0, 8))

        self.biseccion_raiz = self._biseccion_metric(summary, "Raíz Aproximada", "—", ACCENT_PRIMARY)
        self.biseccion_error_final = self._biseccion_metric(summary, "Error Relativo Final", "—", TEXT_PRIMARY)
        self.biseccion_iteraciones_total = self._biseccion_metric(summary, "Iteraciones", "—", TEXT_PRIMARY)
        self.biseccion_estado = self._biseccion_metric(summary, "Estado", "Esperando datos", TEXT_MUTED)

        # Gráfica y Explicación
        work = tk.Frame(parent, bg=BG_WINDOW)
        work.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        t_graf = Tarjeta(work, titulo="Gráfica Interactiva", subtitulo="Comportamiento de f(x) y subintervalo actual")
        t_graf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        self.biseccion_canvas = tk.Canvas(t_graf.contenido, height=220, bg=BG_CARD, highlightthickness=0, bd=0)
        self.biseccion_canvas.pack(fill=tk.BOTH, expand=True)
        self.biseccion_canvas.bind("<Configure>", lambda _event: self._dibujar_grafica_biseccion())
        self._funcion_grafica_biseccion = None
        self._resultado_biseccion = None
        self._iteracion_seleccionada = None

        t_exp = Tarjeta(work, titulo="Lectura del Procedimiento", subtitulo="Detalle paso a paso del intervalo")
        t_exp.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        self.biseccion_selector = ttk.Combobox(t_exp.contenido, state="readonly", width=24)
        self.biseccion_selector.pack(anchor="w", pady=(0, 6))
        self.biseccion_selector.bind("<<ComboboxSelected>>", self._seleccionar_iteracion_biseccion)

        self.biseccion_explicacion = tk.Label(
            t_exp.contenido, text="Carga una función e intervalo con cambio de signo para comenzar.",
            font=FONT_MONO_SM, bg=BG_CARD, fg=TEXT_SECONDARY, justify=tk.LEFT, anchor="nw", wraplength=380
        )
        self.biseccion_explicacion.pack(fill=tk.BOTH, expand=True)

        # Tabla de Iteraciones
        t_tab = Tarjeta(parent, titulo="Tabla de Iteraciones", subtitulo="Historial completo de convergencia numérica")
        t_tab.pack(fill=tk.BOTH, expand=True)

        columns = ("i", "a", "b", "c", "fa", "fb", "fc", "signo", "abs_fc")
        table_frame = tk.Frame(t_tab.contenido, bg=BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.biseccion_tabla = ttk.Treeview(table_frame, columns=columns, show="headings", height=7, selectmode="browse")
        headings = {
            "i": ("i", 45), "a": ("a", 100), "b": ("b", 100),
            "c": ("c (Punto Medio)", 130), "fa": ("f(a)", 105),
            "fb": ("f(b)", 105), "fc": ("f(c)", 105),
            "signo": ("f(a)·f(c)", 95), "abs_fc": ("|f(c)|", 100),
        }
        for columna, (titulo, ancho) in headings.items():
            self.biseccion_tabla.heading(columna, text=titulo)
            self.biseccion_tabla.column(columna, width=ancho, minwidth=ancho, anchor=tk.CENTER,
                                        stretch=columna in ("a", "b", "c", "fa", "fb", "fc"))
        self.biseccion_tabla.tag_configure("ultima", background=ACCENT_SOFT, foreground=ACCENT_PRIMARY)
        self.biseccion_tabla.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.biseccion_tabla.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.biseccion_tabla.xview)
        self.biseccion_tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.biseccion_tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila_biseccion)
        self._dibujar_grafica_biseccion()

    def _biseccion_metric(self, parent, titulo, valor, color):
        block = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        block.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(block, text=titulo, font=FONT_MICRO, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", padx=10, pady=(6, 1))
        label = tk.Label(block, text=valor, font=FONT_TITLE, bg=BG_CARD, fg=color, anchor="w")
        label.pack(fill=tk.X, padx=10, pady=(0, 6))
        return label

    @staticmethod
    def _numero_biseccion(valor, digitos=8):
        return "—" if valor is None else f"{valor:.{digitos}g}"

    def mostrar_resultado_biseccion(self, resultado, funcion):
        self._resultado_biseccion = resultado
        self._funcion_grafica_biseccion = funcion
        self.biseccion_raiz.config(text=f"{resultado.raiz:.10g}")
        self.biseccion_error_final.config(
            text="—" if resultado.error_final is None else f"{resultado.error_final:.6g} %"
        )
        self.biseccion_iteraciones_total.config(text=str(len(resultado.iteraciones)))
        self.biseccion_estado.config(
            text="CONVERGIÓ" if resultado.convergio else "LÍMITE ALCANZADO",
            fg=SUCCESS_TEXT if resultado.convergio else WARNING_TEXT,
        )
        for item in self.biseccion_tabla.get_children():
            self.biseccion_tabla.delete(item)
        for indice, fila in enumerate(resultado.iteraciones):
            self.biseccion_tabla.insert("", tk.END, iid=str(indice), values=(
                fila.numero, self._numero_biseccion(fila.a), self._numero_biseccion(fila.b),
                self._numero_biseccion(fila.c), self._numero_biseccion(fila.fa),
                self._numero_biseccion(fila.fb), self._numero_biseccion(fila.fc),
                fila.signo_producto, self._numero_biseccion(abs(fila.fc)),
            ), tags=("ultima",) if indice == len(resultado.iteraciones) - 1 else ())
        self.biseccion_selector["values"] = tuple(
            f"Iteración {fila.numero}" for fila in resultado.iteraciones
        )
        if resultado.iteraciones:
            indice_final = len(resultado.iteraciones) - 1
            self.biseccion_selector.current(indice_final)
            self._mostrar_iteracion_biseccion(indice_final)
            self.biseccion_tabla.selection_set(str(indice_final))
        else:
            self.biseccion_selector.set("")
            self.biseccion_explicacion.config(text=resultado.motivo)
        self._dibujar_grafica_biseccion()
        self._ops()

    def _seleccionar_iteracion_biseccion(self, _event=None):
        indice = self.biseccion_selector.current()
        if indice >= 0:
            self._mostrar_iteracion_biseccion(indice)
            self.biseccion_tabla.selection_set(str(indice))
            self._dibujar_grafica_biseccion()

    def _seleccionar_fila_biseccion(self, _event=None):
        seleccion = self.biseccion_tabla.selection()
        if seleccion:
            indice = int(seleccion[0])
            self.biseccion_selector.current(indice)
            self._mostrar_iteracion_biseccion(indice)
            self._dibujar_grafica_biseccion()

    def _mostrar_iteracion_biseccion(self, indice):
        if not self._resultado_biseccion or not self._resultado_biseccion.iteraciones:
            return
        fila = self._resultado_biseccion.iteraciones[indice]
        error = "aún no se calcula (primera iteración)" if fila.error_relativo is None else f"{fila.error_relativo:.6g} %"
        criterio = ("Error relativo porcentual entre puntos medios consecutivos."
                    if fila.criterio_error == "error relativo porcentual"
                    else "Como c = 0, se usa el ancho relativo del intervalo para evitar dividir entre cero.")
        texto = (
            f"Intervalo actual: [{fila.a:.10g}, {fila.b:.10g}]\n"
            f"Punto medio: c = (a + b) / 2 = {fila.c:.10g}\n"
            f"f(a) = {fila.fa:.8g}    f(c) = {fila.fc:.8g}\n"
            f"Signo de f(a)·f(c): {fila.signo_producto}\n"
            f"Extremo que cambia: {fila.extremo_modificado}\n"
            f"Nuevo intervalo: [{fila.nuevo_a:.10g}, {fila.nuevo_b:.10g}]\n"
            f"Ea: {error}\n\n{criterio}"
        )
        self.biseccion_explicacion.config(text=texto)
        self._iteracion_seleccionada = fila

    def _dibujar_grafica_biseccion(self):
        canvas = getattr(self, "biseccion_canvas", None)
        if canvas is None:
            return
        canvas.delete("all")
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 80 or height < 80:
            return
        left, right, top, bottom = 54, width - 18, 18, height - 38
        selected = self._iteracion_seleccionada
        if selected:
            xmin, xmax = selected.a, selected.b
        elif self._resultado_biseccion and self._resultado_biseccion.iteraciones:
            first = self._resultado_biseccion.iteraciones[0]
            xmin, xmax = first.a, first.b
        else:
            xmin, xmax = -2.0, 2.0
        span = xmax - xmin or 1.0
        xmin -= span * 0.35
        xmax += span * 0.35

        function = self._funcion_grafica_biseccion
        points = []
        if function:
            samples = 240
            for index in range(samples + 1):
                x = xmin + (xmax - xmin) * index / samples
                try:
                    y = function.evaluar(x)
                    if abs(y) > 1e8:
                        points.append(None)
                    else:
                        points.append((x, y))
                except ValueError:
                    points.append(None)
        values = [point[1] for point in points if point is not None]
        if selected:
            values.extend((selected.fa, selected.fc))
        ymin, ymax = (min(values), max(values)) if values else (-1.0, 1.0)
        if ymin == ymax:
            ymin, ymax = ymin - 1, ymax + 1
        padding = (ymax - ymin) * 0.12
        ymin, ymax = ymin - padding, ymax + padding
        to_x = lambda x: left + (x - xmin) / (xmax - xmin) * (right - left)
        to_y = lambda y: bottom - (y - ymin) / (ymax - ymin) * (bottom - top)

        for tick in range(5):
            x = xmin + (xmax - xmin) * tick / 4
            y = ymin + (ymax - ymin) * tick / 4
            canvas.create_line(to_x(x), top, to_x(x), bottom, fill=BORDER_SUBTLE)
            canvas.create_line(left, to_y(y), right, to_y(y), fill=BORDER_SUBTLE)
            canvas.create_text(to_x(x), bottom + 15, text=f"{x:.4g}", fill=TEXT_MUTED, font=FONT_SMALL)
            canvas.create_text(left - 8, to_y(y), text=f"{y:.4g}", fill=TEXT_MUTED, font=FONT_SMALL, anchor="e")
        if ymin <= 0 <= ymax:
            canvas.create_line(left, to_y(0), right, to_y(0), fill=TEXT_MUTED, width=1)
        canvas.create_line(left, top, left, bottom, fill=TEXT_MUTED)
        canvas.create_line(left, bottom, right, bottom, fill=TEXT_MUTED)

        segment = []
        for point in points + [None]:
            if point is None:
                if len(segment) > 1:
                    coords = [coordinate for x, y in segment for coordinate in (to_x(x), to_y(y))]
                    canvas.create_line(*coords, fill=ACCENT_PRIMARY, width=2, smooth=True)
                segment = []
            else:
                segment.append(point)
        canvas.create_text(right - 4, top + 8, text="f(x)", fill=ACCENT_PRIMARY, font=FONT_SMALL_BOLD, anchor="e")

        if selected:
            for x, label, color in ((selected.a, "a", WARNING_TEXT), (selected.b, "b", WARNING_TEXT),
                                    (selected.c, "c", SUCCESS_TEXT)):
                canvas.create_line(to_x(x), top, to_x(x), bottom, fill=color, dash=(3, 3))
                try:
                    y = function.evaluar(x)
                    canvas.create_oval(to_x(x)-4, to_y(y)-4, to_x(x)+4, to_y(y)+4,
                                       fill=color, outline=BG_CARD, width=1)
                except (ValueError, TypeError):
                    pass
                canvas.create_text(to_x(x), bottom + 27, text=label, fill=color, font=FONT_SMALL_BOLD)

    def limpiar_biseccion(self):
        for atributo in ("biseccion_funcion", "biseccion_a", "biseccion_b",
                         "biseccion_error", "biseccion_max_iter"):
            entry = getattr(self, atributo)
            entry.delete(0, tk.END)
        self.biseccion_raiz.config(text="—")
        self.biseccion_error_final.config(text="—")
        self.biseccion_iteraciones_total.config(text="—")
        self.biseccion_estado.config(text="Esperando datos", fg=TEXT_MUTED)
        self._resultado_biseccion = None
        self._funcion_grafica_biseccion = None
        self._iteracion_seleccionada = None
        self.biseccion_selector["values"] = ()
        self.biseccion_selector.set("")
        for item in self.biseccion_tabla.get_children():
            self.biseccion_tabla.delete(item)
        self.biseccion_explicacion.config(text="Carga una función e intervalo para comenzar.")
        self._dibujar_grafica_biseccion()

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

    def confirmar_proceso_inversa_grande(self, n, nombre_matriz="Matriz"):
        seg = 0.0006 * (n ** 3.1)
        if seg < 1.8:
            tiempo_str = "aproximadamente 1 a 2 segundos"
        elif seg < 60:
            s_val = int(round(seg))
            tiempo_str = f"aproximadamente {s_val} a {s_val + 3} segundos"
        else:
            mins = round(seg / 60, 1)
            tiempo_str = f"aproximadamente {mins} minuto(s)"

        resultado = [False]

        dlg = tk.Toplevel(self.root)
        dlg.title("Confirmación · Matriz Grande")
        dlg.configure(bg=BG_WINDOW)
        dlg.transient(self.root)
        dlg.resizable(False, False)

        w, h = 540, 280
        self.root.update_idletasks()
        rx, ry = self.root.winfo_x(), self.root.winfo_y()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()
        x = rx + max(0, (rw - w) // 2)
        y = ry + max(0, (rh - h) // 2)
        dlg.geometry(f"{w}x{h}+{x}+{y}")

        top_bar = tk.Frame(dlg, bg=BG_CARD, height=40, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar, text=f"  ⚠ Advertencia: Cálculo de Matriz {n}×{n}",
            font=FONT_HEADING, bg=BG_CARD, fg=WARNING_TEXT
        ).pack(side=tk.LEFT, pady=8)

        body = tk.Frame(dlg, bg=BG_CARD, padx=16, pady=12, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        tk.Label(
            body,
            text=f"Ha solicitado invertir una matriz de tamaño {n}×{n} ({nombre_matriz}).\n"
                 f"El cálculo con precisión exacta requerirá transformaciones intensivas.",
            font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRIMARY, justify=tk.LEFT
        ).pack(anchor="w", pady=(0, 8))

        box_tiempo = tk.Frame(body, bg=ACCENT_SOFT, padx=10, pady=6, highlightthickness=1, highlightbackground=ACCENT_BORDER)
        box_tiempo.pack(fill=tk.X, pady=(0, 8))
        tk.Label(box_tiempo, text=f"⏱ Tiempo estimado: {tiempo_str.upper()}", font=FONT_SMALL_BOLD, bg=ACCENT_SOFT, fg=ACCENT_PRIMARY).pack(anchor="w")

        tk.Label(body, text="¿Desea continuar con el cálculo?", font=FONT_BODY, bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor="w")

        btn_bar = tk.Frame(dlg, bg=BG_WINDOW, padx=12, pady=10)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        def on_cancelar(event=None):
            resultado[0] = False
            dlg.destroy()

        def on_confirmar(event=None):
            resultado[0] = True
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", on_cancelar)
        dlg.bind("<Escape>", on_cancelar)
        dlg.bind("<Return>", on_confirmar)

        BotonSecundario(btn_bar, text="Cancelar", command=on_cancelar, font=FONT_SMALL_BOLD, padx=14, pady=6).pack(side=tk.RIGHT, padx=(8, 0))
        BotonPrimario(btn_bar, text="Confirmar y Calcular", command=on_confirmar, font=FONT_SMALL_BOLD, padx=14, pady=6).pack(side=tk.RIGHT)

        dlg.grab_set()
        self.root.wait_window(dlg)
        return resultado[0]
