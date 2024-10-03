#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int lampPin = 6;

int ledPin = 13;
int sensorValue; 


int RawValue = 0;
int Voltage = 0;

int ControlHumidity = 0; // контроль влажности
int HumidityOut = 0;    // влажность вне
int HumidityIn = 0;		// влажность в

int ControlTemp = 0;	// контроль температуры
int TempOut = 0;     	// температура вне
int TempIn = 0;			// температура в

void setup() // считывание
{
  pinMode(A0, INPUT); 	// кондей
  pinMode(A1, INPUT); 	// рег влажности
  pinMode(A3, INPUT); 	// влажность снаружи
  pinMode(A4, INPUT); 	// фоторезистор
  pinMode(A5, INPUT); 	// датчик угла наклона
  pinMode(ledPin, OUTPUT);  // светодиод
  pinMode(lampPin, OUTPUT); // лампа
  
  lcd.begin(16, 2);
  
  digitalWrite(A5, HIGH);
}

void loop()
{
  sensorValue = digitalRead(A5); // получение угла наклона

  if (sensorValue != 1) // автомат наклонили
  {
    
    lcd.clear();
    lcd.print("Attention!!!");
    lcd.setCursor(0, 1);
    lcd.print("Alarm system");
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
  }

  else
  {
    int light = analogRead(A4); // фоторезистор
    
    if(light > 450){
      digitalWrite(lampPin, HIGH); // свет включился
    }
    else{
    digitalWrite(lampPin, LOW);} // свет выключился

    ControlTemp = analogRead(A0) / 100; // кондей

    RawValue = analogRead(A2);
    Voltage = (RawValue / 1023.0) * 5000;
    TempOut = (Voltage - 500) * 0.1; // темп снаружи

    switch (ControlTemp)
    {
    case 0:
      TempIn = TempOut - 10;
      break;
    case 1:
      TempIn = TempOut - 8;
      break;
    case 2:
      TempIn = TempOut - 6;
      break;
    case 3:
      TempIn = TempOut - 4; // изменение темп внутри автомата
      break;
    case 4:
      TempIn = TempOut - 2;
      break;
    case 5:
      TempIn = TempOut;
      break;
    case 6:
      TempIn = TempOut + 2;
      break;
    case 7:
      TempIn = TempOut + 4;
      break;
    case 8:
      TempIn = TempOut + 6;
      break;
    case 9:
      TempIn = TempOut + 8;
      break;
    case 10:
      TempIn = TempOut + 10;
      break;
    }

    ControlHumidity = analogRead(A1) / 100; // рег влажности
    HumidityOut = analogRead(A3) / 10;      // влажность снаружи

    switch (ControlHumidity)
    {
    case 0:
      HumidityIn = HumidityOut - 10;
      break;
    case 1:
      HumidityIn = HumidityOut - 8;
      break;
    case 2:
      HumidityIn = HumidityOut - 6;
      break;
    case 3:
      HumidityIn = HumidityOut - 4;
      break;
    case 4:
      HumidityIn = HumidityOut - 2; // имитация рег влажности
      break;
    case 5:
      HumidityIn = HumidityOut;
      break;
    case 6:
      HumidityIn = HumidityOut + 2;
      break;
    case 7:
      HumidityIn = HumidityOut + 4;
      break;
    case 8:
      HumidityIn = HumidityOut + 6;
      break;
    case 9:
      HumidityIn = HumidityOut + 8;
      break;
    case 10:
      HumidityIn = HumidityOut + 10;
      break;
    }

    lcd.setCursor(0, 0);

    if (TempIn < 10)
    {
      lcd.print("low temp: ");
    }

    else if (TempIn > 30)
    {
      lcd.print("high temp: ");
    }

    else
    {
      lcd.print("temp: ");
    }

    lcd.print(TempIn);
    lcd.print("C");

    lcd.setCursor(0, 1);

    if (HumidityIn < 45)
    {
      lcd.print("low moi-re: ");
    }

    else if (HumidityIn > 65)
    {
      lcd.print("high moi-re: ");
    }

    else
    {
      lcd.print("moisture: ");
    }

    lcd.print(HumidityIn);
    lcd.print("%");
  }

  delay(2000);

  lcd.clear();
}

