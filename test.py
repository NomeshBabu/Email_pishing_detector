# test.py
import sys
import platform

def hello():
    print("✅ Python is working inside VS Code!")
    print("Python version:", sys.version)
    print("Platform:", platform.system(), platform.release())

if __name__ == "__main__":
    hello()
