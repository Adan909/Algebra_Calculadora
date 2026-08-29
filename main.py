import tkinter as tk
from controlador.controlador import Controlador

def main():
    """
    Punto de entrada de la aplicación Calculadora de Eliminación Gaussiana.
    Inicializa el bucle principal de Tkinter y el controlador MVC.
    """
    root = tk.Tk()
    app = Controlador(root)
    root.mainloop()

if __name__ == "__main__":
    main()
