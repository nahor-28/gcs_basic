from controllers.base_controller import BaseController

class StatusController(BaseController):
    """Controller for status-related operations."""
    
    def __init__(self, status_model, status_view_is_no_longer_passed, signal_manager):
        # status_view is no longer passed for direct updates.
        super().__init__(status_model, None, signal_manager)
        # self.connect_signals() # Called by BaseController
    
    def connect_signals(self):
        """Connect signal handlers."""
        # This controller primarily acts by having its methods called.
        # For example, other components might call add_status_message.
        # It doesn't necessarily need to listen to signals itself, unless
        # it were to react to some external events to generate status messages.
        # The StatusModel itself will emit signals for the StatusView.
        if self.signal_manager:
            # Example: If this controller needed to listen to raw STATUSTEXT from telemetry
            # self.signal_manager.status_text_received.connect(self.handle_raw_status_text)
            pass # No specific signals to connect to for this refactored role by default

    # def handle_raw_status_text(self, text, severity):
    #     """If controller were to listen to raw status text to then update model."""
    #     self.add_status_message(text, severity)

    def add_status_message(self, text, severity=0, timestamp=None):
        """
        Add a status message to the model.
        The model will then emit a signal for the view.
        
        Args:
            text: Message text
            severity: Message severity (0=info, 1=warning, 2=error)
            timestamp: Optional timestamp string or object
        """
        if self.model:
            # Pass timestamp to the model's add_message method
            self.model.add_message(text, severity, timestamp)
    
    # Remove the update_view method
    # def update_view(self):
    #     ...
