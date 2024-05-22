import subprocess
import logging
import psutil
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Configure logging
logging.basicConfig(filename='hardware_check.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Functions to perform hardware checks
def check_ram():
    try:
        ram_info = psutil.virtual_memory()
        info = (f"RAM Information:\n"
                f"Total: {ram_info.total / (1024**3):.2f} GB, "
                f"Available: {ram_info.available / (1024**3):.2f} GB, "
                f"Used: {ram_info.used / (1024**3):.2f} GB, "
                f"Percentage: {ram_info.percent}%\n")
        logging.info(f"RAM Information: {ram_info}")
        return info
    except Exception as e:
        error_msg = f"Failed to check RAM: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_storage():
    try:
        total, used, free = shutil.disk_usage("/")
        info = (f"Storage Information:\n"
                f"Total: {total / (1024**3):.2f} GB, "
                f"Used: {used / (1024**3):.2f} GB, "
                f"Free: {free / (1024**3):.2f} GB\n")
        logging.info(f"Storage Information: Total: {total}, Used: {used}, Free: {free}")
        return info
    except Exception as e:
        error_msg = f"Failed to check storage: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_battery():
    try:
        battery_info = subprocess.check_output("upower -i /org/freedesktop/UPower/devices/battery_BAT0", shell=True).decode()
        logging.info(f"Battery Information:\n{battery_info}")
        return f"Battery Information:\n{battery_info}\n"
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to check battery: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_cpu():
    try:
        cpu_info = psutil.cpu_times_percent(interval=1, percpu=False)
        info = (f"CPU Information:\n"
                f"User: {cpu_info.user}%, System: {cpu_info.system}%, Idle: {cpu_info.idle}%\n")
        logging.info(f"CPU Information: {cpu_info}")
        return info
    except Exception as e:
        error_msg = f"Failed to check CPU: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_network():
    try:
        network_info = psutil.net_if_addrs()
        info = "Network Interfaces:\n"
        for interface, addrs in network_info.items():
            for addr in addrs:
                info += f"{interface} - {addr.family.name} Address: {addr.address}\n"
        logging.info(f"Network Information: {network_info}")
        return info
    except Exception as e:
        error_msg = f"Failed to check network: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_audio():
    try:
        audio_info = subprocess.check_output("aplay -l", shell=True).decode()
        logging.info(f"Audio Devices:\n{audio_info}")
        return f"Audio Devices:\n{audio_info}\n"
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to check audio devices: {e}\n"
        logging.error(error_msg)
        return error_msg

def check_keyboard():
    info = "Checking keyboard. Please press some keys...\n"
    logging.info("Checking keyboard...")
    try:
        subprocess.run(["xev"], timeout=10)
        info += "Keyboard is working properly.\n"
        logging.info("Keyboard is working properly.")
    except subprocess.TimeoutExpired:
        info += "Keyboard check timed out. It may not be working properly.\n"
        logging.warning("Keyboard check timed out. It may not be working properly.")
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to check keyboard: {e}\n"
        logging.error(error_msg)
        info += error_msg
    return info

def check_trackpad():
    info = "Checking trackpad. Please move the trackpad...\n"
    logging.info("Checking trackpad...")
    try:
        subprocess.run(["xinput", "test", "Virtual core pointer"], timeout=10)
        info += "Trackpad is working properly.\n"
        logging.info("Trackpad is working properly.")
    except subprocess.TimeoutExpired:
        info += "Trackpad check timed out. It may not be working properly.\n"
        logging.warning("Trackpad check timed out. It may not be working properly.")
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to check trackpad: {e}\n"
        logging.error(error_msg)
        info += error_msg
    return info

def run_checks():
    output = check_ram()
    output += check_storage()
    output += check_battery()
    output += check_cpu()
    output += check_network()
    output += check_audio()
    output += check_keyboard()
    output += check_trackpad()
    return output

# GUI Code
class HardwareCheckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Check Tool")
        self.geometry("600x400")
        
        self.label = tk.Label(self, text="Hardware Check Tool", font=("Arial", 16))
        self.label.pack(pady=10)

        self.run_button = tk.Button(self, text="Run Checks", command=self.run_checks)
        self.run_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=15)
        self.output_text.pack(pady=10)

    def run_checks(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, "Running checks...\n")
        output = run_checks()
        self.output_text.insert(tk.INSERT, output)
        messagebox.showinfo("Checks Completed", "Hardware checks completed successfully.")

if __name__ == "__main__":
    app = HardwareCheckApp()
    app.mainloop()
