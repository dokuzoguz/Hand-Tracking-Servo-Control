#include <Arduino.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <WiFiUdp.h>

#define SERVO 18
#define ESP_PORT X

WiFiUDP udp_comm;

Servo my_servo;

String NETWORK_NAME = "";
String NETWORK_PASSWORD = "";

int servo_angle_last_state = 0;

void setup() {
  pinMode(LED_BUILTIN , OUTPUT);
  digitalWrite(LED_BUILTIN , LOW);
  
  Serial.begin(115200);
  delay(1000);
  Serial.println("System was started");
  delay(300);

  WiFi.begin(NETWORK_NAME , NETWORK_PASSWORD);

  while(true){
    if(WiFi.status() == WL_CONNECTED){
      digitalWrite(LED_BUILTIN , HIGH);
      Serial.println("ESP32 connected to the WiFi");
      Serial.print("IP address of ESP32 is : ");
      Serial.println(WiFi.localIP());
      break;
    }else{
      Serial.println("Connection is being waited");
      delay(1000);
    }
  }

  udp_comm.begin(ESP_PORT);

  my_servo.attach(SERVO);
  my_servo.write(servo_angle_last_state);
}



void loop() {
  int byte_number_of_coming_data = udp_comm.parsePacket();

  if(byte_number_of_coming_data!=0){
    char buffer[32];
    int len = udp_comm.read(buffer , sizeof(buffer)-1);
    buffer[len] = '\0';

    String coming_data = String(buffer);
    servo_angle_last_state = coming_data.toInt();

    Serial.println(servo_angle_last_state);
    my_servo.write(servo_angle_last_state);
  }
}