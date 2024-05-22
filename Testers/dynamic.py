import subprocess

def check_keyboard():
    print("Checking keyboard. Please press some keys...")
    try:
        subprocess.run(["xev"], timeout=10)
        print("Keyboard is working properly.")
    except subprocess.TimeoutExpired:
        print("Keyboard check timed out. It may not be working properly.")
    except subprocess.CalledProcessError as e:
        print("Failed to check keyboard:", e)

def check_trackpad():
    print("Checking trackpad. Please move the trackpad...")
    try:
        subprocess.run(["xinput", "test", "Virtual core pointer"], timeout=10)
        print("Trackpad is working properly.")
    except subprocess.TimeoutExpired:
        print("Trackpad check timed out. It may not be working properly.")
    except subprocess.CalledProcessError as e:
        print("Failed to check trackpad:", e)

def main_dynamic():
    print("Starting dynamic hardware checks...")
    check_keyboard()
    check_trackpad()
    print("Dynamic hardware checks completed.")

if __name__ == "__main__":
    main_dynamic()
