#-*- coding: UTF-8 -*-

#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo-----------------------------------------------


#################################################################
# ************************************************************* #
# *                 CALIBRACION  MODO REAL                    * #
# *             Autor:  Eulogio López Cayuela                 * #
# *                                                           * #
# *            Versión 1.0    Fecha: 03/10/2015               * #
# *                                                           * #
# ************************************************************* #
#################################################################

'''
Modulo de calibracion de camara y tapete de juego
'''


import json
'''
Abre el archivo en el editor de Python. Al principio del código
debes importar las bibliotecas JSON. Escribe el siguiente código para
importarlas: import json

Carga los valores de JSON. JSON utiliza un array de pares clave-valor.
El siguiente código carga un array de JSON con dos pares clave-valor:
array = json.load( { "name": "Joe", "address": "111 Street" } );

Recupera uno de los valores de JSON. Utiliza el nombre clave del array
de JSON para recuperar el valor. El código siguiente recupera el
"name" del array de JSON y lo asigna a la variable "name": name =
array['name']

Imprime el valor en la pantalla. Por lo general, debes imprimir el
resultado del array de JSON en la pantalla del usuario. El código
siguiente imprime en la pantalla: print name

'''

import pygame, sys  #, random
from SimpleCV import Camera, Image, cv2
import time
from pygame.locals import *

try:  
    import cPickle as pickle  
except ImportError:  
    import pickle  

import numpy as np
    
# Definición de algunas constantes generales





# ---------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# ---------------------------------------------


FPS = 40 # establece el maximo de ciclos por segundo del programa
ANCHO_PANTALLA = 640
ALTO_PANTALLA = 480

SCREEN_RESIZE = 0
SCREEN_COLOR_BITS = 32

##valorLevel = 0



