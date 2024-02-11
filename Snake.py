from tkinter import *
from tkinter import ttk
import random

#configuracion del juego
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 60
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#F00B0B"
BACKGROUND_COLOR = "#685959"

#CLASE QUE DIBUJA LA SERPIENTE
class Snake:
    
    #inicializa la serpiente
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        #cordenadas iniciales
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        #crea la serpiente en la ventana
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

#CLASE QUE DIBUJA LA COMIDA
class Food:

    #Genera la comida en cordenadas aleatorias
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) -1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) -1) * SPACE_SIZE

        self.coordinates = [x,y]

        #Crea la comida en la ventana
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#FUNCIAN QUE MANEJA EL TURNO DEL JUEGO
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    #Mueve la serpiente en la direccion actual
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    #Dibuja la cabeza 
    snake.coordinates.insert(0, (x, y))

    #Crea un cuadrado de la sepiente
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #verifica que la serpiente pueda comer
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    #Verifica si hay coliciones 
    if check_collisions(snake):
        game_over()
    else:
        #Programa el proximo turno
        window.after(SPEED, next_turn, snake, food)

#FUNCION PARA CAMBIAR LA DIRECION DE LA SERPIENTE
def change_direction(new_direction):
    
    global direction

    #Cmbia la direcion si no es opuesta a la direcion actual
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

#FUNCION PARA VERIFICAR LA COLICIONES 
def check_collisions(snake):
    x, y = snake.coordinates[0]

    #Verifica si la serpiente choca con los bordes de la ventana
    if x < 0 or x >= GAME_WIDTH:
        return True 
    elif y < 0 or y >= GAME_HEIGHT:
        return True 

    # for body_part in snake.coordinates[1:]:
    #     if x == body_part[0] and y == body_part[1]:
    #         print("GAME OVER")
    #         return True
    
    # return False 

#FUNCION QUE CIERRA LA VENTANA DEL JUEGO
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
    next_turn(snake, food)
    button.destroy()
    button2.destroy()


#FUNCION PARA MOSTRAR EN PANTALLA EL "GAME OVER"
def game_over():


    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2, font=('consolas',70),text="GAME OVER", fill="red", tag="gameover")

    #Boton de exit
    global button
    button = ttk.Button(window, text="EXIT", command= exit, style="Exit.TButton")
    button.pack()
    button.place(x=200, y=400)

    #boton de reinicio
    global button2
    button2 = ttk.Button(window, text="RESTART", command= restart, style="Restart.TButton")
    button2.pack()
    button2.place(x=200, y=450)

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
#styleR = ttk.Style()
style.configure("Exit.TButton", foreground="red")
#style.configure("Restart.TButton",foreground="grren")

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

#COMENZAR EL JUEGO
next_turn(snake, food)

#INICIALIZA EL BUCLE DE LA VENTANA 
window.mainloop()