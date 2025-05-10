from models.base_model import BaseModel
from datetime import datetime

class StatusModel(BaseModel):
    """Model for application status messages."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the status model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.messages = []
        self.max_messages = 100  # Limit number of status messages
        self.connect_signals()
        
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Listen for status messages - use lambda to pass from_signal=True
            # This prevents infinite recursion
            self.signal_manager.status_text_received.connect(
                lambda text, severity: self.add_message(text, severity, from_signal=True)
            )
    
    def add_message(self, text, severity=0, from_signal=False):
        """
        Add a new status message.
        
        Args:
            text: Message text
            severity: Message severity (0=info, 1=warning, 2=error)
            from_signal: Flag to prevent recursive signal emission
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add new message at the beginning
        self.messages.insert(0, {
            "timestamp": timestamp,
            "text": text,
            "severity": severity
        })
        
        # Trim if exceeding max messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[:self.max_messages]
        
        # Notify views, but only if this method wasn't called from the signal
        # to prevent infinite recursion
        if self.signal_manager and not from_signal:
            # Send the most recent message
            self.signal_manager.status_text_received.emit(text, severity)
    
    def get_data(self):
        """
        Get all status messages.
        
        Returns:
            list: List of status messages
        """
        return self.messages
        
    def get_latest_message(self):
        """
        Get the most recent status message.
        
        Returns:
            dict: The most recent status message, or None if no messages
        """
        return self.messages[0] if self.messages else None
