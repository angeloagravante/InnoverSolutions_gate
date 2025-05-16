import serial
import time
import threading


class Arduino:
    OPEN_GATE = "OK\n"
    CLOSE_GATE = "NO\n"
    
    @staticmethod
    def ensure_connection(func):
        """Decorator to ensure the Arduino is connected before executing a method."""
        def wrapper(self, *args, **kwargs):
            if not self.is_connected:
                print("Arduino not connected. Attempting to reconnect...")
                self.find_and_connect()
                if not self.is_connected:
                    raise ConnectionError("Failed to establish a connection with the Arduino.")
            return func(self, *args, **kwargs)
        return wrapper



    def __init__(self, port=None, baud_rate=9600, timeout=1):
        self._port = port
        self._baud_rate = baud_rate
        self._timeout = timeout
        self._connection = None
        self._is_connected = False

    @property
    def is_connected(self):
        if self._connection and self._connection.is_open:
            try:
                self._connection.in_waiting  # Check if the connection is still responsive
                return True
            except (serial.SerialException, OSError):
                print("Connection lost. Attempting to reconnect...")
                self.find_and_connect()
                return self._is_connected
        else:
            print("Connection is not open. Attempting to reconnect...")
            self.find_and_connect()
            return self._is_connected

    @property
    def port(self):
        return self._port

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Timeout must be an integer or float.")
        if value <= 0:
            raise ValueError("Timeout must be greater than zero.")
        self._timeout = value

    def connect(self):
        try:
            self._connection = serial.Serial(self.port, self._baud_rate, timeout=self.timeout)
            time.sleep(2)  # Wait for the connection to establish
            self._is_connected = True
            print(f"Arduino connected successfully on port {self.port}.")
        except serial.SerialException as e:
            self._is_connected = False
            print(f"Failed to connect to Arduino: {e}")

    def find_and_connect(self):
        """Attempt to find the correct port, reset the serial connection, and connect to the Arduino."""
        for port in serial.tools.list_ports.comports():
            try:
                if "IOUSBHostDevice" in port.description or "tty" in port.device or "Arduino" in port.description:
                    print(f"Trying port: {port.device}")
                    self._port = port.device
                    if self._connection and self._connection.is_open:
                        self._connection.close()  # Reset the serial connection
                        print(f"Resetting connection on port {port.device}.")
                    self.connect()
                    if self.is_connected:
                        print(f"Connected to Arduino on port {self.port}.")
                        return 

            except Exception as e:
                print(f"Error connecting to port {port.device}: {e}")

    @ensure_connection
    def send_data(self, data):
        if self._connection and self._connection.is_open:
            self._connection.flush()
            self._connection.write(data.encode())
            print(f"Sent data: {data}")
        else:
            print("Connection is not open. Cannot send data.")

    @ensure_connection
    def receive_data(self, timeout=5):
        if self._connection and self._connection.is_open:
            start_time = time.time()
            while True:
                data = self._connection.readline().decode().strip()
                if data:
                    self.reset()
                    return data
                elif time.time() - start_time > timeout:
                    print("Timeout reached. No data received.")
                    return None
                else:
                    print("Waiting for data...")
                    time.sleep(0.5)
        else:
            print("Connection is not open. Cannot receive data.")
            return None
    
        """Resets the input and output buffers of the serial connection."""
    def reset(self, reset_input=True, reset_output=True):
        if self._connection and self._connection.is_open:
            if reset_input:
                self._connection.reset_input_buffer()
            if reset_output:
                self._connection.reset_output_buffer()
    def close(self):
        if self._connection and self._connection.is_open:
            self._connection.close()
            self._is_connected = False
            print("Connection closed.")

    @ensure_connection
    def read_rfid(self):
        print("Waiting for RFID scan...")
        data = self.receive_data()
        return data


# Example usage:
# arduino = Arduino()
# arduino.find_and_connect()
# arduino.send_data('Hello Arduino')
# response = arduino.receive_data()
# arduino.close()