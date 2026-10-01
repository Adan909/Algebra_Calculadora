import tkinter as tk
from tkinter import ttk, messagebox
from vista.componentes import ScrollableFrame
import time

# ==============================================================================
# PALETA: CONSOLA DE MISION — NEGRO ABSOLUTO + AZUL ELECTRICO
# Texto siempre en blanco puro (#FFFFFF) para maxima legibilidad.
# ==============================================================================

# Fondos
C_ROOT      = "#000000"   # Fondo raiz — negro puro
C_PANEL     = "#030912"   # Panel de contenido
C_SECTION   = "#050e1f"   # Sección / bloque de trabajo
C_INPUT     = "#020710"   # Fondo de entrada / consola
C_HEADER    = "#071428"   # Cabecera de sección

# Azules de estructura
C_BORDER    = "#0d2a52"   # Borde de elementos
C_ACCENT    = "#0055bb"   # Azul de acento (botones, divisores)
C_BRIGHT    = "#0088ff"   # Azul brillante (hover, foco)
C_GLOW      = "#00aaff"   # Azul neón (destacados, titulos de header)
C_NEON      = "#00ccff"   # Cian de alta precisión (valores críticos)

# Texto — SIEMPRE LEGIBLE
C_WHITE     = "#ffffff"   # Texto principal — blanco puro
C_SILVER    = "#c8ddf0"   # Texto secundario — blanco azulado
C_MUTED     = "#7aaaca"   # Texto terciario (aun legible)
C_CODE      = "#40d0ff"   # Valores numéricos / código

# Semántica de estado
C_OK        = "#00e87a"   # Verde osciloscopio
C_WARN      = "#ff3333"   # Rojo alarma
C_CAUTION   = "#ffaa00"   # Ámbar advertencia

# ==============================================================================
# TIPOGRAFÍA
# ==============================================================================
F_DISPLAY  = ("JetBrains Mono", 15, "bold")
F_HEADING  = ("JetBrains Mono", 11, "bold")
F_SUBHEAD  = ("JetBrains Mono", 10, "bold")
F_LABEL    = ("Courier New", 9, "bold")
F_MONO     = ("JetBrains Mono", 10)
F_MONO_B   = ("JetBrains Mono", 10, "bold")
F_MONO_LG  = ("JetBrains Mono", 12, "bold")
F_MATRIX   = ("Consolas", 11, "bold")
F_SMALL    = ("Courier New", 8)


