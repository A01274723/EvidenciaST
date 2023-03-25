# Importa las funciones necesarias de la librería Turtle
from turtle import Turtle, tracer, update, done
from turtle import setup, onscreenclick, hideturtle
from freegames import line  # Importa "line" de la librería "freegames"


def grid():
    """Función para dibujar la cuadrícula del juego"""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """ Función para dibujar la cruz en la posición del jugador X"""
    t = Turtle()  # Crea un objeto de la clase Turtle
    t.pencolor('red')  # Establece el color de la línea en rojo
    t.pensize(10)  # Establece el grosor de la línea en 10
    t.up()  # Levanta el lápiz
    t.goto(x + 20, y + 20)  # Mueve el lápiz a la posición indicada
    t.down()  # Baja el lápiz
    # Dibuja la cruz utilizando la función "goto" en las posiciones indicadas
    t.goto(x + 113, y + 113)
    t.up()
    t.goto(x + 20, y + 113)
    t.down()
    t.goto(x + 113, y + 20)


def drawo(x, y):
    """Función para dibujar el círculo en la posición del jugador O"""
    t = Turtle()  # Crea un objeto de la clase Turtle
    t.up()  # Levanta el lápiz
    t.goto(x + 67, y + 15)  # Mueve el lápiz a la posición indicada
    t.down()  # Baja el lápiz
    t.color('green')  # Establece el color del lápiz en verde
    t.pensize(10)  # Establece el grosor del lápiz en 10
    t.circle(50)  # Dibuja el círculo de radio 50


def floor(value):
    """Función para redondear las coordenadas a la cuadrícula más cercana"""
    return ((value + 200) // 133) * 133 - 200


# Diccionario que almacena el estado actual del juego
state = {'player': 0}

# Lista que contiene las funciones de dibujo de los jugadores
players = [drawx, drawo]


def tap(x, y):
    """función que dibuja el simbolo en el cuadrado donde se hizo el clic"""
    x = floor(x)
    y = floor(y)
    player = state['player']
    draw = players[player]
    draw(x, y)
    update()
    state['player'] = not player


# Configuración inicial de la ventana de dibujo
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)  # Asignación de la función 'tap'
done()
