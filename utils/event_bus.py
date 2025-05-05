# utils/event_bus.py

import collections
import threading
import queue
import logging # Use logging for better feedback

# Optional: Define standard event names using an Enum or just constants
class Events:
    # Telemetry related
    TELEMETRY_UPDATE = "telemetry_update" # Data: dict (parsed message data)

    # Connection related
    CONNECTION_REQUEST = "connection_request" # Data: dict {'conn_string': str, 'baud': int}
    CONNECTION_STATUS_CHANGED = "connection_status_changed" # Data: dict {'status': str, 'message': str}
                                                            # e.g. status='CONNECTING'/'CONNECTED'/'DISCONNECTED'/'ERROR'

    # Vehicle/User Messages
    STATUS_TEXT_RECEIVED = "status_text_received" # Data: dict {'text': str, 'severity': int}

    # Command related (Examples)
    ARM_REQUEST = "arm_request" # Data: None
    DISARM_REQUEST = "disarm_request" # Data: None
    # Add more events as needed


class EventBus:
    def __init__(self):
        # Using defaultdict simplifies subscription handling
        # Key: event_type (str), Value: list of handler functions
        self._subscribers = collections.defaultdict(list)
        # Lock for protecting access to the _subscribers dictionary
        self._lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("EventBus initialized.")

        # --- Placeholder for UI thread safety ---
        # We'll need a reference to the Tkinter app or a way to schedule calls
        # on the main thread later. For now, handlers will be called directly.
        self._ui_queue = None # To be set later, maybe queue.Queue()
        self._tk_app_ref = None # To be set later

    def subscribe(self, event_type: str, handler):
        """Subscribes a handler function to a specific event type."""
        if not callable(handler):
             logging.error(f"Attempted to subscribe non-callable handler to '{event_type}'")
             return

        with self._lock:
            handlers = self._subscribers[event_type]
            if handler not in handlers:
                handlers.append(handler)
                logging.debug(f"Handler {handler.__name__} subscribed to '{event_type}'")
            else:
                 logging.warning(f"Handler {handler.__name__} already subscribed to '{event_type}'")

    def unsubscribe(self, event_type: str, handler):
        """Unsubscribes a handler function from a specific event type."""
        with self._lock:
            handlers = self._subscribers[event_type]
            if handler in handlers:
                handlers.remove(handler)
                logging.debug(f"Handler {handler.__name__} unsubscribed from '{event_type}'")
                # Clean up empty event type keys if desired (optional)
                if not handlers:
                    del self._subscribers[event_type]
            else:
                 logging.warning(f"Attempted to unsubscribe handler {handler.__name__} not found for '{event_type}'")

    def publish(self, event_type: str, *args, **kwargs):
        """
        Publishes an event, calling all subscribed handlers.
        NOTE: Currently calls handlers directly in the publisher's thread.
              UI thread safety needs to be added.
        """
        logging.debug(f"Publishing event '{event_type}' with args={args}, kwargs={kwargs}")
        # Make a copy of the handlers list to iterate over,
        # in case a handler tries to unsubscribe itself during iteration.
        with self._lock:
            # Use .get() to avoid creating an empty list if no subscribers exist
            handlers = list(self._subscribers.get(event_type, []))

        if not handlers:
            logging.debug(f"No subscribers for event '{event_type}'")
            return

        for handler in handlers:
            try:
                # --- Direct call (Needs modification for UI thread safety) ---
                # TODO: Add mechanism to check if handler needs UI thread execution
                # if is_ui_handler(handler):
                #    self.schedule_on_ui_thread(handler, args, kwargs)
                # else:
                handler(*args, **kwargs) # Direct call for now
                # --------------------------------------------------------------
                logging.debug(f"Called handler {handler.__name__} for '{event_type}'")
            except Exception as e:
                logging.error(f"Error executing handler {getattr(handler, '__name__', 'unknown')} for event '{event_type}': {e}", exc_info=True) # Log traceback


    # --- Methods for UI Thread Safety (To be implemented later) ---

    def set_tk_app(self, tk_app):
        """Stores a reference to the main Tkinter application instance."""
        logging.info("Tkinter app reference set for EventBus UI scheduling.")
        self._tk_app_ref = tk_app

    def schedule_on_ui_thread(self, handler, args, kwargs):
        """Schedules a handler to be called on the Tkinter UI thread."""
        if self._tk_app_ref:
            # Use Tkinter's 'after' mechanism to run the handler in the main loop
            # The lambda captures the current args/kwargs for the scheduled call
            self._tk_app_ref.after(0, lambda h=handler, a=args, k=kwargs: self._safe_ui_call(h, a, k))
        else:
            logging.warning("Cannot schedule on UI thread: Tkinter app reference not set. Calling directly.")
            # Fallback to direct call if Tk reference isn't set (undesirable for UI)
            self._safe_ui_call(handler, args, kwargs)

    def _safe_ui_call(self, handler, args, kwargs):
         """Wrapper to safely call a handler and log errors."""
         try:
             handler(*args, **kwargs)
         except Exception as e:
              logging.error(f"Error executing UI handler {getattr(handler, '__name__', 'unknown')}: {e}", exc_info=True)


    # --- Modified publish method incorporating UI scheduling ---
    def publish_safe(self, event_type: str, *args, **kwargs):
        """
        Publishes an event, calling handlers. Checks if handler needs UI thread.
        Assumes handlers that need UI thread are methods of the Tkinter app instance.
        """
        logging.debug(f"Publishing event '{event_type}' with args={args}, kwargs={kwargs}")
        with self._lock:
            handlers = list(self._subscribers.get(event_type, []))

        if not handlers:
            logging.debug(f"No subscribers for event '{event_type}'")
            return

        for handler in handlers:
            # --- Check if handler seems to be a UI method ---
            # Simple check: Is the handler a method bound to our stored Tk app instance?
            # This requires set_tk_app() to have been called.
            # More robust checking might involve decorators or naming conventions.
            is_ui_handler = False
            if self._tk_app_ref and hasattr(handler, '__self__') and handler.__self__ is self._tk_app_ref:
                 is_ui_handler = True

            if is_ui_handler:
                 self.schedule_on_ui_thread(handler, args, kwargs)
                 logging.debug(f"Scheduled UI handler {handler.__name__} for '{event_type}'")
            else:
                try:
                    # Call non-UI handlers directly (e.g., TelemetryManager handling a command)
                    handler(*args, **kwargs)
                    logging.debug(f"Called non-UI handler {handler.__name__} for '{event_type}'")
                except Exception as e:
                    logging.error(f"Error executing non-UI handler {getattr(handler, '__name__', 'unknown')} for event '{event_type}': {e}", exc_info=True)


# --- Global EventBus Instance ---
# Create a single instance that can be imported and used across modules
# This is a simple approach; dependency injection is another option.
event_bus = EventBus()