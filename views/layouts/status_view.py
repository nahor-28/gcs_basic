from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from views.base_view import BaseView

class StatusView(BaseView):
    """Status view component for displaying system status messages."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the status UI components."""
        # Create layout
        main_layout = QVBoxLayout()
        
        # Create group box
        group = QGroupBox("System Status")
        group_layout = QVBoxLayout()
        
        # Create text display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        group_layout.addWidget(self.status_text)
        
        # Set group layout
        group.setLayout(group_layout)
        
        # Add group to main layout
        main_layout.addWidget(group)
        
        # Set main layout
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect signals to slots."""
        if self.signal_manager:
            self.signal_manager.status_text_received.connect(self.add_status_message)
    
    def add_status_message(self, text, severity=0):
        """
        Add a new status message to the display.
        
        Args:
            text: Message text
            severity: Message severity (0=info, 1=warning, 2=error)
        """
        # Determine message color based on severity
        color = "black"
        if severity == 1:
            color = "orange"
        elif severity == 2:
            color = "red"
        
        # Format and add message
        message = f'<font color="{color}">[{severity}] {text}</font><br>'
        self.status_text.insertHtml(message)
        
        # Scroll to bottom
        scrollbar = self.status_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def update_view(self, data):
        """
        Update the view with status data.
        
        Args:
            data: List of status messages
        """
        if not isinstance(data, list):
            return
            
        # Clear existing messages
        self.status_text.clear()
        
        # Add messages in reverse order (newest at the bottom)
        for message in reversed(data):
            severity = message.get('severity', 0)
            text = message.get('text', '')
            timestamp = message.get('timestamp', '')
            
            # Format and add message
            self.add_status_message(f"[{timestamp}] {text}", severity)
