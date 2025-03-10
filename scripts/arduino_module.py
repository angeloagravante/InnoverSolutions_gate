import serial
import time

class Arduino:
    def __init__(self, port, baud_rate=9600, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)  # Wait for the connection to establish
            print(f"Connected to Arduino on port {self.port}")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino: {e}")

    def send_data(self, data):
        if self.connection and self.connection.is_open:
            self.connection.write(data.encode())
            print(f"Sent data: {data}")
        else:
            print("Connection is not open. Cannot send data.")

    def receive_data(self):
        if self.connection and self.connection.is_open:
            data = self.connection.readline().decode().strip()
            print(f"Received data: {data}")
            return data
        else:
            print("Connection is not open. Cannot receive data.")
            return None

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Connection closed.")

# Example usage:
# arduino = Arduino(port='/dev/ttyUSB0')
# arduino.connect()
# arduino.send_data('Hello Arduino')
# response = arduino.receive_data()
# arduino.close()