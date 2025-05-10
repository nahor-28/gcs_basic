from controllers.base_controller import BaseController

class StatusController(BaseController):
    """Controller for status-related operations."""
    
    def __init__(self, status_model, status_view, signal_manager):
        """
        Initialize the status controller.
        
        Args:
            status_model: The status model
            status_view: The status view
            signal_manager: The application's signal manager
        """
        super().__init__(status_model, status_view, signal_manager)
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to status signals
            # Status model already connects to status_text_received in its own connect_signals method
            pass
    
    def add_status_message(self, text, severity=0):
        """
        Add a status message.
        
        Args:
            text: Message text
            severity: Message severity (0=info, 1=warning, 2=error)
        """
        if self.model:
            # Add message to the model
            self.model.add_message(text, severity)
    
    def update_view(self):
        """Update the view with current model data."""
        if self.model and self.view:
            # Get data from model
            data = self.model.get_data()
            
            # Update the view
            self.view.update_view(data)
