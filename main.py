# main.py (Updated for EventBus UI Integration)

import time
# import queue # No longer needed
import logging # Use logging module

from core.telemetry_manager import TelemetryManager
from ui.simple_display import SimpleDisplay
# Import the global event bus instance and Events class
from utils.event_bus import event_bus, Events

# --- Configuration ---
CONNECTION_STRING = '/dev/tty.usbmodem101' # Mac serial
# CONNECTION_STRING = '/dev/ttyACM0'       # Linux serial
# CONNECTION_STRING = 'udp:localhost:14550' # SITL UDP
BAUD_RATE = 115200

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# --- Remove process_queue function ---
# def process_queue(): ... # REMOVED

def main():
    # No longer need global app variable here

    logging.info("Initializing Telemetry Manager...")
    # Pass the global event_bus instance to the manager
    telemetry_manager = TelemetryManager(CONNECTION_STRING, baud=BAUD_RATE, bus=event_bus)

    logging.info("Initializing UI...")
    # UI no longer needs manager directly
    app = SimpleDisplay()

    # --- IMPORTANT: Give the EventBus a reference to the Tk app ---
    # This allows it to schedule UI updates correctly using app.after()
    event_bus.set_tk_app(app)

    # --- Subscribe UI handlers to events ---
    event_bus.subscribe(Events.TELEMETRY_UPDATE, app.handle_telemetry_update)
    event_bus.subscribe(Events.CONNECTION_STATUS_CHANGED, app.handle_connection_status_change)
    event_bus.subscribe(Events.STATUS_TEXT_RECEIVED, app.handle_status_text)
    logging.info("UI event handlers subscribed.")

    # --- Main Execution ---
    try:
        logging.info("Starting Telemetry Manager...")
        if telemetry_manager.start(): # Start the manager thread
             logging.info("Telemetry receiving thread started.")
             # NO queue processing needed - EventBus handles callbacks
             logging.info("Starting UI main loop...")
             app.mainloop() # Start Tkinter event loop (blocks here)
             # --- Code below mainloop() only executes after window is closed ---
             logging.info("UI main loop finished.")
        else:
             logging.error("FATAL: Failed to start Telemetry Manager. Exiting.")
             # Ensure window closes if manager fails to start
             try:
                 app.destroy()
             except tk.TclError: # Catch error if window already destroyed
                 pass

    except Exception as e:
         logging.critical(f"Unhandled exception in main: {e}", exc_info=True)
    finally:
        # --- Graceful Shutdown ---
        # This block executes when mainloop exits (window closed) or on error
        logging.info("Initiating shutdown sequence...")

        # Unsubscribe handlers (optional but good practice)
        try:
            event_bus.unsubscribe(Events.TELEMETRY_UPDATE, app.handle_telemetry_update)
            event_bus.unsubscribe(Events.CONNECTION_STATUS_CHANGED, app.handle_connection_status_change)
            event_bus.unsubscribe(Events.STATUS_TEXT_RECEIVED, app.handle_status_text)
            logging.info("UI Event handlers unsubscribed.")
        except Exception as ue:
             logging.error(f"Error unsubscribing handlers: {ue}")

        # Stop the telemetry manager thread
        # Check if it exists and needs stopping (might have failed to start)
        if hasattr(telemetry_manager, 'stop') and callable(telemetry_manager.stop):
             telemetry_manager.stop()
        else:
             logging.warning("Telemetry manager instance not available for stopping.")

        # Ensure window is closed if not already
        # try:
        #    if app.winfo_exists():
        #        app.destroy()
        # except Exception as de:
        #     logging.error(f"Error destroying app window: {de}")


    logging.info("Application finished.")


if __name__ == "__main__":
    main()