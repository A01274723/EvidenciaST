# Ignorar errores F403 y F405 de flake8
# Funcion añadida 1: imprimir número de taps
# Funcion añadida 2: revisar si las casillas están reveladas

"""Juego de memoria
Evidencia Semana Tec
Jesus Ramirez Delgado
Equipo 1
"""

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
tiles = list(range(32)) * 2
state = {'mark': None}
hide = [True] * 64
taps = 0  # Variable para contar los taps


def square(x, y):
    """Dibuja el tablero blanco con lineas negras (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Añade el indice (x, y)"""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Recuento de casillas en coordenadas (x, y)."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Actualiza las casillas marcadas y en blanco."""
    global taps  # Acceso a la variable tap
    taps += 1  # Incrementa tap
    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    """Genera la imagen y las filas."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 100)

    if not any(hide):  # Revisa si todas las casillas fueron reveladas
        print("Game over! Number of taps:", taps)  # Imprime el numero de taps
        return


shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
