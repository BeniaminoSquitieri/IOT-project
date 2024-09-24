# Safety&Care IoT System

## Project Overview

The **Safety&Care System** is a smart home security and environmental monitoring solution designed to protect and maintain household safety. The system integrates various IoT devices and is controlled either through physical recognition systems, such as RFID, or remotely via interactive graphical interfaces like Google Home and a custom dashboard built with **Node-RED**. This project was developed as part of the **Technologies for Web Software** course by **Group 53**, utilizing the **Internet of Things (IoT)** concepts learned in the course.

## Objectives

The goal of the project was to apply IoT technologies in a familiar and accessible context, enabling users to manage and monitor home safety with ease. By leveraging IoT devices, the system allows real-time control and feedback on home conditions, such as air quality and intrusion detection.

## Key Features

### 1. **Care System**
The Care System monitors air quality in the household using gas sensors. It triggers alarms if dangerous levels of gas are detected, and activates a ventilation system to improve air quality. The Care System features:
- **MQ2 Gas Sensor**: Detects gas leaks and outputs data based on the concentration of gas.
- **DC Motor with Fan**: Automatically turns on to ventilate the area when dangerous gases are detected.
- **Alarms**: Visual (LED) and audio (buzzer) alarms are triggered when thresholds are exceeded.
- **Automatic Deactivation**: The system turns off once air quality returns to acceptable levels or upon manual deactivation.

### 2. **Safety System**
The Safety System provides home security, detecting unauthorized entry attempts. It can be activated manually through an **RFID** system or remotely via Google Home. Key components include:
- **Ultrasonic Sensor**: Detects movement within a specified range and triggers alarms if objects approach too closely.
- **Vibration Switch**: Detects potential tampering or break-in attempts by measuring vibrations on doors or windows.
- **Alarms**: A visual red flashing light and an audio alert are triggered during a potential intrusion.
- **Stepper Motor**: Used to activate and control the positioning of the ultrasonic sensor.

### 3. **Remote Control and Monitoring**
The system can be controlled and monitored remotely using two methods:
- **Google Home**: A smart assistant interface for enabling/disabling both the Care and Safety Systems. Security activation requires a passcode for added protection.
- **Custom Dashboard (Node-RED)**: Displays real-time sensor data, system statuses, and allows for remote activation or deactivation of the systems. Alerts are also sent to a dedicated **Telegram bot** in case of gas leaks or intrusions.

## Hardware Components

The system was built using the following components:
- **ZM1-EVA Microcontroller**: A Zerynth-based microcontroller that integrates Python and C code, facilitating communication between devices and the cloud.
- **RFID Reader**: Used for securely activating the Safety System with an RFID tag.
- **Buzzer**: Audio alarm used for both gas and intrusion alerts.
- **LCD1602 Display**: Shows the current status of the system in real time.
- **RGB LED**: Visual indicator for system statuses:
  - **Blue**: All systems off.
  - **Green**: Care System active.
  - **Yellow**: Safety System active.
  - **Magenta** (blinking): Air contamination detected.
  - **Red** (blinking): Intrusion detected.

## Communication Protocols

Several communication protocols were employed to ensure efficient and reliable data exchange between components:
- **I2C**: Used for communication with the LCD display to show system statuses.
- **SPI**: Used for communication between the RFID reader and the microcontroller.
- **MQTT**: This protocol connects the hardware components with the software interfaces (dashboard and Google Home). It allows for a publish/subscribe model that transmits data between devices and the cloud efficiently.

## Remote Interface and Alerts

### **Google Home**
- Users can enable or disable both the Care and Safety Systems through a Google Home interface. A security passcode is required for activating the Safety System.

### **Node-RED Dashboard**
- The custom Node-RED dashboard allows users to view gas levels and system statuses in real time. It also features controls for activating and deactivating the systems. The dashboard is designed for ease of use and is highly intuitive.

### **Telegram Alerts**
- A custom **Telegram bot** sends notifications in real time when alarms are triggered. Notifications include information on gas levels or intrusion events, and can be sent to individual users or a family group.

## Challenges and Limitations

During the development process, the team encountered several challenges:
- **Incompatibility Issues**: Some digital pins on the ZM1-EVA microcontroller were incompatible with certain devices, requiring adjustments in the wiring and communication setup.
- **PWM Functionality**: The Zerynth platform caused issues with the PWM (Pulse Width Modulation) for certain components, which led to delays in the project.
- **MQTT Communication Errors**: Errors in MQTT communication between the dashboard and the system required significant debugging and problem-solving.
- **Limited Documentation**: Zerynth’s limited documentation posed a challenge, necessitating extensive research and experimentation.


