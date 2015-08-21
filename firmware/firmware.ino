#include <DigiUSB.h>

#define LED 1
#define BUFSIZE 100
char buf[BUFSIZE+1];

void setup() {
  buf[BUFSIZE+1] = '\0';  \\ just guard
  pinMode(LED, OUTPUT);
  digitalWrite(LED,HIGH);
  DigiUSB.begin();
}


int usbread1() {
    while (!DigiUSB.available()) {
      DigiUSB.refresh();
      digitalWrite(LED, !digitalRead(LED));  
    }
    return DigiUSB.read();
}


char* usbread() {
  int ptr = 0, c;
  while (ptr < BUFSIZE) {
    c = usbread1();
    buf[ptr++] = c; 
    if (c=='\0') {
      break; }
  }
  
  return buf;
}


void usbwrite1(char c) {
    DigiUSB.write(c);
    DigiUSB.refresh();   
}


void usbwrite(char* s) {
  char* ptr = s;
  do {
    usbwrite1(*ptr);
  } while (*ptr++ != '\0');
}


void loop() {
  char* s = usbread();
  usbwrite(s);
}

