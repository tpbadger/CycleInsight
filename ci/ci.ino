//GLOBALS
# define WHEEL_DIAMETER 3; //Set wheel diameter
# define WHEEL_CIRC WHEEL_DIAMETER*PI; //Calc and set wheel circumference


//VARIABLES
// For cadence monitoring
 volatile byte crank_rot;
 unsigned long passed_time;
 unsigned int cadence;
 

 // For distance monitoring
 unsigned long wheel_rot;
 unsigned long distance;

//SETUP 
 void setup()
 {
   Serial.begin(115200);
   attachInterrupt(digitalPinToInterrupt(2), distance_detect, RISING);//Initialize the intterrupt pin for distance (Arduino digital pin 1)
   attachInterrupt(digitalPinToInterrupt(3), cadence_detect, RISING);//Initialize the intterrupt pin for cadence (Arduino digital pin 2)

   //Initialise variable values
   wheel_rot = 0;
   distance = 0;

   passed_time = 0;
   crank_rot = 0;  
   cadence = 0; 
 }

//MONITORING
  void distance_detect() {
  wheel_rot ++; //update wheel_rot when called
 }

 void cadence_detect() {
  crank_rot ++; //update crank_rot when called
 }

//LOOP
 void loop()//Measure RPM
 {
  delay(1000); //Update readings every second

  detachInterrupt(2) //detach distance interupt 
  distance = (wheel_rot * WHEEL_CIRC)/1000; //calculate distance (km)
  Serial.print('Distance = ');
  Serial.println(distance); //Print distance to serial
  attachInterrupt(digitalPinToInterrupt(2), distance_detect, RISING);//Initialize the intterrupt pin for distance (Arduino digital pin 1) //reattach distance interupt

  detachInterrupt(3); //detach cadence interupt

  cadence = 60*1000/(millis() - passed_time)*crank_rot; //calculate cadence using tachometer equation
  passed_time = millis(); //update passed time   
  crank_rot = 0; //reset crack_rot
  Serial.print('Cadence = ');
  Serial.println(cadence); //Print cadence to serial

  attachInterrupt(digitalPinToInterrupt(3), cadence_detect, RISING);//Initialize the intterrupt pin for cadence (Arduino digital pin 2) //reattach cadence interupt
 }
 



