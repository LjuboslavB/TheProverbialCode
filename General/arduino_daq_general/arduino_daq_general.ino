const int ai0 = A0;
const int ai1 = A1;
const int ai2 = A2;
const int ai3 = A3;
const int ai4 = A4;
const int ai5 = A5;
int sv0 = 0;
int sv1 = 0;
int sv2 = 0;
int sv3 = 0;
int sv4 = 0;
int sv5 = 0;
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
  Serial.println(sv5);
  delay(200);
}

