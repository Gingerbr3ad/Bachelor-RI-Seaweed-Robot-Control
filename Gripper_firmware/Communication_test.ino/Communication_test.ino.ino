
// Pin values
const int signalPinIn = 4;
const int signalPinOut = 2;

bool Signal;

// ################ SETUP ################
void setup() {
  Serial.begin(9600);

  pinMode(signalPinIn, INPUT_PULLUP);
  pinMode(signalPinOut, OUTPUT);


  digitalWrite(signalPinOut, LOW);

}

// ################ LOOP ################
void loop() {
  Signal = digitalRead(signalPinIn);


  // Close command is active LOW because signalPinIn uses INPUT_PULLUP
  if (Signal == false) {
      Serial.println("Recieving Close");
      digitalWrite(signalPinOut, HIGH);
      Serial.println("Sending Closed");
  
  } else {
    Serial.println("Recieving Open");
    digitalWrite(signalPinOut, LOW);
    Serial.println("Sending Opened");
  }
  
  Serial.println("-------------------------------");

  delay(1000);
}
