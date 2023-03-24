"""Pacman, juego arcade clásico.

Ejercicios

1. Cambiar el tablero.
2. Cambiar el número de fantasmas.
3. Cambiar donde inicia pacman.
4. Cambiar la velocidad de los fantasmas.
5. hacer más inteligentes a los fantasmas.
"""

from random import choice
from turtle import Turtle, bgcolor, clear, up, goto, dot, update
from turtle import ontimer, setup, hideturtle, tracer, listen, onkey, done

from freegames import floor, vector

state = {'score': 0}        # Marcador de puntaje que se mostrara en pantalla.
path = Turtle(visible=False)         # Objetos de tipo turtle que sirven para dibujar pixeles en pantalla.
writer = Turtle(visible=False)
aim = vector(5, 0)      # Dirección inicial a la que pacman apunta para desplazarse.
pacman = vector(-40, -80)       # Posición inciial de pacman.
ghosts = [      # Posición inicial de todos los fantasmas.
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# fmt: apagado.
# Lista de cada una de las casillas usadas en la ventana del juego. El valor 0 representa una casilla negra con colisión, mientras que el valor 1 rerpesenta a las casillas azules con 1 punto disponible y sin colisión.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: encendido.


def square(x, y):
    """Dibujar un cuadrado usando el objeto path en (x, y)"""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Regresa el offset del punto en las casillas."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Regresa True si el punto es válido para las casillas"""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja el mundo usando el objeto path"""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:        # Dibuja el cuadro azul si el valor de la casilla es 1, 2, o superior.
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:       # Dibuja un punto enmedio de la casilla si esta tiene valor de 1.
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Mover a pacman y a todos los fantasmas."""
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):         # Establece la nueva posición de pacman como su posición actual sumado a su vector de movimiento (aim).
        pacman.move(aim)

    index = offset(pacman)

    #Verifica si la tile a la que se dirige pacman es una tile con punto disponible, y en caso de serlo convierte esa tile en una con id 2 y suma un punto al puntaje.
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)       # Mueve el punto de trazado al centro del personaje pacman, y ahí dibuja un nuevo circulo amarillo de radio 20 para generar la ilusión de movimiento.
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):       # Verifica si las coordenadas del movimiento de los fantasmas son válidas.
            point.move(course)
        else:
            options = [         # Elige aleatoriamente una opción de movimiento para los fantasmas cada que topan con una pared.
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')      # Dibuja a los fantasmas como puntos rojos de radio 20.

    update()

    for point, course in ghosts:        # Si las coordenadas de pacman y de los fantasmas se sobrelapan en un radio de 20 pixeles, devuelve un valor.
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)


def change(x, y):
    """Cambia la dirección en la que se mueve pacman a la de un vector, solo si su movimiento es válido."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)         # Medidas y pisición inicial de la ventana donde se ejecuta el juego.
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])        # Muestra el puntaje en pantalla en las coordenadas especificadas en color blanco.
listen()        # Espera una instrucción del usuario
#Cambia el vector de movimeinto de pacman en caso de que detecte que se presione una de las flechas direccionales.
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()     #Llama a las funciones para trazar un nuevo fotograma.
move()
done()
