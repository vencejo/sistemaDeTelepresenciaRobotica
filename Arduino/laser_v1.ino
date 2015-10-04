 /*
 #         _\|/_
 #         (O-O)
 # -----oOO-(_)-OOo------------------------------
 
 #################################################
 # ********************************************* #
 # *                                           * #
 # *      Autor: Eulogio López Cayuela         * #
 # *                                           * #
 # *    Versión 0.2    Fecha: 03/10/2015       * #
 # *                                           * #
 # ********************************************* #
 #################################################
 
 Conexiones:
 Motor Servo --> pin 12
 */
 
#include <Servo.h> //utilizamos la libreria estandar

#define servoVerticalPin 8
#define servoHorizontalPin 9
#define paso 2

Servo servo01;
Servo servo02;

void setup(){
  Serial.begin(9600);
  
  pinMode(servoVerticalPin, OUTPUT);
  servo01.attach(servoVerticalPin);
  servo01.write(0);
  
  pinMode(servoHorizontalPin, OUTPUT); 
  servo02.attach(servoHorizontalPin);
  servo02.write(0);
}

void loop(){ 
  leerPuertoSerie();  
}
  

//-------------------------------------------------------

/*
  Funcion para atender ordenes a través del puerto serie

*/
void leerPuertoSerie(){
  int dato1;
  int dato2;
  
  if (Serial.available() > 0) {
    dato1 = Serial.parseInt();
    if (dato1 < 20) dato1=20;
    if (dato1 >160) dato1=160;
    dato2 = Serial.parseInt();
    if (dato2 < 20) dato2=20;
    if (dato2 >160) dato2=160;
    int basura = Serial.parseInt();
    Serial.println(dato1);
    Serial.println(dato2);
    Serial.println(basura);
    moverMotor(dato1,dato2);
  }
}

/*
  Funcion para mover el motor
*/
void moverMotor(int angulo1,int angulo2){
  
  //Movimiento del servo1
  int i;
  int posicionServo1Actual = servo01.read();
  
  if (posicionServo1Actual > angulo1) {
    for (i=posicionServo1Actual; i >= angulo1; i -= paso){
      servo01.write(i);
      delay(12);
    }
  }
  else{ 
    for (i=posicionServo1Actual; i <= angulo1; i += paso){
      servo01.write(i);
      delay(12);
    } 
  }  

  //Movimiento del servo2
  int j;
  int posicionServo2Actual= servo02.read();
  
  if (posicionServo2Actual > angulo2) {
    for (j=posicionServo2Actual; j >= angulo2; j -= paso){
      servo02.write(j);
      delay(12);
    }
  }
  else{ 
    for (j=posicionServo2Actual; j <= angulo2; j += paso){
      servo02.write(j);
      delay(12);
    } 
  }
}


