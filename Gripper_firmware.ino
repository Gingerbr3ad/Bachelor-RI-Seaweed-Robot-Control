//Original code written by Jakob Midtun and later edited by Wiktor Rutkowski and Mert Can Sarikaya


#include <Servo.h>

Servo myServoG;
Servo myServoR;

//Servo limit values
const int limGup = 163;
const int limGdown = 102;
const int limRup = 0;
const int limRdown = 60;

//Hall sensors treshhold values
const int threshG1 = 490;
const int threshG2 = 522;
const int threshR1 = 550;
const int threshR2 = 500;

//Pin values
const int signalPinIn = 2;
const int signalPinOut = 4;

const int hallG1 = A0;
const int hallG2 = A2;
const int hallR1 = A3;
const int hallR2 = A4;

//Initialize variables
bool close = 0;
bool Gflag = false;
bool Rflag = false;

int valHallG1 = 0;
int valHallG2 = 0;
int valHallR1 = 0;
int valHallR2 = 0;

//################SETUP################
void setup() {
  myServoG.attach(9);     //Servo signal pin
  myServoR.attach(6);     //Servo signal pin
  Serial.begin(9600);     //Open Serial Monitor
  
  //Pin configuration
  pinMode(signalPinIn,INPUT_PULLUP);
  pinMode(signalPinOut,OUTPUT);
  
  pinMode(hallG1,INPUT);
  pinMode(hallG2,INPUT);
  pinMode(hallR1,INPUT);
  pinMode(hallR2,INPUT);
}

//################LOOP################
void loop() {
  close = digitalRead(signalPinIn); //Read close command pin
  delay(50);

  //Read hall sensors
  valHallG1 = analogRead(hallG1); 
  valHallG2 = analogRead(hallG2);
  valHallR1 = analogRead(hallR1);
  valHallR2 = analogRead(hallR2);

  //Check if claws closed from hall sensors
  bool conditionsOKG = ((valHallG1 < threshG1) && (valHallG2 > threshG2));
  bool conditionsOKR = ((valHallR1 < threshR1) && (valHallR2 > threshR2));

  //Close the gripper if conditions OK
  if (close == 0){
    if (conditionsOKG == 1){
      myServoG.write(limGdown);  // Move the servo
      Serial.println("Green Claw Closed");
      Gflag = true;
    }
    if (conditionsOKR == 1){
      myServoR.write(limRdown);  // Move the servo
      Serial.println("Red Claw Closed");
      Rflag = true;
    }

    if (Gflag && Rflag){
      digitalWrite(signalPinOut, false);
      Serial.println("Gripper Closed");
      delay(500);
    }

  //Open the gripper if open command on input pin
  } else if (close == 1){
    myServoG.write(limGup);  // Move the servo
    myServoR.write(limRup);  // Move the servo
    digitalWrite(signalPinOut, true);
    Serial.println("Gripper Open");
    delay(500);
  }

  //Info logging
  Serial.print("Hall effect Red1: ");
  Serial.println(valHallR1);
  Serial.print("Hall effect Red2: ");
  Serial.println(valHallR2);
  Serial.print("Hall effect Green1: ");
  Serial.println(valHallG1);
  Serial.print("Hall effect Green2: ");
  Serial.println(valHallG2);
  Serial.print("Gripper close command: ");
  Serial.println(close);
  Serial.print("-------------------------------");
  Serial.println();
  
}