import turtle
import time
import random

WIDTH, HEIGHT = 700, 600
COLORS =  ['red','green', 'blue', 'orange', 'yellow', 'black', 'purple', 'pink', 'brown', 'cyan']


def get_number_of_racers():
    racers =  0
    while True:
        racers = input('Enter the number of racers (2-10): ')
        if racers.isdigit():
            racers = int(racers)
            
        else:
            print('Input is not numeric...Try Again!')
            continue

        if 2 <= racers <= 10:
            return racers
        else:
            print('Number is not in range 2-10. Try Again!')

#Create Functions:

def race(colors):
    turtles = create_turtles(colors)

    while True:
        for racer in turtles:
            distance =  random.randrange(1,20)
            racer.forward(distance)

            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)]


def create_turtles(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1) 
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20)
        racer.pendown()
        turtles.append(racer)
    
    return turtles
   

def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title('Turtle Racing!')


racers = get_number_of_racers()   #call the function
init_turtle()
random.shuffle(COLORS)
colors =  COLORS[:racers] #Slices the COLORS list, selecting only the first racers elements.
winner = race(colors)
print("The winner is the turtle with color:", winner)
time.sleep(5)








#creating new object

# racer = turtle.Turtle()
# racer.speed(1)
# racer.penup()            #use for remove the line
# racer.shape('turtle')
# racer.color('cyan')
# racer.forward(100)
# racer.left(90)
# racer.pendown() 
# racer.forward(100)
# racer.right(90)
# racer.backward(100)
#time.sleep(20)   we have set speed as mentioned above.

# racer2 = turtle.Turtle()
# racer2.speed(5)
# racer2.penup()            #use for remove the line
# racer2.shape('turtle')
# racer2.color('brown')
# racer2.forward(150)
# racer2.left(90)
# racer2.pendown() 
# racer2.forward(150)
# racer2.right(90)
# racer2.backward(150)
