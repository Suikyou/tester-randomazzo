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
        lines = battery_info.split('\n')
        current_capacity = None
        original_capacity = None
        for line in lines:
            if "energy-full:" in line:
                current_capacity = float(line.split(':')[1].strip().split()[0])
            elif "energy-full-design:" in line:
                original_capacity = float(line.split(':')[1].strip().split()[0])
        
        if current_capacity is not None and original_capacity is not None:
            health_percentage = (current_capacity / original_capacity) * 100
            if health_percentage > 90:
                health = "Ideal"
            elif health_percentage > 80:
                health = "Decent"
            elif health_percentage > 70:
                health = "Okay"
            else:
                health = "Bad"
            health_info = f"Battery Health: {health} ({health_percentage:.2f}%)\n"
        else:
            health_info = "Battery health information not found.\n"

        logging.info(f"Battery Information:\n{battery_info}")
        return f"{health_info}"
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

def get_ports():
    try:
        ports_info = subprocess.check_output("ls /dev", shell=True).decode()
        logging.info(f"Available Ports:\n{ports_info}")
        return f"Available Ports:\n{ports_info}\n"
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to get available ports: {e}\n"
        logging.error(error_msg)
        return error_msg

def generate_report():
    report = ""
    report += check_battery()
    report += check_storage()
    report += check_ram()
    report += check_cpu()
    report += check_network()
    report += check_audio()
    report += get_ports()
    return report

# GUI Code
class HardwareCheckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Check Tool")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.label = tk.Label(self, text="Hardware Check Tool", font=("Arial", 16))
        self.label.pack(pady=10)

        self.run_button = tk.Button(self, text="Generate Report", command=self.generate_report)
        self.run_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def generate_report(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, "Generating hardware report...\n")
        report = generate_report()
        self.output_text.insert(tk.INSERT, report)
        messagebox.showinfo("Report Generated", "Hardware report generated successfully.")

if __name__ == "__main__":
    app = HardwareCheckApp()
    app.mainloop()