class VentanaPrincipal:
    """
    Consola de álgebra lineal — Interfaz técnica industrial.
    Negro absoluto + azul eléctrico. Texto blanco puro en toda la UI.
    """
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("ALGEBRA COMPUTATION SYSTEM  ·  KERNEL v3.0")
        self.root.geometry("1260x900")
        self.root.minsize(1080, 800)
        self.root.configure(bg=C_ROOT)

        self.controlador = controlador
        self._op_count = 0
        self._root_fullscreen = False
        self.root.bind("<F11>", self._toggle_root_fullscreen)

        self._estilos()
        self._header()
        self._footer()
        self._body()
        self._tick()

    # ==========================================================================
    # ESTILOS TTK
    # ==========================================================================
    def _estilos(self):
        s = ttk.Style()
        s.theme_use("clam")

        # Base
        s.configure(".", background=C_PANEL, foreground=C_WHITE, font=F_LABEL)
        s.configure("TFrame", background=C_PANEL)

        # LabelFrame — no usado directamente, pero por si acaso
        s.configure("TLabelFrame", background=C_PANEL, foreground=C_WHITE,
                    bordercolor=C_BORDER, borderwidth=1, relief="solid")
        s.configure("TLabelFrame.Label", background=C_HEADER,
                    foreground=C_WHITE, font=F_LABEL, padding=(8, 2))

        # ── BOTÓN PRIMARIO ─────────────────────────────────────────────────────
        s.configure("P.TButton",
            background=C_ACCENT, foreground=C_WHITE,
            bordercolor=C_BRIGHT, borderwidth=1,
            relief="flat", font=F_MONO_B, padding=(16, 7))
        s.map("P.TButton",
            background=[("active", C_BRIGHT), ("disabled", "#0a1a30")],
            foreground=[("active", C_WHITE),  ("disabled", C_MUTED)],
            bordercolor=[("active", C_NEON)])

        # ── BOTÓN SECUNDARIO ──────────────────────────────────────────────────
        s.configure("S.TButton",
            background=C_HEADER, foreground=C_SILVER,
            bordercolor=C_BORDER, borderwidth=1,
            relief="flat", font=F_LABEL, padding=(10, 5))
        s.map("S.TButton",
            background=[("active", C_ACCENT)],
            foreground=[("active", C_WHITE)],
            bordercolor=[("active", C_BRIGHT)])

        # ── NOTEBOOK PRINCIPAL ────────────────────────────────────────────────
        s.configure("Main.TNotebook", background=C_ROOT, borderwidth=0, tabmargins=[0,0,0,0])
        s.configure("Main.TNotebook.Tab",
            background="#010a1c", foreground=C_MUTED,
            padding=[22, 10], font=F_MONO_B, borderwidth=0)
        s.map("Main.TNotebook.Tab",
            background=[("selected", C_HEADER), ("active", "#0a1e3c")],
            foreground=[("selected", C_WHITE),  ("active", C_SILVER)])

        # ── NOTEBOOK INTERNO ──────────────────────────────────────────────────
        s.configure("Sub.TNotebook", background=C_SECTION, borderwidth=0, tabmargins=[0,0,0,0])
        s.configure("Sub.TNotebook.Tab",
            background=C_PANEL, foreground=C_MUTED,
            padding=[14, 6], font=F_LABEL, borderwidth=0)
        s.map("Sub.TNotebook.Tab",
            background=[("selected", C_ACCENT), ("active", "#0a1e3c")],
            foreground=[("selected", C_WHITE),  ("active", C_SILVER)])

        # ── COMBOBOX ──────────────────────────────────────────────────────────
        s.configure("TCombobox",
            fieldbackground=C_INPUT, background=C_HEADER,
            foreground=C_WHITE, arrowcolor=C_GLOW,
            bordercolor=C_BORDER, insertcolor=C_NEON, padding=(6, 4))
        s.map("TCombobox",
            fieldbackground=[("readonly", C_INPUT)],
            foreground=[("readonly", C_WHITE)],
            bordercolor=[("focus", C_GLOW)])

        # ── SPINBOX ───────────────────────────────────────────────────────────
        s.configure("TSpinbox",
            fieldbackground=C_INPUT, background=C_HEADER,
            foreground=C_WHITE, arrowcolor=C_GLOW,
            bordercolor=C_BORDER, insertcolor=C_NEON, padding=(6, 4))
        s.map("TSpinbox", bordercolor=[("focus", C_GLOW)])

        # ── SCROLLBAR ─────────────────────────────────────────────────────────
        s.configure("TScrollbar",
            background=C_HEADER, troughcolor=C_ROOT,
            bordercolor=C_ROOT, arrowcolor=C_ACCENT,
            relief="flat", gripcount=0)
        s.map("TScrollbar", background=[("active", C_BRIGHT)])

        # ── LABEL ─────────────────────────────────────────────────────────────
        s.configure("TLabel", background=C_SECTION, foreground=C_WHITE, font=F_LABEL)

    # ==========================================================================
    # HEADER
    # ==========================================================================
    def _header(self):
        # Barra superior
        bar = tk.Frame(self.root, bg="#030e20", height=58)
        bar.pack(fill=tk.X, side=tk.TOP)
        bar.pack_propagate(False)

        # Marcador de identidad izquierdo
        marker = tk.Frame(bar, bg=C_NEON, width=5)
        marker.pack(side=tk.LEFT, fill=tk.Y)

        left = tk.Frame(bar, bg="#030e20")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(14, 0))

        tk.Label(left, text="ALGEBRA COMPUTATION ENGINE",
                 font=F_DISPLAY, bg="#030e20", fg=C_WHITE).pack(anchor="w", pady=(8, 0))
        tk.Label(left, text="KERNEL v3.0  ·  PRECISION RACIONAL EXACTA  ·  ESPACIO R^n",
                 font=F_SMALL, bg="#030e20", fg=C_MUTED).pack(anchor="w")

        # Bloque derecho — reloj y estado
        right = tk.Frame(bar, bg="#030e20")
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        self.lbl_clock = tk.Label(right, text="--:--:--",
                                   font=F_HEADING, bg="#030e20", fg=C_GLOW)
        self.lbl_clock.pack(anchor="e", pady=(10, 2))

        tk.Label(right, text="MOTOR ACTIVO",
                 font=F_SMALL, bg="#030e20", fg=C_OK).pack(anchor="e")

        # Líneas decorativas de separación
        tk.Frame(self.root, bg=C_NEON, height=2).pack(fill=tk.X, side=tk.TOP)
        tk.Frame(self.root, bg=C_ACCENT, height=1).pack(fill=tk.X, side=tk.TOP)

    # ==========================================================================
    # FOOTER
    # ==========================================================================
    def _footer(self):
        tk.Frame(self.root, bg=C_BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)

        foot = tk.Frame(self.root, bg="#020b18", height=28)
        foot.pack(fill=tk.X, side=tk.BOTTOM)
        foot.pack_propagate(False)

        tk.Frame(foot, bg=C_OK, width=4).pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(foot, text="  ● SISTEMA ACTIVO",
                 font=F_SMALL, bg="#020b18", fg=C_OK).pack(side=tk.LEFT, pady=6)

        tk.Label(foot, text="  |  GAUSS-JORDAN  |  VECTORES R^n  |  BASES NUMERICAS  |  NUMEROS ROMANOS",
                 font=F_SMALL, bg="#020b18", fg=C_MUTED).pack(side=tk.LEFT, pady=6)

        self.lbl_op_count = tk.Label(foot, text="OPS: 0",
                                      font=F_LABEL, bg="#020b18", fg=C_SILVER)
        self.lbl_op_count.pack(side=tk.RIGHT, padx=16)

    # ==========================================================================
    # BODY — Notebook principal
    # ==========================================================================
    def _body(self):
        container = tk.Frame(self.root, bg=C_ROOT)
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.nb_main = ttk.Notebook(container, style="Main.TNotebook")
        self.nb_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=(8, 6))

        self.tab_gauss     = ttk.Frame(self.nb_main, style="TFrame", padding="14")
        self.tab_vectorial = ttk.Frame(self.nb_main, style="TFrame", padding="14")
        self.tab_conv      = ttk.Frame(self.nb_main, style="TFrame", padding="14")
        self.tab_romanos   = ttk.Frame(self.nb_main, style="TFrame", padding="14")

        self.nb_main.add(self.tab_gauss,     text="  GAUSS-JORDAN  ")
        self.nb_main.add(self.tab_vectorial, text="  VECTORIAL & MATRICES  ")
        self.nb_main.add(self.tab_conv,      text="  CONVERSION DE BASES  ")
        self.nb_main.add(self.tab_romanos,   text="  NUMEROS ROMANOS  ")

        self._build_gauss()
        self._build_vectorial()
        self._build_conv()
        self._build_romanos()

    # ==========================================================================
    # HELPERS
    # ==========================================================================
    def _bloque(self, parent, titulo, color_acento=C_ACCENT, **pack_kw):
        """
        Bloque de sección con barra de título técnica horizontal.
        Sin card flotante. Sin esquinas redondeadas. Sin sombra.
        """
        wrap = tk.Frame(parent, bg=C_SECTION, highlightthickness=1,
                        highlightbackground=C_BORDER)
        wrap.pack(**pack_kw)

        # Barra de título
        bar = tk.Frame(wrap, bg=C_HEADER, height=28)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        tk.Frame(bar, bg=color_acento, width=4).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(bar, text=f"  {titulo}",
                 font=F_LABEL, bg=C_HEADER, fg=C_WHITE).pack(side=tk.LEFT, padx=4, pady=4)

        # Línea separadora
        tk.Frame(wrap, bg=C_BORDER, height=1).pack(fill=tk.X)

        inner = tk.Frame(wrap, bg=C_SECTION, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        wrap.bar = bar
        return wrap, inner

    def _conectar_consola_fullscreen(self, widget_text, titulo, bar=None, proveedor_texto=None):
        """
        Conecta un widget de consola a la funcionalidad universal de pantalla completa:
        - Agrega botón '⛶ PANTALLA COMPLETA' en la barra de cabecera si se proporciona.
        - Asocia doble clic en la consola para abrir en pantalla completa.
        - Agrega menú contextual de clic derecho (Abrir en pantalla completa, Copiar todo).
        """
        target = proveedor_texto if proveedor_texto is not None else widget_text

        if bar is not None:
            btn_fs = tk.Button(
                bar, text=" ⛶ PANTALLA COMPLETA ", font=F_SMALL,
                bg="#061a36", fg=C_NEON, activebackground=C_ACCENT,
                activeforeground=C_WHITE, bd=0, relief="flat",
                cursor="hand2", padx=8, pady=1,
                command=lambda: self.abrir_consola_fullscreen(titulo, target)
            )
            btn_fs.pack(side=tk.RIGHT, padx=6, pady=2)

        # Doble clic sobre el texto de la consola
        widget_text.bind(
            "<Double-Button-1>",
            lambda e: self.abrir_consola_fullscreen(titulo, target)
        )

        # Menú contextual con clic derecho
        menu = tk.Menu(widget_text, tearoff=0, bg=C_HEADER, fg=C_WHITE,
                       activebackground=C_ACCENT, activeforeground=C_WHITE,
                       font=F_LABEL, bd=1, relief="solid")
        menu.add_command(
            label="  ⛶  Abrir en Pantalla Completa",
            command=lambda: self.abrir_consola_fullscreen(titulo, target)
        )
        menu.add_separator()
        def copiar():
            texto = widget_text.get("1.0", tk.END).strip()
            if texto:
                self.root.clipboard_clear()
                self.root.clipboard_append(texto)
        menu.add_command(label="  📋  Copiar Todo", command=copiar)

        def popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        widget_text.bind("<Button-3>", popup)

    def abrir_consola_fullscreen(self, titulo, widget_origen):
        """
        Abre una ventana emergente en pantalla completa técnica industrial.
        Permite zoom con teclado o ratón, copiar al portapapeles, refrescar,
        alternar pantalla completa pura con F11 o botón, y cerrar con ESC.
        """
        ventana_fs = tk.Toplevel(self.root)
        ventana_fs.title(f"CONSOLA EN PANTALLA COMPLETA · {titulo.upper()}")
        ventana_fs.configure(bg=C_ROOT)

        es_fullscreen = [True]
        try:
            ventana_fs.attributes("-fullscreen", True)
        except Exception:
            pass

        tamano_fuente = [12]

        def actualizar_fuente():
            txt_fs.config(font=("JetBrains Mono", tamano_fuente[0]))

        def zoom_in(event=None):
            if tamano_fuente[0] < 28:
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
                text=" 🗗 RESTAURAR (F11) " if es_fullscreen[0] else " ⛶ PANTALLA COMPLETA (F11) "
            )

        def copiar_todo(event=None):
            contenido = txt_fs.get("1.0", tk.END).strip()
            if contenido:
                self.root.clipboard_clear()
                self.root.clipboard_append(contenido)
                lbl_copiado.config(text="✔ COPIADO AL PORTAPAPELES", fg=C_OK)
                ventana_fs.after(2500, lambda: lbl_copiado.config(text=""))

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
                texto = "[ CONSOLA VACÍA — NO SE HA GENERADO NINGÚN RESULTADO AÚN ]"
            txt_fs.insert(tk.END, texto)
            txt_fs.config(state=tk.NORMAL)

        # ── Barra superior técnica ───────────────────────────────────────────
        top_bar = tk.Frame(ventana_fs, bg=C_HEADER, height=44)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        tk.Frame(ventana_fs, bg=C_NEON, height=2).pack(fill=tk.X, side=tk.TOP)

        # Lado izquierdo: indicador y título
        left_box = tk.Frame(top_bar, bg=C_HEADER)
        left_box.pack(side=tk.LEFT, fill=tk.Y, padx=14)

        tk.Label(
            left_box, text="● MODO PANTALLA COMPLETA  ┃ ",
            font=("JetBrains Mono", 10, "bold"), bg=C_HEADER, fg=C_OK
        ).pack(side=tk.LEFT)

        tk.Label(
            left_box, text=titulo.upper(),
            font=("JetBrains Mono", 11, "bold"), bg=C_HEADER, fg=C_WHITE
        ).pack(side=tk.LEFT)

        lbl_copiado = tk.Label(
            left_box, text="", font=F_SMALL, bg=C_HEADER, fg=C_OK
        )
        lbl_copiado.pack(side=tk.LEFT, padx=12)

        # Lado derecho: Botones de control
        right_box = tk.Frame(top_bar, bg=C_HEADER)
        right_box.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Botones de Zoom
        tk.Button(
            right_box, text=" A − ", font=F_MONO_B,
            bg="#061833", fg=C_SILVER, activebackground=C_ACCENT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=6, pady=4, command=zoom_out
        ).pack(side=tk.LEFT, padx=2, pady=6)

        tk.Button(
            right_box, text=" A + ", font=F_MONO_B,
            bg="#061833", fg=C_SILVER, activebackground=C_ACCENT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=6, pady=4, command=zoom_in
        ).pack(side=tk.LEFT, padx=2, pady=6)

        # Botón Copiar
        tk.Button(
            right_box, text=" 📋 COPIAR TODO ", font=F_MONO_B,
            bg="#062244", fg=C_NEON, activebackground=C_BRIGHT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=10, pady=4, command=copiar_todo
        ).pack(side=tk.LEFT, padx=4, pady=6)

        # Botón Recargar
        tk.Button(
            right_box, text=" ⟳ REFRESCAR ", font=F_MONO_B,
            bg="#061833", fg=C_SILVER, activebackground=C_ACCENT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=8, pady=4, command=recargar_contenido
        ).pack(side=tk.LEFT, padx=4, pady=6)

        # Botón Toggle Fullscreen
        btn_toggle_fs = tk.Button(
            right_box, text=" 🗗 RESTAURAR (F11) ", font=F_MONO_B,
            bg="#061833", fg=C_SILVER, activebackground=C_ACCENT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=8, pady=4, command=toggle_fullscreen
        )
        btn_toggle_fs.pack(side=tk.LEFT, padx=4, pady=6)

        # Botón Cerrar
        tk.Button(
            right_box, text=" ✕ CERRAR (ESC) ", font=F_MONO_B,
            bg="#380505", fg="#ff8888", activebackground="#aa1111", activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=12, pady=4, command=ventana_fs.destroy
        ).pack(side=tk.LEFT, padx=(6, 2), pady=6)

        # ── Cuerpo: Área de texto con scrollbars ──────────────────────────────
        body_frame = tk.Frame(ventana_fs, bg=C_ROOT, padx=12, pady=10)
        body_frame.pack(fill=tk.BOTH, expand=True)

        txt_fs = tk.Text(
            body_frame, font=("JetBrains Mono", tamano_fuente[0]),
            bg=C_INPUT, fg=C_WHITE, insertbackground=C_NEON,
            selectbackground=C_ACCENT, selectforeground=C_WHITE,
            relief="flat", bd=0, wrap=tk.NONE,
            highlightthickness=1, highlightbackground=C_BORDER,
            highlightcolor=C_GLOW
        )
        sc_y = ttk.Scrollbar(body_frame, orient="vertical", command=txt_fs.yview)
        sc_x = ttk.Scrollbar(body_frame, orient="horizontal", command=txt_fs.xview)
        txt_fs.configure(yscrollcommand=sc_y.set, xscrollcommand=sc_x.set)

        txt_fs.grid(row=0, column=0, sticky="nsew")
        sc_y.grid(row=0, column=1, sticky="ns")
        sc_x.grid(row=1, column=0, sticky="ew")

        body_frame.grid_rowconfigure(0, weight=1)
        body_frame.grid_columnconfigure(0, weight=1)

        # ── Footer informativo ────────────────────────────────────────────────
        footer = tk.Frame(ventana_fs, bg="#020b18", height=24)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="  [ESC] Cerrar  ·  [F11] Pantalla Completa  ·  [Ctrl + C] Copiar  ·  [Ctrl + Rueda / A+, A-] Zoom",
            font=F_SMALL, bg="#020b18", fg=C_MUTED
        ).pack(side=tk.LEFT, padx=10, pady=3)

        recargar_contenido()

        ventana_fs.bind("<Escape>", lambda e: ventana_fs.destroy())
        ventana_fs.bind("<F11>", toggle_fullscreen)
        ventana_fs.bind("<Control-plus>", zoom_in)
        ventana_fs.bind("<Control-minus>", zoom_out)
        ventana_fs.bind("<Control-equal>", zoom_in)
        ventana_fs.bind("<Control-Button-4>", lambda e: zoom_in())
        ventana_fs.bind("<Control-Button-5>", lambda e: zoom_out())
        ventana_fs.focus_set()

    def _obtener_resumen_gauss_texto(self):
        clasif = self.lbl_clasificacion.cget("text")
        sol = self.txt_solucion.get("1.0", tk.END).strip()
        ver = self.txt_verificacion.get("1.0", tk.END).strip()
        hist = self.txt_historial.get("1.0", tk.END).strip()

        lineas = []
        lineas.append("================================================================================")
        lineas.append(f"  {clasif}")
        lineas.append("================================================================================\n")
        lineas.append("── VECTOR DE SOLUCIÓN ──────────────────────────────────────────────────────────")
        lineas.append(sol if sol else "[ Sin solución calculada ]")
        lineas.append("\n── COMPROBACIÓN EN ECUACIONES ORIGINALES ───────────────────────────────────────")
        lineas.append(ver if ver else "[ Sin comprobación calculada ]")
        if hist:
            lineas.append("\n── HISTORIAL DE PIVOTEO PASO A PASO ────────────────────────────────────────────")
            lineas.append(hist)
        return "\n".join(lineas)

    def _obtener_resumen_romanos_texto(self):
        r_rom = self.lbl_res_romano.cget("text")
        r_ara = self.lbl_res_normal.cget("text")
        desglose = self.txt_rom_desglose.get("1.0", tk.END).strip()
        lineas = []
        lineas.append("================================================================================")
        lineas.append(f"  RESULTADO EN NÚMEROS ROMANOS:  {r_rom}")
        lineas.append(f"  RESULTADO EN SISTEMA ÁRABE:   {r_ara}")
        lineas.append("================================================================================\n")
        lineas.append("── DESGLOSE Y PROCEDIMIENTO DETALLADO ──────────────────────────────────────────")
        lineas.append(desglose if desglose else "[ Sin cálculo de números romanos registrado aún ]")
        return "\n".join(lineas)

    def _toggle_root_fullscreen(self, event=None):
        self._root_fullscreen = not getattr(self, "_root_fullscreen", False)
        try:
            self.root.attributes("-fullscreen", self._root_fullscreen)
        except Exception:
            pass

    def _lbl(self, parent, text, color=C_WHITE, font=F_LABEL, **kw):
        return tk.Label(parent, text=text, font=font, bg=C_SECTION, fg=color, **kw)

    def _lbl_p(self, parent, text, color=C_WHITE, font=F_LABEL, **kw):
        """Label sobre fondo de panel (C_PANEL)"""
        return tk.Label(parent, text=text, font=font, bg=C_PANEL, fg=color, **kw)

    def _lbl_h(self, parent, text, color=C_WHITE, font=F_LABEL, **kw):
        """Label sobre fondo de header (C_HEADER)"""
        return tk.Label(parent, text=text, font=font, bg=C_HEADER, fg=color, **kw)

    def _entry(self, parent, width=8, bg=C_INPUT, hbg=C_BORDER, **kw):
        return tk.Entry(parent, width=width, font=F_MATRIX, justify="center",
                        bg=bg, fg=C_WHITE, insertbackground=C_NEON,
                        relief="flat", bd=0,
                        highlightthickness=1, highlightbackground=hbg,
                        highlightcolor=C_GLOW, **kw)

    def _console(self, parent, height=12, wrap=tk.WORD, **kw):
        return tk.Text(parent, height=height, font=F_MONO,
                       bg=C_INPUT, fg=C_WHITE,
                       insertbackground=C_NEON,
                       selectbackground=C_ACCENT, selectforeground=C_WHITE,
                       relief="flat", bd=0,
                       highlightthickness=1, highlightbackground=C_BORDER,
                       highlightcolor=C_GLOW,
                       state=tk.DISABLED, wrap=wrap, **kw)

    def _sep(self, parent, pady=4, color=C_BORDER):
        tk.Frame(parent, bg=color, height=1).pack(fill=tk.X, pady=pady)

    def _write(self, widget, texto):
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, texto)
        widget.config(state=tk.DISABLED)

    def _ops(self):
        self._op_count += 1
        self.lbl_op_count.config(text=f"OPS: {self._op_count}")

    def _tick(self):
        self.lbl_clock.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self._tick)

    # ==========================================================================
    # MÓDULO 1 — GAUSS-JORDAN
    # Layout: [Configuracion arriba] [Matriz + Botón centro] [Resultados abajo]
    # ==========================================================================
    def _build_gauss(self):
        parent = self.tab_gauss

        # ── Fila superior: Config + Ejemplos ──────────────────────────────────
        top = tk.Frame(parent, bg=C_PANEL)
        top.pack(fill=tk.X, pady=(0, 8))

        # Bloque: Configuración del sistema
        _, cfg = self._bloque(top, "CONFIGURACION DEL SISTEMA",
                              side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        row1 = tk.Frame(cfg, bg=C_SECTION)
        row1.pack(fill=tk.X, pady=(0, 4))

        self._lbl(row1, "FILAS m :").pack(side=tk.LEFT, padx=(0, 4))
        self.spin_m = ttk.Spinbox(row1, from_=1, to=10, width=5)
        self.spin_m.set(3)
        self.spin_m.pack(side=tk.LEFT, padx=(0, 14))

        self._lbl(row1, "COLUMNAS n :").pack(side=tk.LEFT, padx=(0, 4))
        self.spin_n = ttk.Spinbox(row1, from_=1, to=10, width=5)
        self.spin_n.set(3)
        self.spin_n.pack(side=tk.LEFT, padx=(0, 14))

        ttk.Button(row1, text="GENERAR CUADRICULA", style="P.TButton",
                   command=self.controlador.generar_cuadricula).pack(side=tk.LEFT)

        row2 = tk.Frame(cfg, bg=C_SECTION)
        row2.pack(fill=tk.X, pady=(4, 0))

        self._lbl(row2, "ALGORITMO :").pack(side=tk.LEFT, padx=(0, 4))
        self.metodo = tk.StringVar(value="Gauss")
        self.selector_metodo = ttk.Combobox(row2, textvariable=self.metodo,
                                             values=("Gauss", "Gauss-Jordan"),
                                             state="readonly", width=15)
        self.selector_metodo.pack(side=tk.LEFT, padx=(0, 0))

        # Bloque: Ejemplos precargados
        _, ej = self._bloque(top, "SISTEMAS PRECARGADOS",
                             color_acento=C_GLOW,
                             side=tk.RIGHT, fill=tk.Y)

        for label, tipo, color in [
            ("SOLUCION UNICA",      "unica",        C_OK),
            ("INFINITAS SOLUCIONES","infinitas",    C_CAUTION),
            ("INCONSISTENTE",       "inconsistente", C_WARN),
            ("INVERSA DE MATRIZ",   "inversa",      C_NEON),
        ]:
            btn_frame = tk.Frame(ej, bg=C_SECTION)
            btn_frame.pack(fill=tk.X, pady=2)
            tk.Frame(btn_frame, bg=color, width=3).pack(side=tk.LEFT, fill=tk.Y)
            ttk.Button(btn_frame, text=f"  {label}", style="S.TButton",
                       command=lambda t=tipo: self.controlador.cargar_ejemplo(t)
                       ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ── Centro: Matriz aumentada ──────────────────────────────────────────
        _, mat = self._bloque(parent, "MATRIZ AUMENTADA   [ A | b ]",
                              fill=tk.X, expand=False, pady=(0, 8))

        self.scroll_matriz = ScrollableFrame(mat, bg_color=C_SECTION)
        self.scroll_matriz.pack(fill=tk.BOTH, expand=True)
        self.matriz_entries = []
        self.vector_entries = []

        self.btn_resolver = ttk.Button(mat,
            text="  ▶  EJECUTAR ELIMINACION  —  RESOLVER SISTEMA  ",
            style="P.TButton", state=tk.DISABLED,
            command=self.controlador.resolver_sistema)
        self.btn_resolver.pack(pady=(10, 2))

        # ── Abajo: Resultados ─────────────────────────────────────────────────
        wrap_res, res = self._bloque(parent, "RESULTADOS", fill=tk.BOTH, expand=True)

        # Botón de informe completo a pantalla completa en la barra del bloque
        btn_fs_gauss = tk.Button(
            wrap_res.bar, text=" ⛶ PANTALLA COMPLETA ", font=F_SMALL,
            bg="#061a36", fg=C_NEON, activebackground=C_ACCENT,
            activeforeground=C_WHITE, bd=0, relief="flat", cursor="hand2", padx=8, pady=1,
            command=lambda: self.abrir_consola_fullscreen(
                "GAUSS-JORDAN · INFORME COMPLETO",
                self._obtener_resumen_gauss_texto
            )
        )
        btn_fs_gauss.pack(side=tk.RIGHT, padx=6, pady=2)

        nb = ttk.Notebook(res, style="Sub.TNotebook")
        nb.pack(fill=tk.BOTH, expand=True)

        # Pestaña: Diagnóstico
        t_diag = ttk.Frame(nb, padding="10")
        nb.add(t_diag, text="  DIAGNOSTICO & SOLUCION  ")

        self.lbl_clasificacion = tk.Label(
            t_diag, text="CLASIFICACION :  —",
            font=F_SUBHEAD, bg=C_SECTION, fg=C_MUTED)
        self.lbl_clasificacion.pack(anchor="w", pady=(0, 8))

        # Layout de 2 columnas para solucion + verificacion
        cols = tk.Frame(t_diag, bg=C_SECTION)
        cols.pack(fill=tk.BOTH, expand=True)

        col_l = tk.Frame(cols, bg=C_SECTION)
        col_l.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        col_r = tk.Frame(cols, bg=C_SECTION)
        col_r.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        bar_l = tk.Frame(col_l, bg=C_SECTION)
        bar_l.pack(fill=tk.X, pady=(0, 4))
        tk.Label(bar_l, text="VECTOR SOLUCION:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT)
        self.txt_solucion = self._console(col_l, height=8)
        self.txt_solucion.pack(fill=tk.BOTH, expand=True)
        self._conectar_consola_fullscreen(self.txt_solucion, "GAUSS-JORDAN · VECTOR SOLUCIÓN", bar_l)

        bar_r = tk.Frame(col_r, bg=C_SECTION)
        bar_r.pack(fill=tk.X, pady=(0, 4))
        tk.Label(bar_r, text="COMPROBACION EN ECUACIONES ORIGINALES:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT)
        self.txt_verificacion = self._console(col_r, height=8)
        self.txt_verificacion.pack(fill=tk.BOTH, expand=True)
        self._conectar_consola_fullscreen(self.txt_verificacion, "GAUSS-JORDAN · COMPROBACIÓN", bar_r)

        # Pestaña: Historial
        t_hist = ttk.Frame(nb, padding="10")
        nb.add(t_hist, text="  HISTORIAL DE PIVOTEO PASO A PASO  ")

        bar_h = tk.Frame(t_hist, bg=C_SECTION)
        bar_h.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        tk.Label(bar_h, text="HISTORIAL DE PIVOTEO (DOBLE CLIC PARA PANTALLA COMPLETA):",
                 font=F_LABEL, bg=C_SECTION, fg=C_MUTED).pack(side=tk.LEFT)

        self.txt_historial = self._console(t_hist, height=18, wrap=tk.NONE)
        sc_y = ttk.Scrollbar(t_hist, orient="vertical", command=self.txt_historial.yview)
        sc_x = ttk.Scrollbar(t_hist, orient="horizontal", command=self.txt_historial.xview)
        self.txt_historial.configure(yscrollcommand=sc_y.set, xscrollcommand=sc_x.set)
        self.txt_historial.grid(row=1, column=0, sticky="nsew")
        sc_y.grid(row=1, column=1, sticky="ns")
        sc_x.grid(row=2, column=0, sticky="ew")
        t_hist.grid_rowconfigure(1, weight=1)
        t_hist.grid_columnconfigure(0, weight=1)

        self._conectar_consola_fullscreen(self.txt_historial, "GAUSS-JORDAN · HISTORIAL DE PIVOTEO", bar_h)

    def construir_cuadricula(self, m, n):
        for w in self.scroll_matriz.scrollable_frame.winfo_children():
            w.destroy()
        self.matriz_entries = []
        self.vector_entries = []
        c = self.scroll_matriz.scrollable_frame

        # Headers
        tk.Label(c, text="Coeficientes  A", font=F_LABEL, bg=C_SECTION, fg=C_GLOW
                 ).grid(row=0, column=1, columnspan=n, pady=(0, 6))
        tk.Label(c, text="┃", font=("Consolas", 14), bg=C_SECTION, fg=C_ACCENT
                 ).grid(row=0, column=n+1, padx=4)
        tk.Label(c, text="b", font=F_LABEL, bg=C_SECTION, fg=C_NEON
                 ).grid(row=0, column=n+2, padx=(8, 0), pady=(0, 6))

        for i in range(m):
            tk.Label(c, text=f"R{i+1}", font=F_LABEL, bg=C_SECTION, fg=C_MUTED
                     ).grid(row=i+1, column=0, padx=(0, 6))
            fila = []
            for j in range(n):
                e = self._entry(c, width=8)
                e.grid(row=i+1, column=j+1, padx=3, pady=4)
                e.insert(0, "0")
                fila.append(e)
            self.matriz_entries.append(fila)

            tk.Label(c, text="┃", font=("Consolas", 14), bg=C_SECTION, fg=C_ACCENT
                     ).grid(row=i+1, column=n+1, padx=4)

            eb = self._entry(c, width=8, bg="#040d20", hbg=C_BRIGHT)
            eb.grid(row=i+1, column=n+2, padx=(4, 2), pady=4)
            eb.insert(0, "0")
            self.vector_entries.append(eb)

        self.btn_resolver.config(state=tk.NORMAL)

    def actualizar_resumen(self, clasificacion, solucion_texto, verificacion_texto):
        es_unica = "Única" in clasificacion
        es_inf   = "Infinitas" in clasificacion
        color = C_OK if es_unica else (C_CAUTION if es_inf else C_WARN)
        self.lbl_clasificacion.config(
            text=f"CLASIFICACION  :  {clasificacion.upper()}",
            fg=color
        )
        self._write(self.txt_solucion, solucion_texto)
        self._write(self.txt_verificacion, verificacion_texto)
        self._ops()

    def actualizar_historial(self, h):
        self._write(self.txt_historial, h)

    # ==========================================================================
    # MÓDULO 2 — VECTORIAL & MATRICIAL
    # ==========================================================================
    def _build_vectorial(self):
        self.nb_vectorial = ttk.Notebook(self.tab_vectorial, style="Sub.TNotebook")
        self.nb_vectorial.pack(fill=tk.BOTH, expand=True)

        # ── Sub-tab: Vectores ─────────────────────────────────────────────────
        tv = ttk.Frame(self.nb_vectorial, padding="12")
        self.nb_vectorial.add(tv, text="  VECTORES EN R^n  ")

        _, cfg_v = self._bloque(tv, "CONFIGURACION", fill=tk.X, pady=(0, 8))

        row_v = tk.Frame(cfg_v, bg=C_SECTION)
        row_v.pack(fill=tk.X)

        for lbl, attr, default in [("DIMENSION n:", "spin_dim_v", 3), ("CANTIDAD k:", "spin_cant_v", 2)]:
            tk.Label(row_v, text=lbl, font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 4))
            sp = ttk.Spinbox(row_v, from_=1, to=10, width=5)
            sp.set(default)
            sp.pack(side=tk.LEFT, padx=(0, 14))
            setattr(self, attr, sp)

        ttk.Button(row_v, text="GENERAR ENTRADAS", style="P.TButton",
                   command=self.controlador.generar_vectores).pack(side=tk.LEFT, padx=(0, 16))

        tk.Label(row_v, text="ESCALAR c:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 4))
        self.entrada_escalar_vector = self._entry(row_v, width=7)
        self.entrada_escalar_vector.insert(0, "1")
        self.entrada_escalar_vector.pack(side=tk.LEFT)

        self.scroll_vectores = ScrollableFrame(tv, bg_color=C_SECTION)
        self.scroll_vectores.pack(fill=tk.BOTH, expand=True, pady=8)
        self.vec_entries   = []
        self.vec_b_entries = []

        ttk.Button(tv, text="  ▶  CALCULAR OPERACIONES  —  VERIFICAR COMBINACION LINEAL  ",
                   style="P.TButton",
                   command=self.controlador.operar_vectores).pack(pady=(0, 6))

        wrap_v, res_v = self._bloque(tv, "RESULTADO", fill=tk.BOTH, expand=True)
        frame_txt_v = tk.Frame(res_v, bg=C_SECTION)
        frame_txt_v.pack(fill=tk.BOTH, expand=True)
        self.txt_res_vectores = self._console(frame_txt_v, height=14)
        sc_v = ttk.Scrollbar(frame_txt_v, orient="vertical", command=self.txt_res_vectores.yview)
        self.txt_res_vectores.configure(yscrollcommand=sc_v.set)
        self.txt_res_vectores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_v.pack(side=tk.RIGHT, fill=tk.Y)
        self._conectar_consola_fullscreen(self.txt_res_vectores, "OPERACIONES VECTORIALES & COMBINACIÓN LINEAL", wrap_v.bar)

        # ── Sub-tab: Álgebra Matricial ────────────────────────────────────────
        tm = ttk.Frame(self.nb_vectorial, padding="12")
        self.tab_sub_matrices = tm
        self.nb_vectorial.add(tm, text="  ALGEBRA MATRICIAL  ( A+B, A-B, A×B, A⁻¹ )  ")

        _, cfg_m = self._bloque(tm, "DIMENSIONES DE MATRICES", fill=tk.X, pady=(0, 8))

        row_m = tk.Frame(cfg_m, bg=C_SECTION)
        row_m.pack(fill=tk.X)

        tk.Label(row_m, text="MATRIZ A ( f × c ):", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_fa = ttk.Spinbox(row_m, from_=1, to=100, width=4); self.spin_fa.set(2); self.spin_fa.pack(side=tk.LEFT, padx=2)
        self.spin_ca = ttk.Spinbox(row_m, from_=1, to=100, width=4); self.spin_ca.set(2); self.spin_ca.pack(side=tk.LEFT, padx=(2, 16))

        tk.Label(row_m, text="MATRIZ B ( f × c ):", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 4))
        self.spin_fb = ttk.Spinbox(row_m, from_=1, to=100, width=4); self.spin_fb.set(2); self.spin_fb.pack(side=tk.LEFT, padx=2)
        self.spin_cb = ttk.Spinbox(row_m, from_=1, to=100, width=4); self.spin_cb.set(2); self.spin_cb.pack(side=tk.LEFT, padx=(2, 16))

        ttk.Button(row_m, text="GENERAR MATRICES", style="P.TButton",
                   command=self.controlador.generar_matrices_ops).pack(side=tk.LEFT)

        # Fila de ejemplos precargados para matrices
        row_ej = tk.Frame(cfg_m, bg=C_SECTION)
        row_ej.pack(fill=tk.X, pady=(8, 0))
        tk.Label(row_ej, text="EJEMPLOS INVERSA:", font=F_LABEL, bg=C_SECTION, fg=C_GLOW).pack(side=tk.LEFT, padx=(0, 8))
        for lbl, tipo in [
            ("EJEMPLO 2×2", "inv_2x2"),
            ("EJEMPLO 3×3", "inv_3x3"),
            ("MATRIZ SINGULAR (NO INVERTIBLE)", "inv_singular"),
        ]:
            ttk.Button(row_ej, text=lbl, style="S.TButton",
                       command=lambda t=tipo: self.controlador.cargar_ejemplo_matrices(t)).pack(side=tk.LEFT, padx=(0, 6))

        self.scroll_matrices_ops = ScrollableFrame(tm, bg_color=C_SECTION)
        self.scroll_matrices_ops.pack(fill=tk.BOTH, expand=True, pady=8)
        self.mat_entries_a = []
        self.mat_entries_b = []

        # Controles de operación
        _, ops = self._bloque(tm, "OPERACIONES", fill=tk.X, pady=(0, 6))
        ctrl = tk.Frame(ops, bg=C_SECTION)
        ctrl.pack(fill=tk.X)

        for txt, op in [("A + B", "suma"), ("A − B", "resta"), ("A × B", "multiplicacion")]:
            ttk.Button(ctrl, text=txt, style="P.TButton",
                       command=lambda o=op: self.controlador.operar_matrices(o)).pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(ctrl, text="  ESCALAR c:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(8, 4))
        self.entrada_escalar_mat = self._entry(ctrl, width=6)
        self.entrada_escalar_mat.insert(0, "2")
        self.entrada_escalar_mat.pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(ctrl, text="c × A", style="S.TButton",
                   command=lambda: self.controlador.operar_matrices("escalar")).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(ctrl, text="A⁻¹ (INVERSA A)", style="P.TButton",
                   command=lambda: self.controlador.operar_matrices("inversa_a")).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(ctrl, text="B⁻¹ (INVERSA B)", style="S.TButton",
                   command=lambda: self.controlador.operar_matrices("inversa_b")).pack(side=tk.LEFT)

        wrap_m, res_m = self._bloque(tm, "RESULTADO", fill=tk.BOTH, expand=True)
        frame_txt_m = tk.Frame(res_m, bg=C_SECTION)
        frame_txt_m.pack(fill=tk.BOTH, expand=True)
        self.txt_res_matrices = self._console(frame_txt_m, height=18, wrap=tk.NONE)
        sc_my = ttk.Scrollbar(frame_txt_m, orient="vertical", command=self.txt_res_matrices.yview)
        sc_mx = ttk.Scrollbar(frame_txt_m, orient="horizontal", command=self.txt_res_matrices.xview)
        self.txt_res_matrices.configure(yscrollcommand=sc_my.set, xscrollcommand=sc_mx.set)
        self.txt_res_matrices.grid(row=0, column=0, sticky="nsew")
        sc_my.grid(row=0, column=1, sticky="ns")
        sc_mx.grid(row=1, column=0, sticky="ew")
        frame_txt_m.grid_rowconfigure(0, weight=1)
        frame_txt_m.grid_columnconfigure(0, weight=1)
        self._conectar_consola_fullscreen(self.txt_res_matrices, "ÁLGEBRA MATRICIAL & MATRIZ INVERSA", wrap_m.bar)

    def construir_vectores(self, n, k):
        for w in self.scroll_vectores.scrollable_frame.winfo_children():
            w.destroy()
        self.vec_entries   = []
        self.vec_b_entries = []
        c = self.scroll_vectores.scrollable_frame

        for i in range(k):
            tk.Label(c, text=f"v{i+1}", font=F_LABEL, bg=C_SECTION, fg=C_GLOW).grid(row=i, column=0, padx=6, pady=4)
            tk.Label(c, text="(", font=("Consolas", 13), bg=C_SECTION, fg=C_ACCENT).grid(row=i, column=1)
            fila = []
            for j in range(n):
                e = self._entry(c, width=7); e.grid(row=i, column=j+2, padx=3, pady=4); e.insert(0, "0")
                fila.append(e)
            self.vec_entries.append(fila)
            tk.Label(c, text=")", font=("Consolas", 13), bg=C_SECTION, fg=C_ACCENT).grid(row=i, column=n+2)

        tk.Label(c, text="b", font=F_HEADING, bg=C_SECTION, fg=C_NEON).grid(row=k, column=0, padx=6, pady=10)
        tk.Label(c, text="(", font=("Consolas", 13), bg=C_SECTION, fg=C_NEON).grid(row=k, column=1, pady=10)
        for j in range(n):
            e = self._entry(c, width=7, bg="#040d20", hbg=C_BRIGHT)
            e.grid(row=k, column=j+2, padx=3, pady=10); e.insert(0, "0")
            self.vec_b_entries.append(e)
        tk.Label(c, text=")", font=("Consolas", 13), bg=C_SECTION, fg=C_NEON).grid(row=k, column=n+2, pady=10)

    def mostrar_resultado_vectores(self, t):
        self._write(self.txt_res_vectores, t); self._ops()

    def construir_matrices_ops(self, m_a, n_a, m_b, n_b):
        for w in self.scroll_matrices_ops.scrollable_frame.winfo_children():
            w.destroy()
        self.mat_entries_a = []
        self.mat_entries_b = []
        c = self.scroll_matrices_ops.scrollable_frame

        tk.Label(c, text="Matriz A", font=F_LABEL, bg=C_SECTION, fg=C_GLOW).grid(
            row=0, column=0, columnspan=n_a+2, pady=4)
        for i in range(m_a):
            tk.Label(c, text="[", font=("Consolas", 13), bg=C_SECTION, fg=C_ACCENT).grid(row=i+1, column=0)
            fila = []
            for j in range(n_a):
                e = self._entry(c, width=7); e.grid(row=i+1, column=j+1, padx=2, pady=2); e.insert(0, "0")
                fila.append(e)
            self.mat_entries_a.append(fila)
            tk.Label(c, text="]", font=("Consolas", 13), bg=C_SECTION, fg=C_ACCENT).grid(row=i+1, column=n_a+1)

        off = n_a + 3
        tk.Label(c, text="Matriz B", font=F_LABEL, bg=C_SECTION, fg=C_NEON).grid(
            row=0, column=off, columnspan=n_b+2, pady=4)
        for i in range(m_b):
            tk.Label(c, text="[", font=("Consolas", 13), bg=C_SECTION, fg=C_NEON).grid(row=i+1, column=off)
            fila = []
            for j in range(n_b):
                e = self._entry(c, width=7, bg="#040d20", hbg=C_BRIGHT)
                e.grid(row=i+1, column=j+off+1, padx=2, pady=2); e.insert(0, "0")
                fila.append(e)
            self.mat_entries_b.append(fila)
            tk.Label(c, text="]", font=("Consolas", 13), bg=C_SECTION, fg=C_NEON).grid(row=i+1, column=n_b+off+1)

    def mostrar_resultado_matrices(self, t):
        self._write(self.txt_res_matrices, t); self._ops()

    # ==========================================================================
    # MÓDULO 3 — CONVERSION DE BASES
    # Layout: 2 bloques en la misma fila, luego consola de resultados abajo
    # ==========================================================================
    def _build_conv(self):
        parent = self.tab_conv

        # Fila de conversores
        top = tk.Frame(parent, bg=C_PANEL)
        top.pack(fill=tk.X, pady=(0, 10))

        # Bloque: Hacia Decimal
        _, ca = self._bloque(top, "HACIA DECIMAL  —  DESCOMPOSICION POLINOMICA",
                             side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        row_a = tk.Frame(ca, bg=C_SECTION)
        row_a.pack(fill=tk.X, pady=(0, 6))
        tk.Label(row_a, text="VALOR ORIGINAL:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_conv_origen = self._entry(row_a, width=16)
        self.entry_conv_origen.insert(0, "101101")
        self.entry_conv_origen.pack(side=tk.LEFT)

        row_b = tk.Frame(ca, bg=C_SECTION)
        row_b.pack(fill=tk.X)
        tk.Label(row_b, text="BASE RADIX:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.base_origen = tk.StringVar(value="Binario")
        ttk.Combobox(row_b, textvariable=self.base_origen,
                     values=("Binario", "Octal", "Hexadecimal"),
                     state="readonly", width=14).pack(side=tk.LEFT, padx=(0, 12))
        ttk.Button(row_b, text="CONVERTIR  →  DECIMAL", style="P.TButton",
                   command=self.controlador.convertir_a_decimal).pack(side=tk.LEFT)

        # Bloque: Desde Decimal
        _, cd = self._bloque(top, "DESDE DECIMAL  —  DIVISIONES SUCESIVAS",
                             color_acento=C_GLOW,
                             side=tk.RIGHT, fill=tk.BOTH, expand=True)

        row_c = tk.Frame(cd, bg=C_SECTION)
        row_c.pack(fill=tk.X, pady=(0, 6))
        tk.Label(row_c, text="ENTERO DECIMAL:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.entry_conv_decimal = self._entry(row_c, width=16)
        self.entry_conv_decimal.insert(0, "45")
        self.entry_conv_decimal.pack(side=tk.LEFT)

        row_d = tk.Frame(cd, bg=C_SECTION)
        row_d.pack(fill=tk.X)
        tk.Label(row_d, text="BASE DESTINO:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.base_destino = tk.StringVar(value="Hexadecimal")
        ttk.Combobox(row_d, textvariable=self.base_destino,
                     values=("Binario", "Octal", "Hexadecimal"),
                     state="readonly", width=14).pack(side=tk.LEFT, padx=(0, 12))
        ttk.Button(row_d, text="CONVERTIR  →  BASE", style="P.TButton",
                   command=self.controlador.convertir_desde_decimal).pack(side=tk.LEFT)

        # Consola de resultados
        wrap_c, res_c = self._bloque(parent, "DESGLOSE Y REGISTRO DE CALCULO",
                                fill=tk.BOTH, expand=True)
        frame_txt_c = tk.Frame(res_c, bg=C_SECTION)
        frame_txt_c.pack(fill=tk.BOTH, expand=True)
        self.txt_resultados_conv = self._console(frame_txt_c, height=22, wrap=tk.WORD)
        sc_cy = ttk.Scrollbar(frame_txt_c, orient="vertical", command=self.txt_resultados_conv.yview)
        self.txt_resultados_conv.configure(yscrollcommand=sc_cy.set)
        self.txt_resultados_conv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_cy.pack(side=tk.RIGHT, fill=tk.Y)
        self._conectar_consola_fullscreen(self.txt_resultados_conv, "CONVERSIÓN DE BASES NUMÉRICAS", wrap_c.bar)

    def mostrar_resultado_conversion(self, t):
        self._write(self.txt_resultados_conv, t); self._ops()

    # ==========================================================================
    # MÓDULO 4 — NUMEROS ROMANOS
    # Layout: [Configuracion] [Entradas dinamicas] [Resultados]
    # ==========================================================================
    def _build_romanos(self):
        parent = self.tab_romanos

        # Fila superior: configuración
        top = tk.Frame(parent, bg=C_PANEL)
        top.pack(fill=tk.X, pady=(0, 8))

        # Bloque de configuración
        _, cfg_r = self._bloque(top, "NUMEROS ROMANOS — OPERACIONES ARITMETICAS",
                                fill=tk.BOTH, expand=True)

        row1 = tk.Frame(cfg_r, bg=C_SECTION)
        row1.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row1, text="OPERANDOS:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.spin_cant_romanos = ttk.Spinbox(row1, from_=2, to=10, width=4)
        self.spin_cant_romanos.set(2)
        self.spin_cant_romanos.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(row1, text="GENERAR", style="S.TButton",
                   command=self.controlador.generar_campos_romanos).pack(side=tk.LEFT, padx=(0, 16))

        tk.Label(row1, text="OPERACIÓN:", font=F_LABEL, bg=C_SECTION, fg=C_WHITE).pack(side=tk.LEFT, padx=(0, 6))
        self.op_romanos = tk.StringVar(value="Suma (+)")
        self.combo_op_romanos = ttk.Combobox(row1, textvariable=self.op_romanos,
                                              values=("Suma (+)", "Resta (-)", "Multiplicación (×)", "División (÷)"),
                                              state="readonly", width=18)
        self.combo_op_romanos.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(row1, text="CALCULAR", style="P.TButton",
                   command=self.controlador.calcular_operacion_romanos).pack(side=tk.LEFT, padx=(0, 16))

        row2 = tk.Frame(cfg_r, bg=C_SECTION)
        row2.pack(fill=tk.X, pady=(4, 0))
        tk.Label(row2, text="EJEMPLOS:", font=F_LABEL, bg=C_SECTION, fg=C_MUTED).pack(side=tk.LEFT, padx=(0, 6))
        for lbl, tipo in [("SUMA 3", "suma3"), ("MULT", "mult"), ("DIV", "div"), ("RESTA", "resta3")]:
            ttk.Button(row2, text=lbl, style="S.TButton",
                       command=lambda t=tipo: self.controlador.cargar_ejemplo_romanos(t)).pack(side=tk.LEFT, padx=(0, 4))

        self.entry_expresion_romana = None

        # Panel de entradas dinámicas
        _, inp = self._bloque(parent, "OPERANDOS",
                              fill=tk.X, pady=(0, 8))
        self.scroll_romanos = ScrollableFrame(inp, bg_color=C_SECTION)
        self.scroll_romanos.pack(fill=tk.X, expand=True)
        self.romanos_entries = []
        self.construir_campos_romanos(2)

        # Panel de resultados — 2 pestañas: Romano y Árabe
        wrap_rom_res, res = self._bloque(parent, "RESULTADOS", fill=tk.BOTH, expand=True)

        btn_fs_rom = tk.Button(
            wrap_rom_res.bar, text=" ⛶ PANTALLA COMPLETA ", font=F_SMALL,
            bg="#061a36", fg=C_NEON, activebackground=C_ACCENT,
            activeforeground=C_WHITE, bd=0, relief="flat", cursor="hand2", padx=8, pady=1,
            command=lambda: self.abrir_consola_fullscreen(
                "NÚMEROS ROMANOS · INFORME COMPLETO",
                self._obtener_resumen_romanos_texto
            )
        )
        btn_fs_rom.pack(side=tk.RIGHT, padx=6, pady=2)

        nb_r = ttk.Notebook(res, style="Sub.TNotebook")
        nb_r.pack(fill=tk.BOTH, expand=True)

        self.tab_res_romanos  = ttk.Frame(nb_r, padding="20")
        self.tab_res_normales = ttk.Frame(nb_r, padding="20")
        self.tab_res_desglose = ttk.Frame(nb_r, padding="8")
        nb_r.add(self.tab_res_romanos,  text="  ROMANO  ")
        nb_r.add(self.tab_res_normales, text="  ARABIGO  ")
        nb_r.add(self.tab_res_desglose, text="  DETALLE  ")

        # Resultado en Romano — texto grande centrado
        self.lbl_res_romano = tk.Label(
            self.tab_res_romanos, text="—",
            font=("JetBrains Mono", 28, "bold"),
            bg=C_SECTION, fg=C_NEON,
            anchor="center"
        )
        self.lbl_res_romano.pack(fill=tk.BOTH, expand=True)

        # Resultado en Árabe — texto grande centrado
        self.lbl_res_normal = tk.Label(
            self.tab_res_normales, text="—",
            font=("JetBrains Mono", 28, "bold"),
            bg=C_SECTION, fg=C_WHITE,
            anchor="center"
        )
        self.lbl_res_normal.pack(fill=tk.BOTH, expand=True)

        # Detalle / desglose
        bar_rom = tk.Frame(self.tab_res_desglose, bg=C_SECTION)
        bar_rom.pack(fill=tk.X, pady=(0, 4))
        tk.Label(bar_rom, text="REGISTRO DETALLADO DEL CÁLCULO (DOBLE CLIC PARA MAXIMIZAR):",
                 font=F_LABEL, bg=C_SECTION, fg=C_MUTED).pack(side=tk.LEFT)

        frame_txt_rom = tk.Frame(self.tab_res_desglose, bg=C_SECTION)
        frame_txt_rom.pack(fill=tk.BOTH, expand=True)

        self.txt_rom_desglose = self._console(frame_txt_rom, height=18, wrap=tk.WORD)
        sc_rom = ttk.Scrollbar(frame_txt_rom, orient="vertical", command=self.txt_rom_desglose.yview)
        self.txt_rom_desglose.configure(yscrollcommand=sc_rom.set)
        self.txt_rom_desglose.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_rom.pack(side=tk.RIGHT, fill=tk.Y)

        self._conectar_consola_fullscreen(self.txt_rom_desglose, "NÚMEROS ROMANOS · DESGLOSE DE CÁLCULO", bar_rom)

    def construir_campos_romanos(self, cantidad):
        for w in self.scroll_romanos.scrollable_frame.winfo_children():
            w.destroy()
        self.romanos_entries = []
        c = self.scroll_romanos.scrollable_frame

        for i in range(cantidad):
            f = tk.Frame(c, bg=C_SECTION, padx=6, pady=4)
            f.pack(side=tk.LEFT, padx=8)
            tk.Label(f, text=f"#{i+1}", font=F_LABEL, bg=C_SECTION, fg=C_MUTED).pack(anchor="w")
            e = self._entry(f, width=10)
            e.configure(font=F_MONO_LG)
            e.pack(pady=3)
            e.insert(0, "X" if i == 0 else "V" if i == 1 else "I")
            self.romanos_entries.append(e)

    def mostrar_resultados_romanos(self, resultado_dict):
        res_romano  = resultado_dict.get('resultado_romano', '?')
        res_normal  = resultado_dict.get('resultado_normal', '?')
        desglose    = resultado_dict.get('desglose_operandos', '').strip()
        proc_n      = resultado_dict.get('proceso_normal', '').strip()

        # Construir ecuación en romano:  II + II = IV
        mapa_ops = {
            "Suma (+)":           "+",
            "Resta (-)":          "−",
            "Multiplicación (×)": "×",
            "División (÷)":       "÷",
        }
        signo = mapa_ops.get(self.op_romanos.get(), "?")
        operandos_r = [e.get().strip().upper() for e in self.romanos_entries]

        if len(operandos_r) >= 2:
            expr_romano = f" {signo} ".join(operandos_r)
            ec_romano   = f"{expr_romano}  =  {res_romano}"
        else:
            ec_romano = f"{operandos_r[0]}  =  {res_romano}"

        # Construir ecuación en árabe desde el texto del proceso normal
        # proc_n tiene "Expresión numérica: 2 + 2" en la primera línea útil
        ec_normal = str(res_normal)
        for linea in proc_n.splitlines():
            if "Expresión" in linea and ":" in linea:
                expr_n = linea.split(":", 1)[1].strip()
                ec_normal = f"{expr_n}  =  {res_normal}"
                break
            # Para expresión libre el formato es distinto
            if "traducida" in linea and ":" in linea:
                expr_n = linea.split(":", 1)[1].strip()
                ec_normal = f"{expr_n}  =  {res_normal}"
                break

        self.lbl_res_romano.config(text=ec_romano)
        self.lbl_res_normal.config(text=ec_normal)
        self._write(self.txt_rom_desglose, desglose)
        self._ops()

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

    def confirmar_proceso_inversa_grande(self, n, nombre_matriz="Matriz"):
        """
        Muestra una alerta modal cuando una matriz cuadrada supera 10x10.
        Menciona el tiempo promedio estimado que tardará el cálculo por Gauss-Jordan
        con aritmética fraccionaria exacta.
        Presenta abajo dos opciones claras: CANCELAR y CONFIRMAR.
        Retorna True si el usuario confirma, o False si cancela.
        """
        # Estimación de tiempo promedio empírico para cálculo exacto y desglose
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
        dlg.title("Confirmación de Proceso · Matriz Inversa")
        dlg.configure(bg=C_ROOT)
        dlg.transient(self.root)
        dlg.resizable(False, False)

        # Centrar la alerta sobre la ventana principal
        w, h = 560, 320
        self.root.update_idletasks()
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        x = rx + max(0, (rw - w) // 2)
        y = ry + max(0, (rh - h) // 2)
        dlg.geometry(f"{w}x{h}+{x}+{y}")

        # Cabecera técnica de advertencia
        top_bar = tk.Frame(dlg, bg=C_HEADER, height=36)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        tk.Frame(top_bar, bg=C_WARN, width=5).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(
            top_bar,
            text=f"  ⚠ ADVERTENCIA · CÁLCULO DE MATRIZ {n}×{n}",
            font=F_SUBHEAD, bg=C_HEADER, fg=C_WARN
        ).pack(side=tk.LEFT, pady=6)

        # Contenido del mensaje
        body = tk.Frame(dlg, bg=C_SECTION, padx=18, pady=14,
                        highlightthickness=1, highlightbackground=C_BORDER)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        msg1 = (
            f"Ha solicitado invertir una matriz de tamaño {n}×{n} ({nombre_matriz}), la cual\n"
            f"supera el límite estándar de 10×10.\n\n"
            f"El cálculo mediante Gauss-Jordan con precisión racional exacta generará\n"
            f"múltiples transformaciones elementales por fila y desgloses de pasos."
        )
        tk.Label(body, text=msg1, font=F_LABEL, bg=C_SECTION, fg=C_WHITE, justify=tk.LEFT).pack(anchor="w", pady=(0, 10))

        # Panel destacado con el tiempo estimado
        box_tiempo = tk.Frame(body, bg="#061933", padx=12, pady=8,
                              highlightthickness=1, highlightbackground=C_ACCENT)
        box_tiempo.pack(fill=tk.X, pady=(0, 10))

        tk.Label(box_tiempo, text="⏱  TIEMPO PROMEDIO ESTIMADO:",
                 font=F_LABEL, bg="#061933", fg=C_NEON).pack(anchor="w")
        tk.Label(box_tiempo, text=f"    {tiempo_str.upper()}",
                 font=F_MONO_LG, bg="#061933", fg=C_WHITE).pack(anchor="w", pady=(2, 0))

        tk.Label(body, text="¿Desea confirmar y proceder con el cálculo o cancelar la operación?",
                 font=F_LABEL, bg=C_SECTION, fg=C_SILVER).pack(anchor="w")

        # Barra de botones: Cancelar y Confirmar
        btn_bar = tk.Frame(dlg, bg=C_ROOT, padx=14, pady=12)
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

        btn_cancel = tk.Button(
            btn_bar, text="  ✕  CANCELAR  ", font=F_MONO_B,
            bg=C_HEADER, fg=C_SILVER, activebackground="#1e293b", activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=18, pady=7, command=on_cancelar
        )
        btn_cancel.pack(side=tk.RIGHT, padx=(8, 0))

        btn_ok = tk.Button(
            btn_bar, text="  ✔  CONFIRMAR  ", font=F_MONO_B,
            bg=C_ACCENT, fg=C_WHITE, activebackground=C_BRIGHT, activeforeground=C_WHITE,
            bd=0, relief="flat", cursor="hand2", padx=20, pady=7, command=on_confirmar
        )
        btn_ok.pack(side=tk.RIGHT)

        dlg.grab_set()
        self.root.wait_window(dlg)
        return resultado[0]
