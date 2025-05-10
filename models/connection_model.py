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
            # Connect to relevant signals
            self.signal_manager.connection_request.connect(self.handle_connection_request)
            self.signal_manager.disconnect_request.connect(self.handle_disconnect_request)
            self.signal_manager.reconnect_request.connect(self.handle_reconnect_request)
    
    def _emit_model_changed(self):
        """Emit a signal indicating the model's data has changed."""
        if self.signal_manager:
            self.signal_manager.connection_model_changed.emit(self.get_data())
    
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
        self._emit_model_changed()
    
    def handle_disconnect_request(self):
        """Handle a disconnect request."""
        self.connection_status = "DISCONNECTED"
        self.status_message = "Disconnected"
        self._emit_model_changed()
    
    def handle_reconnect_request(self):
        """Handle a reconnect request."""
        self.connection_status = "CONNECTING" # Set to connecting before emitting
        self.status_message = f"Reconnecting to {self.connection_string}..."
        self._emit_model_changed() 
        # Actual reconnect logic might be triggered by ConnectionController
        # telling TelemetryManager to connect, which then updates status.
    
    def update_connection_status(self, status, message=""):
        """
        Update the connection status. Called by ConnectionController or TelemetryManager.
        """
        changed = False
        if self.connection_status != status:
            self.connection_status = status
            changed = True
        if message and self.status_message != message:
            self.status_message = message
            changed = True
        
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
