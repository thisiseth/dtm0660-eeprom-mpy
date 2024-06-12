# dtm0660-eeprom-mpy

Just a small micropython script to edit DTM0660/DM1106EN-based digital multimeter EEPROM settings

First please check a wonderful work by Kerry D. Wong on DTM0660 datasheet translation and more [here](http://www.kerrywong.com/blog/wp-content/uploads/2016/04/DTM0660DataSheet.pdf), 
so you understand what you are actually editing :)

## What can be edited

I bought AstroAI DT132A, so things i was interested in:
* Give it full 6000 count range instead of 4000
* Set backlight timeout to 180 secs instead of 15
* I tried other Vlcd values, because the display had severe ghosting at angles i usually use it - settled on 2.8V instead of 3.0V
* Poweroff timeout also can be changed, but i think default 15 mins are ok

Also it is possible to enable UART on these chips, but i don't need it (yet)

## How to (approximately)

These multimeters store their settings in a 8-pin SOP-8 (or is it SOIC?..) 256-byte I2C EEPROM, it will be some kind of T24C02

I had a EEPROM clip laying around, my multimeter runs of 3 AAAs - desiged for ~3V operation, and i used 3.3V GPIO ESP32S3,
so i was just able to do this in-circuit without level-shifting magic:
* Remove the back cover and the batteries! don't forget about the batteries!
* Set the multimeter to NOT 'off' position, V~ for example
* Clip the EEPROM, the pinout is:
```
  GND  A2  A1  A0    <- all 4 are wired to ground on the PCB
   |   |   |   |(pin 1, dot on chip)
       T24C02
   |   |   |   |(pin 8)
  SDA SCL  WP VDD
```
* Connect SDA, SCL, VDD, GND accordingly. VDD in my case is 3.3V from MCU
* WP (write protect) has to be connected to ground to write anything - before doing this make sure you saved your factory EEPROM dump!

Now the tricky part - since we connected the VDD, multimeter will just turn on as usual and block our I2C communication with flash, so:
* Wait for the multimeter to turn off at 15 min timeout - it will beep before it will go to sleep
* If you try running the script before the MCU is asleep nothing bad will happen, the script just hangs
* In the meanwhile, set your pins and I2C settings in the script, refer to your MCU MicroPython port documentation

After the long beep and the screen going blank, you can run the script (without grounding the WP pin!)
* First output is all found I2C devices, i believe one is EEPROM and the other one is the chip itself
* Try both, if the `eeprom contents:` printout is all 0xff - it is the wrong one
* In DT132A EEPROM has i2c address 80, and the chip is 88
* Save your EEPROM contents
* Ground the WP pin of EEPROM to allow writing
* Uncomment whatever `i2c.writeto_mem(I2C_EEPROM_ADDRESS, <byte address>, bytes([<values>]))` you need or write your own
* My EEPROM did not like successive write commands without some rest, so i added `time.sleep_ms()` in between

 

