//Original code written by Jakob Midtun and later edited by Wiktor Rutkowski and Mert Can Sarikaya


#include <Servo.h>

Servo myServoG;
Servo myServoR;

// Servo limit values
const int limGup = 140;
const int limGdown = 70;
const int limRup = 05;
const int limRdown = 85;

// Hall sensor threshold values
const int threshG1 = 490;
const int threshG2 = 510;
const int threshR1 = 525;
const int threshR2 = 525;

// Pin values
const int signalPinIn = 4;
const int signalPinOut = 2;

const int hallG1 = A0;
const int hallG2 = A2;
const int hallR1 = A3;
const int hallR2 = A4;

// Initialize variables
bool open = false;
bool Gflag = false;
bool Rflag = false;

int valHallG1 = 0;
int valHallG2 = 0;
int valHallR1 = 0;
int valHallR2 = 0;

// ################ SETUP ################
void setup() {
  myServoG.attach(9);
  myServoR.attach(6);

  Serial.begin(9600);

  pinMode(signalPinIn, INPUT_PULLUP);
  pinMode(signalPinOut, OUTPUT);

  pinMode(hallG1, INPUT);
  pinMode(hallG2, INPUT);
  pinMode(hallR1, INPUT);
  pinMode(hallR2, INPUT);

  digitalWrite(signalPinOut, LOW);

  // Start unlocked/open
  myServoG.write(limGup);
  myServoR.write(limRup);
}

// ################ LOOP ################
void loop() {
  open = digitalRead(signalPinIn);

  // Read hall sensors
  valHallG1 = analogRead(hallG1);
  valHallG2 = analogRead(hallG2);
  valHallR1 = analogRead(hallR1);
  valHallR2 = analogRead(hallR2);

  // Check if each claw is in the lockable closed position
  bool conditionsOKG = ((valHallG1 < threshG1) && (valHallG2 > threshG2));
  bool conditionsOKR = ((valHallR1 > threshR1) && (valHallR2 > threshR2));

  // Close command is active LOW because signalPinIn uses INPUT_PULLUP
  if (open == false) {

    // Lock green claw only if green claw is physically ready to lock
    if (conditionsOKG) {
      myServoG.write(limGdown);
      Gflag = true;
      Serial.println("Green Claw Locked");
    } else {
      // Green claw is no longer in lockable position
      Gflag = false;
    }

    // Lock red claw only if red claw is physically ready to lock
    if (conditionsOKR) {
      myServoR.write(limRdown);
      Rflag = true;
      Serial.println("Red Claw Locked");
    } else {
      // Red claw is no longer in lockable position
      Rflag = false;
    }

    // Only report closed if both claws are currently confirmed locked
    if (Gflag && Rflag) {
      digitalWrite(signalPinOut, HIGH);
      Serial.println("Gripper Closed");
    } else {
      digitalWrite(signalPinOut, LOW);
    }

  } else {
    // Open command: unlock both claws
    myServoG.write(limGup);
    myServoR.write(limRup);

    Gflag = false;
    Rflag = false;

    digitalWrite(signalPinOut, LOW);

    Serial.println("Gripper Open");
  }

  // Info logging
  Serial.print("Hall effect Red1: ");
  Serial.println(valHallR1);
  Serial.print("Hall effect Red2: ");
  Serial.println(valHallR2);
  Serial.print("Hall effect Green1: ");
  Serial.println(valHallG1);
  Serial.print("Hall effect Green2: ");
  Serial.println(valHallG2);
  Serial.print("Gripper open command: ");
  Serial.println(open);
  Serial.print("Green lockable: ");
  Serial.println(conditionsOKG);
  Serial.print("Red lockable: ");
  Serial.println(conditionsOKR);
  Serial.print("Green locked flag: ");
  Serial.println(Gflag);
  Serial.print("Red locked flag: ");
  Serial.println(Rflag);
  Serial.println("-------------------------------");

  delay(1000);
}
