
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
      Serial.println("Recieving HIGH");
      digitalWrite(signalPinOut, HIGH);
      Serial.println("Sending HIGH");
  
  } else {
    Serial.println("Recieving LOW");
    digitalWrite(signalPinOut, LOW);
    Serial.println("Sending LOW");
  }
  
  Serial.println("-------------------------------");

  delay(1000);
}
