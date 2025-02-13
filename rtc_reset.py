import time
import board
import busio
import smbus
import datetime
import argparse
import adafruit_ds3231


parser = argparse.ArgumentParser(description='Sets RTC time using Raspberry Pi time')

parser.add_argument('-d',
                            '--day_of_the_week',
                            type=str,
                            required=True,
                            metavar='',
                            help="""Enter day of the week. Write the words in full and confirm
                                 the spelling. The argument is not case-sensitive.""")

args = parser.parse_args()


bus = smbus.SMBus(1)
DS3231 = 0x68
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(myI2C)
t = rtc.datetime

SECONDS_REG = 0x00
ALARM1_SECONDS_REG = 0x07
CONTROL_REG = 0x0E
STATUS_REG = 0x0F

def int_to_bcd(x):
    return int(str(x)[-2:], 0x10)

def write_time_to_clock(address, hours, minutes, seconds):
    bus.write_byte_data(DS3231, address, int_to_bcd(seconds))
    bus.write_byte_data(DS3231, address + 1, int_to_bcd(minutes))
    bus.write_byte_data(DS3231, address +2, int_to_bcd(hours))

def set_alarm1_mask_bits(bits):
    address = ALARM1_SECONDS_REG
    for bit in reversed(bits):
        reg = bus.read_byte_data(DS3231, address)
        if bit:
            reg = reg | 0x80
        else:
            reg = reg & 0x7F
        bus.write_byte_data(DS3231, address, reg)
        address+=1

def enable_alarm1():
    reg = bus.read_byte_data(DS3231, CONTROL_REG)
    bus.write_byte_data(DS3231, CONTROL_REG, reg | 0x05)

def clear_alarm1_flag():
    reg = bus.read_byte_data(DS3231, STATUS_REG)
    bus.write_byte_data(DS3231, STATUS_REG, reg & 0xFE)

def check_alarm1_triggered():
    return bus.read_byte_data(DS3231, STATUS_REG) & 0x01 != 0

def set_timer(hours, minutes, seconds):
    # set the clock to the current time of the rtc
    write_time_to_clock(SECONDS_REG, t.tm_hour,t.tm_min,t.tm_sec)
    # set the alarm
    write_time_to_clock(ALARM1_SECONDS_REG, hours, minutes, seconds) 
    #set the alarm to match hours minutes and seconds
    # need to set some flags
    set_alarm1_mask_bits((True, False, False, False))
    enable_alarm1()
    clear_alarm1_flag()

"""
next_wakeup_time=[t.tm_hour+1,t.tm_min,t.tm_sec]
if next_wakeup_time[0]<17:
    set_timer(tuple(next_wakeup_time))
elif next_wakeup_time[0]==17 and next_wakeup_time[1]<30:
    set_timer(tuple(next_wakeup_time))
elif next_wakeup_time[0]==17 and next_wakeup_time[1]>30:
    set_timer(8,0,0)
elif next_wakeup_time[0]>=18:
    set_timer(8,0,0)
"""
#
# Your sensor behaviour goes here
#
set_timer(0,1,0)



i2c = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(i2c)


#obtain current raspberry pi time
t=time.strftime("%Y-%m-%d %H:%M:%S")
print('Raspberry Pi time >>>>', t)

days_indx_dict = {'monday':0,
                  'tuesday':1,
                  'wednesday':2,
                  'thursday':3,
                  'friday':4,
                  'saturday':5,
                  'sunday':6}

day = args.day_of_the_week

if day.lower() in days_indx_dict:
    day_indx = days_indx_dict[day.lower()]
else:
    raise Exception('{} is  an invalid input. Confirm the spelling of the day and try again.'.format(day))

#show current rtc time
rtc_time = rtc.datetime
print('Current RTC time  >>>>', rtc_time)

#set rtc time
rtc.datetime = time.struct_time((int(t[:4]),int(t[5:7]),int(t[8:10]),int(t[11:13]),int(t[14:16]),int(t[17:19]),day_indx,268,-1))

rtc_time = rtc.datetime

print('Updated RTC time  >>>>',rtc_time)

print('\nSet a sample alarm to trigger after 10 seconds')
t=rtc.datetime
t=list(t)
print('Current RTC time >>>>', t)
t[5]=t[5]+10
if t[5]>=60:
	t[5]=t[5]-60
	t[4]+=1
t=tuple(t)
print('Alarm trigger time >>>>', t)
rtc.alarm1 = (time.struct_time(t),'daily')
if rtc.alarm1_status:
	print("wake up!")
	rtc.alarm1_status = False
