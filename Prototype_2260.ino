#include <Adafruit_NeoPixel.h>
 
#define PIN       11 // Marked D1 on GEMMA
#define NUM_LEDS 64
 
// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type:
//   NEO_GRB  Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB  Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB);
 
uint32_t color = strip.Color(000, 100, 250); // Change RGB color value here

// These are the pixels in order of animation-- 36 pixels in total:
int sine[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
 
int recv = 0;

int recordKnapp = 2;
int spillAvKnapp = 3;
int recordLys = 4;
int nyMeldingLys = 5;
int spillAvLys = 6;
int muteKnapp = 7;
boolean mute = false;

int ledState = HIGH;         // the current state of the output pin
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 20;    // the debounce time; increase if the output flickers

int ledState1 = HIGH;         // the current state of the output pin
int buttonState1;             // the current reading from the input pin
int lastButtonState1 = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime1 = 0;  // the last time the output pin was toggled
unsigned long debounceDelay1 = 20;    // the debounce time; increase if the output flickers

void setup() {
  pinMode(spillAvKnapp, INPUT);
  pinMode(recordKnapp, INPUT);
  pinMode(recordLys, OUTPUT);
  pinMode(nyMeldingLys, OUTPUT);
  pinMode(spillAvLys, OUTPUT);
  strip.begin();
  strip.show();            // Initialize all pixels to 'off'
  strip.setBrightness(150); // 40/255 brightness (about 15%)
  Serial.begin(9600);
}

void loop(){
  sjekkMute();
  sjekkSpillAvKnapp();
  sjekkRecordKnapp();
}


void sjekkSpillAvKnapp(){
  if(sjekkKnapp()){
    digitalWrite(spillAvLys, HIGH);
    delay(300);
    Serial.println("Start avspilling");
    boolean a = true;
    //stream.readBytes(buffer, length);
    String linje = Serial.readString();
    while(a){
      //String linje = Serial.read()
      if(sjekkKnapp() || linje == "Lydfil ferdig"){
       a = false;
       Serial.println("Stopp avspilling");
       
      }
    }
    digitalWrite(spillAvLys, LOW);
    avLys();
  }
}

void sjekkRecordKnapp(){
//Sjekker om knappen er trykket inn, hvis den er det sender den inn til pcen og tar opp til arduinoen registrerer et nytt knappetrykk
  if(sjekkKnapp1()){
    digitalWrite(recordLys, HIGH);
    Serial.println("Start opptak");
    
    boolean b = true;
    while(b){
      if(sjekkKnapp1()){
       b = false;
       Serial.println("Stopp opptak");
      }
    }
    digitalWrite(recordLys, LOW);
    paaLys();
  }
}


void sjekkMute(){

}

boolean sjekkKnapp(){
  boolean d = false;
  int reading = digitalRead(spillAvKnapp);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
        d = true;
      }
    }
  }
  lastButtonState = reading;
  return d;
}
boolean sjekkKnapp1(){
  boolean c = false;
  int reading1 = digitalRead(recordKnapp);
  if (reading1 != lastButtonState1) {
    lastDebounceTime1 = millis();
  }
  if ((millis() - lastDebounceTime1) > debounceDelay1) {
    if (reading1 != buttonState1) {
      buttonState1 = reading1;

      // only toggle the LED if the new button state is HIGH
      if (buttonState1 == HIGH) {
        c = true;
      }
    }
  }
  lastButtonState1 = reading1;
  return c;
}

void paaLys(){
  for(int i=0; i<13; i++) {
    strip.setPixelColor(sine[i], color);             // Draw 'head' pixel
    //strip.setPixelColor(sine[(i + 12 - 8) % 12], color); // Erase 'tail'
    strip.show();
    delay(40);
  }
}
void avLys(){
  for(int i=0; i<13; i++) {
    //strip.setPixelColor(sine[i], color);             // Draw 'head' pixel
    strip.setPixelColor(sine[(i + 12 - 8) % 12], 0); // Erase 'tail'
    strip.show();
    delay(40);
  }
}




