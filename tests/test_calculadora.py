
import pytest
from operaciones import calcular


def test_suma():
    assert calcular(10, 5, "+") == 15


def test_resta():
    assert calcular(10, 5, "-") == 5


def test_multiplicacion():
    assert calcular(10, 5, "*") == 50


def test_division():
    assert calcular(10, 5, "/") == 2


def test_division_por_cero():
    with pytest.raises(ZeroDivisionError):
        calcular(10, 0, "/")


def test_numeros_negativos():
    assert calcular(-5, -3, "+") == -8


def test_decimales():
    assert calcular(2.5, 1.5, "+") == 4.0


def test_operacion_invalida():
    with pytest.raises(ValueError):
        calcular(10, 5, "%")
