/* @file MultiKey.ino
|| @version 1.0
|| @author Mark Stanley
|| @contact mstanley@technologist.com
||
|| @description
|| | The latest version, 3.0, of the keypad library supports up to 10
|| | active keys all being pressed at the same time. This sketch is an
|| | example of how you can get multiple key presses from a keypad or
|| | keyboard.
|| #
*/

#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //three columns
int BUTTONS = 0;
 
char keys[ROWS][COLS] =
 {{1,2,3,4},
  {5,6,7,8},
  {9,10,11,12},
  {13,14,15,16}};
  
//connect to the row pinouts of the keypad
byte rowPins[ROWS] = {5, 4, 3, 2};

//connect to the column pinouts of the keypad
byte colPins[COLS] = {9, 8, 7, 6};

// number of millisec for considering as HOLD state
int holdTime = 750;

Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

// pressReleaseFactor: 
//  -1 when pressed 
//  1 when released
//  1000 when hold
int pressReleaseFactor;

// keep a track of the lask message send by hitting key
int lastKeyMsg = 0;



// measuring the time for sending info
long sendInfoMeasure1 = 0;
long intervalSendInfo = 2000;

// for saying how many buttons
String informationMessage;

void setup() {
    Serial.begin(9600);
    // initializing the serial comunication
    Serial.println("Initializing of ControlCombo...");
      
    BUTTONS = ROWS * COLS;  
    
    // preparing information message
    informationMessage = String("NB_ROW ") + ROWS + String(" NB_COLUMNS ") + COLS;
      
    // set the ms needed for HOLD status
    kpd.setHoldTime(holdTime);
}


void loop() {

    // sending informations
    sendsInfo();
  
    // Fills kpd.key[ ] array with up-to 10 active keys.
    // Returns true if there are ANY active keys.
    if (kpd.getKeys())
    {
        // Scan the whole key list.
        for (int i=0; i<LIST_MAX; i++)   
        {
            // Only find keys that have changed state.
            if ( kpd.key[i].stateChanged )   
            {
              
                // Report active key state : IDLE, PRESSED, HOLD, or RELEASED
                switch (kpd.key[i].kstate) {  
                    case PRESSED:
                      pressReleaseFactor = -1;
                      break;
                    case HOLD:
                      pressReleaseFactor = 1000;
                      break;
                    case RELEASED:
                      pressReleaseFactor = 1;
                      break;
                   //case IDLE:
                }
                
                // making the message to be sent
                int keyMsg = int(kpd.key[i].kchar) * pressReleaseFactor;
                
                // little patch to prevent multiple release signal
                if(lastKeyMsg != keyMsg){
                  Serial.println(keyMsg);
                  lastKeyMsg = keyMsg;
                }

            } // ending if state changed
        }// ending loop over the pad
    }// ending if getting keys
}  // End loop


// send info like the size of the matrix
void sendsInfo(){

  unsigned long sendInfoMeasure2 = millis();
 
  if(sendInfoMeasure2 - sendInfoMeasure1 > intervalSendInfo) {
    // save the last time you blinked the LED 
    sendInfoMeasure1 = sendInfoMeasure2;   
    Serial.println(informationMessage);
  }
}
