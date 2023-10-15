import RPi.GPIO as GPIO
import sys
import time
import subprocess
import logging as log

##############################
# Variáveis e configurações
##############################
# Configurações do pino, timeout e temperaturas:
numeroPino = 21 #int(sys.argv[1])
sleepVerifica = 5
tempMax = 45.0
tempMin = 38.0
# Configuração do log:
log.basicConfig(
    level=log.INFO,
    filename="fan_control.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
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
        log.info("Temperatura: {} Estado do FAN: {}".format(temperatura, fan_ligado))

        if temperatura >= tempMax and fan_ligado == 0:
            # Ativando gpio e ligando o fan
            log.info("Ativando GPIO {}".format(numeroPino))
            escreveParaPorta(numeroPino, True)
            fan_ligado = 1
        elif temperatura <= tempMin and fan_ligado == 1:
            # Desativando o gpio e desligando o fan
            log.info("Desativando GPIO {}".format(numeroPino))
            escreveParaPorta(numeroPino, False)
            fan_ligado = 0

        time.sleep(sleepVerifica)
            
except KeyboardInterrupt:
    log.info("Encerrando manualmente...")
    GPIO.cleanup()    
    exit()
except:
    log.error("Generic Exception")
    GPIO.cleanup()
    exit()
    
        
