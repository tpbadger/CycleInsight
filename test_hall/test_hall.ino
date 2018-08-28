# define WHEEL_DIAMETER 2;
// volatile byte half_revolutions;
// unsigned int rpm;
// unsigned long timeold;
 unsigned int distance;
 unsigned int revs;
 
 void setup()
 {
   Serial.begin(115200);
   attachInterrupt(digitalPinToInterrupt(2), magnet_detect, RISING);//Initialize the intterrupt pin (Arduino digital pin 2)
   distance = 0;
   revs = 0;
 }
 
 void loop()//Measure RPM
 {
   Serial.println(revs);
   Serial.println(distance);
 }
 void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   revs ++;
   distance = distance + WHEEL_DIAMETER;
   Serial.println("detect");
 }
