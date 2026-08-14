//Draft of code required for Stepper Motor 

#include <LiquidCrystal.h> 
#include <Stepper.h>
//Libraries necessary for program

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
//Identifies pins associated with the LCD

//Constants relating to values associated with Stepper Motor
const long stepsPerRev = 6400; //change to accommodate the stepper motor driver  
const int indexPerRev = 72;
const int stepDelay = 100;
const int stepSpeed = 30; //30 RPM subject to change

//Identifies later the exact quantity necessary to move for precision
long targetStep = 0.0;
long stepsToMove = 0.0;
//long targetStep = (long)((currentIndex + 1) * stepsPerRev / indexPerRev);
//long stepsToMove = targetStep - currentStep;

//Current positions of stepper motor
long currentStep = 0;
int currentIndex = 0;
float currentAngle = 0.00;

Stepper stepper = Stepper(stepsPerRev, 7, 8, 9, 10); //may be replaced depending on driver type
//Identifies pins associated with Stepper Motor 

//Booleans 
bool homing = false; //Is it in the process of homing?
bool homed = false; //Is it already homed?
bool sweep = false; //Has it reached a full rotation? 

//Buttons 
const int homePin = A0; //refers to blue push button
const int movePin = A1; //refers to green push button
const int flagPin = A2; //refers to optical sensor/white push button
const int resetPin = A3; //refers to red push button

//LED
const int statLED = A4; //refers to blue LED 
//when ON = motor is currently measuring
//when OFF = motor is no longer measuring

void setup(){ 
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("Starting "); 
  lcd.setCursor(0,1);
  lcd.print("Program");
  
  Serial.begin(9600);
  Serial.println("Blue Button = Home Button");
  Serial.println("Green Button = Move Button");
  Serial.println("White Button = Flag Button");
  Serial.println("Red Button = Reset Button");
  Serial.println(" ");
  Serial.println("STATUS: Motor is currently not homed.");
  Serial.println("Press home button, then flag button to begin."); //EDIT after optical sensor inputted 
  
  //sets all buttons as INPUT_PULLUP which means the Arduino board creates a resistance
  //** all inputs are inverted OFF = 1 ON = 0 
  pinMode(homePin, INPUT_PULLUP);
  pinMode(movePin, INPUT_PULLUP);
  pinMode(flagPin, INPUT_PULLUP);
  pinMode(resetPin, INPUT_PULLUP);

  pinMode(statLED, OUTPUT);

  stepper.setSpeed(stepSpeed);
}

void loop(){ //constantly loops so that everytime a button is pressed
  //one of these four functions "respond" 
  home();
  pulse();
  checkSweep();
  reset();
}  

void home(){
  if (digitalRead(homePin) == LOW){ //if home button is pressed 
    homing = true; 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Homing "); 
  }
  else if ((digitalRead(flagPin) == LOW) && (homing == true)){ //if flag button is pressed
    lcd.clear(); 
    lcd.setCursor(0,0);
  	lcd.print("Homed "); 
    homed = true;
  }
}              

void pulse(){
  if ((homed == true) && (digitalRead(movePin) == LOW) && (sweep == false)){ 
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Moving "); 

    targetStep = (long)((currentIndex + 1) * stepsPerRev / indexPerRev);
    stepsToMove = targetStep - currentStep;

  	stepper.step(stepsToMove);
    currentStep = targetStep;
  	delay(1000); //REVIEW delays 
    
  	measurement();
  	delay(1000); 

    lcd.clear();
 	  lcd.setCursor(0,0);
  	lcd.print("Done");

    currentIndex += 1; 
	  currentAngle = (360.0 * currentStep/stepsPerRev);     

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

void measurement(){ //called by pulse() when movement occurs
  digitalWrite(statLED, HIGH);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Measuring "); 
  delay(1500); //REVIEW delays 
  digitalWrite(statLED, LOW);
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

void reset(){
  if ((digitalRead(resetPin) == LOW)){ //if reset occurs
    lcd.clear();
    lcd.setCursor(0,0);
  	lcd.print("Resetting "); 
    while (currentIndex > 0){
    currentIndex -= 1;

    targetStep = (long)(currentIndex * stepsPerRev / indexPerRev);
    stepsToMove = targetStep - currentStep;

    stepper.step(stepsToMove);

    currentStep = targetStep;
    currentAngle = 360.0 * currentStep / stepsPerRev;
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

    //may need to set everything to 0 to prevent software error 

    sweep = false; 
  }
} 
