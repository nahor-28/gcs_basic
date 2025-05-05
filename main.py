# main.py (Updated for UI Integration)

import time
import queue
from core.telemetry_manager import TelemetryManager
from ui.simple_display import SimpleDisplay # Import the UI class

# --- Configuration ---
CONNECTION_STRING = '/dev/tty.usbmodem101' # Mac serial
# CONNECTION_STRING = '/dev/ttyACM0'       # Linux serial
# CONNECTION_STRING = 'udp:localhost:14550' # SITL UDP
BAUD_RATE = 115200

# How often to check the queue for updates (milliseconds)
QUEUE_CHECK_INTERVAL_MS = 100

# --- Global variable for the app instance ---
# This is simpler than passing it around explicitly for the after() loop
app = None

def process_queue():
    """Processes messages from the telemetry queue and updates the UI."""
    global app # Need to access the global app instance
    if not app:
        print("ERROR: App not initialized in process_queue")
        return

    manager = app.telemetry_manager # Get manager from app
    if not manager:
        print("ERROR: Telemetry Manager not found in app")
        return

    data_queue = manager.get_data_queue()
    processed_count = 0
    max_batch = 20 # Process up to 20 messages per cycle to avoid freezing UI

    try:
        while processed_count < max_batch:
            data_update = data_queue.get_nowait()
            # print(f"UI Processing: {data_update}") # Debug print
            app.update_telemetry(data_update) # Call the UI update method
            processed_count += 1
    except queue.Empty:
        # No more messages in the queue for now
        pass
    except Exception as e:
         print(f"Error processing queue: {type(e).__name__}: {e}")
    finally:
        # Schedule the next check
        app.after(QUEUE_CHECK_INTERVAL_MS, process_queue)


def main():
    global app # Declare app as global to assign the instance

    print("Initializing Telemetry Manager...")
    # Note: We don't pass the queue here, manager creates its own
    telemetry_manager = TelemetryManager(CONNECTION_STRING, baud=BAUD_RATE)

    print("Initializing UI...")
    # Pass the manager instance to the UI for shutdown handling
    app = SimpleDisplay(telemetry_manager)

    try:
        print("Starting Telemetry Manager...")
        if telemetry_manager.start(): # Start the manager
             print("Telemetry receiving thread started.")
             # Schedule the first call to process the queue after UI is ready
             app.after(QUEUE_CHECK_INTERVAL_MS, process_queue)
             print("Starting UI main loop...")
             app.mainloop() # Start the Tkinter event loop (blocks until window closed)
        else:
             print("FATAL: Failed to start Telemetry Manager. Exiting.")
             app.destroy() # Close the (potentially empty) window
    except Exception as e:
        print(f"Unhandled exception occurred: {type(e).__name__}: {e}")

    # No 'finally' block needed here for manager.stop(),
    # because app.on_closing() handles calling manager.stop() when the window is closed.

    print("Application finished.")


if __name__ == "__main__":
    main()