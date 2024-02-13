from tkinter import *
from tkinter import ttk
import random

# Configuración del juego
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 80
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#F00B0B"
OBSTACLE_COLOR = "#808080"
BACKGROUND_COLOR = "#685959"

# Clase que dibuja la serpiente
class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Coordenadas iniciales de la serpiente
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Crea la serpiente en el lienzo
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Clase que dibuja la comida
class Food:

    def __init__(self):
        # Genera la comida en coordenadas aleatorias
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Crea la comida en el lienzo
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Clase que dibuja los obstáculos
class Obstacle:

    def __init__(self):
        # Genera los obstáculos en coordenadas aleatorias
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Crea los obstáculos en el lienzo
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")

# Función que maneja el próximo turno del juego
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    # Mueve la serpiente en la dirección actual
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    # Inserta la nueva cabeza de la serpiente
    snake.coordinates.insert(0, (x, y))

    # Crea un nuevo cuadrado en la posición de la nueva cabeza de la serpiente
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Verifica si la serpiente alcanza la comida
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()  # Crea nueva comida

    else:
        # Elimina la última parte de la serpiente
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Verifica si hay colisiones con los obstáculos
    if check_collisions(snake):
        game_over()
    else:
        # Programa el próximo turno
        window.after(SPEED, next_turn, snake, food)

# Función para cambiar la dirección de la serpiente
def change_direction(new_direction):
    global direction
    # Cambia la dirección solo si no es opuesta a la dirección actual
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Función para verificar colisiones
def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Verifica si la serpiente choca con los bordes del área de juego
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True 
    # Verifica si la serpiente choca con un obstáculo
    for obstacle in obstacles:
        if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
            return True
    return False

# Función que cierra la ventana del juego
def exit():
    window.destroy()

# Función para reiniciar el juego
def restart():
    global score, direction, button, button2
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete("all")
    snake = Snake()
    food = Food()
    create_obstacles()  # Crea nuevos obstáculos
    next_turn(snake, food)
    button.destroy()
    button2.destroy()

# Función para mostrar el mensaje de "GAME OVER"
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2, font=('consolas',70),text="GAME OVER", fill="red", tag="gameover")
    # Botón de exit
    global button
    button = ttk.Button(window, text="EXIT", command= exit, style="Exit.TButton")
    button.pack()
    button.place(x=200, y=400)
    # Botón de reinicio
    global button2
    button2 = ttk.Button(window, text="RESTART", command= restart, style="Restart.TButton")
    button2.pack()
    button2.place(x=200, y=450)

def create_obstacles():
    global obstacles
    obstacles = []
    for _ in range(10):  # Crear 10 obstáculos
        obstacle = Obstacle()
        obstacles.append(obstacle)

#CREA LA VENTANA DEL JUEGO
window = Tk()
window.title("Snake Game")
#CONFIGURACION INICIAL
window.readprofile(False, False)

#INICIALIZACION DEL PUNTAJE DEL JUEGO 
score = 0
direction = 'dow'

#ETIQUETA PARA MOSTRAR EL PUNTAJE
label = Label(window,text="Score{} ".format(score),font=('consolas',40))
label.pack()

#CEREA EL LIENZO PARA EL JUEGO
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Definir estilo para el botón de salida
style = ttk.Style()
style.configure("Exit.TButton", foreground="red")

#CREA LA VENTANA DE LA PANTALLA 
window.update()
window_whith = window.winfo_width()
window_heigth = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_heigth = window.winfo_screenheight()

x = int((screen_width/2) - (window_whith/2))
y = int((screen_heigth/2) - (window_heigth/2))

window.geometry(f"{window_whith}x{window_heigth}+{x}+{y}")

#ASIGNA LAS TECLAS PARA COMBIAR LA DIRECCION DE LA SERPIENTE
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

#INICAIALIZA LA SERPIENTE Y LA COMIDA 
snake = Snake()
food = Food()
create_obstacles()  # Crear obstáculos

#COMENZAR EL JUEGO
next_turn(snake, food)

#INICIALIZA EL BUCLE DE LA VENTANA 
window.mainloop()