# Bloque de definicion de colores con nombres para facilitar su uso.
COLOR_BLANCO = (255, 255, 255)
COLOR_BLANCO_SUCIO = (150, 150, 150) # Color Blanco sucio.
COLOR_NEGRO = (0, 0, 0)
COLOR_NEGRO_SUCIO = (35, 25, 35) # Color Gris oscuro casi negro.
COLOR_ROJO = (255, 0, 0)
COLOR_ROJO_OSCURO = (175, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_AZUL_OSCURO = (0, 0, 170)
COLOR_AZUL_CIELO = (45, 180, 235)
COLOR_AMARILLO = (255,255,0)
COLOR_ROSA = (255,0,210) # Color Rosa vivo.


BACKGROUND_COLOR = COLOR_NEGRO

# inicializar valores del juego
cogerObjeto = False
tecla_CONTROL = False
primerClick = False
segundoClick = False
leftButton = False
mmiddleButton = False
rightButton = False
index = 0 #indice utilicado para localizar a los controles de volumen



nivel_R = 0
nivel_G = 0
nivel_B = 0
UMBRAL_BINARIZADO = 0


# --------------------------------------------
# FIN DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# --------------------------------------------







# --------------------------------------------
#  INICIO DEL BLOQUE DE DEFINICIÓN DE CLASES
# --------------------------------------------
class miControlDeslizante:
    def __init__(self, posicion, size, indice, componentes, minVal=0, maxVal=255):
        self.size = size
        self.x = posicion[0]
        self.y = posicion[1]
        self.componentes = componentes
        self.valorLevel = 0
        self.minimoValor = minVal
        self.maximoValor = maxVal
        #Definicion de los elementos del control de volumen
        # * Barra
        self.barra = self.componentes[0] #diccionario que contiene la barra
        self.barraImage = self.barra['surface'] #palabra 'surface' con la imagen de la barra
        self.barraImage = pygame.transform.scale(self.barraImage, (int(self.size), int(4)))
        self.barraRect = self.barraImage.get_rect() #obtencion del -rect- al crear objeto
        self.barraRect.width = size
        self.barraRect.left = self.x #asignacion de su posicion x propia
        self.barraRect.centery = self.y #asignacion de su posicion y propia
        # * Cursor
        self.cursor = self.componentes[1] #diccionario que contiene el cursor
        self.cursorImage = self.cursor['surface']
        self.cursorRect = self.cursorImage.get_rect()
        self.cursorRect.left = self.x
        self.cursorRect.centery = self.y

        self.recorrido = self.barraRect.width - self.cursorRect.width

    def draw(self, screen):
        screen.blit( self.barraImage, self.barraRect)
        screen.blit( self.cursorImage, self.cursorRect)


    # Metodos para los controles
    def cambiarValor(self):
        self.cursorPos = self.cursorRect.left - self.barraRect.left
        self.valorLevel = int((self.cursorPos*self.maximoValor/self.recorrido))
        if self.valorLevel < self.minimoValor:
            self.valorLevel = self.minimoValor
##        print(self.cursorPos)
##        print(self.recorrido)
##        print(self.valorLevel)
##        print(self.cursorRect.left)
##        print(self.barraRect.left)
##        
##        print('-------------')
        

# --------------------------------------------
#    FIN DEL BLOQUE DE DEFINICIÓN DE CLASES
# --------------------------------------------
            


# --------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE FUNCIONES 
# --------------------------------------------

# --------------------------------------------
def dibujar_Textos(text, size,color, surface, x, y, center = 0):
    textobj = size.render(text, 1, color,(0,0,0))
    textrect = textobj.get_rect()
    if center == 1 or center == 'center':
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = y
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# --------------------------------------------

def marcarPunto(posicion):
    global rx, ax
    ''' creaccion de marcas para las esquinas seleccionadas '''
    if paso1 == True:
        rect = imagenMarca.get_rect()
        rect.centerx = posicion[0]
        rect.centery = posicion[1]
        nuevaMarca = (imagenMarca, rect)
        marcas.append(nuevaMarca)
    return ()
# --------------------------------------------

def localizarEsquinas(esquinasDesordenadas):

    '''Para poder situar bien el tablero hemos de conocer cada
    esquina. Como es posible que el usuario no realice siempre un
    mismo orden el la seleccion de dichas esquinas durante el proceso
    de calibracion, esta funcion se encarga de identificarlas y
    ordenarlas para su correcto manejo por parte de la funcion
    -encuadrar()-'''
    
    esquinas = esquinasDesordenadas[:]
    global listaOrdenada
    listaOrdenada = []
    pasadas = len(esquinas)
    j = 0
    while j < pasadas:
        ref = esquinas.pop()
        i = 0
        while i < len(esquinas):
            if esquinas[i][0] < ref[0]:
                temp = ref         #salvamos el valor de referencia
                ref = esquinas[i]  #cargamos referencia con el siguiente valor de la lista
                esquinas[i] = temp #y ponemos en su lugar la copia de ref salvada previamente 
            i +=1
        listaOrdenada.append(ref)
        j +=1
    p1 = listaOrdenada[0]
    p2 = listaOrdenada[1]
    p3 = listaOrdenada[2]
    p4 = listaOrdenada[3]

    #segunda pasada para comprobar la perspectiva (cerrada o abierta)    
    if p2[1] < p1[1]:
        temp = p1
        p1 = p2
        p2 = temp
    if p4[1] < p3[1]:
        temp = p3
        p3 = p4
        p4 = temp
    listaOrdenada = [p1,p2,p3,p4]
    
    print 'Sup Izq: ', p1[0],p1[1]
    print 'Sup Der: ', p3[0],p3[1]
    print 'Inf Izq: ', p2[0],p2[1]
    print 'Inf Der: ', p4[0],p4[1]
##    salvarDatos(listaOrdenada)    
    global x1,y1,x2,y2,x3,y3,x4,y4
    x1,y1,x2,y2,x3,y3,x4,y4 = p1[0],p1[1],p3[0],p3[1],p2[0],p2[1],p4[0],p4[1]
    return #listaOrdenada p1[0],p1[1],p3[0],p3[1],p2[0],p2[1],p4[0],p4[1]
# --------------------------------------------

def salvarDatos(datos, fileName='calibracion.dat'):
    ''' Salvado de datos a fichero '''
     
    ficheroDatos = open(fileName, "wb")
    pickle.dump(datos, ficheroDatos, protocol=-1) # -1, seleccion automatica del más alto disponible  
    ficheroDatos.close()
    return()
# --------------------------------------------

def finalizarPrograma():
    pygame.quit()
    sys.exit()
    
# --------------------------------------------
def comprobarControlDeslizable(posicion,listaObjetos):
    '''
    En cada llamada 'traemos' la -lista de objetos Seleccionables- y las -coordenadas del raton-
    Comprueba si al hacer click con el ratón en esas coordenadas
    hay un objeto perteneciente a la lista 'ObjetosSeleccionables'.
    '''
    x = posicion[0]
    y = posicion[1]
    for objeto in listaObjetos:        
        rect = objeto.cursorRect
        if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
            return(objeto)

    return(False)
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
#  FIN DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------


# ********************************************
#           INICIO DEL PROGRAMA
# ********************************************



# Definir imagenes para el control de volumen
barraImagen = pygame.image.load('imagenes/barradeslizable.png')
barraRect = barraImagen.get_rect()
deslizanteImagen = pygame.image.load('imagenes/mandodeslizante.png')
deslizanteRect = deslizanteImagen.get_rect()


barraDeslizante = {'rect':barraRect,'surface':barraImagen,'index':1003,}
mandoDeslizante = {'rect':deslizanteRect,'surface':deslizanteImagen,'index':1004,}

componentesDeslizador = [barraDeslizante, mandoDeslizante]
control_RED = miControlDeslizante((90, 25),250, 1, componentesDeslizador)
control_GREEN = miControlDeslizante((90, 75),250, 2, componentesDeslizador)
control_BLUE = miControlDeslizante((90,125),250, 3, componentesDeslizador)
control_BINARIZE = miControlDeslizante((90,185),250, 4, componentesDeslizador, 0, 255)


control_RED.valorLevel = nivel_R
control_GREEN.valorLevel = nivel_G
control_BLUE.valorLevel = nivel_B
control_BINARIZE.valorLevel = UMBRAL_BINARIZADO


listaControles = [control_RED, control_GREEN, control_BLUE, control_BINARIZE]

COEFICIENTE_AMPLIACION = 10
tableroANCHO = 42
tableroALTO  = 42
# --------------------------------------------
pygame.init()
mainCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
pygame.display.set_caption(' - PANTALLA DE CALIBRACION - ')
# Definir tipos de letra
font15 = pygame.font.SysFont(None, 15)
font20 = pygame.font.SysFont(None, 20)
font25 = pygame.font.SysFont(None, 25)
font30 = pygame.font.SysFont(None, 30)
font35 = pygame.font.SysFont(None, 35)
font40 = pygame.font.SysFont(None, 40)
font45 = pygame.font.SysFont(None, 45)
font48 = pygame.font.SysFont(None, 48)
font50 = pygame.font.SysFont(None, 50)
font65 = pygame.font.SysFont(None, 65)

# --------------------------------------------



camara = Camera(1)
time.sleep(3)
img = camara.getImage()
img = camara.getImage()
img.save('temp/vistaTapete.png')
imagen_calibracion =  pygame.image.load('temp/vistaTapete.png')


marcas = []
listasDeEsquinas = []
paso1 = True  #el paso 1 es pedir que se marquen las esquinas del tablero
paso2 = False #ajustes para deteccion de color


imagenMarca = pygame.image.load('imagenes/marca.png')

# ********************************************
#           INICIO DEL PROGRAMA
# ********************************************

# Establecer el color del fondo de la pantalla)
SCREEN.fill(COLOR_NEGRO)


# ********************************************
# Bucle principal del programa
# ********************************************

terminarCalibracion = False
while terminarCalibracion == False:

    # Atender eventos de teclado y raton    
    for event in pygame.event.get():
        if event.type == QUIT:
            if paso1 == False: 
                terminarCalibracion = True
                print '============================='
                print '            RED  : ', nivel_R
                print '            GREEN: ', nivel_G
                print '            BLUE : ', nivel_B
                print 'UMBRAL BINARIZADO: ', UMBRAL_BINARIZADO
                print '============================='

                img = Image('temp/vistaTapete.png')
                blobs = img.findBlobs()
                if blobs:
                    print'\nLISTADO DE AREAS DETECTADAS (%0d):' %(len(blobs))
                    for blob in blobs:
                        print blob.area()
                    print '============================='
                global listaOrdenada
                listaOrdenada.append((nivel_R,nivel_G,nivel_B))
                listaOrdenada.append(UMBRAL_BINARIZADO)
                salvarDatos(listaOrdenada,'alldata.dat')


        if event.type == MOUSEBUTTONDOWN:
            leftButton, mmiddleButton, rightButton = pygame.mouse.get_pressed()
            movRelativoX1, movRelativoY1 = pygame.mouse.get_pos()
            item = comprobarControlDeslizable(event.pos, listaControles)
            # Gesion de click sobre objeto Puerta
            if item != False and leftButton == True:
                # * Seleccion de objeto para moverlo, (si se mantiene pulsado el ratón)
                focusRect = item.cursorRect
                x,y = pygame.mouse.get_pos()
                offsetX = x - focusRect.centerx # Distancia x del centro del objeto al puntero del raton
                offsetY = y - focusRect.centery # Distancia y del centro del objeto al puntero del raton
                cogerObjeto = True
        if event.type == MOUSEBUTTONUP:
            movRelativoX2, movRelativoY2 = pygame.mouse.get_pos()
            if movRelativoX2 - movRelativoX1 == 0 and movRelativoY2 - movRelativoY1 == 0:
                primerClick = True
            if segundoClick == True:
                primerClick = False
                segundoClick = False
            cogerObjeto = False

        if event.type == KEYDOWN:
            if event.key == K_DELETE or event.key == K_BACKSPACE:
                if len(marcas)>0:
                    marcas.pop()
                    listasDeEsquinas.pop()


            if event.key == K_RETURN or K_SPACE:
                if len(marcas) == 4 and paso2 == False:
                    paso1 = False
                    localizarEsquinas(listasDeEsquinas)
                    paso2 = True
                
        if event.type == MOUSEBUTTONDOWN:
            posicion = event.pos #pygame.mouse.get_pos()
            if paso1 == True:
                listasDeEsquinas.append (posicion)
                marcarPunto(event.pos)
# --------------------------------------------

    # Borrar la pantalla
    SCREEN.fill(COLOR_NEGRO)
    if paso1 == True:
        img = camara.getImage()
        img.save('temp/vistaTapete.png')
        imagen_calibracion =  pygame.image.load('temp/vistaTapete.png')
        SCREEN.blit(imagen_calibracion, (0,0))

    if paso1 == True and len(marcas) == 0: 
        dibujar_Textos('CALIBRACION ', font30, COLOR_ROJO, SCREEN, 10, 100,'center')
        dibujar_Textos('DE LA PERSPECTIVA', font30, COLOR_ROJO, SCREEN, 10, 130,'center')
        dibujar_Textos('Haz clic sobre las esquinas del tapete',
                       font25, COLOR_BLANCO, SCREEN, 10, 200,'center')
        dibujar_Textos('(pulsa DEL o SUP para borrar puntos)',
                       font25, COLOR_BLANCO, SCREEN, 10, 230,'center')
    if paso1 == True and len(marcas) > 0: 
        dibujar_Textos('pulsa DEL o SUP para borrar puntos',
                       font15, COLOR_ROJO, SCREEN, 5, 20, 'no center')
        if len(marcas) == 4:
            dibujar_Textos('pulsa ENTER o BARRA ESPACIADORA para finalizar',
                           font25, COLOR_VERDE, SCREEN, 10, 260,'center')



    if len(marcas) > 4:
        marcas.pop(-1)
    if paso1 == True:
        for marca in marcas:
            SCREEN.blit(marca[0], marca[1]) # imagen, rect

    if paso1 == False and paso2 == False:
        dibujar_Textos('GRACIAS,', font40, COLOR_AZUL_CIELO, SCREEN, 10, 100,'center')
        dibujar_Textos('CALIBRACION DE TAPETE FINALIZADA', font40, COLOR_AZUL_CIELO, SCREEN, 10, 150,'center')

    if paso2 == True:
        img = camara.getImage()
        nivel_R = control_RED.valorLevel
        nivel_G = control_GREEN.valorLevel
        nivel_B = control_BLUE.valorLevel
        UMBRAL_BINARIZADO = control_BINARIZE.valorLevel
        
        tableroEncuadrado = encuadrar_RAM(img, 1)
        img = funcionNula(tableroEncuadrado)
        
##        img = img.colorDistance((nivel_R, nivel_G, nivel_B))
##        img = img.binarize(UMBRAL_BINARIZADO)
        
        img.save('temp/vistaTapete.png')
        imagen_calibracion =  pygame.image.load('temp/vistaTapete.png')
        SCREEN.blit(imagen_calibracion, (0,0))

        # dibujar los contoles deslizables
        for control_deslizable in listaControles:
            control_deslizable.draw(SCREEN)
            
        # Dibujar Etiquetas(y otros textos)
        dibujar_Textos('(R)   %0d'  %(nivel_R),  font20, COLOR_BLANCO_SUCIO, SCREEN, 10,  15, 0)
        dibujar_Textos('(G)   %0d' %(nivel_G), font20, COLOR_BLANCO_SUCIO, SCREEN, 10,  65, 0)
        dibujar_Textos('(B)   %0d' %(nivel_B),  font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 115, 0)
        dibujar_Textos('BINARIZADO   %0d' %(UMBRAL_BINARIZADO),   font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 160, 0) 

    # Mover Objeto: Si hay objeto Focus seleccionado, moverlo
    if cogerObjeto == True:
        borde = False
        movRelativoX, movRelativoY = pygame.mouse.get_rel()
        posX, posY = pygame.mouse.get_pos()# posicion del raton mientras 'sujeta' un objeto
        focusRect.centerx = (posX-offsetX)
        # comprobar si el objeto rebasa los limites
        if focusRect.left < item.barraRect.left:
            focusRect.left = item.barraRect.left
            borde = True
        if focusRect.right > item.barraRect.right:
            focusRect.right = item.barraRect.right
            borde = True
        if borde == True:
            #pass
            pygame.mouse.set_pos(offsetX + focusRect.centerx, posY)
        item.cambiarValor()    

    # Refresco de la pantalla para regenerar todos los elementos
    pygame.display.update()
    mainCLOCK.tick(FPS)
# --------------------------------------------
#   FIN DEL BUCLE PRINCIPAL DEL PROGRAMA
# --------------------------------------------

    
pygame.quit ()
    
