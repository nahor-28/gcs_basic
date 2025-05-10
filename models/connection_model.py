from models.base_model import BaseModel

class ConnectionModel(BaseModel):
    """Model for connection-related data."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the connection model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.connection_string = "udp:localhost:14550"
        self.baud_rate = 115200
        self.connection_status = "DISCONNECTED"
        self.status_message = "Not connected"
        self.connect_signals()
        
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Listen to connection status updates from TelemetryManager
            self.signal_manager.connection_status_changed.connect(self._handle_external_status_update)
    
    def _handle_external_status_update(self, status: str, message: str, actual_conn_string: str):
        """Handles status updates typically from TelemetryManager."""
        print(f"ConnectionModel: Received status={status}, message={message}, actual_conn_string={actual_conn_string}")
        self.update_connection_status(status, message, actual_conn_string)
    
    def _emit_model_changed(self):
        """Emit a signal indicating the model's data has changed."""
        current_data = self.get_data()
        print(f"ConnectionModel: Emitting connection_model_changed with data: {current_data}")
        if self.signal_manager:
            self.signal_manager.connection_model_changed.emit(current_data)
    
    def handle_connection_request(self, conn_string, baud_rate):
        """
        Handle a connection request.
        
        Args:
            conn_string: Connection string (e.g., 'udp:localhost:14550')
            baud_rate: Baud rate for serial connections
        """
        self.connection_string = conn_string
        self.baud_rate = baud_rate
        self.connection_status = "CONNECTING"
        self.status_message = f"Connecting to {conn_string}..."
        print(f"ConnectionModel: Setting status to CONNECTING for {conn_string}")
        self._emit_model_changed()
    
    def handle_disconnect_request(self):
        """Handle a disconnect request."""
        self.connection_status = "DISCONNECTED"
        self.status_message = "Disconnected"
        print(f"ConnectionModel: Setting status to DISCONNECTED")
        self._emit_model_changed()
    
    def update_connection_status(self, status: str, message: str = "", actual_conn_string: str | None = None):
        """
        Update the connection status based on external updates (e.g., from TelemetryManager).
        
        Args:
            status: The new connection status ("CONNECTED", "DISCONNECTED", etc.)
            message: Optional status message
            actual_conn_string: Optional connection string that was actually used
        """
        changed = False

        # Update connection string if provided
        if actual_conn_string and self.connection_string != actual_conn_string:
            self.connection_string = actual_conn_string
            changed = True
            print(f"ConnectionModel: Updated connection string to {actual_conn_string}")

        # Update status if changed
        if self.connection_status != status:
            self.connection_status = status
            changed = True
            print(f"ConnectionModel: Updated status to {status}")
        
        # Update message if provided and changed
        if message and self.status_message != message:
            self.status_message = message
            changed = True
            print(f"ConnectionModel: Updated message to {message}")
        elif not message and self.status_message: 
            self.status_message = ""
            changed = True
            print(f"ConnectionModel: Cleared message")

        # Emit model changed signal if anything changed
        if changed:
            self._emit_model_changed()
    
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
