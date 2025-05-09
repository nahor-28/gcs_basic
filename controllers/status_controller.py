from PySide6.QtCore import QObject

class StatusController(QObject):
    """Controller for status-related operations."""
    
    def __init__(self, status_model, status_view, signal_manager):
        super().__init__()
        self.status_model = status_model
        self.status_view = status_view
        self.signal_manager = signal_manager
        
    def update_view(self):
        """Update the status view with current messages."""
        if self.status_view:
            # Pass messages as a dictionary with type and data
            self.status_view.update_view({
                'type': 'messages',
                'data': self.status_model.get_messages()
            })
            
    def clear_messages(self):
        """Clear all status messages."""
        self.status_model.clear_messages()
        self.update_view() 