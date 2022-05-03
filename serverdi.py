#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from paho.mqtt.client import Client 
from multiprocessing import Process
import paho.mqtt.publish as publish

CONEXION = "wild.mat.ucm.es"

def on_message(mqttc,userdata,msg): #jugador1,b1,A1 
   message = str(msg.payload)[2:-1]
   if len(message.split(","))==3:
       player,boat,word = message.split(',')
       if player == 'jugador1':
           boats1[boat].append(word)
           boards['tablero1'][word] = "barco"
       else:
           boats2[boat].append(word)
           boards['tablero2'][word] = "barco"
       if len(boats2['b5']) == 4 and len(boats1['b5']) == 4:
           mens = 'COMIENZA EL JUEGO'
           publish = Process(target=publishing,args=(mens,))
           publish.start()
   else: #jugador1,A1
       tick(message)

def tick(message): #jugador1,A1
    sender,word = message.split(',')
    if sender == 'jugador1':
        board = 'tablero2'
    else: 
        board = 'tablero1'  
    state = boards[board][word]
    if state == "pintado":
        message = sender+' ha elegido una casilla ya marcada'
        publish = Process(target=publishing,args=(message, ))
        publish.start() 
    else:
        if state == "agua":
            boards[board][word] = "pintado"
            message=sender+',en la posicion '+word+',has tocado agua'
            publish = Process(target=publishing,args=(message, ))
            publish.start() 
        else:
            boards[board][word] = "pintado"
            if sender == 'jugador1':
                is_sunken=sinkplayer1(word)
                if is_sunken:
                    message=sender+',en la posicion '+word+',barco tocado,si lo has hundido'
                else:
                    message=sender+',en la posicion '+word+',barco tocado,no lo has hundido'
                publish = Process(target=publishing,args=(message, ))
                publish.start()
                if is_sunken and boats2 == {}:
                    mens = 'ULTIMO BARCO HUNDIDO, HA GANADO EL JUGADOR1'
                    publish1 = Process(target=publishing,args=(mens,))
                    publish1.start()  
                elif is_sunken and len(boats2)<len(boats1):
                    mens='Va ganando el jugador1'
                    publish1=Process(target=publishing,args=(mens, ))
                    publish1.start()
                elif is_sunken and len(boats1)==len(boats2):
                    mens='Vais empatados, acaba de remontar el jugador1'
                    publish1=Process(target=publishing,args=(mens, ))
                    publish1.start()
            else:
                is_sunken=sinkplayer2(word)
                if is_sunken:
                    message=sender+',en la posicion '+word+',barco tocado,si lo has hundido'
                else:
                    message=sender+',en la posicion '+word+',barco tocado,no lo has hundido'
                publish = Process(target=publishing,args=(message, ))
                publish.start()
                if is_sunken and boats1 == {}:
                    mens = 'ULTIMO BARCO HUNDIDO, HA GANADO EL JUGADOR2'
                    publish1 = Process(target=publishing,args=(mens,))
                    publish1.start()  
                elif is_sunken and len(boats1)<len(boats2):
                    mens='Va ganando el jugador2'
                    publish1=Process(target=publishing,args=(mens, ))
                    publish1.start()

                elif is_sunken and len(boats1)==len(boats2):
                    mens='Vais empatados, acaba de remontar el jugador2'
                    publish1=Process(target=publishing,args=(mens, ))
                    publish1.start()
    

def sinkplayer1(word):
    i = 0
    lista = list(boats2.keys())
    boolean=True
    while boolean and i<len(lista):
        if word in boats2[lista[i]]:
            boats2[lista[i]].remove(word)
            boolean=False#ya he encontrado el barco en el que estaba así que paro el bucle
            if len(boats2[lista[i]])==0:
                boats2.pop(lista[i])
                is_sunken =True                                                 
            else:
                is_sunken = False                
        i+=1
    return is_sunken 

def sinkplayer2(word):
    i = 0
    lista = list(boats1.keys())
    boolean=True
    while boolean and i<len(lista):
        if word in boats1[lista[i]]:
            boats1[lista[i]].remove(word)
            boolean=False#ya he encontrado el barco en el que estaba así que paro el bucle
            if len(boats1[lista[i]])==0:
                boats1.pop(lista[i])
                is_sunken =True                             
            else:
                is_sunken = False                
        i+=1
    return is_sunken

def publishing(message):
    print(message)
    publish.single('clients/sinking',payload=message,hostname=CONEXION)



def createbo():
    d={}
    for i in range(65,86):
        for j in range(20):
            d[chr(i)+str(j)]="agua"
    return d

bo1 = createbo()
bo2 = createbo()
boards={'tablero1':bo1,'tablero2':bo2}
boats2={'b1':[],'b2':[],'b3':[],'b4':[],'b5':[]}
boats1={'b1':[],'b2':[],'b3':[],'b4':[],'b5':[]}


mqttc = Client(userdata=(boards,boats1,boats2))
mqttc.on_message = on_message
mqttc.enable_logger()

mqttc.connect(CONEXION)
mqttc.subscribe('clients/gaps')
mqttc.loop_forever()