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
        
        # Notify about status change
        if self.signal_manager:
            self.signal_manager.connection_status_changed.emit(
                self.connection_status, 
                self.status_message
            )
    
    def handle_disconnect_request(self):
        """Handle a disconnect request."""
        self.connection_status = "DISCONNECTED"
        self.status_message = "Disconnected"
        
        # Notify about status change
        if self.signal_manager:
            self.signal_manager.connection_status_changed.emit(
                self.connection_status, 
                self.status_message
            )
    
    def handle_reconnect_request(self):
        """Handle a reconnect request."""
        # Reuse existing connection parameters
        self.handle_connection_request(self.connection_string, self.baud_rate)
    
    def update_connection_status(self, status, message=""):
        """
        Update the connection status.
        
        Args:
            status: New connection status
            message: Status message
        """
        self.connection_status = status
        if message:
            self.status_message = message
        
        # Notify about status change
        if self.signal_manager:
            self.signal_manager.connection_status_changed.emit(
                self.connection_status, 
                self.status_message
            )
    
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
