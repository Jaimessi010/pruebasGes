
def calcular(a, b, operacion):
    if operacion == "+":
        return a + b

    elif operacion == "-":
        return a - b

    elif operacion == "*":
        return a * b

    elif operacion == "/":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b

    else:
        raise ValueError("Operación no válida")
