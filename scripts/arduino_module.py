import serial
import time
import threading



class Arduino:

    OPEN_GATE = "OK\n"
    CLOSE_GATE = "NO\n"

    def __init__(self, port, baud_rate=9600, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.connection = None
        self.is_connected = False  # Add is_connected property

    def connect(self):

        def establish_connection():
            try:
                self.connection = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
                time.sleep(2)  # Wait for the connection to establish
                self.is_connected = True  # Set is_connected to True
                #print("Arduino connected successfully.")
            except serial.SerialException as e:
                self.is_connected = False  # Set is_connected to False on failure
                print(f"Failed to connect to Arduino: {e}")

        connection_thread = threading.Thread(target=establish_connection)
        connection_thread.start()
            

    def send_data(self, data):
        if self.connection and self.connection.is_open:
            self.connection.flush()
            self.connection.write(data.encode())
            print(f"Sent data: {data}")
        else:
            print("Connection is not open. Cannot send data.")

    def receive_data(self, timeout=5):
        if self.connection and self.connection.is_open:
            start_time = time.time()
            while True:
                data = self.connection.readline().decode().strip()
                if data:
                    if data:
                        self.connection.reset_input_buffer()  # Clear the serial input buffer
                        self.connection.reset_output_buffer()  # Clear the serial output buffer
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
    
    def reset(self):
        if self.connection and self.connection.is_open:
            self.connection.reset_input_buffer()
            self.connection.reset_output_buffer()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            self.is_connected = False  # Set is_connected to False when closed
            print("Connection closed.")


    def read_rfid(self):
        print("Waiting for RFID scan...")
        data = self.receive_data()
        #if data:
        return data


# Example usage:
# arduino = Arduino(port='/dev/ttyUSB0')
# arduino.connect()
# arduino.send_data('Hello Arduino')
# response = arduino.receive_data()
# arduino.close()