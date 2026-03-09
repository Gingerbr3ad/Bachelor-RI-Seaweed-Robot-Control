import gpiozero
import time

pin = gpiozero.OutputDevice(4)
pin.on()

def main():
    while True:
        pin.on()
        print("on")
        time.sleep(8)
        pin.off()
        print("off")
        time.sleep(8)


if __name__ == '__main__':
    main()
