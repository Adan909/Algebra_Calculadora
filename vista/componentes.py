"""
Biblioteca de Componentes UI Reutilizables para 'Algebra Computation Engine'.
Proporciona widgets ergonómicos, modulares y con soporte de accesibilidad visual.
"""

import tkinter as tk
from tkinter import ttk
from vista.tema import (
    BG_WINDOW, BG_CARD, BG_SECONDARY, BG_HOVER, BG_ACTIVE,
    BORDER_SUBTLE, BORDER_FOCUS, BORDER_ERROR,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ON_ACCENT, TEXT_ON_SEC,
    ACCENT_PRIMARY, ACCENT_HOVER, ACCENT_ACTIVE, ACCENT_SOFT, ACCENT_BORDER,
    SUCCESS_BG, SUCCESS_TEXT, SUCCESS_BORDER,
    WARNING_BG, WARNING_TEXT, WARNING_BORDER,
    ERROR_BG, ERROR_TEXT, ERROR_BORDER,
    INFO_BG, INFO_TEXT, INFO_BORDER,
    RADIUS_SM, RADIUS_MD, RADIUS_LG, BORDER_WIDTH,
    PAD_XS, PAD_SM, PAD_MD, PAD_LG,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, FONT_MICRO,
    FONT_MONO, FONT_MONO_BOLD, FONT_MONO_SM, FONT_MATRIX
)


# ==============================================================================
# TOOLTIPS LIGEROS
# ==============================================================================
class Tooltip:
    """
    Muestra una etiqueta flotante tras colocar el puntero sobre un widget.
    """
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self._id_after = None

        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<ButtonPress>", self._on_leave)

    def _on_enter(self, event=None):
        self._cancelar()
        self._id_after = self.widget.after(350, self._mostrar)

    def _on_leave(self, event=None):
        self._cancelar()
        self._ocultar()

    def _cancelar(self):
        if self._id_after:
            self.widget.after_cancel(self._id_after)
            self._id_after = None

    def _mostrar(self):
        if not self.text:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        frame = tk.Frame(tw, bg=TEXT_PRIMARY, padx=8, pady=4)
        frame.pack()

        lbl = tk.Label(
            frame, text=self.text, font=FONT_SMALL,
            bg=TEXT_PRIMARY, fg="#FFFFFF", justify="left"
        )
        lbl.pack()

    def _ocultar(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# ==============================================================================
# BOTONES ERGONÓMICOS
# ==============================================================================
class BotonPrimario(tk.Button):
    """
    Botón de acción principal con fondo índigo, texto blanco y microinteracciones hover.
    """
    def __init__(self, parent, text="", command=None, shortcut="", **kwargs):
        label_text = f"{text}  [{shortcut}]" if shortcut else text
        super().__init__(
            parent, text=label_text, command=command,
            font=kwargs.pop("font", FONT_SUBHEAD),
            bg=ACCENT_PRIMARY, fg=TEXT_ON_ACCENT,
            activebackground=ACCENT_ACTIVE, activeforeground=TEXT_ON_ACCENT,
            relief="flat", bd=0, padx=kwargs.pop("padx", 14), pady=kwargs.pop("pady", 7),
            cursor="hand2", **kwargs
        )
        self.bind("<Enter>", lambda e: self.configure(bg=ACCENT_HOVER))
        self.bind("<Leave>", lambda e: self.configure(bg=ACCENT_PRIMARY))


class BotonSecundario(tk.Button):
    """
    Botón de acción secundaria con fondo blanco/secundario y borde fino de 1px.
    """
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            font=kwargs.pop("font", FONT_BODY),
            bg=BG_CARD, fg=TEXT_PRIMARY,
            activebackground=BG_ACTIVE, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, highlightcolor=BORDER_FOCUS,
            padx=kwargs.pop("padx", 12), pady=kwargs.pop("pady", 6),
            cursor="hand2", **kwargs
        )
        self.bind("<Enter>", lambda e: self.configure(bg=BG_HOVER, highlightbackground=ACCENT_PRIMARY))
        self.bind("<Leave>", lambda e: self.configure(bg=BG_CARD, highlightbackground=BORDER_SUBTLE))


