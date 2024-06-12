from machine import Pin, I2C
import time

PIN_SCL = 41
PIN_SDA = 42

I2C_EEPROM_ADDRESS = 80 #whatever you will find 

i2c = I2C(1, freq=400000, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA))
      #or SoftI2C, check your port doc

print(i2c.scan())

dump = i2c.readfrom_mem(I2C_EEPROM_ADDRESS, 0, 256)
#dump2 = i2c.readfrom_mem(88, 0, 256)

hex_dump = [hex(byte) for byte in dump]
#hex_dump2 = [hex(byte) for byte in dump2]

print('eeprom contents:')
print(hex_dump)

print(f'backlight: {hex_dump[0xFC]} = {dump[0xFC]} secs')
#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0xFC, bytes([180])) #180 sec backlight
time.sleep_ms(10) #give eeprom some time to process the command

print(f'full range: {hex_dump[0x10]}, {hex_dump[0x11]} = {dump[0x10] + (dump[0x11] << 8)}')
#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0x10, bytes([0x70, 0x17])) #full range to 6000
time.sleep_ms(10)

print(f'range up: {hex_dump[0x12]}, {hex_dump[0x13]} = {dump[0x12] + (dump[0x13] << 8)}')
#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0x12, bytes([0x38, 0x18])) #range up to 6200
time.sleep_ms(10)

print(f'range down: {hex_dump[0x14]}, {hex_dump[0x15]} = {dump[0x14] + (dump[0x15] << 8)}')
#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0x14, bytes([0x44, 0x02])) #range down to 580
time.sleep_ms(10)

print(f'byte F9: {hex_dump[0xF9]}')

byte_f9 = dump[0xF9]
byte_f9 &= 0b11110011 #set vlcd to 2.8 - default was 3.0 
byte_f9 |= 0b00001000 #and it felt a bit overdriven - ghost icons at acute angles

#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0xF9, bytes([byte_f9])) #set vlcd to 2.8
time.sleep_ms(10)

print(f'poweroff timeout: {hex_dump[0xFB]} = {dump[0xFB]} mins')
#i2c.writeto_mem(I2C_EEPROM_ADDRESS, 0xFB, bytes([15])) #15 mins
time.sleep_ms(10)


