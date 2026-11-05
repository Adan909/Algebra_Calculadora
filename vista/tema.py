"""
Sistema Central de Tokens de Diseño para 'Algebra Computation Engine'.
Implementa una guía de estilos moderna con soporte para Tema Claro (Light Mode)
y Tema Oscuro (Dark Mode), con tipografía escalable, paleta accesible (WCAG 4.5:1 / 3:1)
y constantes unificadas.
"""

import tkinter as tk
import tkinter.font as tkfont

# ==============================================================================
# DEFINICIÓN DE PALETAS (TEMA CLARO Y TEMA OSCURO)
# ==============================================================================

PALETAS = {
    "claro": {
        # Fondos y Superficies
        "BG_WINDOW":       "#F7F8FA",  # Fondo principal de la ventana
        "BG_CARD":         "#FFFFFF",  # Paneles, tarjetas y contenedores elevados
        "BG_SECONDARY":    "#F1F3F6",  # Zonas secundarias, cabeceras, celdas de solo lectura
        "BG_HOVER":        "#F8F9FA",  # Hover sutil en botones secundarios
        "BG_ACTIVE":       "#EAECF0",  # Presión en botones secundarios

        # Bordes y Separadores
        "BORDER_SUBTLE":   "#E4E7EC",  # Borde fino de 1px estándar
        "BORDER_FOCUS":    "#4F46E5",  # Borde de foco activo
        "BORDER_ERROR":    "#F04438",  # Borde de error de validación

        # Tipografía y Textos
        "TEXT_PRIMARY":    "#101828",  # Texto principal de alto contraste
        "TEXT_SECONDARY":  "#475467",  # Texto secundario de apoyo
        "TEXT_MUTED":      "#98A2B3",  # Texto deshabilitado o placeholder
        "TEXT_ON_ACCENT":  "#FFFFFF",  # Texto blanco sobre elementos con acento
        "TEXT_ON_SEC":     "#344054",  # Texto oscuro sobre fondos secundarios

        # Acento Principal (Índigo Utilitario)
        "ACCENT_PRIMARY":  "#4F46E5",  # Botón primario, pestañas activas, foco
        "ACCENT_HOVER":    "#4338CA",  # Hover de botón primario
        "ACCENT_ACTIVE":   "#3730A3",  # Presión de botón primario
        "ACCENT_SOFT":     "#EEF2FF",  # Fondo suave para selección, resaltado y columna b
        "ACCENT_BORDER":   "#C7D2FE",  # Borde fino para elementos con acento suave

        # Colores Semánticos (Fondo Suave + Texto Oscuro)
        "SUCCESS_BG":      "#ECFDF3",
        "SUCCESS_TEXT":    "#027A48",
        "SUCCESS_BORDER":  "#A6F4C5",

        "WARNING_BG":      "#FFFAEB",
        "WARNING_TEXT":    "#B54708",
        "WARNING_BORDER":  "#FEDF89",

        "ERROR_BG":        "#FEF3F2",
        "ERROR_TEXT":      "#B42318",
        "ERROR_BORDER":    "#FECDCA",

        "INFO_BG":         "#EFF8FF",
        "INFO_TEXT":       "#175CD3",
        "INFO_BORDER":     "#B2DDFF",
    },
    "oscuro": {
        # Fondos y Superficies
        "BG_WINDOW":       "#0F172A",  # Slate 900 - Fondo principal de la ventana
        "BG_CARD":         "#1E293B",  # Slate 800 - Paneles y tarjetas elevadas
        "BG_SECONDARY":    "#334155",  # Slate 700 - Zonas secundarias y cabeceras
        "BG_HOVER":        "#2C3B4E",  # Hover en botones
        "BG_ACTIVE":       "#475569",  # Slate 600 - Presión activa

        # Bordes y Separadores
        "BORDER_SUBTLE":   "#334155",  # Borde fino oscuro
        "BORDER_FOCUS":    "#818CF8",  # Indigo 400
        "BORDER_ERROR":    "#F87171",  # Red 400

        # Tipografía y Textos
        "TEXT_PRIMARY":    "#F8FAFC",  # Slate 50 - Alto contraste
        "TEXT_SECONDARY":  "#94A3B8",  # Slate 400 - Texto secundario
        "TEXT_MUTED":      "#64748B",  # Slate 500 - Placeholder y deshabilitado
        "TEXT_ON_ACCENT":  "#FFFFFF",  # Texto blanco sobre acento
        "TEXT_ON_SEC":     "#E2E8F0",  # Slate 200

        # Acento Principal (Índigo Luminoso)
        "ACCENT_PRIMARY":  "#6366F1",  # Indigo 500
        "ACCENT_HOVER":    "#4F46E5",  # Indigo 600
        "ACCENT_ACTIVE":   "#4338CA",  # Indigo 700
        "ACCENT_SOFT":     "#2E2A72",  # Fondo suave índigo oscuro para selección y columna b
        "ACCENT_BORDER":   "#4F46E5",

        # Colores Semánticos (Fondo Profundo + Texto Brillante)
        "SUCCESS_BG":      "#064E3B",
        "SUCCESS_TEXT":    "#6EE7B7",
        "SUCCESS_BORDER":  "#047857",

        "WARNING_BG":      "#451A03",
        "WARNING_TEXT":    "#FDE68A",
        "WARNING_BORDER":  "#B45309",

        "ERROR_BG":        "#450A0A",
        "ERROR_TEXT":      "#FCA5A5",
        "ERROR_BORDER":    "#991B1B",

        "INFO_BG":         "#172554",
        "INFO_TEXT":       "#93C5FD",
        "INFO_BORDER":     "#1D4ED8",
    }
}

