from models.base_model import BaseModel
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ConnectionModel(BaseModel):
    """Model for connection-related data."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the connection model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.connection_status = "DISCONNECTED" # e.g., DISCONNECTED, CONNECTING, CONNECTED, ERROR
        self.connection_message = ""
        self.connection_string = "udp:0.0.0.0:14550" # Default value or last used
        self.baud_rate = 115200
        self.available_ports = []
        self.connected_to_actual = ""
        self.connect_signals()
        logger.info("ConnectionModel initialized")
        
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Listen to connection status updates from TelemetryManager
            logger.debug("ConnectionModel: Connecting to connection_status_changed signal")
            self.signal_manager.connection_status_changed.connect(self._handle_external_status_update)
        else:
            logger.error("ConnectionModel: No signal_manager available for signal connections")
    
    def _handle_external_status_update(self, status: str, message: str, actual_conn_string: str):
        """Handles status updates typically from TelemetryManager."""
        logger.debug(f"ConnectionModel: Received status update - status={status}, message={message}, conn_string={actual_conn_string}")
        self.update_connection_status(status, message, actual_conn_string)
    
    def _emit_changed(self):
        """Emit a signal that the model has changed."""
        # logger.debug("ConnectionModel: Emitting connection_model_changed signal")
        if self.signal_manager:
            self.signal_manager.connection_model_changed.emit(self.get_data())
            
    def update_connection_status(self, status: str, message: str = "", conn_str_actual: str = ""):
        """Update connection status and emit a signal."""
        # logger.debug(f"ConnectionModel: Updating status to {status}, message: '{message}', actual_conn: '{conn_str_actual}'")
        self.connection_status = status
        self.connection_message = message
        if conn_str_actual:
            self.connected_to_actual = conn_str_actual
        self._emit_changed()
        
    def handle_connection_request(self, conn_string: str, baud_rate: int):
        """Handle a connection request by updating model state."""
        # logger.debug(f"ConnectionModel: Handling connection request for {conn_string} at {baud_rate}")
        self.connection_string = conn_string
        self.baud_rate = baud_rate
        self.connection_status = "CONNECTING"
        self.connection_message = f"Attempting to connect to {conn_string}..."
        self._emit_changed()
        
    def handle_disconnect_request(self):
        """Handle a disconnect request."""
        # logger.debug("ConnectionModel: Handling disconnect request")
        self.connection_status = "DISCONNECTED"
        self.connection_message = "Disconnected"
        self.connected_to_actual = ""
        self._emit_changed()
        
    def set_available_ports(self, ports: list):
        """Set the list of available serial ports."""
        # logger.debug(f"ConnectionModel: Setting available ports: {ports}")
        self.available_ports = ports
        self._emit_changed()

    def get_data(self):
        """Get all current connection data."""
        data = {
            "status": self.connection_status,
            "message": self.connection_message,
            "connection_string": self.connection_string,
            "baud_rate": self.baud_rate,
            "available_ports": self.available_ports,
            "connected_to_actual": self.connected_to_actual
        }
        # logger.debug(f"ConnectionModel: get_data called, returning: {data}")
        return data
