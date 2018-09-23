//GLOBALS
# define WHEEL_DIAMETER 0.68 //Set wheel diameter
# define WHEEL_CIRC WHEEL_DIAMETER*PI //Calc and set wheel circumference


//VARIABLES
// For cadence monitoring
volatile byte crank_rot;
unsigned long passed_time;
unsigned int cadence;


// For distance monitoring
unsigned long wheel_rot;
double distance;

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

  //  detachInterrupt(2); //detach distance interupt
  
  distance = (wheel_rot * WHEEL_CIRC); //calculate distance 
  if (distance >= 1000) 
  {
    Serial.print("Distance (km) = ");
    Serial.println(distance/1000); //Print distance to serial    
  }
  else 
  {
    Serial.print("Distance (m) = ");
    Serial.println(distance); //Print distance to serial  
  }
    
  //  attachInterrupt(digitalPinToInterrupt(2), distance_detect, RISING);//Initialize the intterrupt pin for distance (Arduino digital pin 1) //reattach distance interupt

  //  detachInterrupt(3); //detach cadence interupt
  if (crank_rot >= 5)
  {
    cadence = 30 * 1000 / (millis() - passed_time) * crank_rot;
    passed_time = millis();
    crank_rot = 0;
    Serial.print("Cadence = ");
    Serial.println(cadence, DEC); //Print cadence to serial
  }
  else
  {
    Serial.println("Pedal to get cadence reading"); //Print cadence to serial
  }  

  //  attachInterrupt(digitalPinToInterrupt(3), cadence_detect, RISING);//Initialize the intterrupt pin for cadence (Arduino digital pin 2) //reattach cadence interupt
}
