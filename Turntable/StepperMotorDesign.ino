//Draft of code required for Stepper Motor 

#include <LiquidCrystal.h> 
#include <Stepper.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
//Identifies pins associated with the LCD

const long stepsPerRev = 6400;
const int indexPerRev = 72;
const int stepDelay = 100;
const int stepSpeed = 30; //30 RPM subject to change

long currentStep = 0;
int currentIndex = 0;
float currentAngle = 0.00;

bool homing = false;
bool homed = false;
bool sweep = false;

const int homePin = A0; //refers to push button with brown wiring
const int movePin = A1; //refers to push button with gray wiring
const int flagPin = A2; //refers to optical sensor with white wiring
const int resetPin = A3; //refers to push button with purple wiring

Stepper stepper = Stepper(stepsPerRev, 7, 8, 9, 10);

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
  
  stepper.setSpeed(stepSpeed);
}

void measurement(){ //called by pulse() when movement occurs
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Measuring "); 
  delay(1500); 
  }

void pulse(){
  if ((homed == true) && (digitalRead(movePin) == LOW) && (sweep == false)){ 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Moving "); 
  	stepper.step(89);
  	delay(1000); 
    
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
    //digitalWrite(directionLED,HIGH); //remain in forward state
  }
  else{ //if one full revolution occurs
  //digitalWrite(directionLED,LOW); //in reverse state
  }
  if (digitalRead(resetPin) == LOW){ //if reset occurs
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Resetting "); 
    while (currentIndex > 0){ //while the value is not at 0
     stepper.step(-89);
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
    }
   }    
                      
void loop(){ //constantly loops so that everytime a button is pressed
  //one of these four functions "respond" 
  home();
  direction();
  pulse();
  checkSweep();
}  