TEMA_ACTUAL = "claro"

# Variables globales inicializadas con el tema por defecto (claro)
BG_WINDOW       = PALETAS["claro"]["BG_WINDOW"]
BG_CARD         = PALETAS["claro"]["BG_CARD"]
BG_SECONDARY    = PALETAS["claro"]["BG_SECONDARY"]
BG_HOVER        = PALETAS["claro"]["BG_HOVER"]
BG_ACTIVE       = PALETAS["claro"]["BG_ACTIVE"]

BORDER_SUBTLE   = PALETAS["claro"]["BORDER_SUBTLE"]
BORDER_FOCUS    = PALETAS["claro"]["BORDER_FOCUS"]
BORDER_ERROR    = PALETAS["claro"]["BORDER_ERROR"]

TEXT_PRIMARY    = PALETAS["claro"]["TEXT_PRIMARY"]
TEXT_SECONDARY  = PALETAS["claro"]["TEXT_SECONDARY"]
TEXT_MUTED      = PALETAS["claro"]["TEXT_MUTED"]
TEXT_ON_ACCENT  = PALETAS["claro"]["TEXT_ON_ACCENT"]
TEXT_ON_SEC     = PALETAS["claro"]["TEXT_ON_SEC"]

ACCENT_PRIMARY  = PALETAS["claro"]["ACCENT_PRIMARY"]
ACCENT_HOVER    = PALETAS["claro"]["ACCENT_HOVER"]
ACCENT_ACTIVE   = PALETAS["claro"]["ACCENT_ACTIVE"]
ACCENT_SOFT     = PALETAS["claro"]["ACCENT_SOFT"]
ACCENT_BORDER   = PALETAS["claro"]["ACCENT_BORDER"]

SUCCESS_BG      = PALETAS["claro"]["SUCCESS_BG"]
SUCCESS_TEXT    = PALETAS["claro"]["SUCCESS_TEXT"]
SUCCESS_BORDER  = PALETAS["claro"]["SUCCESS_BORDER"]

WARNING_BG      = PALETAS["claro"]["WARNING_BG"]
WARNING_TEXT    = PALETAS["claro"]["WARNING_TEXT"]
WARNING_BORDER  = PALETAS["claro"]["WARNING_BORDER"]

