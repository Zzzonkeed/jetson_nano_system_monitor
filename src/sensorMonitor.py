import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/private_key/jetsonNano_firebase_key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://jetson-nano-monitor-default-rtdb.firebaseio.com/"
})

#ref = db.reference('/')
#print(ref.get())



class SensorMonitor(object):
    def __init__(self):
        self.date = ''
        self.ref = db.reference('/')

    def initiateDB(self):
        self.ref.set({
                        "Jetson-Monitor":
                        {
                            "TP16":{"CPU-temp": 0, "GPU-temp": 0, "Heatsink-temp": 0, "Voltage": 0, "Current": 0, "Power": 0, "Timestamp": 0},
                            "TP17":{"CPU-temp": 0, "GPU-temp": 0, "Heatsink-temp": 0, "Voltage": 0, "Current": 0, "Power": 0, "Timestamp": 0},
                            "TP21":{"CPU-temp": 0, "GPU-temp": 0, "Heatsink-temp": 0, "Voltage": 0, "Current": 0, "Power": 0, "Timestamp": 0}
                        }
                    })

    def sendData(self):
        while True:
            #------------------ TIMESTAMP ------------------
            self.date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.ref = db.reference('/Jetson-Monitor/TP16/Timestamp')
            self.ref.push().set(str(self.date))
            #------------------ CPU TEMP -------------------
            with open("/sys/class/thermal/thermal_zone1/temp", 'r') as tempFile: cpu_temp = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/CPU-temp')
            self.ref.push().set(float(cpu_temp)/1000.0)

            #------------------ GPU TEMP -------------------
            with open("/sys/class/thermal/thermal_zone2/temp", 'r') as tempFile: gpu_temp = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/GPU-temp')
            self.ref.push().set(float(gpu_temp)/1000.0)

            #------------------ HEATSINK -------------------
            with open("/sys/class/thermal/thermal_zone5/temp", 'r') as tempFile: sink_temp = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/Heatsink-temp')
            self.ref.push().set(float(sink_temp)/1000.0)

            #------------------ VOLTAGE IN -----------------
            # jetson nano:  cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_voltage0_input
            # notebook:     /sys/class/power_supply/BAT0/voltage_now
            with open("/sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_voltage0_input", 'r') as tempFile: voltage_in = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/Voltage')
            self.ref.push().set(float(voltage_in)/1000000.0)

            #------------------ CURRENT IN -----------------
            with open("/sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_current0_input", 'r') as tempFile: current_in = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/Current')
            self.ref.push().set(float(current_in)/1000000.0)

            #------------------ POWER IN -------------------
            with open("/sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power0_input", 'r') as tempFile: power_in = tempFile.read()
            self.ref = db.reference('/Jetson-Monitor/TP16/Power')
            self.ref.push().set(float(power_in)/1000000.0)

            time.sleep(10)


if __name__ == '__main__':
    jetsonMonitor = SensorMonitor()
    try:
        jetsonMonitor.sendData()
    except:
        pass
