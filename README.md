
# Serial PID Tuner
[![Logo](https://github.com/marwan275/Serial-PID-Tuner/blob/main/logo.png)](https://xengineering.net/)

Serial PID Tuner is an open-source application developed for [XEngineering](https://xengineering.net/), designed to communicate with an Arduino (or any other microcontroller with Serial USB) to send and receive PID values and sensor data. This tool enables users to easily tune and monitor PID controllers over a serial connection, with real-time data visualization for improved control and feedback.

## Features
- Real-time PID Tuning: Update and send PID values to an Arduino or other microcontroller in real-time.
- Sensor Data Monitoring: Visualize sensor data on a graph to observe changes in response to PID adjustments.
- User-Friendly Interface: Intuitive UI with sections for PID values, sensor readings, and control options.
- Adjustable X-Axis Length: Customize the length of the x-axis to focus on short-term or long-term data trends.


## Screenshots

![App Screenshot](https://github.com/marwan275/Serial-PID-Tuner/blob/main/screenshots/Screenshot1.png)
![App Screenshot](https://github.com/marwan275/Serial-PID-Tuner/blob/main/screenshots/Screenshot2.png)


## Installation
1. Clone the Repository:
```bash
git clone https://github.com/marwan275/Serial-PID-Tuner
cd serial-pid-tuner
```
2. Install Dependencies:
```bash
pip install -r requirements.txt
```

    
## Usage
1. Connect Your Arduino or microcontroller
2. In labels.py
    ```python
    USB_port = "COM13"
    software_title = "Serial PID Tuner"
    logo_path = "logo.png"
    ```
    Change the USB_port to port connected to your microcontroller
3. Run the main.py
    ```python
    python main.py
    ```
4. The microcontroller should be sending data in the supported format at baud rate __115200__
## Data Format
The data sent from the Arduino (any other microcontroller) to the software follows a specific structure, where each value is separated by a slash (/). The values include sensor data, PID controller values, and other control parameters. The Arduino sends this data in a single line, and each component is separated by a /.

```bash
sensor1_value/sensor2_value/sensor3_value/sensor4_value/sensor5_value/sensor6_value/millis_value/P_value/I_value/D_value/set_point_value/override_value/PWMDirect_value
```
Here is what each value represents:
- sensor1_value to sensor6_value: These are the sensor readings.
- millis_value: The millisecond time value from the Arduino.
- P_value, I_value, D_value: The PID controller values for proportional, integral, and derivative gains.
- set_point_value: The target setpoint for the PID controller.
- override_value: The override status, which is a flag to set the PID controller to overridden.
- PWMDirect_value: The direct PWM value being used for manual control of the system control.

## Notes:
- Data Transmission Speed: The string-based format, using slashes for readability, is simple and works well for tuning purposes but can be slow for large data. For better performance, array format could be more efficient, though they require extra handling.

- Arduino Serial.println(): The use of Serial.println() makes it easy for Arduino users to send the data as a string, but for other systems, a structured array format might be preferable for more efficient data transfer.
## Microcontroller Example
**Arduino**
```cpp
// Example Arduino code to send PID and sensor data to the Serial PID Tuner software

// Define the sensor values and PID parameters
float sensor1 = 23.5;
float sensor2 = 47.8;
float sensor3 = 12.3;
float sensor4 = 56.1;
float sensor5 = 34.9;
float sensor6 = 29.4;
unsigned long millisValue = 0;

// PID values
float P = 2.5;
float I = 1.2;
float D = 0.8;
float setPoint = 50.0;
uint8_t override = 1;
float pwmDirect = 128;  // Example PWM value

void setup() {
  // Start the Serial communication
  Serial.begin(115200);
}

void loop() {
  // Update millisValue to current time in milliseconds
  millisValue = millis();
  
  // Create the data string
  String dataString = String(sensor1) + "/" +
                      String(sensor2) + "/" +
                      String(sensor3) + "/" +
                      String(sensor4) + "/" +
                      String(sensor5) + "/" +
                      String(sensor6) + "/" +
                      String(millisValue) + "/" +
                      String(P) + "/" +
                      String(I) + "/" +
                      String(D) + "/" +
                      String(setPoint) + "/" +
                      String(override) + "/" +
                      String(pwmDirect);
  
  // Send the data over Serial
  Serial.println(dataString);
  
  // Add a delay to simulate sensor reading interval
  delay(1000);  // 1 second delay
}

```
**Other Microcontroller**
```C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Define the structure to hold sensor and PID data
typedef struct {
    float sensor1;
    float sensor2;
    float sensor3;
    float sensor4;
    float sensor5;
    float sensor6;
    unsigned long millis;
    float P;
    float I;
    float D;
    float setPoint;
    float override;
    float pwmDirect;
} PIDData;

// Function to format the data as a string
void formatPIDData(PIDData *data, char *formattedString) {
    // Format the data as a string with slashes separating the values
    sprintf(formattedString, "%f/%f/%f/%f/%f/%f/%lu/%f/%f/%f/%f/%f/%f",
            data->sensor1,
            data->sensor2,
            data->sensor3,
            data->sensor4,
            data->sensor5,
            data->sensor6,
            data->millis,
            data->P,
            data->I,
            data->D,
            data->setPoint,
            data->override,
            data->pwmDirect);
}

// Function to send the formatted string over USB
void SerialSendOverUSB(const char *data) {
    // Send the data over USB (via UART or USB-CDC)
    // In this example, we use printf to simulate the transmission via USB
    // Replace with your microcontroller's specific USB/UART transmission function
    printf("%s\n", data);
}

// Main function
int main() {
    // Example data to be sent
    PIDData data = {
        23.5, 47.8, 12.3, 56.1, 34.9, 29.4, // sensor values
        123456, // millis
        2.5, 1.2, 0.8, 50.0, 1.0, 128.0 // PID values
    };
    
    // Buffer to store the formatted data string
    char formattedString[256];  // Ensure this is large enough for the formatted string
    
    // Format the data
    formatPIDData(&data, formattedString);
    
    // Send the formatted data over USB
    SerialSendOverUSB(formattedString);
    
    return 0;
}

```
## License
This project is open-source and distributed under the MIT License by XEngineering and me sharing the source code was by their permission.

## Credits
Developed by [Marwan Mobarak](https://github.com/marwan275) for [XEngineering](https://xengineering.net/).