class BotonFantasma(tk.Button):
    """
    Botón plano sin borde, ideal para barras de herramientas compactas.
    """
    def __init__(self, parent, text="", command=None, **kwargs):
        bg_parent = kwargs.pop("bg", BG_CARD)
        super().__init__(
            parent, text=text, command=command,
            font=kwargs.pop("font", FONT_SMALL_BOLD),
            bg=bg_parent, fg=TEXT_SECONDARY,
            activebackground=BG_SECONDARY, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=0,
            padx=kwargs.pop("padx", 8), pady=kwargs.pop("pady", 4),
            cursor="hand2", **kwargs
        )
        self._bg_orig = bg_parent
        self.bind("<Enter>", lambda e: self.configure(bg=BG_SECONDARY, fg=TEXT_PRIMARY))
        self.bind("<Leave>", lambda e: self.configure(bg=self._bg_orig, fg=TEXT_SECONDARY))


# ==============================================================================
# TARJETAS Y PANELES ELEVADOS (CARDS)
# ==============================================================================
class Tarjeta(tk.Frame):
    """
    Contenedor de tarjeta blanca con borde fino de 1px y cabecera opcional.
    """
    def __init__(self, parent, titulo=None, subtitulo=None, accion_widget=None, **kwargs):
        pad_x = kwargs.pop("padx", PAD_MD)
        pad_y = kwargs.pop("pady", PAD_MD)
        
        super().__init__(
            parent, bg=BG_CARD,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, highlightcolor=BORDER_SUBTLE,
            **kwargs
        )

        if titulo:
            self.header_frame = tk.Frame(self, bg=BG_CARD)
            self.header_frame.pack(fill=tk.X, padx=pad_x, pady=(pad_y, PAD_SM))

            left_box = tk.Frame(self.header_frame, bg=BG_CARD)
            left_box.pack(side=tk.LEFT, fill=tk.Y)

            tk.Label(
                left_box, text=titulo, font=FONT_HEADING,
                bg=BG_CARD, fg=TEXT_PRIMARY
            ).pack(anchor="w")

            if subtitulo:
                tk.Label(
                    left_box, text=subtitulo, font=FONT_SMALL,
                    bg=BG_CARD, fg=TEXT_SECONDARY
                ).pack(anchor="w", pady=(1, 0))

            if accion_widget:
                accion_widget(self.header_frame).pack(side=tk.RIGHT)

            # Línea separadora sutil bajo la cabecera
            tk.Frame(self, bg=BORDER_SUBTLE, height=1).pack(fill=tk.X, pady=(4, 0))

        # Contenedor interior para los elementos de la tarjeta
        self.contenido = tk.Frame(self, bg=BG_CARD)
        self.contenido.pack(fill=tk.BOTH, expand=True, padx=pad_x, pady=pad_y)


