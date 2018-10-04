//GLOBALS
# define WHEEL_DIAMETER 0.68 //Set wheel diameter
# define WHEEL_CIRC WHEEL_DIAMETER*PI //Calc and set wheel circumference


//VARIABLES
// For utility
unsigned int elapsed_time;

// For cadence monitoring
volatile byte crank_rot;
unsigned long passed_time;
unsigned int cadence;


// For distance monitoring
unsigned long wheel_rot;
double distance;
String payload;

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

  elapsed_time = 0;

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
  elapsed_time ++;
  distance = (wheel_rot * WHEEL_CIRC); // calculate distance

  cadence = 30 * 1000 / (millis() - passed_time) * crank_rot; // calculate cadence
  passed_time = millis();
  crank_rot = 0;

  payload  = String(distance) + "," + String(cadence) + "," + String(elapsed_time); // send data over serial
  Serial.println(payload); //Print cadence to serial
}
