from models.base_model import BaseModel
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class StatusModel(BaseModel):
    """Model for handling status messages."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the status model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.messages = []
        self.max_messages = 100  # Max messages to store
        logger.info("StatusModel initialized")
        self.connect_signals()
        
    def connect_signals(self):
        """Connect to relevant signals."""
        if self.signal_manager:
            # logger.debug("StatusModel: Connecting to status_text_received signal")
            self.signal_manager.status_text_received.connect(self._handle_raw_status_text)
        else:
            logger.error("StatusModel: No signal_manager available")
    
    def _handle_raw_status_text(self, text: str, severity: int):
        """Handles a raw status text received from TelemetryManager (e.g., STATUSTEXT)."""
        # logger.debug(f"StatusModel: Received raw status text: '{text}', severity: {severity}")
        self.add_message(text, severity, source="MAVLink")
    
    def add_message(self, text: str, severity: int, timestamp: float = None, source: str = "Application"):
        """Add a new status message."""
        if timestamp is None:
            timestamp = time.time()
            
        # logger.debug(f"StatusModel: Adding message - Text: '{text}', Severity: {severity}, Source: {source}")

        message_data = {
            "text": text,
            "severity": severity,
            "timestamp": timestamp,
            "time_str": datetime.fromtimestamp(timestamp).strftime('%H:%M:%S'),
            "source": source
        }
        
        self.messages.append(message_data)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0) # Remove the oldest message
            
        # Emit a signal with the new message data
        if self.signal_manager:
            # logger.debug(f"StatusModel: Emitting status_model_new_message with data: {message_data}")
            self.signal_manager.status_model_new_message.emit(message_data)
    
    def get_messages(self):
        """Get all current status messages."""
        # logger.debug(f"StatusModel: get_messages called, returning {len(self.messages)} messages")
        return self.messages

    def get_data(self):
        """Get all current status messages (compatible with BaseController)."""
        return self.get_messages()
        
    def get_latest_message(self):
        """
        Get the most recent status message.
        
        Returns:
            dict: The most recent status message, or None if no messages
        """
        return self.messages[0] if self.messages else None
