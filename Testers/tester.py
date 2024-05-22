import subprocess

def check_ram():
    ram_info = subprocess.check_output("free -h", shell=True).decode()
    print("RAM Information:")
    print(ram_info)

def check_storage():
    storage_info = subprocess.check_output("df -h", shell=True).decode()
    print("Storage Information:")
    print(storage_info)

def check_keyboard():
    print("Checking keyboard...")
    try:
        subprocess.run(["xev"], timeout=10)
        print("Keyboard is working properly.")
    except subprocess.TimeoutExpired:
        print("Keyboard check timed out. It may not be working properly.")

def check_trackpad():
    print("Checking trackpad...")
    try:
        subprocess.run(["xinput", "test", "Virtual core pointer"], timeout=10)
        print("Trackpad is working properly.")
    except subprocess.TimeoutExpired:
        print("Trackpad check timed out. It may not be working properly.")

def check_battery():
    battery_info = subprocess.check_output("upower -i /org/freedesktop/UPower/devices/battery_BAT0", shell=True).decode()
    print("Battery Information:")
    print(battery_info)

def main():
    check_ram()
    check_storage()
    check_keyboard()
    check_trackpad()
    check_battery()

if __name__ == "__main__":
    main()
