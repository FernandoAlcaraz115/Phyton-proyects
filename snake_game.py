from tkinter import *
import random

# Configuración del juego
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "red"
FOOD_COLOR = "blue"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Inicializa la serpiente con BODY_PARTS segmentos
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = self.generate_food()

        # Dibuja la comida en el canvas
        canvas.create_oval(self.coordinates[0], self.coordinates[1], 
                           self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE, 
                           fill=FOOD_COLOR, tag="food")

    def generate_food(self):
        # Genera coordenadas aleatorias para la comida dentro de los límites del juego
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

def next_turn(snake, food):
    global score

    # Obtiene la posición actual de la cabeza de la serpiente
    x, y = snake.coordinates[0]

    # Calcula la nueva posición de la cabeza según la dirección
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Inserta la nueva posición de la cabeza en las coordenadas de la serpiente
    snake.coordinates.insert(0, [x, y])

    # Dibuja el nuevo segmento de la serpiente
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Verifica si la serpiente comió la comida
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")  # Elimina la comida actual
        food = Food(canvas)  # Crea una nueva comida
    else:
        # Si no comió, elimina el último segmento de la serpiente
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    # Verifica colisiones
    if check_collision(snake):
        game_over()
    else:
        # Llama a la siguiente iteración del juego
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    # Cambia la dirección de la serpiente, evitando que se mueva en la dirección opuesta
    if new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
    elif new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]

    # Verifica colisiones con los bordes del juego
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Verifica colisiones con el cuerpo de la serpiente
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    # Muestra el mensaje de "Game Over" y el puntaje final
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
                       font=("Consolas", 40), text="Game Over", fill="red", anchor=CENTER)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50, 
                       font=("Consolas", 40), text="Score: {}".format(score), fill="red", anchor=CENTER)
    
    # Botón para reiniciar el juego
    global restart_button
    restart_button = Button(window, text="Reiniciar", font=("Consolas", 20), command=restart_game)
    restart_button.place(relx=0.5, rely=0.7, anchor=CENTER)  # Coloca el botón en el centro

def restart_game():
    global score, direction, snake, food, restart_button

    # Reinicia las variables del juego
    score = 0
    direction = "down"
    label.config(text="Score: {}".format(score))

    # Elimina el botón de reinicio si existe
    if restart_button:
        restart_button.destroy()

    # Limpia el canvas
    canvas.delete(ALL)

    # Reinicia la serpiente y la comida
    snake = Snake(canvas)
    food = Food(canvas)

    # Vuelve a iniciar el juego
    next_turn(snake, food)

# Configuración de la ventana
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
restart_button = None  # Variable para almacenar el botón de reinicio

# Etiqueta para mostrar el puntaje
label = Label(window, text="Score: {}".format(score), font=("Consolas", 40))
label.pack()

# Canvas para dibujar el juego
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Centrar la ventana en la pantalla
window_width = canvas.winfo_width()
window_height = canvas.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

window.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

# Asignar las teclas para cambiar la dirección
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

# Inicializar la serpiente y la comida
snake = Snake(canvas)
food = Food(canvas)

# Iniciar el juego
next_turn(snake, food)

window.mainloop()