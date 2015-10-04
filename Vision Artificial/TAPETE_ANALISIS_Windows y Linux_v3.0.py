# -*- coding: cp1252 -*-
#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *             'Vision Artificial'   para telesituacion            * #
# *                                                                 * #
# *                    Autor: Eulogio López Cayuela                 * #
# *                Versión RAM v.2    Fecha: 03/10/2015             * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################

from math import *


from SimpleCV import Camera, Image, cv2
import numpy as np
from scipy import ndimage

try:  
    import cPickle as pickle  
except ImportError:  
    import pickle  

import time


'''
==========================================================

*** VISTA Cenitalateral del sistema apuntador LASER ***


vision camara
(0,0)    tableroANCHO
 ---------------------------
|        |                 |
|        | puntoY          |
|        |                 | tableroALTO
| -------PUNTO             |
| puntoX |                 |
|        |                 |
|         | (0,0)usado     |
----------------------------
          |    |
          |ALFA|            
           |---| 
            \  |  <--- posteDistanciaY
             \ |
--------------POSTE   (Sera necesario conocer su altura, 'altura_POSTE')          
posteDistanciaX


posteDistanciaX  = (tableroANCHO / 2)

angulo_ALFA = atan2(catetoY_ALFA / catetoX_ALFA) ----->(usar la funcon 'atan2' que si posiciona bien los angulos en su cuadrante)  

catetoY_ALFA = posteDistanciaX - puntoX  ----->(sustituyendo 'posteDistanciaX')

*catetoY_ALFA = (tableroANCHO / 2) - puntoX

*catetoX_ALFA = posteDistanciaY + (tableroALTO - puntoY)

*hipotenusa_ALFA = (catetoX_ALFA**2 + catetoY_ALFA**2)**0.5


#### La 'hipotenusa_ALFA' será uno de los catetos necesarios en el calculo del angulo
     en el plano vertical (BETA), el otro cateto es la altura del poste




        #trasladar las coodenadas en el fotograma capturado a coordenadas sobre el tapete
        posicionRobotX = (robotDetectado.x / COEFICIENTE_AMPLIACION) - (tableroANCHO/2)
        posicionRobotY = tableroALTO - (robotDetectado.y / COEFICIENTE_AMPLIACION)



*** VISTA Lateral del sistema apuntador LASER ***


                  /|
                /  |
              / ---|
            / BETA |
          /        |  altura_POSTE
        /          |
      /            |
    /              |
  /                |
/                  |
--------------------
  hipotenusa_ALFA


angulo_BETA = atan2(catetoY_BETA / catetoX_BETA)

*catetoY_BETA = hipotenusa_ALFA
*catetoX_BETA = altura_POSTE

==========================================================
'''




# --------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------
    
def cargarDatos():
    ''' carga de datos desde fichero '''
      
    ficheroDatos = open('alldata.dat',"rb")
    listaOrdenada = pickle.load(ficheroDatos)
    ficheroDatos.close()

    p1 = listaOrdenada[0]
    p2 = listaOrdenada[1]
    p3 = listaOrdenada[2]
    p4 = listaOrdenada[3]
    color = listaOrdenada[4]
    binarize = listaOrdenada[5]  
    return p1[0],p1[1],p3[0],p3[1],p2[0],p2[1],p4[0],p4[1],color,binarize #listaOrdenada
# --------------------------------------------