ERROR_BG        = PALETAS["claro"]["ERROR_BG"]
ERROR_TEXT      = PALETAS["claro"]["ERROR_TEXT"]
ERROR_BORDER    = PALETAS["claro"]["ERROR_BORDER"]

INFO_BG         = PALETAS["claro"]["INFO_BG"]
INFO_TEXT       = PALETAS["claro"]["INFO_TEXT"]
INFO_BORDER     = PALETAS["claro"]["INFO_BORDER"]


def establecer_tema(nombre_tema):
    """
    Aplica la paleta de colores del tema especificado ('claro' u 'oscuro')
    actualizando todas las constantes globales del módulo.
    """
    global TEMA_ACTUAL
    global BG_WINDOW, BG_CARD, BG_SECONDARY, BG_HOVER, BG_ACTIVE
    global BORDER_SUBTLE, BORDER_FOCUS, BORDER_ERROR
    global TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ON_ACCENT, TEXT_ON_SEC
    global ACCENT_PRIMARY, ACCENT_HOVER, ACCENT_ACTIVE, ACCENT_SOFT, ACCENT_BORDER
    global SUCCESS_BG, SUCCESS_TEXT, SUCCESS_BORDER
    global WARNING_BG, WARNING_TEXT, WARNING_BORDER
    global ERROR_BG, ERROR_TEXT, ERROR_BORDER
    global INFO_BG, INFO_TEXT, INFO_BORDER

    if nombre_tema not in PALETAS:
        nombre_tema = "claro"

    TEMA_ACTUAL = nombre_tema
    paleta = PALETAS[nombre_tema]

    BG_WINDOW       = paleta["BG_WINDOW"]
    BG_CARD         = paleta["BG_CARD"]
    BG_SECONDARY    = paleta["BG_SECONDARY"]
    BG_HOVER        = paleta["BG_HOVER"]
    BG_ACTIVE       = paleta["BG_ACTIVE"]

    BORDER_SUBTLE   = paleta["BORDER_SUBTLE"]
    BORDER_FOCUS    = paleta["BORDER_FOCUS"]
    BORDER_ERROR    = paleta["BORDER_ERROR"]

    TEXT_PRIMARY    = paleta["TEXT_PRIMARY"]
    TEXT_SECONDARY  = paleta["TEXT_SECONDARY"]
    TEXT_MUTED      = paleta["TEXT_MUTED"]
    TEXT_ON_ACCENT  = paleta["TEXT_ON_ACCENT"]
    TEXT_ON_SEC     = paleta["TEXT_ON_SEC"]

    ACCENT_PRIMARY  = paleta["ACCENT_PRIMARY"]
    ACCENT_HOVER    = paleta["ACCENT_HOVER"]
    ACCENT_ACTIVE   = paleta["ACCENT_ACTIVE"]
    ACCENT_SOFT     = paleta["ACCENT_SOFT"]
    ACCENT_BORDER   = paleta["ACCENT_BORDER"]

    SUCCESS_BG      = paleta["SUCCESS_BG"]
    SUCCESS_TEXT    = paleta["SUCCESS_TEXT"]
    SUCCESS_BORDER  = paleta["SUCCESS_BORDER"]

    WARNING_BG      = paleta["WARNING_BG"]
    WARNING_TEXT    = paleta["WARNING_TEXT"]
    WARNING_BORDER  = paleta["WARNING_BORDER"]

    ERROR_BG        = paleta["ERROR_BG"]
    ERROR_TEXT      = paleta["ERROR_TEXT"]
    ERROR_BORDER    = paleta["ERROR_BORDER"]

    INFO_BG         = paleta["INFO_BG"]
    INFO_TEXT       = paleta["INFO_TEXT"]
    INFO_BORDER     = paleta["INFO_BORDER"]

    # También actualizar referencias en el módulo componentes si ya fue cargado
    import sys
    if "vista.componentes" in sys.modules:
        comp = sys.modules["vista.componentes"]
        for k, v in paleta.items():
            setattr(comp, k, v)


