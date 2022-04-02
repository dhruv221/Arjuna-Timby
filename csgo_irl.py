# USB
from time import sleep

import pyautogui
import serial

serialcomm = serial.Serial('COM3', 9600)
serialcomm.timeout = 1
print("serial comm initiaised")


last_pos = None

print("Starting loop")
while True:
    sleep(0.01)
    cur_pos = pyautogui.position()
    # wraparound 180, 180
    cur_pos = int(cur_pos[0] / (1920 / 180)), int(cur_pos[1] / (1080 / 180))

    if last_pos != cur_pos:
        last_pos = cur_pos
        motorX = f"%X{cur_pos[1]}#"
        motorY = f"%Y{cur_pos[0]}#"
        serialcomm.write(motorX.encode())
        serialcomm.write(motorY.encode())

        print("Current vlaues", cur_pos)
        # sleep(0.2)
