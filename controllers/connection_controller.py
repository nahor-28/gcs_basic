from controllers.base_controller import BaseController

class ConnectionController(BaseController):
    """Controller for connection-related operations."""
    
    def __init__(self, connection_model, header_view, signal_manager):
        """
        Initialize the connection controller.
        
        Args:
            connection_model: The connection model
            header_view: The header view that contains connection UI
            signal_manager: The application's signal manager
        """
        super().__init__(connection_model, header_view, signal_manager)
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to connection signals
            self.signal_manager.connection_request.connect(self.handle_connection_request)
            self.signal_manager.disconnect_request.connect(self.handle_disconnect_request)
            self.signal_manager.reconnect_request.connect(self.handle_reconnect_request)
    
    def handle_connection_request(self, conn_string, baud_rate):
        """
        Handle connection request.
        
        Args:
            conn_string: Connection string (e.g., 'udp:localhost:14550')
            baud_rate: Baud rate for serial connections
        """
        print(f"ConnectionController: Connecting to {conn_string} at {baud_rate} baud")
        
        if self.model:
            # Update the model
            self.model.handle_connection_request(conn_string, baud_rate)
            
            # In a real application, this would attempt to establish a connection
            # and then update the status based on the result
            
            # For demo purposes, simulate a successful connection
            self.model.update_connection_status("CONNECTED", f"Connected to {conn_string}")
    
    def handle_disconnect_request(self):
        """Handle disconnect request."""
        print("ConnectionController: Disconnecting")
        
        if self.model:
            # Update the model
            self.model.handle_disconnect_request()
            
            # In a real application, this would close the connection
    
    def handle_reconnect_request(self):
        """Handle reconnect request."""
        print("ConnectionController: Reconnecting")
        
        if self.model:
            # Update the model
            self.model.handle_reconnect_request()
            
            # In a real application, this would attempt to reestablish the connection
    
    def update_view(self):
        """Update the view with current model data."""
        if self.model and self.view:
            # Get data from model
            data = self.model.get_data()
            
            # Update the view
            self.view.update_view(data)
