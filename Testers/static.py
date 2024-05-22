import subprocess

def check_ram():
    try:
        ram_info = subprocess.check_output("free -h", shell=True).decode()
        print("RAM Information:\n", ram_info)
    except subprocess.CalledProcessError as e:
        print("Failed to check RAM:", e)

def check_storage():
    try:
        storage_info = subprocess.check_output("df -h", shell=True).decode()
        print("Storage Information:\n", storage_info)
    except subprocess.CalledProcessError as e:
        print("Failed to check storage:", e)

def check_battery():
    try:
        battery_info = subprocess.check_output("upower -i /org/freedesktop/UPower/devices/battery_BAT0", shell=True).decode()
        print("Battery Information:\n", battery_info)
    except subprocess.CalledProcessError as e:
        print("Failed to check battery:", e)

def main_static():
    print("Starting static hardware checks...")
    check_ram()
    check_storage()
    check_battery()
    print("Static hardware checks completed.")

if __name__ == "__main__":
    main_static()