# ==============================================================================
# SPINBOX NUMÉRICO CON BOTONES PROPIOS (+ / −)
# ==============================================================================
class SpinboxNumerico(tk.Frame):
    """
    Campo numérico con botones visuales integrados de incremento y decremento.
    Permite enlazar un comando `on_change` que se dispara al modificar el valor.
    """
    def __init__(self, parent, min_val=1, max_val=10, initial_val=3, on_change=None, width=4, **kwargs):
        super().__init__(
            parent, bg=BG_CARD,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            **kwargs
        )
        self.min_val = min_val
        self.max_val = max_val
        self.on_change = on_change

        self.btn_dec = tk.Button(
            self, text="−", font=FONT_BODY_BOLD, width=2,
            bg=BG_SECONDARY, fg=TEXT_PRIMARY, activebackground=BG_ACTIVE,
            relief="flat", bd=0, cursor="hand2",
            command=self._decrementar
        )
        self.btn_dec.pack(side=tk.LEFT, fill=tk.Y)

        self.var = tk.StringVar(value=str(initial_val))
        self.entry = tk.Entry(
            self, textvariable=self.var, width=width, font=FONT_MONO_BOLD,
            justify="center", bg=BG_CARD, fg=TEXT_PRIMARY,
            insertbackground=ACCENT_PRIMARY, relief="flat", bd=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.entry.bind("<FocusOut>", self._validar_manual)
        self.entry.bind("<Return>", self._validar_manual)

        self.btn_inc = tk.Button(
            self, text="+", font=FONT_BODY_BOLD, width=2,
            bg=BG_SECONDARY, fg=TEXT_PRIMARY, activebackground=BG_ACTIVE,
            relief="flat", bd=0, cursor="hand2",
            command=self._incrementar
        )
        self.btn_inc.pack(side=tk.RIGHT, fill=tk.Y)

    def _incrementar(self):
        try:
            val = int(self.var.get().strip())
        except ValueError:
            val = self.min_val
        if val < self.max_val:
            self.set(val + 1)
            if self.on_change:
                self.on_change(val + 1)

    def _decrementar(self):
        try:
            val = int(self.var.get().strip())
        except ValueError:
            val = self.min_val
        if val > self.min_val:
            self.set(val - 1)
            if self.on_change:
                self.on_change(val - 1)

    def _validar_manual(self, event=None):
        try:
            val = int(self.var.get().strip())
            val = max(self.min_val, min(self.max_val, val))
        except ValueError:
            val = self.min_val
        self.set(val)
        if self.on_change:
            self.on_change(val)

    def get(self):
        return self.var.get().strip()

    def get_int(self):
        try:
            return int(self.var.get().strip())
        except ValueError:
            return self.min_val

    def set(self, val):
        self.var.set(str(val))

    def delete(self, first, last=None):
        self.entry.delete(first, last)

    def insert(self, index, string):
        self.entry.insert(index, string)
        self._validar_manual()


# ==============================================================================
# CONTROL SEGMENTADO (PILL TABS)
# ==============================================================================
class ControlSegmentado(tk.Frame):
    """
    Selector por segmentos estilo píldora para alternar pestañas o modos.
    """
    def __init__(self, parent, opciones, comando=None, initial_index=0, **kwargs):
        super().__init__(
            parent, bg=BG_SECONDARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            **kwargs
        )
        self.opciones = opciones
        self.comando = comando
        self.seleccionado = initial_index
        self.botones = []

        for idx, texto in enumerate(opciones):
            btn = tk.Button(
                self, text=texto, font=FONT_SMALL_BOLD,
                relief="flat", bd=0, cursor="hand2",
                padx=14, pady=5,
                command=lambda i=idx: self.seleccionar(i)
            )
            btn.pack(side=tk.LEFT, padx=1, pady=1)
            self.botones.append(btn)

        self._actualizar_estilo()

    def seleccionar(self, index):
        if 0 <= index < len(self.opciones):
            self.seleccionado = index
            self._actualizar_estilo()
            if self.comando:
                self.comando(index, self.opciones[index])

    def _actualizar_estilo(self):
        for idx, btn in enumerate(self.botones):
            if idx == self.seleccionado:
                btn.configure(
                    bg=ACCENT_PRIMARY, fg=TEXT_ON_ACCENT,
                    activebackground=ACCENT_HOVER, activeforeground=TEXT_ON_ACCENT
                )
            else:
                btn.configure(
                    bg=BG_SECONDARY, fg=TEXT_SECONDARY,
                    activebackground=BG_ACTIVE, activeforeground=TEXT_PRIMARY
                )


# ==============================================================================
# CHIP DE SISTEMA PRECARGADO
# ==============================================================================
class ChipSistema(tk.Frame):
    """
    Tarjeta compacta e interactiva para cargar ejemplos y presets de sistemas.
    """
    def __init__(self, parent, titulo, descripcion, tipo_color="info", comando=None, **kwargs):
        super().__init__(
            parent, bg=BG_CARD, cursor="hand2",
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            **kwargs
        )
        self.comando = comando

        colores = {
            "success": (SUCCESS_BG, SUCCESS_TEXT, SUCCESS_BORDER),
            "warning": (WARNING_BG, WARNING_TEXT, WARNING_BORDER),
            "error":   (ERROR_BG, ERROR_TEXT, ERROR_BORDER),
            "info":    (INFO_BG, INFO_TEXT, INFO_BORDER),
            "accent":  (ACCENT_SOFT, ACCENT_PRIMARY, ACCENT_BORDER),
        }
        bg_col, fg_col, bd_col = colores.get(tipo_color, (INFO_BG, INFO_TEXT, INFO_BORDER))
        self.bd_col = bd_col

        # Borde izquierdo de estado
        tk.Frame(self, bg=fg_col, width=3).pack(side=tk.LEFT, fill=tk.Y)

        body = tk.Frame(self, bg=BG_CARD, padx=8, pady=5)
        body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lbl_tit = tk.Label(body, text=titulo, font=FONT_SMALL_BOLD, bg=BG_CARD, fg=TEXT_PRIMARY)
        lbl_tit.pack(anchor="w")

        lbl_desc = tk.Label(body, text=descripcion, font=FONT_MICRO, bg=BG_CARD, fg=TEXT_SECONDARY)
        lbl_desc.pack(anchor="w")

        # Eventos interactivos en todo el widget
        for w in (self, body, lbl_tit, lbl_desc):
            w.bind("<Button-1>", lambda e: self.comando() if self.comando else None)
            w.bind("<Enter>", lambda e: self.configure(highlightbackground=fg_col))
            w.bind("<Leave>", lambda e: self.configure(highlightbackground=BORDER_SUBTLE))


# ==============================================================================
# BADGE DE ESTADO SEMÁNTICO
# ==============================================================================
class BadgeEstado(tk.Frame):
    """
    Etiqueta tipo píldora semántica con fondo suave y texto de alto contraste.
    """
    def __init__(self, parent, text="ESTADO", tipo="info", **kwargs):
        super().__init__(parent, **kwargs)
        self.lbl = tk.Label(self, text=text, font=FONT_MICRO, padx=8, pady=3)
        self.lbl.pack(fill=tk.BOTH, expand=True)
        self.set_estado(text, tipo)

    def set_estado(self, text, tipo="info"):
        colores = {
            "success": (SUCCESS_BG, SUCCESS_TEXT, SUCCESS_BORDER),
            "warning": (WARNING_BG, WARNING_TEXT, WARNING_BORDER),
            "error":   (ERROR_BG, ERROR_TEXT, ERROR_BORDER),
            "info":    (INFO_BG, INFO_TEXT, INFO_BORDER),
            "neutral": (BG_SECONDARY, TEXT_SECONDARY, BORDER_SUBTLE),
            "accent":  (ACCENT_SOFT, ACCENT_PRIMARY, ACCENT_BORDER),
        }
        bg_col, fg_col, bd_col = colores.get(tipo, (INFO_BG, INFO_TEXT, INFO_BORDER))
        self.configure(bg=bg_col, highlightthickness=1, highlightbackground=bd_col)
        self.lbl.configure(text=f"  {text}  ", bg=bg_col, fg=fg_col)


# ==============================================================================
# ESTADO VACÍO (EMPTY STATE)
# ==============================================================================
class EstadoVacio(tk.Frame):
    """
    Contenedor informativo con icono/símbolo y texto guía para orientar al usuario.
    """
    def __init__(self, parent, titulo="Sin datos aún", mensaje="Ingresa tu matriz y presiona Resolver", icono="📊", **kwargs):
        super().__init__(parent, bg=BG_CARD, padx=20, pady=30, **kwargs)

        tk.Label(
            self, text=icono, font=("Segoe UI", 32),
            bg=BG_CARD, fg=TEXT_MUTED
        ).pack(pady=(0, 6))

        tk.Label(
            self, text=titulo, font=FONT_HEADING,
            bg=BG_CARD, fg=TEXT_PRIMARY
        ).pack(pady=(0, 4))

        tk.Label(
            self, text=mensaje, font=FONT_BODY,
            bg=BG_CARD, fg=TEXT_SECONDARY, justify="center"
        ).pack()


# ==============================================================================
# CELDA MATRICIAL CON VALIDACIÓN VISUAL EN VIVO
# ==============================================================================
class CeldaMatriz(tk.Entry):
    """
    Celda de entrada numérica con formato monoespaciado, validación en vivo,
    selección completa al enfocar y navegación fluida por teclado.
    """
    def __init__(self, parent, valor_inicial="0", es_columna_b=False, on_validate=None, **kwargs):
        bg_base = ACCENT_SOFT if es_columna_b else BG_CARD
        self.es_columna_b = es_columna_b
        self.on_validate = on_validate

        super().__init__(
            parent, font=FONT_MATRIX, justify="center", width=kwargs.pop("width", 7),
            bg=bg_base, fg=TEXT_PRIMARY, insertbackground=ACCENT_PRIMARY,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=ACCENT_BORDER if es_columna_b else BORDER_SUBTLE,
            highlightcolor=ACCENT_PRIMARY, **kwargs
        )

        self.insert(0, str(valor_inicial))
        self.bind("<FocusIn>", self._al_enfocar)
        self.bind("<FocusOut>", self._al_desenfocar)
        self.bind("<KeyRelease>", self._validar_en_vivo)

    def _al_enfocar(self, event=None):
        self.select_range(0, tk.END)

    def _al_desenfocar(self, event=None):
        self._validar_en_vivo()

    def _validar_en_vivo(self, event=None):
        texto = self.get().strip()
        es_valido = True

        if texto:
            from fractions import Fraction
            try:
                # Acepta fracciones (1/2), enteros (-4) y decimales (0.75)
                Fraction(texto)
                es_valido = True
            except (ValueError, ZeroDivisionError):
                es_valido = False

        if es_valido:
            self.configure(
                highlightbackground=ACCENT_BORDER if self.es_columna_b else BORDER_SUBTLE,
                highlightcolor=ACCENT_PRIMARY
            )
        else:
            self.configure(
                highlightbackground=BORDER_ERROR,
                highlightcolor=BORDER_ERROR
            )

        if self.on_validate:
            self.on_validate(self, es_valido)


# ==============================================================================
# FRAME CON SCROLL INTEGRADO (SCROLLABLE FRAME)
# ==============================================================================
class ScrollableFrame(ttk.Frame):
    """
    Contenedor con barra de desplazamiento vertical y horizontal en tema claro.
    """
    def __init__(self, container, bg_color=BG_WINDOW, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(
            self, borderwidth=0, highlightthickness=0,
            bg=bg_color
        )
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self._window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<Configure>", self._al_redimensionar_canvas)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _al_redimensionar_canvas(self, event):
        min_width = self.scrollable_frame.winfo_reqwidth()
        min_height = self.scrollable_frame.winfo_reqheight()
        width = max(event.width, min_width)
        height = max(event.height, min_height)
        self.canvas.itemconfigure(self._window_id, width=width, height=height)

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ==============================================================================
# INTERRUPTOR DE MODO OSCURO / CLARO
# ==============================================================================
class InterruptorTema(tk.Frame):
    """
    Interruptor ergonómico para alternar entre Tema Claro y Tema Oscuro.
    Muestra el estado activo (☀️ Modo Claro / 🌙 Modo Oscuro) con estilo interactivo
    y microinteracciones visuales.
    """
    def __init__(self, parent, es_oscuro=False, comando=None, **kwargs):
        bg_parent = kwargs.pop("bg", BG_CARD)
        super().__init__(parent, bg=bg_parent, **kwargs)
        self.es_oscuro = es_oscuro
        self.comando = comando

        texto_btn = "☀️ Modo Claro" if es_oscuro else "🌙 Modo Oscuro"
        self.btn = tk.Button(
            self,
            text=texto_btn,
            font=FONT_SMALL_BOLD,
            bg=BG_SECONDARY,
            fg=TEXT_PRIMARY,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_SUBTLE,
            highlightcolor=BORDER_FOCUS,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._al_click
        )
        self.btn.pack(side=tk.LEFT)
        self.btn.bind("<Enter>", lambda e: self.btn.configure(bg=BG_HOVER, highlightbackground=ACCENT_PRIMARY))
        self.btn.bind("<Leave>", lambda e: self.btn.configure(bg=BG_SECONDARY, highlightbackground=BORDER_SUBTLE))

        tip = "Cambiar a Tema Claro (☀️)" if es_oscuro else "Cambiar a Tema Oscuro (🌙)"
        Tooltip(self.btn, tip)

    def _al_click(self):
        if self.comando:
            self.comando()
