import psutil

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery information not available"
    
    percent = battery.percent
    max_capacity = battery.max
    
    health = (percent / max_capacity) * 100
    
    if health >= 80:
        health_status = "Healthy"
    elif health >= 60:
        health_status = "Fair"
    elif health >= 40:
        health_status = "Poor"
    else:
        health_status = "Very Poor"
    
    return f"Battery Percentage: {percent}%\nMax Capacity: {max_capacity} mAh\nHealth: {health:.2f}% ({health_status})"

if __name__ == "__main__":
    battery_info = get_battery_info()
    print(battery_info)
