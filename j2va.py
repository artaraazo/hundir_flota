#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from paho.mqtt.client import Client
import pygame

BLACK = (0, 0, 0) #Fondo
WHITE = (255, 255, 255) #Cuando no se sabe
BLUE = (0,0,255) #Cuando es agua
RED = (255, 0, 0) #Tocado
WIDE  = 20
LONG = 20
DIMBOARD = 20
DIMBOARD2 = 42
MARGIN = 4
DIM_WINDOW = [500, 990]
CONEXION = "wild.mat.ucm.es"
LETTERS=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'," ",'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
NUMBERS = [' ','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
images = {"ola" : pygame.image.load("ola.png"), "cabezahorizontal" : pygame.image.load("cabezahorizontal.jpg"), 
                "culohorizontal" : pygame.image.load("culohorizontal.jpg"),"culovertical" : pygame.image.load("culovertical.jpg"),
                "cabezavertical" : pygame.image.load("cabezavertical.jpg"),"cuerpo":pygame.image.load("cuerpo.jpg"),
                "cabezahorizontal2" : pygame.image.load("cabezahorizontal2.jpg"), "culohorizontal2" : pygame.image.load("culohorizontal2.jpg"),
                "culovertical2" : pygame.image.load("culovertical2.jpg"),"cabezavertical2" : pygame.image.load("cabezavertical2.jpg"),
                "cuerpo2":pygame.image.load("cuerpo2.jpg")}

def on_message(mqttc, userdata, msg):    
    message = str(msg.payload)[2:-1]
    if message == 'ULTIMO BARCO HUNDIDO, HA GANADO EL JUGADOR1' or message == 'ULTIMO BARCO HUNDIDO, HA GANADO EL JUGADOR2':
        print(message)
        pygame.quit()
    elif message[8:]==" ha elegido una casilla ya marcada":
        if message[:8]=="jugador2":
            print('Casilla ya marcada')
            j[1]=True
    elif message == 'COMIENZA EL JUEGO':
        j[1]=True
    elif message[:14] == 'Va ganando el ':
        if message[14:]=="jugador2":
            print('Barco hundido')
            j[1]=True
    elif message[:37]=='Vais empatados, acaba de remontar el ':
            if message[37:]=='jugador2':
                j[1]=True
    elif len(message.split(','))==3: #jugador2,en la posicion A1,has tocado agua
        sender, sentence1, sentence2=message.split(',')
        word=sentence1[15:]
        state=sentence2[11:]
        paint(sender,word,state)
        j[1]=True
    else:   #jugador2,en la posicion A1,barco tocado,no lo has hundido
        sender, sentence1,sentence2,sentence3 = message.split(',')
        word=sentence1[15:]
        state=sentence2[6:]
        sink=sentence3[:2]
        paint(sender,word,state)
        if sink=='no':
            j[1]=True
            

def paint(sender,word,state):
    if sender == 'jugador1':
        board = 'tablero2'
    else: 
        board = 'tablero1'  
    if state == 'agua':
        color= BLUE
    else:
        color= RED
    letter = word[0]
    number=int(word[1:])
    if board == 'tablero1':
        letter1 = ord(letter)-44
        el_board[letter1][number+1] = color
    else:
        letter1=ord(letter)-65
        old = el_board[letter1][number+1]
        if old in d.values():
            color = old +"2"
        el_board[letter1][number+1] = color
    pygame.init()
    screen = pygame.display.set_mode(DIM_WINDOW)
    tam_font = 20
    font = pygame.font.SysFont('arial', tam_font)
    screen.fill(BLACK)
    pygame.display.set_caption("Tableros jugador2")
    for row in range(41):
        for column in range(20):
            savecolor = el_board[row][column]
            if row == 22:
                text1 = font.render(NUMBERS[column],1,RED)
                screen.blit(text1, [MARGIN+(MARGIN+LONG) * column, (MARGIN+20 - tam_font)*121])
            if savecolor == BLUE:
                pygame.draw.rect(screen,WHITE,[(MARGIN+WIDE) * column + MARGIN,
                          (MARGIN+LONG) * row + MARGIN,WIDE,LONG])
                picture = pygame.transform.scale(images["ola"],[20,20])
                screen.blit(picture,[(MARGIN+WIDE) * column + MARGIN,
                          (MARGIN+LONG) * row + MARGIN])
            elif savecolor in images.keys():
                picture = pygame.transform.scale(images[savecolor],[20,20])
                screen.blit(picture,[(MARGIN+WIDE) * column + MARGIN,
                          (MARGIN+LONG) * row + MARGIN])
            else:
                pygame.draw.rect(screen,savecolor,[(MARGIN+WIDE) * column + MARGIN,
                          (MARGIN+LONG) * row + MARGIN,WIDE,LONG])
        text = font.render(LETTERS[row], 1, RED)
        screen.blit(text, [MARGIN+20 - tam_font, MARGIN+(MARGIN+LONG) * row])
    pygame.display.flip()   
            
def drawText(screen, text, position, font):
    Text = font.render(text, 1, BLUE)
    screen.blit(Text, position)
    
def positionMal(gap):#te dice si el jugador ha metido una casilla mal
    letter=gap[0]
    number=gap[1:]
    if not letter in LETTERS[0:len(LETTERS)//2] or not number in NUMBERS[1:] :
        return True
    else:
        return False

def boardaux(n):
    board=[]
    for i in range(n):
        row=[BLACK]
        for j in range(n):
            if (chr(i+65),j) in d.keys():
                row.append(d[(chr(i+65),j)])
            else:
                row.append(WHITE)
        board.append(row)
    board.append([BLACK]*n)
    for i in range(n):
        row=[BLACK]
        for j in range(n):
            row.append(WHITE)
        board.append(row)
        
    return board

def boatsMal(l, boat1): #te dice si la posición incialque quieres meter de los barcos se sale de rango o está mal escrita 
    boat=boat1.split(',')
    if boat[1] == 'h':
       t = ord(boat[0][0])
       s = (int(boat[0][1:]) + l-1)
       if 0 <= s < 19 and 65 <= t < 85:
           return False
       else:
           return True
    elif boat[1] == 'v':
        s = int(boat[0][1:])
        t = ord(boat[0][0]) + l-1
        if  0 <= s < 19 and 65 <= t < 85:
            return False
        else:
            return True
    else:           
        return True



boats=[]
for i in [2,3,3,4,4]:
    boat = input(f'Dame una posición para el barco de longitud {i} y su orientación: ')
    while boatsMal(i,boat):
        boat=input('No puedes poner ese barco en la casilla que deseas, prueba con otra: ')
    boats.append((i,boat))



        
n=1
d={}
messages=[]
for (i,boat) in boats:
    word,z=boat.split(',')
    x=int(word[1:]) #numeros
    y=word[0] #cojo solo la letra
    if z=="v":
        letter = chr(ord(y)+(i-1))
        d[(letter,x)]="culovertical"
        messages.append("jugador2,b" + str(n) +","+ letter +str(x))
        i-=1
        while i>0:
            letter = chr(ord(y)+(i-1))
            messages.append("jugador2,b" + str(n) +","+ letter +str(x))
            if i ==1:
                d[(letter,x)]="cabezavertical"
            else:
                d[(letter,x)]="cuerpo"

            i -=1
    if z=="h":
        d[(y,x+(i-1))]="culohorizontal"
        messages.append("jugador2,b" + str(n) +","+ y+str(x+(i-1)))
        i-=1
        while i>0:
            messages.append("jugador2,b" + str(n) +","+ y+str(x+(i-1)))
            if i==1:
                d[(y,x+(i-1))]="cabezahorizontal"
            else:
                d[(y,x+(i-1))]="cuerpo"
            i-=1
    n=n+1
el_board = boardaux(DIMBOARD)


j=[el_board,False]
mqttc = Client(userdata=j)
mqttc.on_message = on_message
mqttc.enable_logger()

mqttc.connect(CONEXION)
mqttc.subscribe('clients/sinking')


mqttc.loop_start()

for message in messages:
    mqttc.publish('clients/gaps',message)


while True:
    if j[1]:
        position = input('Dime una casilla: ')
        while positionMal(position):
            position=input('Casilla erronea, vuelve a introducir otra: ')
        mens='jugador2'+','+position
        j[1]=False
        mqttc.publish('clients/gaps',mens)

