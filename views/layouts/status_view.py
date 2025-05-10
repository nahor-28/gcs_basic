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
            # Listen to the new model signal that carries a new message dictionary
            self.signal_manager.status_model_new_message.connect(self._add_new_status_message)
    
    def _add_new_status_message(self, message_data: dict):
        """
        Add a new status message (received as a dict) to the display.
        
        Args:
            message_data: Dictionary containing message details (text, severity, timestamp).
        """
        text = message_data.get('text', '')
        severity = message_data.get('severity', 0)
        timestamp = message_data.get('timestamp', '') # Or format it if needed

        color = "black"
        if severity == 1: color = "orange"
        elif severity == 2: color = "red"
        
        # Format and add message including timestamp if available
        prefix = f"[{timestamp}] " if timestamp else ""
        formatted_message = f'<font color="{color}">{prefix}[{severity}] {text}</font><br>'
        
        self.status_text.insertHtml(formatted_message)
        self.status_text.verticalScrollBar().setValue(self.status_text.verticalScrollBar().maximum())
