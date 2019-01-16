const int ai0 = A0;
const int ai1 = A1;
const int ai2 = A2;
const int ai3 = A3;
const int ai4 = A4;
const int ai5 = A5;

const int ai6 = A6;
const int ai7 = A7;
const int ai8 = A8;
const int ai9 = A9;
const int ai10 = A10;
const int ai11 = A11;

int sv0 = 0;
int sv1 = 0;
int sv2 = 0;
int sv3 = 0;
int sv4 = 0;
int sv5 = 0;

int sv6 = 0;
int sv7 = 0;
int sv8 = 0;
int sv9 = 0;
int sv10 = 0;
int sv11 = 0;

int counter = 0;
void setup()
{
  Serial.begin(115200);
}
void loop()
{
  counter += 1;
  sv0 = analogRead(ai0);
  sv1 = analogRead(ai1);
  sv2 = analogRead(ai2);
  sv3 = analogRead(ai3);
  sv4 = analogRead(ai4);
  sv5 = analogRead(ai5);

  sv6 = analogRead(ai6);
  sv7 = analogRead(ai7);
  sv8 = analogRead(ai8);
  sv9 = analogRead(ai9);
  sv10 = analogRead(ai10);
  sv11 = analogRead(ai11);
  
  Serial.print(counter);
  Serial.print(",");
  Serial.print(millis());
  Serial.print(",");
  Serial.print(sv0);
  Serial.print(",");
  Serial.print(sv1);
  Serial.print(",");
  Serial.print(sv2);
  Serial.print(",");
  Serial.print(sv3);
  Serial.print(",");
  Serial.print(sv4);
  Serial.print(",");
  Serial.print(sv5);
  Serial.print(",");
  
  Serial.print(sv6);
  Serial.print(",");
  Serial.print(sv7);
  Serial.print(",");
  Serial.print(sv8);
  Serial.print(",");
  Serial.print(sv9);
  Serial.print(",");
  Serial.print(sv10);
  Serial.print(",");
  Serial.println(sv11);
  delay(200);
}