def alternar_tema():
    """
    Alterna entre 'claro' y 'oscuro' y retorna el nuevo tema activo.
    """
    nuevo_tema = "oscuro" if TEMA_ACTUAL == "claro" else "claro"
    establecer_tema(nuevo_tema)
    return nuevo_tema


def es_oscuro():
    """
    Retorna True si el tema actual es oscuro, False en caso contrario.
    """
    return TEMA_ACTUAL == "oscuro"


def obtener_tema():
    """
    Retorna el identificador del tema actual ('claro' o 'oscuro').
    """
    return TEMA_ACTUAL


# ==============================================================================
# DIMENSIONES, RADIOS Y ESPACIADOS
# ==============================================================================
RADIUS_SM       = 4
RADIUS_MD       = 8
RADIUS_LG       = 12

BORDER_WIDTH    = 1

PAD_XS          = 4
PAD_SM          = 8
PAD_MD          = 12
PAD_LG          = 16
PAD_XL          = 20

# ==============================================================================
# TIPOGRAFÍA Y DETECCIÓN DINÁMICA DE FUENTES
# ==============================================================================
_FONT_UI_FAMILY = "Segoe UI"
_FONT_MONO_FAMILY = "Consolas"

def detectar_fuentes():
    """
    Detecta dinámicamente las fuentes disponibles en el sistema operativo y selecciona
    la mejor opción disponible según la lista de prioridades de diseño.
    """
    global _FONT_UI_FAMILY, _FONT_MONO_FAMILY
    try:
        familias = set(tkfont.families())
        
        # Prioridad para fuentes de interfaz (Sans-serif)
        ui_preferidas = ["Inter", "Segoe UI", "DejaVu Sans", "Helvetica", "Arial"]
        for f in ui_preferidas:
            if f in familias:
                _FONT_UI_FAMILY = f
                break
                
        # Prioridad para datos numéricos y matrices (Monospace)
        mono_preferidas = ["JetBrains Mono", "DejaVu Sans Mono", "Consolas", "Courier New"]
        for f in mono_preferidas:
            if f in familias:
                _FONT_MONO_FAMILY = f
                break
    except Exception:
        pass

# Ejecutar detección inicial
detectar_fuentes()

def get_font_ui(size=11, weight="normal", slant="roman"):
    return (_FONT_UI_FAMILY, size, weight if weight == "bold" else "normal")

def get_font_mono(size=11, weight="normal"):
    return (_FONT_MONO_FAMILY, size, weight if weight == "bold" else "normal")

# Fuentes predefinidas
FONT_TITLE_LG   = (_FONT_UI_FAMILY, 15, "bold")
FONT_TITLE      = (_FONT_UI_FAMILY, 13, "bold")
FONT_HEADING    = (_FONT_UI_FAMILY, 11, "bold")
FONT_SUBHEAD    = (_FONT_UI_FAMILY, 10, "bold")
FONT_BODY       = (_FONT_UI_FAMILY, 10, "normal")
FONT_BODY_BOLD  = (_FONT_UI_FAMILY, 10, "bold")
FONT_SMALL      = (_FONT_UI_FAMILY, 9, "normal")
FONT_SMALL_BOLD = (_FONT_UI_FAMILY, 9, "bold")
FONT_MICRO      = (_FONT_UI_FAMILY, 8, "bold")

FONT_MONO       = (_FONT_MONO_FAMILY, 10, "normal")
FONT_MONO_BOLD  = (_FONT_MONO_FAMILY, 10, "bold")
FONT_MONO_SM    = (_FONT_MONO_FAMILY, 9, "normal")
FONT_MONO_LG    = (_FONT_MONO_FAMILY, 12, "bold")
FONT_MATRIX     = (_FONT_MONO_FAMILY, 11, "bold")
