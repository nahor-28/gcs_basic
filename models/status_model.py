from PySide6.QtCore import QObject
from collections import deque

class StatusModel(QObject):
    """Model for status messages and system state."""
    
    def __init__(self, signal_manager, max_messages=100):
        super().__init__()
        self.signal_manager = signal_manager
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)
        
        # Connect to signal manager
        if signal_manager:
            signal_manager.status_text_received.connect(self.add_message)
            
    def add_message(self, text, severity):
        """Add a new status message."""
        message = {
            'text': text,
            'severity': severity,
            'timestamp': None  # Could add timestamp if needed
        }
        self.messages.append(message)
        
    def get_messages(self):
        """Get all status messages."""
        return list(self.messages)
        
    def clear_messages(self):
        """Clear all status messages."""
        self.messages.clear() 