# main.py (Pass initial connection string)

import time
import logging # Use logging module

from core.telemetry_manager import TelemetryManager
from ui.simple_display import SimpleDisplay
from utils.event_bus import event_bus, Events

# --- Configuration ---
# Set the DEFAULT connection string here
DEFAULT_CONNECTION_STRING = 'udp:localhost:14550' # SITL UDP
#DEFAULT_CONNECTION_STRING = '/dev/tty.usbmodem101' # Mac serial
DEFAULT_BAUD_RATE = 115200 # Serial baud rate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# --- Remove process_queue function ---
# def process_queue(): ... # REMOVED

# --- Main Class ---
def main():
    logging.info("Initializing Telemetry Manager...")
    # Pass initial default connection details to the manager
    telemetry_manager = TelemetryManager(
        initial_conn_string=DEFAULT_CONNECTION_STRING,
        initial_baud=DEFAULT_BAUD_RATE,
        bus=event_bus
    )

    logging.info("Initializing UI...")
    app = SimpleDisplay() # UI now reads defaults from its own StringVars

    event_bus.set_tk_app(app)

    # Subscribe UI handlers
    event_bus.subscribe(Events.TELEMETRY_UPDATE, app.handle_telemetry_update)
    event_bus.subscribe(Events.CONNECTION_STATUS_CHANGED, app.handle_connection_status_change)
    event_bus.subscribe(Events.STATUS_TEXT_RECEIVED, app.handle_status_text)
    logging.info("UI event handlers subscribed.")

    try:
        # --- Start the UI first, manager connects on user command ---
        # logging.info("Starting Telemetry Manager...") # DON'T start automatically
        # if telemetry_manager.start(): ... # REMOVED

        logging.info("Starting UI main loop...")
        app.mainloop() # Start Tkinter event loop
        logging.info("UI main loop finished.")

    except Exception as e:
         logging.critical(f"Unhandled exception in main: {e}", exc_info=True)
    finally:
        logging.info("Initiating shutdown sequence...")
        # Unsubscribe handlers
        try:
            # ... (unsubscribing code remains the same) ...
            event_bus.unsubscribe(Events.TELEMETRY_UPDATE, app.handle_telemetry_update)
            event_bus.unsubscribe(Events.CONNECTION_STATUS_CHANGED, app.handle_connection_status_change)
            event_bus.unsubscribe(Events.STATUS_TEXT_RECEIVED, app.handle_status_text)
            # Unsubscribe manager handlers too
            event_bus.unsubscribe(Events.CONNECT_REQUEST, telemetry_manager.handle_connect_request)
            event_bus.unsubscribe(Events.DISCONNECT_REQUEST, telemetry_manager.handle_disconnect_request)
            logging.info("Event handlers unsubscribed.")
        except Exception as ue:
             logging.error(f"Error unsubscribing handlers: {ue}")

        # Stop the telemetry manager if it was running
        telemetry_manager.stop() # Call stop regardless of state, it handles checks internally

    logging.info("Application finished.")

if __name__ == "__main__":
    main()