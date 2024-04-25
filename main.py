from check import init
import sys

def main() -> None:
    if init() != 0:
        print('Neporarilo se importovat knihovnu  " curses ", ujistete se ze je spravne nainstalovana')
        sys.exit()

if __name__ == "__main__": main()
