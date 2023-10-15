import RPi.GPIO as GPIO
import sys
import time
import subprocess

##############################
# Variáveis
##############################
numeroPino = 21 #int(sys.argv[1])
sleepVerifica = 5
tempMax = 45.0
tempMin = 38.0
##############################

def inicializaBoard():    
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)

def definePinoComoSaida(numeroPino):
    GPIO.setup(numeroPino, GPIO.OUT, initial = False)

def definePinoComoEntrada(numeroPino):
    GPIO.setup(numeroPino, GPIO.IN)
    

def escreveParaPorta(numeroPino, estadoPorta):
    GPIO.output(numeroPino, estadoPorta)    

try:  

    inicializaBoard()
    definePinoComoSaida(numeroPino)
    fan_ligado = 0
    
    while True:
        # Obtém a temperatura da cpu
        cmd = "vcgencmd measure_temp | cut -d '=' -f2 | cut -d \"'\" -f1 | tr -d '\n'"
        temperatura = float(subprocess.check_output(cmd, shell = True ))
        print("Temperatura: {} Estado do FAN: {}".format(temperatura, fan_ligado))        

        if temperatura >= tempMax and fan_ligado == 0:
            # Ativando gpio e ligando o fan
            print("Ativando GPIO {}".format(numeroPino))                                
            escreveParaPorta(numeroPino, True)
            fan_ligado = 1
        elif temperatura <= tempMin and fan_ligado == 1:
            # Desativando o gpio e desligando o fan
            print("Desativando GPIO {}".format(numeroPino))
            escreveParaPorta(numeroPino, False)
            fan_ligado = 0

        time.sleep(sleepVerifica)
            
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Encerrando...")
    exit()
        
