# POWERING THE RASPBERRY PI IN THE FIELD

The Raspberry Pi is a single board computer that runs on a Debian based operating system. The Raspberry Pi finds many applications due the fact it can operate like a normal computer and its ability to interact with the outside world using sensors. Due to it small size, it make it easier to deploy in the field for applications that require high computing capabilities that are not found in microcontrollers. When deploying sensor systems in the field, power is one of the most important factors to consider. The fact that the Raspberry Pi operates like a normal computer makes it even more important. Shutting the Raspberry Pi unconventionally due to power outage may result to corruption of it storage leading to loss of one's work and/or data. It is for this reason the we developed the [DSAIL Power Management Board](https://kiariegabriel.github.io/powering-the-raspberrypi.html) to power the Raspberry Pi in the field intelligently.

<p align="center">
  <img width="460" height="300" src="/img/power-board.jpg">
  
</p>

<p align="center"> 
  <em>Figure 1: DSAIL Power Management Board</em>
</p>

To enable the Raspberry Pi to control power management board, several programs were written. The programs are:

## Power Management Program
The [power management program](https://github.com/DeKUT-DSAIL/powering-raspberrypi/blob/main/power.py) enables the Raspberry Pi to monitor the state of charge (SOC) of the battery used in the system. This helps ensure that the Raspberry Pi does not shut down due to depletion of charge in the battery. This also protects the battery from being over discharged resulting to a longer lifespan. The program enables the Raspberry Pi to make an informed decision of shutting down when the battery reaches the cut off voltage. The program has a provision for setting the number of hours one intend to power the Raspberry Pi in a day. It is possible to set the system to power the Raspberry Pi during different time windows in a day. The program is responsible for shutting down the system when the time matches the specified shutdown time.

The program is written in Python and uses third party libraries from [Adafruit](https://www.adafruit.com/) which are `board`, `busio`, and `digitalio`. The program reads the battery voltage after every 30 seconds and compares it with the predetermined cut off voltage. Whenever the voltage goes below the specified cut off voltage, the program initiates the shutdown of the Raspberry Pi and the entire system. The program uses our own made modules to achieve this. The modules are [rtc.py](https://github.com/DeKUT-DSAIL/powering-raspberrypi/blob/main/rtc.py) and [adc.py](https://github.com/DeKUT-DSAIL/powering-raspberrypi/blob/main/adc.py) that we will look into in the following two sections:

### RTC module

The [rtc.py module](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/rtc.py) helps in setting the alarm of a [DS3231 Real Time Clock (RTC) board](https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/overview) on the power management board to schedule the wake up of the system. The alarm function of the rtc.py module is called to set the RTC's alarm to schedule wake up of the system whenever the Raspberry Pi has "decided" to shut down.

### ADC module

The [adc.py module](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/adc.py) is used by the power management program to read the voltage of the battery used in the system. The Raspberry Pi lacks an onboard analog to digital converter (ADC) and hence has to use an external ADC to read the battery voltage which is an analog quantity. In our system, we used the [MCP3008 i/p ADC](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008) to enable our system to read the battery voltage. The power management program calls the volt function from this module after every thirty seconds to read the battery voltage. After every five minutes, the voltage reading at that moment is saved in a datestamped CSV file alongside with the time at that moment using the volt_csv function from this module.

The flow chart below shows the performance of the power management program:
<p align="center">
  <img width="auto" height="auto" src="/img/power.png">
  
</p>

<p align="center"> 
  <em>Figure 2: Power management program flow chart</em>
</p>

## 5. Time set program
The [time set program](https://github.com/DeKUT-DSAIL/powering-raspberrypi/blob/main/timeset.py) program is  used to set time of the Raspberry Pi every time on wake up since the Raspberry Pi lacks an onboard RTC.

# Setting up the Raspberry Pi

## Requirements
1. Raspberry Pi 2/3/4
2. Raspberry Pi power supply
3. An SD Card loaded with Raspberry Pi OS
4. Access to the internet.
5. Ability to access the Raspberry Pi's command line.

Clone this repository in the Raspberry Pi by running the following command on the commandline:

```cpp
git clone https://github.com/DeKUT-DSAIL/powering-raspberrypi.git
```
After cloning, run the following commands to create a virtual environment and install the requirements needed to run the programs:

```cpp
cd powering-raspberrypi
./raspi_setup.sh
```

Next, we will need to schedule the programs to run every time on boot using `crontab`. Run the following the command:

```cpp
crontab -e
```
If it is the first time using crontab, you will be prompted to choose an editor. Choose nano editor by entering 1. Copy and paste the following in the crontab:

```cpp
@reboot /home/pi/powering-raspberrypi/timeset.sh
@reboot /home/pi/powering-raspberrypi/power.sh
```
 
The system is now ready for deployment. To monitor the voltage profile of the battery, check the csv files stored in the created battery-voltage folder. In case the system fails, check for the errors raised in the log files stored in the powering-raspberrypi folder.
