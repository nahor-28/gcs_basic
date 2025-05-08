# main.py

import sys
import logging
from PySide6.QtWidgets import QApplication

from core.telemetry_manager import TelemetryManager
from core.signal_manager import SignalManager
from ui.main_window import MainWindow

# --- Configuration ---
# Set the DEFAULT connection string here
DEFAULT_CONNECTION_STRING = 'udp:localhost:14550' # SITL UDP
#DEFAULT_CONNECTION_STRING = '/dev/tty.usbmodem101' # Mac serial
DEFAULT_BAUD_RATE = 115200 # Serial baud rate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# --- Main Class ---
def main():
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # Create signal manager
    signal_manager = SignalManager()
    
    # Create telemetry manager
    telemetry_manager = TelemetryManager(
        initial_conn_string=DEFAULT_CONNECTION_STRING,
        initial_baud=DEFAULT_BAUD_RATE,
        signal_manager=signal_manager
    )
    
    # Create main window
    window = MainWindow(signal_manager)
    window.show()
    
    # Start Qt event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())