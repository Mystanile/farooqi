import time
import os

def text_wave(text, delay=0.5):
    while True:
        for i in range(1, len(text) + 1):
            os.system('cls' if os.name == 'nt' else 'clear')
            for j in range(1, i + 1):
                print(text[:j])
            time.sleep(delay)
        for i in range(len(text) - 1, 0, -1):
            os.system('cls' if os.name == 'nt' else 'clear')
            for j in range(1, i + 1):
                print(text[:j])
            time.sleep(delay)

if __name__ == "__main__":
    text = input("Enter the text: ")
    text_wave(text)