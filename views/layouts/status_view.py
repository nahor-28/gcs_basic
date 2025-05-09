from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCursor

from views.base_view import BaseView

class StatusView(BaseView):
    """Status view component for displaying system status messages."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
        self.max_messages = 100  # Maximum number of messages to keep
        
    def setup_ui(self):
        """Setup the status UI components."""
        layout = QVBoxLayout(self)
        
        # Create title label
        title = QLabel("Status Messages")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Create text edit for messages
        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)
        self.message_area.setMaximumHeight(150)
        self.message_area.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)
        
        # Add message area to layout
        layout.addWidget(self.message_area)
        
    def connect_signals(self):
        """Connect signals to slots."""
        # No direct signal connections needed as updates come through update_view
        pass
        
    def update_view(self, data):
        """Update the status display with new data."""
        if isinstance(data, dict):
            if data.get("type") == "STATUSTEXT":
                text = data.get("text", "")
                severity = data.get("severity", 0)
                self.add_message(text, severity)
            elif data.get("type") == "messages":
                # Clear existing messages
                self.message_area.clear()
                # Add all messages
                for message in data.get("data", []):
                    self.add_message(message.get("text", ""), message.get("severity", 0))
            
    def add_message(self, text, severity):
        """Add a new status message with appropriate formatting."""
        # Create color based on severity
        color = self._get_severity_color(severity)
        
        # Format the message
        formatted_text = f'<span style="color: {color};">{text}</span><br>'
        
        # Add message to text area
        self.message_area.append(formatted_text)
        
        # Limit the number of messages
        if self.message_area.document().blockCount() > self.max_messages:
            cursor = self.message_area.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            
        # Scroll to bottom
        self.message_area.verticalScrollBar().setValue(
            self.message_area.verticalScrollBar().maximum()
        )
        
    def _get_severity_color(self, severity):
        """Get color based on message severity."""
        # MAVLink severity levels
        if severity <= 1:  # EMERGENCY, ALERT, CRITICAL
            return "#FF0000"  # Red
        elif severity <= 3:  # ERROR, WARNING
            return "#FFA500"  # Orange
        elif severity <= 5:  # NOTICE, INFO
            return "#0000FF"  # Blue
        else:  # DEBUG
            return "#808080"  # Gray 