import time
import keyboard

def press_and_release(key: str):
    keyboard.press(key)
    time.sleep(1)
    keyboard.release(key)

# Don't start too early
while not keyboard.is_pressed('p'):
    time.sleep(0.001)
while keyboard.is_pressed('p'):
    time.sleep(0.001)
sleep_time = 1
time.sleep(sleep_time)
press_and_release('e')