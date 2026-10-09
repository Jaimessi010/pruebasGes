
import tkinter as tk
import ast
from operaciones import calcular

# Colores
FONDO = "#101c2e"
PANEL = "#1a2e49"
VERDE = "#3bcaa9"
BLANCO = "#ffffff"
GRIS_BOTON = "#2d3e57"


class Calculadora:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora - pruebasGes")
        self.ventana.geometry("380x590")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=FONDO)

        self.expresion = ""

        # Título
        tk.Label(
            ventana,
            text="CALCULADORA",
            font=("Arial", 22, "bold"),
            bg=FONDO,
            fg=BLANCO
        ).pack(pady=(18, 12))

        # Pantalla de resultados
        self.pantalla = tk.Entry(
            ventana,
            font=("Arial", 28, "bold"),
            bg=PANEL,
            fg=BLANCO,
            bd=0,
            justify="right",
            insertbackground=BLANCO,
            state="readonly",
            readonlybackground=PANEL
        )
        self.pantalla.pack(
            fill="x", padx=20, ipady=18, pady=(0, 15)
        )

        # Marco de botones
        marco = tk.Frame(ventana, bg=FONDO)
        marco.pack(padx=15, pady=5, fill="both", expand=True)

        for fila in range(5):
            marco.rowconfigure(fila, weight=1)

        for columna in range(4):
            marco.columnconfigure(columna, weight=1)

        botones = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for fila, elementos in enumerate(botones):
            for columna, texto in enumerate(elementos):

                if texto in ["÷", "×", "-", "+", "="]:
                    color = VERDE
                    color_texto = FONDO
                elif texto in ["C", "⌫", "%"]:
                    color = "#40536f"
                    color_texto = BLANCO
                else:
                    color = GRIS_BOTON
                    color_texto = BLANCO

                boton = tk.Button(
                    marco,
                    text=texto,
                    font=("Arial", 17, "bold"),
                    bg=color,
                    fg=color_texto,
                    activebackground="#8ee6d2",
                    activeforeground=FONDO,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda t=texto: self.presionar(t)
                )

                # Última fila: 0 ocupa dos columnas
                if fila == 4:
                    if texto == "0":
                        boton.grid(
                            row=4, column=0, columnspan=2,
                            sticky="nsew", padx=4, pady=4
                        )
                    elif texto == ".":
                        boton.grid(
                            row=4, column=2,
                            sticky="nsew", padx=4, pady=4
                        )
                    else:
                        boton.grid(
                            row=4, column=3,
                            sticky="nsew", padx=4, pady=4
                        )
                else:
                    boton.grid(
                        row=fila, column=columna,
                        sticky="nsew", padx=4, pady=4
                    )

        # Atajos de teclado
        self.ventana.bind(
            "<Key>", self.usar_teclado
        )

        self.actualizar_pantalla()

    def presionar(self, tecla):

        if tecla == "C":
            self.expresion = ""

        elif tecla == "⌫":
            self.expresion = self.expresion[:-1]

        elif tecla == "=":
            try:
                resultado = self.evaluar_expresion(
                    self.expresion
                )
                self.expresion = f"{resultado:.10g}"

            except (ValueError, ZeroDivisionError,
                    OverflowError, SyntaxError):
                self.expresion = "Error"

        elif tecla == "%":
            try:
                resultado = self.evaluar_expresion(
                    self.expresion
                )
                self.expresion = f"{resultado / 100:.10g}"

            except (ValueError, ZeroDivisionError,
                    OverflowError, SyntaxError):
                self.expresion = "Error"

        else:
            if self.expresion == "Error":
                self.expresion = ""

            self.expresion += tecla

        self.actualizar_pantalla()

    def evaluar_expresion(self, expresion):
        # Interpretar las operaciones sin utilizar eval()
        expresion = expresion.replace("×", "*")
        expresion = expresion.replace("÷", "/")

        operadores = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/"
        }

        def resolver(nodo):

            if isinstance(nodo, ast.Constant):
                if type(nodo.value) in (int, float):
                    return nodo.value
                raise ValueError("Número inválido")

            if isinstance(nodo, ast.UnaryOp):
                valor = resolver(nodo.operand)

                if isinstance(nodo.op, ast.USub):
                    return -valor

                if isinstance(nodo.op, ast.UAdd):
                    return valor

            if isinstance(nodo, ast.BinOp):
                operacion = operadores.get(type(nodo.op))

                if operacion is None:
                    raise ValueError("Operación inválida")

                numero1 = resolver(nodo.left)
                numero2 = resolver(nodo.right)

                return calcular(
                    numero1, numero2, operacion
                )

            raise ValueError("Expresión inválida")

        arbol = ast.parse(expresion, mode="eval")
        return resolver(arbol.body)

    def actualizar_pantalla(self):
        self.pantalla.config(state="normal")
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(
            0, self.expresion if self.expresion else "0"
        )
        self.pantalla.config(state="readonly")

    def usar_teclado(self, evento):
        tecla = evento.char

        if tecla in "0123456789.+-":
            self.presionar(tecla)

        elif tecla == "*":
            self.presionar("×")

        elif tecla == "/":
            self.presionar("÷")

        elif evento.keysym in ("Return", "KP_Enter"):
            self.presionar("=")

        elif evento.keysym == "BackSpace":
            self.presionar("⌫")

        elif evento.keysym == "Escape":
            self.presionar("C")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Calculadora(ventana)
    ventana.mainloop()