def encuadrar_RAM(filename, transform):

    '''Si el parametro 'transform' = 1, se encarga de distorsionar el
    tablero para corregir la inclinacion y poder trabajar en el como
    si de una imagen frontal se tratase.
    Si el parametro 'transform' = 0 u otro valor distinto de 1,
    hace el proceso inverso, de manera que una imagen de vista frontal
    es distorsionada para que se adapte a la perspectiva de la realidad.
    De esta manera conseguimos el efecto realista de las fichas
    resaltadas sobre el tablero'''
    
    # Las dimensiones reales (cm) del trablero las multiplico un coeficiente para disponer de una cantidad de pixeles
    # que permita tener suficiente nitidez para trabajar con la imagen
    ancho = tableroANCHO * COEFICIENTE_AMPLIACION
    alto = tableroALTO * COEFICIENTE_AMPLIACION


        
    if transform == 1:
        antes = filename.getNumpyCv2()
        puntosIniciales = np.float32([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
        puntosFinales = np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
        transformacion = cv2.getPerspectiveTransform(puntosIniciales,puntosFinales)
        sinDistorsion = cv2.warpPerspective(antes,transformacion,(ancho,alto))
        despues = Image(sinDistorsion, cv2image=True)
    if transform != 1:
        antes = filename.getNumpyCv2()
        puntosIniciales = np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
        puntosFinales = np.float32([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
        transformacion = cv2.getPerspectiveTransform(puntosIniciales,puntosFinales)
        conDistorsion = cv2.warpPerspective(antes,transformacion,(640,480))
        despues = Image(conDistorsion, cv2image=True)
    return (despues)

# --------------------------------------------


def ajustarColor_RAM(fichero):

    '''Aplicamos un ajuste a cada imagen de la partida para realzar
    los colores y facilitar las detecciones. Ahora mismo funciona para
    iluminaciones pobres o muy pobres, es posible que requiera ajustes
    cuando se someta a otras condiciones de iluminación'''
    
    original = fichero.getNumpyCv2()
    customFilter =  np.float32([[0,1,0],
                                [0,1,0],
                                [0,1,0]])

    ajuste = customFilter/1

    corregida = cv2.filter2D(original,-1,ajuste)
    fichero = Image(corregida,cv2image=True)
    return (fichero)
# --------------------------------------------

def funcionNula(ficheroSimpleCV):

    '''convierte un fichero SimpleCV en OpenCV y despues lo vuelve a
    convertir en SimpleCV, todo ello sin aplicar ningun efecto o
    tratacimento a la imagen. Esto es necesarios porque las
    transformaciones de numpy (en windows) me voltean la matriz de
    la imagen al convertir entre simpleCV y OpenCV. Aplicar  una nueva
    conversion  'nula' (sin efectos) a la imagen corrige dichos problemas'''
    
    OpenCV = ficheroSimpleCV.getNumpyCv2()
    ficheroSimpleCV = Image(OpenCV, cv2image=True)
    return (ficheroSimpleCV)
# --------------------------------------------

def calcularAnguloLaser(x,y):
    catetoX_ALFA = posteDistanciaY + y   
    catetoY_ALFA = x
    angulo_ALFA = atan2(catetoY_ALFA, catetoX_ALFA) #Ojo, RADIANES. usar la funcon 'atan2' que si posiciona bien los angulos en su cuadrante
    grados_ALFA = degrees (angulo_ALFA)
    hipotenusa_ALFA = (catetoX_ALFA**2 + catetoY_ALFA**2)**0.5
    angulo_BETA = atan2(hipotenusa_ALFA, altura_POSTE) #Ojo, RADIANES
    grados_BETA = degrees (angulo_BETA)

    return grados_ALFA, grados_BETA



# --------------------------------------------
#  FIN DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------


#Establecer medidas del tapete, altura del poste, y distancia del poste al tablero
'''El poste esta situado en la mitad del ancho del tapete y distanciado lo necesario
para que la camara pueda capturarlo completamente'''
#Medidas en centimetros

#variables para contener las coordenadas obtenidas de la posicion del robot (inicializadas en 0,0)
posicionRobotX = 0
posicionRobotY = 0

altura_POSTE = 42   #altura a la que esta situada el puntero laser
posteDistanciaY = 0  #separacion del poste al tapete

tableroANCHO = 42
tableroALTO  = 42
COEFICIENTE_AMPLIACION = 10 #factor para multiplicar los cm del las medidas del tapete 
                            #para conseguir un valor de al menos 400 pixeles y asi disponer 
                            #de buena resolucion de imagen para detectar los blobs

#ajustes para la deteccion del color del robot
COLOR_OBJETIVO = (255, 0, 0)
UMBRAL_BINARIZADO = 0

#establecemos como globales las coordenadas del tapete de juego
'''De esta forma evitamos las repetidas lectura del fichero de coordenadas 
desde el disco en cada ciclo de encuadre, con los retrasos que ello conlleva'''
x1,y1,x2,y2,x3,y3,x4,y4,COLOR_OBJETIVO, UMBRAL_BINARIZADO = cargarDatos() 

print COLOR_OBJETIVO
print UMBRAL_BINARIZADO
##UMBRAL_BINARIZADO = 187
# Activar si se ejecuta en linux para evitar errores de conversion entre simpleCV y OpenCV que se producen en windows
runInLinux = False 


# Niveles de detalle en la muestra/guardado de informacion de debug
guardar_detalles_encuadre = False # Guarda el tablero encuadrado y ajustado de color
mostrar_detalles_simples = True # Muestra en consola direccio y posicion del robot y angulos del sistema laser
mostrar_detalles_completos = False # muestra ademas los detalles de los blobs que forman el robot
visionRobot = True # Guarda fichero con los blobs marcados en colores +  'mostrar_detalles_simples'



# BUCLE PRINCIPAL PARA ANALIZAR EL TAPETE
# carga de la pizarra negra para hacer los circulos de superposicion
pizarraVacia = Image('imagenes/pizarraNegra.png')

WebCam = Camera(1) #seleccion de la webcam externa USB
time.sleep(3)  #pausa para que 'caliente' el ccd
img = WebCam.getImage()  #las lecturas tras el primer acceso suelen aparecer en negro
img = WebCam.getImage()  

contador  = 0

while True:
    contador +=1
    
    #capturamos el fotograma de la webcam sobre el que trataremos de localizar al Robot sobre el tapete
    inicio = time.time()
    img = WebCam.getImage()

    # Llamamos a la funcion que se encarga de encuadrar el tablero
    # previo cambio de resolucion de la imagen a 640x480 si fuese necesario
    #img = img.resize(640,480)
    tableroReal = img
    tableroEncuadrado = encuadrar_RAM(img, 1)

    #ajuste de color para realzar rojos, azules, verdes y amarillos
##    tableroAjustado = ajustarColor_RAM(tableroEncuadrado) #ojo si me salto el paso de ajustar colo, la imagen queda volteda. (los problemas de 'siempre'
##    img = tableroAjustado

    #si no ajustamos color, hemos de aplicar la transformacion nula
    img = funcionNula(tableroEncuadrado)  


    if runInLinux == True:
        img.save ('temp/tempFile.png')
        img = Image('temp/tempFile.png')    

    if guardar_detalles_encuadre == True:
        img.save ('temp/tablero_encuadrado%02d.png' %(contador))


    # Detección del robot (o cualquier otro objeto sobre el tablero)
    robot_filter = img.colorDistance(COLOR_OBJETIVO)#.invert()
    robot_filter = robot_filter.binarize(UMBRAL_BINARIZADO)#.invert()
    blobs_Robot = robot_filter.findBlobs()

    #Solo procedemos a calcular posicioners y angulos si existen candidatos a robot
    if blobs_Robot and len(blobs_Robot) >=2: 
        culo_ROBOT = blobs_Robot.pop()   #el blob mas grande es el culo 
        cabeza_ROBOT = blobs_Robot.pop() #el blob pequeño es la cabeza

        #trasladamos las coordenadas a unos ejes en el centro de la imagen
        ofssetX = int((tableroANCHO * COEFICIENTE_AMPLIACION) /2)
        ofssetY = int((tableroALTO * COEFICIENTE_AMPLIACION) /2)

        cabezaX = cabeza_ROBOT.x - ofssetX
        cabezaY = ofssetY - cabeza_ROBOT.y

        culoX = culo_ROBOT.x - ofssetX
        culoY = ofssetY - culo_ROBOT.y

        #Posicion del robot
        X_ROBOT = culoX +int((cabezaX - culoX)/2)
        Y_ROBOT = cabezaY + int((culoY - cabezaY)/2)

        #Orientacion del robot
        angulo_ROBOT = atan2(cabezaY - culoY, cabezaX - culoX) #Ojo, RADIANES
        grados_angulo_ROBOT = degrees (angulo_ROBOT)

        #trasladar las coodenadas aun eje propicio para el calculo de los angulos de giro para el laser
        #dichos ejes estaran situados:
        # X: en la extremo  horizontal del tapete mas cercano al poste
        # Y: la vertical que pasa por el centro del tapete
        posicionLaserX = X_ROBOT
        posicionLaserY = Y_ROBOT + ofssetY
        alfa, beta = calcularAnguloLaser(posicionLaserX/COEFICIENTE_AMPLIACION, posicionLaserY/COEFICIENTE_AMPLIACION)
        fin = time.time()
        tiempo = fin-inicio

        if mostrar_detalles_completos == True:
            print 'numero de blobs RUIDO:   ', len(blobs_Robot)
            print'------ DATOS ROJO ---------'
            print 'angulo 1:   ', cabeza_ROBOT.angle()
            print 'longitud 1: ', cabeza_ROBOT.length()
            print 'centro 1:   ', cabeza_ROBOT.x, cabeza_ROBOT.y
            print 'AREA 1:     ', cabeza_ROBOT.area()
            print
            print'------ DATOS AZUL ---------'
            print 'angulo 2:   ', culo_ROBOT.angle()
            print 'longitud 2: ', culo_ROBOT.length()
            print 'centro 2:   ', culo_ROBOT.x, culo_ROBOT.y
            print 'AREA 2:     ', culo_ROBOT.area()
            print'========================'
            print'\n'

        if visionRobot == True:
            cabeza_ROBOT.drawOutline(color=(255,0,0), alpha=255, width=3, layer=None)
            culo_ROBOT.drawOutline(color=(0,0,255), alpha=255, width=3, layer=None)
            robot_filter.save('temp/piezasDeColores.png')

        if mostrar_detalles_simples == True or visionRobot == True:
            print 'Tiempo total invertido: ', tiempo            
            print '** ROBOT APUNTANDO HACIA : ', grados_angulo_ROBOT
            print '** ROBOT COORDENADAS,    X: ', X_ROBOT, ', Y: ',Y_ROBOT
            print 'angulos sistema LASER:'
            print 'motor Horizontal: ', alfa
            print 'motor Vertical  : ', beta
            print'================================'
            time.sleep(9) #pausa para tenr tiempo de ver imagenes y datos en pantalla



                



