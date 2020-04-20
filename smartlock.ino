//Austin Steepleton
//Smart Child Safety Locks
//Senior Design Spring 2020

#include<SPI.h>
#include<RF24.h>
#include <EEPROM.h>

//Radio Information
RF24 radio(10, 11);
const byte SETUP_CHANNEL = 0x01;
const byte DATA_CHANNEL = 0x76;
const uint64_t READING_PIPE = (0xE8E8F0F0E1LL);
const char DEFAULT_NAME[] = "New device";
const int CONNECTED_ADDRESS = 0;
const int DEVICE_NAME_STARTING_ADDRESS = 1;

//Pin Definitions
const int INTERRUPT_PIN = 3;
const int MOTOR_FORWARD = 5;
const int MOTOR_BACKWARD = 6;
const int LOCKED_PIN = A3;
const int UNLOCKED_PIN = A4;

//Global Variables
int connected_to_hub = EEPROM.read(CONNECTED_ADDRESS);
char device_name[32] = {0};
bool device_locked;

//Function Prototypes
void setup_device();
String read_device_name();
void write_device_name(String device_name);
String device_name_string = read_device_name();


void setup()
{
  pinMode(MOTOR_FORWARD, OUTPUT);
  pinMode(MOTOR_BACKWARD, OUTPUT);
  //attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), wakeup, RISING);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  if (connected_to_hub == 0)
  {
    setup_device();
  }
  radio.setChannel(DATA_CHANNEL);
  radio.openReadingPipe(1, READING_PIPE);
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
}

void loop()
{
  radio.startListening();
  char receivedMessage[32] = {0};
  if (radio.available())
  {
    radio.read(receivedMessage, sizeof(receivedMessage));
    radio.stopListening();
  }
  String stringMessage(receivedMessage);
  String deviceName(device_name);
  if (stringMessage == deviceName)
  {
    device_locked = get_lock_status();
    if (device_locked == true)
    {
      while (device_locked == true)
      {
        analogWrite(MOTOR_BACKWARD, 128);
        device_locked = get_lock_status();
      }
    }
    delay(10000);
    if (device_locked == false)
    {
      while (device_locked == false)
      {
        analogWrite(MOTOR_FORWARD, 128);
        device_locked = get_lock_status();
      }
    }
  }

}

void setup_device()
{
  radio.setChannel(SETUP_CHANNEL);
  radio.openReadingPipe(1, READING_PIPE);
  radio.startListening();
  char receivedMessage[32] = {0};
  if (radio.available())
  {
    radio.read(receivedMessage, sizeof(receivedMessage));
    radio.stopListening();
  }
  write_device_name(receivedMessage);
  EEPROM.write(CONNECTED_ADDRESS, 1);
  delay(100);
}

String read_device_name()
{
  char device_name[32];
  int len = 0;
  unsigned char character;
  character = EEPROM.read(DEVICE_NAME_STARTING_ADDRESS);
  while (character != '\0' && len < 32)
  {
    character = EEPROM.read(DEVICE_NAME_STARTING_ADDRESS + len);
    device_name[len] = character;
    len++;
  }
  device_name[len] = '\0';
  return String(device_name);
}

void write_device_name(String device_name)
{
  int name_size = device_name.length();
  for (int i = 0; i < name_size; i++)
  {
    EEPROM.write(DEVICE_NAME_STARTING_ADDRESS, i);
  }
  EEPROM.write(DEVICE_NAME_STARTING_ADDRESS + name_size, '\0');
}

void wakeup()
{
  radio.powerUp();
  loop();
}

bool get_lock_status()
{
  if (analogRead(LOCKED_PIN) > analogRead(UNLOCKED_PIN))
    return true;
  else
    return false;
}
