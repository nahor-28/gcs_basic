from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel, QScrollArea,
    QWidget, QSizePolicy
)
from PySide6.QtCore import Qt

class StatusLayout(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Status Messages", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Creates and arranges the status message display."""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Create scroll area for messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create widget to hold messages
        self.message_widget = QWidget()
        self.message_layout = QVBoxLayout(self.message_widget)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_layout.setSpacing(2)
        
        scroll.setWidget(self.message_widget)
        layout.addWidget(scroll)
        
        # Set fixed height and style
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 3px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        self.setLayout(layout)
        
    def add_message(self, text, severity):
        """Add a new status message."""
        severity_map = {
            0: ("EMERGENCY", "color: #dc3545;"),  # Red
            1: ("ALERT", "color: #dc3545;"),      # Red
            2: ("CRITICAL", "color: #dc3545;"),   # Red
            3: ("ERROR", "color: #dc3545;"),      # Red
            4: ("WARNING", "color: #ffc107;"),    # Yellow
            5: ("NOTICE", "color: #17a2b8;"),     # Cyan
            6: ("INFO", "color: #28a745;"),       # Green
            7: ("DEBUG", "color: #6c757d;")       # Gray
        }
        
        sev_str, color = severity_map.get(severity, (f"SEV {severity}", "color: #6c757d;"))
        
        # Create message label
        message = QLabel(f"[{sev_str}] {text}")
        message.setStyleSheet(color)
        message.setWordWrap(True)
        
        # Add to layout
        self.message_layout.addWidget(message)
        
        # Limit number of messages to prevent memory issues
        while self.message_layout.count() > 50:
            item = self.message_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater() 