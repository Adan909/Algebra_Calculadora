"""
============================================================
  CALCULADORA DE SISTEMAS DE ECUACIONES LINEALES
  Método: Eliminación por Filas (Eliminación Gaussiana)
  Interfaz: tkinter (Python estándar)
  Restricción: Solo Python puro, sin NumPy/SciPy
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────────────────────────
# PALETA DE COLORES Y ESTILOS (tema oscuro moderno)
# ─────────────────────────────────────────────────────────────
COLOR = {
    "bg":          "#0f1117",
    "panel":       "#1a1d2e",
    "card":        "#22263a",
    "border":      "#2e3250",
    "accent":      "#6c63ff",
    "accent2":     "#a78bfa",
    "success":     "#22d3a5",
    "warning":     "#f59e0b",
    "danger":      "#f43f5e",
    "info":        "#38bdf8",
    "text":        "#e2e8f0",
    "text_dim":    "#94a3b8",
    "highlight":   "#312e81",
    "entry_bg":    "#1e2235",
    "entry_fg":    "#c7d2fe",
    "btn_fg":      "#ffffff",
    "step_even":   "#1e2235",
    "step_odd":    "#161929",
}

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_SUB    = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_MONO   = ("Courier New", 11)
FONT_MONO_B = ("Courier New", 11, "bold")
FONT_SMALL  = ("Segoe UI", 9)

TOLERANCE = 1e-10


# ══════════════════════════════════════════════════════════════
#  SECCIÓN 1 – LÓGICA MATEMÁTICA (puro Python, sin NumPy)
# ══════════════════════════════════════════════════════════════

def copiar_matriz(mat):
    """Devuelve una copia profunda de una lista de listas."""
    return [fila[:] for fila in mat]


def formatear_num(valor):
    """
    Formatea un número flotante: si es entero lo muestra sin decimales;
    si no, lo muestra con hasta 6 decimales significativos.
    """
    if abs(valor - round(valor)) < TOLERANCE:
        return str(int(round(valor)))
    s = f"{valor:.6f}".rstrip("0").rstrip(".")
    return s


def imprimir_matriz_texto(mat, m, n):
    """
    Convierte la matriz aumentada [A|b] en texto formateado como tabla,
    con separador visual '|' antes de la columna b.
    """
    lineas = []
    anchos = []
    for j in range(n + 1):
        max_w = max(len(formatear_num(mat[i][j])) for i in range(m))
        max_w = max(max_w, 1)
        anchos.append(max_w)

    sep_w = sum(anchos) + 3 * n + 7
    sep = "─" * sep_w
    lineas.append(sep)
    for i in range(m):
        fila_txt = "│ "
        for j in range(n):
            s = formatear_num(mat[i][j])
            fila_txt += s.rjust(anchos[j]) + "  "
        fila_txt += "│  "
        fila_txt += formatear_num(mat[i][n]).rjust(anchos[n])
        fila_txt += "  │"
        lineas.append(fila_txt)
    lineas.append(sep)
    return "\n".join(lineas)


def eliminar_filas(mat_orig, m, n, callback_paso):
    """
    Eliminación Gaussiana hacia adelante con pivoteo parcial.
    Llama a callback_paso(titulo, mat_snapshot, detalle) en cada paso.
    Retorna (mat_escalonada, lista_de_pasos).
    """
    mat = copiar_matriz(mat_orig)
    pasos = []
    fila_pivote = 0

    for col in range(n):
        if fila_pivote >= m:
            break

        # Pivoteo parcial: buscar mayor valor absoluto en la columna
        max_val = abs(mat[fila_pivote][col])
        max_fila = fila_pivote
        for k in range(fila_pivote + 1, m):
            if abs(mat[k][col]) > max_val:
                max_val = abs(mat[k][col])
                max_fila = k

        # Si el mejor pivote es ~0, saltar esta columna
        if max_val < TOLERANCE:
            detalle = f"  Columna {col+1}: todos los elementos son ~0. Se omite."
            callback_paso(f"Columna {col+1}: sin pivote", copiar_matriz(mat), detalle)
            pasos.append(detalle)
            continue

        # Intercambiar filas si es necesario
        if max_fila != fila_pivote:
            mat[fila_pivote], mat[max_fila] = mat[max_fila], mat[fila_pivote]
            detalle = f"  Intercambio: F{fila_pivote+1} <-> F{max_fila+1}"
            callback_paso(f"Intercambio F{fila_pivote+1} <-> F{max_fila+1}",
                          copiar_matriz(mat), detalle)
            pasos.append(detalle)

        pivote = mat[fila_pivote][col]

        # Eliminación hacia adelante
        for i in range(fila_pivote + 1, m):
            if abs(mat[i][col]) < TOLERANCE:
                continue
            factor = mat[i][col] / pivote
            factor_txt = formatear_num(factor)
            for j in range(col, n + 1):
                mat[i][j] = mat[i][j] - factor * mat[fila_pivote][j]
            detalle = f"  F{i+1}  <-  F{i+1}  -  ({factor_txt}) * F{fila_pivote+1}"
            callback_paso(f"F{i+1} <- F{i+1} - ({factor_txt}) * F{fila_pivote+1}",
                          copiar_matriz(mat), detalle)
            pasos.append(detalle)

        fila_pivote += 1

    return mat, pasos


def calcular_rangos(mat_esc, m, n):
    """
    Calcula rango de A y rango de [A|b] desde la forma escalonada.
    Fila no nula en A  -> contribuye a rango_A y rango_Ab.
    Fila 0..0|c (c!=0) -> solo contribuye a rango_Ab (inconsistencia).
    """
    rango_A = 0
    rango_Ab = 0
    for i in range(m):
        coef_no_nulo = any(abs(mat_esc[i][j]) > TOLERANCE for j in range(n))
        termino_no_nulo = abs(mat_esc[i][n]) > TOLERANCE
        if coef_no_nulo:
            rango_A += 1
            rango_Ab += 1
        elif termino_no_nulo:
            rango_Ab += 1
    return rango_A, rango_Ab


def clasificar_sistema(rango_A, rango_Ab, n):
    """
    Clasifica el sistema según el Teorema de Rouché-Frobenius.
    Retorna (tipo_str, mensaje_str).
    """
    if rango_A != rango_Ab:
        return ("inconsistente",
                "Sistema Inconsistente: Sin Solucion\n"
                f"  rango(A) = {rango_A}  !=  rango([A|b]) = {rango_Ab}")
    if rango_A == n:
        return ("determinado",
                "Sistema Consistente Determinado:\nSolucion Unica\n"
                f"  rango(A) = rango([A|b]) = n = {n}")
    return ("indeterminado",
            "Sistema Consistente Indeterminado:\nInfinitas Soluciones\n"
            f"  rango(A) = rango([A|b]) = {rango_A}  <  n = {n}")


def sustitucion_atras(mat_esc, m, n):
    """
    Back-substitution en sistema triangular superior.
    Retorna lista [x1, x2, ..., xn].
    Lanza ValueError si hay pivote nulo.
    """
    sol = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(mat_esc[i][i]) < TOLERANCE:
            raise ValueError(f"Pivote nulo en fila {i+1}.")
        suma = mat_esc[i][n]
        for j in range(i + 1, n):
            suma -= mat_esc[i][j] * sol[j]
        sol[i] = suma / mat_esc[i][i]
    return sol


def verificar_solucion(mat_orig, sol, m, n):
    """
    Sustituye la solución en las ecuaciones originales.
    Retorna lista de (lhs, rhs, cumple_bool).
    """
    resultados = []
    for i in range(m):
        lhs = sum(mat_orig[i][j] * sol[j] for j in range(n))
        rhs = mat_orig[i][n]
        cumple = abs(lhs - rhs) < 1e-6
        resultados.append((lhs, rhs, cumple))
    return resultados


# ══════════════════════════════════════════════════════════════
#  SECCIÓN 2 – INTERFAZ GRÁFICA (tkinter)
# ══════════════════════════════════════════════════════════════

class GaussApp(tk.Tk):
    """
    Ventana principal. Tres columnas:
      [Izq] Configuración + grilla de entrada
      [Centro] Pasos del proceso (scroll)
      [Der] Resultado, clasificación y verificación
    """

    def __init__(self):
        super().__init__()
        self.title("Calculadora de Eliminacion Gaussiana")
        self.geometry("1420x860")
        self.minsize(1100, 700)
        self.configure(bg=COLOR["bg"])
        self.resizable(True, True)

        self.m_var = tk.IntVar(value=3)
        self.n_var = tk.IntVar(value=3)
        self.entradas = []
        self.mat_orig = []

        self._construir_ui()
        self._generar_grilla()

    # ── LAYOUT ──────────────────────────────────────────────

    def _construir_ui(self):
        # Barra superior
        barra = tk.Frame(self, bg=COLOR["accent"], height=56)
        barra.pack(fill="x", side="top")
        barra.pack_propagate(False)

        tk.Label(barra, text="  Calculadora de Eliminacion Gaussiana",
                 font=FONT_TITLE, bg=COLOR["accent"], fg=COLOR["btn_fg"],
                 anchor="w").pack(side="left", padx=20, pady=8)

        tk.Label(barra, text="Python Puro  |  Sin NumPy/SciPy",
                 font=FONT_SMALL, bg=COLOR["accent"], fg="#c4b5fd",
                 anchor="e").pack(side="right", padx=20, pady=8)

        # Tres columnas
        cont = tk.Frame(self, bg=COLOR["bg"])
        cont.pack(fill="both", expand=True, padx=12, pady=12)

        self.col_izq = tk.Frame(cont, bg=COLOR["panel"], width=380)
        self.col_izq.pack(side="left", fill="y", padx=(0, 8))
        self.col_izq.pack_propagate(False)

        col_centro = tk.Frame(cont, bg=COLOR["panel"])
        col_centro.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.col_der = tk.Frame(cont, bg=COLOR["panel"], width=360)
        self.col_der.pack(side="right", fill="y")
        self.col_der.pack_propagate(False)

        self._panel_izq()
        self._panel_centro(col_centro)
        self._panel_der()

    def _encabezado(self, parent, texto, color=None):
        c = color or COLOR["accent2"]
        tk.Frame(parent, bg=c, height=2).pack(fill="x", padx=12, pady=(16, 0))
        tk.Label(parent, text=texto, font=FONT_SUB,
                 bg=COLOR["panel"], fg=c, anchor="w").pack(fill="x", padx=14, pady=(6, 4))

    # ── PANEL IZQUIERDO ──────────────────────────────────────

    def _panel_izq(self):
        p = self.col_izq
        self._encabezado(p, "  Configuracion del Sistema")

        cfg = tk.Frame(p, bg=COLOR["card"], padx=12, pady=12)
        cfg.pack(fill="x", padx=12, pady=(4, 8))

        tk.Label(cfg, text="Ecuaciones (m):", font=FONT_BODY,
                 bg=COLOR["card"], fg=COLOR["text_dim"]).grid(row=0, column=0, sticky="w", pady=4)
        tk.Spinbox(cfg, from_=1, to=8, textvariable=self.m_var,
                   width=4, font=FONT_BODY, bg=COLOR["entry_bg"],
                   fg=COLOR["entry_fg"], buttonbackground=COLOR["accent"],
                   relief="flat", bd=4,
                   command=self._generar_grilla).grid(row=0, column=1, padx=8, pady=4)

        tk.Label(cfg, text="Variables (n):", font=FONT_BODY,
                 bg=COLOR["card"], fg=COLOR["text_dim"]).grid(row=1, column=0, sticky="w", pady=4)
        tk.Spinbox(cfg, from_=1, to=8, textvariable=self.n_var,
                   width=4, font=FONT_BODY, bg=COLOR["entry_bg"],
                   fg=COLOR["entry_fg"], buttonbackground=COLOR["accent"],
                   relief="flat", bd=4,
                   command=self._generar_grilla).grid(row=1, column=1, padx=8, pady=4)

        tk.Button(cfg, text="Actualizar grilla", font=FONT_SMALL,
                  bg=COLOR["accent"], fg=COLOR["btn_fg"], relief="flat",
                  bd=0, padx=10, pady=6, cursor="hand2",
                  command=self._generar_grilla).grid(row=2, column=0, columnspan=2,
                                                      pady=(8, 0), sticky="ew")

        self._encabezado(p, "  Matriz Aumentada  [A | b]", color=COLOR["info"])
        tk.Label(p, text="Ultima columna = vector b independiente",
                 font=FONT_SMALL, bg=COLOR["panel"], fg=COLOR["text_dim"],
                 wraplength=340, justify="left").pack(padx=14, pady=(0, 6))

        self.frame_grilla = tk.Frame(p, bg=COLOR["panel"])
        self.frame_grilla.pack(fill="x", padx=12, pady=4)

        self._encabezado(p, "  Ejecutar", color=COLOR["success"])
        frame_btns = tk.Frame(p, bg=COLOR["panel"])
        frame_btns.pack(fill="x", padx=12, pady=8)

        tk.Button(frame_btns, text="Cargar ejemplo", font=FONT_BODY,
                  bg=COLOR["card"], fg=COLOR["accent2"], relief="flat",
                  bd=0, padx=8, pady=8, cursor="hand2",
                  command=self._menu_ejemplos).pack(fill="x", pady=(0, 6))

        tk.Button(frame_btns, text="Limpiar", font=FONT_BODY,
                  bg=COLOR["card"], fg=COLOR["warning"], relief="flat",
                  bd=0, padx=8, pady=8, cursor="hand2",
                  command=self._limpiar).pack(fill="x", pady=(0, 6))

        tk.Button(frame_btns, text="  CALCULAR  ", font=("Segoe UI", 12, "bold"),
                  bg=COLOR["accent"], fg=COLOR["btn_fg"], relief="flat",
                  bd=0, padx=8, pady=12, cursor="hand2",
                  command=self._ejecutar).pack(fill="x")

    # ── PANEL CENTRAL (SCROLL) ───────────────────────────────

    def _panel_centro(self, parent):
        self._encabezado(parent, "  Proceso Paso a Paso", color=COLOR["warning"])

        cf = tk.Frame(parent, bg=COLOR["panel"])
        cf.pack(fill="both", expand=True, padx=8, pady=4)

        self.canvas_pasos = tk.Canvas(cf, bg=COLOR["panel"],
                                       highlightthickness=0, bd=0)
        sb = ttk.Scrollbar(cf, orient="vertical",
                            command=self.canvas_pasos.yview)
        self.canvas_pasos.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas_pasos.pack(side="left", fill="both", expand=True)

        self.frame_pasos = tk.Frame(self.canvas_pasos, bg=COLOR["panel"])
        self.canvas_pasos.create_window((0, 0), window=self.frame_pasos,
                                         anchor="nw", tags="fpasos")

        self.frame_pasos.bind("<Configure>",
            lambda e: self.canvas_pasos.configure(
                scrollregion=self.canvas_pasos.bbox("all")))
        self.canvas_pasos.bind("<Configure>",
            lambda e: self.canvas_pasos.itemconfig("fpasos", width=e.width))

        self.canvas_pasos.bind_all("<MouseWheel>",
            lambda e: self.canvas_pasos.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas_pasos.bind_all("<Button-4>",
            lambda e: self.canvas_pasos.yview_scroll(-1, "units"))
        self.canvas_pasos.bind_all("<Button-5>",
            lambda e: self.canvas_pasos.yview_scroll(1, "units"))

    # ── PANEL DERECHO ────────────────────────────────────────

    def _panel_der(self):
        p = self.col_der
        self._encabezado(p, "  Clasificacion", color=COLOR["success"])

        self.lbl_clase = tk.Label(p, text="—", font=("Segoe UI", 11, "bold"),
                                   bg=COLOR["card"], fg=COLOR["text"],
                                   wraplength=320, justify="center",
                                   padx=12, pady=16)
        self.lbl_clase.pack(fill="x", padx=12, pady=6)

        self._encabezado(p, "  Solucion", color=COLOR["success"])
        self.txt_sol = tk.Text(p, height=8, bg=COLOR["card"],
                                fg=COLOR["success"], font=FONT_MONO_B,
                                relief="flat", bd=0, state="disabled",
                                padx=10, pady=8)
        self.txt_sol.pack(fill="x", padx=12, pady=4)

        self._encabezado(p, "  Verificacion", color=COLOR["info"])
        self.txt_ver = tk.Text(p, height=14, bg=COLOR["card"],
                                fg=COLOR["text"], font=FONT_MONO,
                                relief="flat", bd=0, state="disabled",
                                padx=10, pady=8)
        self.txt_ver.pack(fill="both", expand=True, padx=12, pady=4)

        # Tags de color
        self.txt_ver.tag_config("ok",  foreground=COLOR["success"])
        self.txt_ver.tag_config("err", foreground=COLOR["danger"])
        self.txt_ver.tag_config("lbl", foreground=COLOR["text_dim"])
        self.txt_ver.tag_config("hdr", foreground=COLOR["info"], font=FONT_MONO_B)
        self.txt_sol.tag_config("var", foreground=COLOR["accent2"])
        self.txt_sol.tag_config("val", foreground=COLOR["success"])
        self.txt_sol.tag_config("inf", foreground=COLOR["warning"])
        self.txt_sol.tag_config("err", foreground=COLOR["danger"])

    # ── GRILLA DE ENTRADA ────────────────────────────────────

    def _generar_grilla(self):
        """Genera widgets Entry para la matriz aumentada [A|b]."""
        for w in self.frame_grilla.winfo_children():
            w.destroy()
        self.entradas = []

        m = self.m_var.get()
        n = self.n_var.get()

        # Encabezados
        for j in range(n + 1):
            nombre = f"x{j+1}" if j < n else "b"
            color_h = COLOR["accent"] if j < n else COLOR["warning"]
            tk.Label(self.frame_grilla, text=nombre,
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR["panel"], fg=color_h,
                     width=5, anchor="center").grid(row=0, column=j+1, padx=3, pady=2)

        for i in range(m):
            tk.Label(self.frame_grilla, text=f"F{i+1}",
                     font=("Segoe UI", 9, "bold"),
                     bg=COLOR["panel"], fg=COLOR["text_dim"],
                     width=3, anchor="e").grid(row=i+1, column=0, padx=(0, 4), pady=3)

            fila_e = []
            for j in range(n + 1):
                fg_e = COLOR["entry_fg"] if j < n else COLOR["warning"]
                e = tk.Entry(self.frame_grilla, width=5, font=FONT_MONO,
                             bg=COLOR["entry_bg"], fg=fg_e,
                             insertbackground=COLOR["text"],
                             relief="flat", bd=4, justify="center")
                e.insert(0, "0")
                e.grid(row=i+1, column=j+1, padx=3, pady=3, ipady=4)
                fila_e.append(e)

                # Separador visual antes de b
                if j == n - 1:
                    tk.Label(self.frame_grilla, text="|",
                             font=FONT_BODY, bg=COLOR["panel"],
                             fg=COLOR["border"]).grid(row=i+1, column=n, padx=1)
            self.entradas.append(fila_e)

    # ── LECTURA DE MATRIZ ────────────────────────────────────

    def leer_matriz(self):
        """Lee la grilla y retorna la matriz aumentada o None si hay error."""
        m = self.m_var.get()
        n = self.n_var.get()
        mat = []
        for i in range(m):
            fila = []
            for j in range(n + 1):
                txt = self.entradas[i][j].get().strip()
                try:
                    fila.append(float(txt))
                except ValueError:
                    messagebox.showerror("Error",
                        f"Valor invalido en F{i+1}, col {j+1}: '{txt}'")
                    return None
            mat.append(fila)
        return mat

    # ── EJEMPLOS ─────────────────────────────────────────────

    def _menu_ejemplos(self):
        menu = tk.Menu(self, tearoff=0, bg=COLOR["card"], fg=COLOR["text"],
                       activebackground=COLOR["accent"],
                       activeforeground=COLOR["btn_fg"],
                       font=FONT_BODY, bd=0, relief="flat")
        menu.add_command(label="Sistema 3x3 – Solucion Unica",
                         command=lambda: self._cargar("determinado"))
        menu.add_command(label="Sistema 3x3 – Infinitas Soluciones",
                         command=lambda: self._cargar("indeterminado"))
        menu.add_command(label="Sistema 3x3 – Sin Solucion",
                         command=lambda: self._cargar("inconsistente"))
        menu.add_separator()
        menu.add_command(label="Sistema 4x4 – Solucion Unica",
                         command=lambda: self._cargar("4x4"))
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()

    def _cargar(self, tipo):
        """Carga datos de ejemplo según el tipo de sistema."""
        if tipo == "determinado":
            m, n = 3, 3
            # 2x+y-z=8, -3x-y+2z=-11, -2x+y+2z=-3  → x=2, y=3, z=-1
            datos = [[2,1,-1,8],[-3,-1,2,-11],[-2,1,2,-3]]
        elif tipo == "indeterminado":
            m, n = 3, 3
            # Sistema dependiente (todas las filas son proporcionales)
            datos = [[1,2,3,6],[2,4,6,12],[3,6,9,18]]
        elif tipo == "inconsistente":
            m, n = 3, 3
            # Ultima ecuacion contradice al resto (20 != 18)
            datos = [[1,2,3,6],[2,4,6,12],[3,6,9,20]]
        elif tipo == "4x4":
            m, n = 4, 4
            datos = [[2,1,0,0,3],[1,3,1,0,6],[0,1,4,1,8],[0,0,1,3,10]]
        else:
            return

        self.m_var.set(m)
        self.n_var.set(n)
        self._generar_grilla()
        for i in range(m):
            for j in range(n + 1):
                self.entradas[i][j].delete(0, "end")
                self.entradas[i][j].insert(0, str(datos[i][j]))

    # ── LIMPIAR ───────────────────────────────────────────────

    def _limpiar(self):
        for fila in self.entradas:
            for e in fila:
                e.delete(0, "end")
                e.insert(0, "0")
        self._limpiar_resultados()

    def _limpiar_resultados(self):
        for w in self.frame_pasos.winfo_children():
            w.destroy()
        self.lbl_clase.config(text="—", fg=COLOR["text"], bg=COLOR["card"])
        for txt in (self.txt_sol, self.txt_ver):
            txt.config(state="normal")
            txt.delete("1.0", "end")
            txt.config(state="disabled")

    # ── EJECUCIÓN ─────────────────────────────────────────────

    def _ejecutar(self):
        """Orquesta todo el flujo de cálculo."""
        self._limpiar_resultados()

        # 1. Leer datos
        mat = self.leer_matriz()
        if mat is None:
            return
        m = self.m_var.get()
        n = self.n_var.get()
        self.mat_orig = copiar_matriz(mat)

        # 2. Mostrar matriz inicial
        self._paso(titulo="Matriz Aumentada Inicial  [A | b]",
                   mat_txt=imprimir_matriz_texto(mat, m, n),
                   detalle="",
                   numero=0,
                   color_t=COLOR["info"])

        # 3. Eliminación Gaussiana
        num = [1]
        def cb(titulo, snap, detalle):
            self._paso(titulo=titulo,
                       mat_txt=imprimir_matriz_texto(snap, m, n),
                       detalle=detalle,
                       numero=num[0])
            num[0] += 1

        mat_esc, _ = eliminar_filas(mat, m, n, cb)

        # Forma escalonada final
        self._paso(titulo="Forma Escalonada Final",
                   mat_txt=imprimir_matriz_texto(mat_esc, m, n),
                   detalle="  Proceso de eliminacion completado.",
                   numero=num[0],
                   color_t=COLOR["success"])

        # 4. Clasificación
        rango_A, rango_Ab = calcular_rangos(mat_esc, m, n)
        tipo, msg = clasificar_sistema(rango_A, rango_Ab, n)

        colores = {"determinado": COLOR["success"],
                   "indeterminado": COLOR["warning"],
                   "inconsistente": COLOR["danger"]}
        self.lbl_clase.config(text=msg, fg=colores[tipo], bg=COLOR["card"])

        # 5. Solución y verificación
        for txt in (self.txt_sol, self.txt_ver):
            txt.config(state="normal")
            txt.delete("1.0", "end")

        if tipo == "determinado":
            try:
                sol = sustitucion_atras(mat_esc, m, n)
                self.txt_sol.insert("end", "Solucion encontrada:\n\n", "var")
                for i, v in enumerate(sol):
                    self.txt_sol.insert("end", f"  x{i+1} = ", "var")
                    self.txt_sol.insert("end", f"{formatear_num(v)}\n", "val")

                vers = verificar_solucion(self.mat_orig, sol, m, n)
                self.txt_ver.insert("end", "Comprobacion  A·x = b:\n\n", "hdr")
                todas_ok = True
                for i, (lhs, rhs, ok) in enumerate(vers):
                    self.txt_ver.insert("end", f"  Ec {i+1}: ", "lbl")
                    tag = "ok" if ok else "err"
                    self.txt_ver.insert("end", f"{formatear_num(lhs)}", tag)
                    self.txt_ver.insert("end", f"  {'==' if ok else '!='} ", "lbl")
                    self.txt_ver.insert("end", f"{formatear_num(rhs)}", tag)
                    self.txt_ver.insert("end", f"  {'[OK]' if ok else '[FAIL]'}\n", tag)
                    if not ok:
                        todas_ok = False
                self.txt_ver.insert("end", "\n")
                if todas_ok:
                    self.txt_ver.insert("end",
                        "  Verificacion exitosa: todas OK.\n", "ok")
                else:
                    self.txt_ver.insert("end",
                        "  Algunas ecuaciones no verificadas.\n", "err")
            except ValueError as e:
                self.txt_sol.insert("end", f"Error: {e}", "err")

        elif tipo == "indeterminado":
            self.txt_sol.insert("end",
                f"Sistema con infinitas soluciones.\n\n"
                f"  Grados de libertad: {n - rango_A}\n"
                f"  Variables libres:   {n - rango_A}\n\n"
                f"Se requiere parametrizacion para\nexpresar la solucion general.", "inf")
            self.txt_ver.insert("end",
                "  (No aplica: infinitas soluciones.)\n", "lbl")
        else:
            self.txt_sol.insert("end",
                "El sistema no tiene solucion.\n\n"
                "Se detecto una ecuacion\ncontradictoria: 0 = c  (c != 0).", "err")
            self.txt_ver.insert("end",
                "  (No aplica: sistema inconsistente.)\n", "lbl")

        for txt in (self.txt_sol, self.txt_ver):
            txt.config(state="disabled")

        self.canvas_pasos.yview_moveto(0)

    # ── BLOQUE DE PASO VISUAL ─────────────────────────────────

    def _paso(self, titulo, mat_txt, detalle, numero, color_t=None):
        """Inserta un bloque visual en el panel de pasos."""
        ct = color_t or COLOR["warning"]
        bg = COLOR["step_even"] if numero % 2 == 0 else COLOR["step_odd"]

        bloque = tk.Frame(self.frame_pasos, bg=bg, pady=4, padx=8)
        bloque.pack(fill="x", pady=2, padx=4)

        cab = tk.Frame(bloque, bg=bg)
        cab.pack(fill="x")

        if numero > 0:
            tk.Label(cab, text=f" Paso {numero} ",
                     font=("Segoe UI", 9, "bold"),
                     bg=ct, fg="#000000", padx=4, pady=2).pack(side="left")

        tk.Label(cab, text=f"  {titulo}",
                 font=("Segoe UI", 10, "bold"),
                 bg=bg, fg=ct, anchor="w").pack(side="left", pady=2)

        if detalle:
            tk.Label(bloque, text=detalle,
                     font=("Segoe UI", 9, "italic"),
                     bg=bg, fg=COLOR["text_dim"],
                     anchor="w", justify="left").pack(fill="x", padx=4, pady=(0, 2))

        tk.Label(bloque, text=mat_txt,
                 font=("Courier New", 10),
                 bg=COLOR["card"], fg=COLOR["text"],
                 anchor="w", justify="left",
                 padx=10, pady=8).pack(fill="x", padx=4, pady=4)


# ══════════════════════════════════════════════════════════════
#  SECCIÓN 3 – MAIN
# ══════════════════════════════════════════════════════════════

def main():
    """Configura ttk, crea la app y lanza el event loop."""
    app = GaussApp()
    estilo = ttk.Style(app)
    estilo.theme_use("clam")
    estilo.configure("Vertical.TScrollbar",
                     background=COLOR["border"],
                     troughcolor=COLOR["panel"],
                     arrowcolor=COLOR["accent2"],
                     borderwidth=0, relief="flat")
    app.mainloop()


if __name__ == "__main__":
    main()
