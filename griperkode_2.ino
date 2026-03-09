#include <Servo.h>

Servo myServoG;
Servo myServoR;
// Grenseverdier
const int limGup = 163;
const int limGdown = 102;
const int limRup = 40;
const int limRdown = 115;

const int threshG1 = 490;
const int threshG2 = 522;
const int threshR1 = 530;
const int threshR2 = 559;

int close = 0;

const int potPin = A0;   // Potentiometer connected to A0
const int signalPinIn = 2;
const int signalPinOut = 4;
int potValue = 0;        // Raw analog value
int angle1 = (limGup+limGdown)/2;           
int angle2 = (limRup+limRdown)/2;

int hallG1 = A0;
int hallG2 = A2;
int hallR1 = A3;
int hallR2 = A4;

int valHallG1 = 0;
int valHallG2 = 0;
int valHallR1 = 0;
int valHallR2 = 0;

void setup() {
  myServoG.attach(9);     // Servo signal pin
  myServoR.attach(6);     // Servo signal pin
  Serial.begin(9600);    // Open Serial Monitor
  // Lytt etter close signal
  pinMode(signalPinIn,INPUT_PULLUP);
  pinMode(signalPinOut,OUTPUT);
  // Detekter input fra Hall-effektsensorer
  pinMode(hallG1,INPUT);
  pinMode(hallG2,INPUT);
  pinMode(hallR1,INPUT);
  pinMode(hallR2,INPUT);
}

void loop() {

  // Sjekk deteksjon
  close = digitalRead(signalPinIn);
  delay(1000);
  // TEST-funksjon åpner/lukker hvert andre sekund dersom kriteriene er møtt

  // if (close == 0){
  //   close = 1;
  // }
  // else {
  //   close = 0;
  // }
  // delay(2000);
  
  valHallG1 = analogRead(hallG1); 
  valHallG2 = analogRead(hallG2);
  valHallR1 = analogRead(hallR1);
  valHallR2 = analogRead(hallR2);

  bool conditionsOKG =
  (valHallG1 < threshG1) &&
  (valHallG2 > threshG2);

  bool conditionsOKR =
  (valHallR1 > threshR1) &&
  (valHallR2 > threshR2);


  if (close == 0){
    if (conditionsOKG == 1){
      delay(200);
      if (conditionsOKG == 1){
        Serial.println("Gripper Green Closed");
        myServoG.write(limGdown);  // Move the servo
    }
    }
    if (conditionsOKR == 1){
      Serial.println("Gripper Red Closed");
      myServoR.write(limRdown);  // Move the servo
    }

    if ((conditionsOKR == 1) && (conditionsOKG == 1)){
      digitalWrite(signalPinOut, 1);
    }
    
    delay(100);

  } else if (close == 1){

    Serial.println("Gripper Open");
    myServoG.write(limGup);  // Move the servo
    myServoR.write(limRup);  // Move the servo
    digitalWrite(signalPinOut,0);
    delay(100);

  }

  Serial.println(valHallR1);
  Serial.println(valHallR2);
  Serial.println(close);
  Serial.println();
  
}
