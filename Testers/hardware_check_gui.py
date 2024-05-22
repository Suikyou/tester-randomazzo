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
        return f"Battery Information:\n{battery_info}\n{health_info}"
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

def run_checks():
    output = check_ram()
    output += check_storage()
    output += check_battery()
    output += check_cpu()
    output += check_network()
    output += check_audio()
    return output

# Keyboard Test GUI
class KeyboardTestApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Keyboard Test")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.bind("<KeyPress>", self.on_key_press)
        self.tested_keys = set()

        self.label = tk.Label(self, text="Press each key on the keyboard. The key will turn green when pressed.", font=("Arial", 14))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.keys = [
            "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BackSpace",
            "Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
            "Caps_Lock", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Return",
            "Shift_L", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Shift_R",
            "Control_L", "Super_L", "Alt_L", "space", "Alt_R", "Menu", "Control_R",
            "Left", "Up", "Down", "Right"
        ]

        self.key_buttons = {}
        for key in self.keys:
            btn = tk.Button(self.canvas, text=key, width=5, height=2, bg="red", fg="white", font=("Arial", 10))
            self.key_buttons[key] = btn

        self.position_keys()

        self.fail_button = tk.Button(self, text="Test Failed", command=self.fail_test)
        self.fail_button.pack(pady=10)

    def position_keys(self):
        # Position keys on the canvas (this is a simplified layout, adjust as needed)
        positions = [
            (5, 5, "Escape"), (80, 5, "F1"), (120, 5, "F2"), (160, 5, "F3"), (200, 5, "F4"), (240, 5, "F5"),
            (280, 5, "F6"), (320, 5, "F7"), (360, 5, "F8"), (400, 5, "F9"), (440, 5, "F10"), (480, 5, "F11"), (520, 5, "F12"),
            (5, 45, "`"), (45, 45, "1"), (85, 45, "2"), (125, 45, "3"), (165, 45, "4"), (205, 45, "5"),
            (245, 45, "6"), (285, 45, "7"), (325, 45, "8"), (365, 45, "9"), (405, 45, "0"), (445, 45, "-"),
            (485, 45, "="), (525, 45, "BackSpace"),
            (5, 85, "Tab"), (45, 85, "q"), (85, 85, "w"), (125, 85, "e"), (165, 85, "r"), (205, 85, "t"),
            (245, 85, "y"), (285, 85, "u"), (325, 85, "i"), (365, 85, "o"), (405, 85, "p"), (445, 85, "["),
            (485, 85, "]"), (525, 85, "\\"),
            (5, 125, "Caps_Lock"), (45, 125, "a"), (85, 125, "s"), (125, 125, "d"), (165, 125, "f"), (205, 125, "g"),
            (245, 125, "h"), (285, 125, "j"), (325, 125, "k"), (365, 125, "l"), (405, 125, ";"), (445, 125, "'"),
            (485, 125, "Return"),
            (5, 165, "Shift_L"), (65, 165, "z"), (105, 165, "x"), (145, 165, "c"), (185, 165, "v"), (225, 165, "b"),
            (265, 165, "n"), (305, 165, "m"), (345, 165, ","), (385, 165, "."), (425, 165, "/"), (465, 165, "Shift_R"),
            (5, 205, "Control_L"), (65, 205, "Super_L"), (125, 205, "Alt_L"), (185, 205, "space"), (425, 205, "Alt_R"),
            (485, 205, "Menu"), (525, 205, "Control_R"),
            (565, 245, "Left"), (605, 205, "Up"), (605, 245, "Down"), (645, 245, "Right")
        ]
        for x, y, key in positions:
            btn = self.key_buttons.get(key)
            if btn:
                self.canvas.create_window(x, y, anchor=tk.NW, window=btn)

    def on_key_press(self, event):
        key = event.keysym
        if key in self.key_buttons:
            self.key_buttons[key].config(bg="green")
            self.tested_keys.add(key)
            if self.tested_keys == set(self.keys):
                messagebox.showinfo("Keyboard Test", "All keys have been tested successfully!")
                self.destroy()

    def fail_test(self):
        messagebox.showerror("Keyboard Test", "Keyboard test failed.")
        self.destroy()

# GUI Code
class HardwareCheckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Check Tool")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.label = tk.Label(self, text="Hardware Check Tool", font=("Arial", 16))
        self.label.pack(pady=10)

        self.run_button = tk.Button(self, text="Run Checks", command=self.run_checks)
        self.run_button.pack(pady=10)

        self.keyboard_button = tk.Button(self, text="Check Keyboard", command=self.open_keyboard_test)
        self.keyboard_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def run_checks(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, "Running checks...\n")
        output = run_checks()
        self.output_text.insert(tk.INSERT, output)
        messagebox.showinfo("Checks Completed", "Hardware checks completed successfully.")

    def open_keyboard_test(self):
        KeyboardTestApp(self)

if __name__ == "__main__":
    app = HardwareCheckApp()
    app.mainloop()
