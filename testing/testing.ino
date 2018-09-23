volatile byte detects;


void magDetect() {
    detects++;
    Serial.println("detected");
}


void setup() {
    Serial.begin(115200);
    attachInterrupt(digitalPinToInterrupt(2), magDetect, RISING);//Initialize the intterrupt pin for distance (Arduino digital pin 1)
    detects = 0;
}

void loop() {
    delay(1000);
    Serial.print("Detected :");
    Serial.println(detects);
}
