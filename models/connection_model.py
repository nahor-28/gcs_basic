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
        self.connection_string = "udp:0.0.0.0:14550"
        self.baud_rate = 115200
        self.connection_status = "DISCONNECTED"
        self.status_message = "Not connected"
        self.connect_signals()
        logger.debug("ConnectionModel initialized")
        
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
    
    def _emit_model_changed(self):
        """Emit a signal indicating the model's data has changed."""
        current_data = self.get_data()
        logger.debug(f"ConnectionModel: Emitting connection_model_changed with data: {current_data}")
        if self.signal_manager:
            self.signal_manager.connection_model_changed.emit(current_data)
        else:
            logger.error("ConnectionModel: Cannot emit connection_model_changed - no signal_manager")
    
    def handle_connection_request(self, conn_string, baud_rate):
        """
        Handle a connection request.
        
        Args:
            conn_string: Connection string (e.g., 'udp:localhost:14550')
            baud_rate: Baud rate for serial connections
        """
        logger.debug(f"ConnectionModel: Handling connection request for {conn_string} at {baud_rate} baud")
        self.connection_string = conn_string
        self.baud_rate = baud_rate
        self.connection_status = "CONNECTING"
        self.status_message = f"Connecting to {conn_string}..."
        self._emit_model_changed()
    
    def handle_disconnect_request(self):
        """Handle a disconnect request."""
        logger.debug("ConnectionModel: Handling disconnect request")
        self.connection_status = "DISCONNECTED"
        self.status_message = "Disconnected"
        self._emit_model_changed()
    
    def update_connection_status(self, status: str, message: str = "", actual_conn_string: str | None = None):
        """
        Update the connection status based on external updates (e.g., from TelemetryManager).
        
        Args:
            status: The new connection status ("CONNECTED", "DISCONNECTED", etc.)
            message: Optional status message
            actual_conn_string: Optional connection string that was actually used
        """
        logger.debug(f"ConnectionModel: Updating connection status - status={status}, message={message}, actual_conn_string={actual_conn_string}")
        changed = False

        # Update connection string if provided
        if actual_conn_string and self.connection_string != actual_conn_string:
            self.connection_string = actual_conn_string
            changed = True
            logger.debug(f"ConnectionModel: Updated connection string to {actual_conn_string}")

        # Update status if changed
        if self.connection_status != status:
            self.connection_status = status
            changed = True
            logger.debug(f"ConnectionModel: Updated status to {status}")
        
        # Update message if provided and changed
        if message and self.status_message != message:
            self.status_message = message
            changed = True
            logger.debug(f"ConnectionModel: Updated message to {message}")
        elif not message and self.status_message: 
            self.status_message = ""
            changed = True
            logger.debug("ConnectionModel: Cleared message")

        # Emit model changed signal if anything changed
        if changed:
            self._emit_model_changed()
        else:
            logger.debug("ConnectionModel: No changes to emit")
    
    def get_data(self):
        """
        Get the current connection data.
        
        Returns:
            dict: The current connection data
        """
        return {
            "connection_string": self.connection_string,
            "baud_rate": self.baud_rate,
            "status": self.connection_status,
            "message": self.status_message
        }
