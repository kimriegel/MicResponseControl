//Used in tangent with TinkerCAD simulation and circuit
//Meant to draft a circuit design for stepper motor + gearbox

#include <LiquidCrystal.h> 
#include <Stepper.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
//Identifies pins associated with the LCD

const long stepsPerRev = 6400;
const int indexPerRev = 72;
const int stepDelay = 100;

long currentStep = 0;
int currentIndex = 0;
float currentAngle = 0.00;

bool homing = false;
bool homed = false;
bool sweep = false;

const int homePin = A0; //refers to push button with brown wiring
const int movePin = A1; //refers to push button with gray wiring
const int flagPin = A2; //refers to push button with white wiring
const int resetPin = A3; //refers to push button with purple wiring

const int directionLED = 10; //refers to blue LED 
//meant to simulate the direction of the Stepper Motor's movement
//when ON = motor is moving foward 
//when OFF = motor is moving backwars
const int stepLED = 8; //refers to red LED 
//meant to simulate when the Stepper Motor is moving 
//when ON = motor is moving
//when OFF = motor is not moving
const int statLED = 9; //refers to green LED 
//meant to simulate measurement time 
//when ON = motor is currently measuring
//when OFF = motor is no longer measuring

void setup(){ 
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("Starting "); 
  lcd.setCursor(0,1);
  lcd.print("Program");
  
  Serial.begin(9600);
  Serial.println("Brown-Wired Button = Home Button");
  Serial.println("Grey-Wired Button = Move Button");
  Serial.println("White-Wired Button = Flag Button");
  Serial.println("Purple-Wired Button = Reset Button");
  Serial.println(" ");
  Serial.println("STATUS: Motor is currently not homed.");
  Serial.println("Press home button, then flag button to begin.");
  
  //sets all buttons as INPUT_PULLUP which means the Arduino board creates a resistance
  //** all inputs are inverted OFF = 1 ON = 0 
  pinMode(homePin, INPUT_PULLUP);
  pinMode(movePin, INPUT_PULLUP);
  pinMode(flagPin, INPUT_PULLUP);
  pinMode(resetPin, INPUT_PULLUP);
  
  pinMode(directionLED, OUTPUT);
  pinMode(stepLED, OUTPUT); 
  pinMode(statLED, OUTPUT); 
}

void measurement(){ //called by pulse() when movement occurs
  digitalWrite(statLED, HIGH);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Measuring "); 
  delay(1500); 
  
  digitalWrite(statLED, LOW);
}

void pulse(){
  if ((homed == true) && (digitalRead(movePin) == LOW) && (sweep == false)){ 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Moving "); 
  	digitalWrite(stepLED, HIGH);
  	delay(1000); 
    
  	digitalWrite(stepLED, LOW);
  	measurement();
  	delay(1000); 
    lcd.clear();
 	lcd.setCursor(0,0);
  	lcd.print("Done");
    currentIndex += 1; //will have a total 72 indexes b/c 72 * 5 degrees = 360 degrees 
    currentStep += 89; //estimate for amount of steps taken if 6400
    //steps per revolutions at 360 degrees 
	currentAngle = (360 * currentStep/stepsPerRev);     
    Serial.println("STATUS:");
  	Serial.print("Index = ");
	Serial.print(currentIndex);
	Serial.print("  Steps = ");
	Serial.print(currentStep);
	Serial.print("  Angle = ");
	Serial.println(currentAngle);
  } 
  else{}
}

void checkSweep(){
  if (currentIndex == indexPerRev){
    sweep = true; 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Revolution Completed "); 
    lcd.setCursor(0,1);
  	lcd.print("Must Reset ");
  }
  else{}
}

void direction(){
  if (sweep == false){ //if not one full revolution
    digitalWrite(directionLED,HIGH); //remain in forward state
  }
  else{ //if one full revolution occurs
  digitalWrite(directionLED,LOW); //in reverse state
  }
  if (digitalRead(resetPin) == LOW){ //if reset occurs
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Resetting "); 
    while (currentIndex > 0){ //while the value is not at 0
     digitalWrite(directionLED, LOW);
     digitalWrite(stepLED, HIGH);
     delay(1000);
     digitalWrite(stepLED, LOW);
     delay(1000); 
     currentIndex -= 1; //go down until index is at 0
     currentStep -= 89;
	 currentAngle = (360 * currentStep/stepsPerRev);     
    }
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Done "); 
    Serial.println("STATUS:");
  	Serial.print("Index = ");
	Serial.print(currentIndex);
	Serial.print("  Steps = ");
	Serial.print(currentStep);
	Serial.print("  Angle = ");
	Serial.println(currentAngle);
  }
} 

void home(){
  if (digitalRead(homePin) == LOW){ //if home button is pressed 
    digitalWrite(stepLED, HIGH); //to simulate the motor spinning
    homing = true; 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Homing "); 
  }
  else if ((digitalRead(flagPin) == LOW) && (homing = true)){ //if flag button is pressed
    	lcd.clear(); 
    	lcd.setCursor(0,0);
  		lcd.print("Homed "); 
    	homed = true;
    	digitalWrite(stepLED, LOW); //motor stops spinning and is now in 0 degree position
    }
   }    
                      
void loop(){ //constantly loops so that everytime a button is pressed
  //one of these four functions "respond" 
  home();
  direction();
  pulse();
  checkSweep();
}  
