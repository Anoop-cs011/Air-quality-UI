# Air-quality-UI
1. WHO data show that almost all of the global population (99%) breathe air that exceeds WHO guideline limits and contains high levels of pollutants, with low- and middle-income countries suffering from the highest exposures.
2. More than 80% of people living in urban areas that monitor air pollution are exposed to air quality levels that exceed WHO limits.

## System description and operation
### Hardware
1. ESP32 microcontroller
2. Grove - Gas Sensor V2 (Multichannel)
### Libraries
You will need to install the following libraries to run the Python code:
1. tkinter: main module to create GUI
2. pySerial: to get sensor data from the microcontroller
3. functools: to flatten functions with multiple parameters
4. NumPy: Fundamental package for scientific computing with Python.
5. pandas: A powerful data analysis and manipulation library.

## How to use it?
### With Hardware
1. Upload the Arduino code “gas_sensor.ino” with the ESP32-WROOM-DA Module as the selected board.
![image](https://github.com/user-attachments/assets/61520c21-af23-4620-a6cf-d4818c4169c3)

2. Once uploaded successfully, close the Arduino IDE. The same device & port can not be accessed by the different IDEs at the same time.
3. Run the Python program “mainGUI.py”. Make sure you have entered the correct port name and baud rate.
![image](https://github.com/user-attachments/assets/98ea3581-ebe4-47a1-b43e-3108527bb3c4)

### Without Hardware (on stored data)
If you do not have the hardware, you may run the test code.
1. Comment out the dispData() call, and uncomment the testDispData() in “mainGUI.py”.<br />
**From**<br />
![image](https://github.com/user-attachments/assets/a44941b5-e830-452d-a7df-3037c4334ee1)<br />
  **to**<br />
![image](https://github.com/user-attachments/assets/8baee933-9be7-4ff5-a66e-15e414083cde)


2. Change the value of the parameter manually from 0 to 11 to check the program for changing gas values. Run the program **mainGUI.py**; no need to run **gas_sensor.ino**.

![image](https://github.com/user-attachments/assets/17d21bac-b3fc-464e-a4d0-7f31a40e9c71)
![image](https://github.com/user-attachments/assets/ae6bb6cf-6735-4df1-8c7e-69747b34edfe)
    
*The colours are assigned based on the standards laid out by the [U.S. Environmental Protection Agency](https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf)*

3. The  “?” button is displayed whenever the concentrations of the gas reach levels that are not healthy. Clicking on the button displays the possible sources, effects on health & precautionary measures.

![image](https://github.com/user-attachments/assets/bd5e71fc-a8a0-4608-8087-b0a8cd97d5dd)
![image](https://github.com/user-attachments/assets/37571fd1-85d6-47c7-ac33-81e5883f92d9)



