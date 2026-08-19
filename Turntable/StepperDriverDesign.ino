//Draft code with TB6600 Stepper Motor Driver in mind 

#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Constants relating to values associated with Stepper Motor
const long stepsPerRev = 6400; //May need to be changed 
const int indexPerRev = 72; //72 * 5 degrees = 360 degrees 
const int stepDelay = 100; //May need to be changed

//Connected to the driver 
const int stepPin = 7;
const int dirPin = 8;

//Identifies later the exact quantity necessary to move for precision
long targetStep = 0;
long stepsToMove = 0;

//Current positions of stepper motor
long currentStep = 0;
int currentIndex = 0;
float currentAngle = 0.00;

//Booleans 
bool homing = false;
bool homed = false;
bool sweep = false;

//Buttons 
const int homePin = A2; //refers to blue push button
const int movePin = A3; //refers to green push button
const int flagPin = A0; //refers to optical sensor/white push button
const int resetPin = A1; //refers to red push button

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
  Serial.println("Press home button, then flag button to begin.");
  
 //Inputs 
  //sets all buttons as INPUT_PULLUP which means the Arduino board creates a resistance
  //** all inputs are inverted OFF = 1 ON = 0  
  pinMode(homePin, INPUT_PULLUP);
  pinMode(movePin, INPUT_PULLUP);
  pinMode(flagPin, INPUT_PULLUP);
  pinMode(resetPin, INPUT_PULLUP);

//Outputs 
  pinMode(statLED, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop(){
  home();
  pulse();
  checkSweep();
  reset();
}

void moveStepper(long steps){
  if (steps > 0){ //moving foward
    digitalWrite(dirPin, HIGH);
  }
  else{ //prevents moving if already past 360 (from stepsToMove calculation)
    digitalWrite(dirPin, LOW);
    steps = -steps;
  }

  for (long i = 0; i < steps; i++){ //moving step by step until it reaches the amount needed
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelay);

    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelay);
  }
}

void home(){ //if home button is pressed 
  if (digitalRead(homePin) == LOW){
    homing = true; 
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Homing "); 
    digitalWrite(stepPin, HIGH);
    digitalWrite(dirPin, HIGH);

  }
  else if ((digitalRead(flagPin) == LOW) && (homing == true)){
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
    lcd.clear(); 
    lcd.setCursor(0,0);
    lcd.print("Homed "); 
    homed = true;
    homing = false;
  }
}

void pulse(){
  if ((homed == true) && (digitalRead(movePin) == LOW) && (sweep == false)){ 
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Moving "); 

    currentIndex += 1;

    targetStep = (long)((currentIndex * stepsPerRev) / indexPerRev); 
    stepsToMove = targetStep - currentStep;

//ex: currentIndex = 1 stepsPerRev = 51200 indexPerRev = 72 currentStep = 711.1
//(2*51200)/72 = 711.1 
//1422.22 - 711.1 = 711.12
//currentStep is typically close to 711.1 however it may change slightly

    moveStepper(stepsToMove); //calls moveStepper function
    currentStep = targetStep;

    delay(1000); 
    
    measurement();
    delay(1000); 

    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Done");

    currentAngle = 360.0 * currentStep / stepsPerRev;     

    Serial.println("STATUS:");
    Serial.print("Index = ");
    Serial.print(currentIndex);
    Serial.print("  Steps = ");
    Serial.print(currentStep);
    Serial.print("  Angle = ");
    Serial.println(currentAngle);
  } 
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
}

void reset(){
  if (digitalRead(resetPin) == LOW){ //if reset occurs
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Resetting "); 

    while (currentIndex > 0){
      currentIndex -= 1;

      targetStep = (long)(currentIndex * stepsPerRev / indexPerRev);
      stepsToMove = targetStep - currentStep;

      moveStepper(stepsToMove);

      currentStep = targetStep;
      currentAngle = 360.0 * currentStep / stepsPerRev;
    }
    //prevent software discrepancies - may be unnecessary 
    currentIndex = 0;
    currentStep = 0;
    currentAngle = 0.0;
    sweep = false;

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
