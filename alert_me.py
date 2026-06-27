import winsound
import time
import sys

def play_alert():
    # Play a distinct beep pattern: 3 short, 1 long
    for _ in range(3):
        winsound.Beep(1000, 200) # frequency 1000Hz, duration 200ms
        time.sleep(0.1)
    time.sleep(0.2)
    winsound.Beep(1000, 800) # frequency 1000Hz, duration 800ms

if __name__ == "__main__":
    print("Playing alert chime...")
    play_alert()
