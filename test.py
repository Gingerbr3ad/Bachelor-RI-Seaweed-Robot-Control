from gpiozero import InputDevice

pin = InputDevice(27, pull_up=False)

prevTemp = False

while True:
    temp = pin.is_active

    if(temp != prevTemp):
        prevTemp = temp
        print(pin.is_active)