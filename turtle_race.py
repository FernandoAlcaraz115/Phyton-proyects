import turtle
import random

# Configuración de la ventana
w = turtle.Screen()
w.bgcolor("white")
w.title("Carrera de Tortugas")

# Configuración de las tortugas
colors = ["red", "green", "blue", "purple"]
turtles = []

# Posiciones iniciales de las tortugas
start_positions = [(-200, 100), (-200, 50), (-200, 0), (-200, -50)]

for i in range(4):
    t = turtle.Turtle()
    t.color(colors[i])
    t.penup()
    t.shape("turtle")
    t.goto(start_positions[i])
    turtles.append(t)

# Variables para los puntos de las tortugas
puntos = [0, 0, 0, 0]

# Configuración de los textos de los puntos
tex_turtles = []
posiciones_textos = [(-300, 200), (-100, 200), (-300, -220), (-100, -220)]  # Posiciones de los textos

for i in range(4):
    tex = turtle.Turtle()
    tex.penup()
    tex.color(colors[i])  # Usamos el color de la tortuga para los textos
    tex.goto(posiciones_textos[i])  # Posición de los textos
    tex.hideturtle()
    tex_turtles.append(tex)

# Función para mover las tortugas
def mover_tortuga(index):
    global puntos
    distancia = random.randint(1, 5)
    turtles[index].fd(distancia)
    puntos[index] += distancia

# Función para mostrar los puntos de las tortugas
def mostrar_puntos():
    for i in range(4):
        tex_turtles[i].clear()
        tex_turtles[i].write("Puntos {}: {}".format(colors[i].capitalize(), puntos[i]), font=("Arial", 16, "bold"))

# Función para dibujar la pista
def dibujar_pista():
    pista = turtle.Turtle()
    pista.speed(0)
    pista.penup()
    pista.hideturtle()

    # Dibujar líneas horizontales para los carriles
    for y in [-70, -20, 30, 80]:
        pista.goto(-250, y)
        pista.pendown()
        pista.goto(250, y)
        pista.penup()

    # Dibujar línea de inicio
    pista.goto(-200, 120)
    pista.pendown()
    pista.goto(-200, -120)
    pista.penup()
    
    # Dibujar línea de meta
    pista.goto(115, 120)
    pista.pendown()
    pista.goto(115, -120)
    pista.penup()

# Dibujar la pista
dibujar_pista()

# Bucle principal de la carrera
while max(puntos) < 300:
    for i in range(4):
        mover_tortuga(i)
    mostrar_puntos()

# Determinar el ganador de la carrera
ganador = puntos.index(max(puntos))
tex_turtles[ganador].goto(-100, 0)
tex_turtles[ganador].write("Ganador: {}".format(colors[ganador].capitalize()), font=("Arial", 24, "bold"))

# Esperar a que el usuario cierre la ventana
w.exitonclick()
