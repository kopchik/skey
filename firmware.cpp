#include <DigiUSB.h>

#define LED 1
#define BUFSIZE 100
char buf[BUFSIZE];


void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED,HIGH);
  DigiUSB.begin();
}


char* readln() {
  int ptr = 0;
  while (ptr < BUFSIZE) {
    if (!DigiUSB.available()) {
      DigiUSB.refresh();
      continue; }
    int c = DigiUSB.read();
    DigiUSB.refresh();
    if (c=='\n') {
      break; }
    buf[ptr++] = c; 
//    digitalWrite(LED, !digitalRead(LED));
  }
  
  buf[ptr] = '\0';
  return buf;
}


void writeln(char* s) {
  char* ptr = s;
  do {
    DigiUSB.write(*ptr);
    DigiUSB.refresh(); 
    ptr++;
  } while (*ptr != '\0');
  DigiUSB.write('\n');
  DigiUSB.refresh();
}


void loop() {
  char* s = readln();
  DigiUSB.refresh();
  digitalWrite(LED, !digitalRead(LED));
  writeln(s);
}

