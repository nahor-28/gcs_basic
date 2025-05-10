from PySide6.QtCore import QObject

class ConnectionController(QObject):
    """Controller for connection-related operations."""
    
    def __init__(self, connection_model, header_view, signal_manager):
        super().__init__()
        self.connection_model = connection_model
        self.header_view = header_view
        self.signal_manager = signal_manager
        
        # Connect view signals
        if header_view:
            header_view.connect_requested.connect(self.connect)
            header_view.disconnect_requested.connect(self.disconnect)
            
    def connect(self, connection_string, baud_rate):
        """Connect to vehicle."""
        self.connection_model.connect(connection_string, baud_rate)
        self.update_view()
        
    def disconnect(self):
        """Disconnect from vehicle."""
        self.connection_model.disconnect()
        self.update_view()
        
    def update_view(self):
        """Update the header view with current connection state."""
        if self.header_view:
            self.header_view.update_view(self.connection_model.data)