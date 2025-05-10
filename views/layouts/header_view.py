from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from core.signal_manager import SignalManager
from views.base_view import BaseView
from .connection_view import ConnectionView

class HeaderView(BaseView):
    """Header view component for the GCS application."""
    
    # View signals
    connect_requested = Signal(str, int)  # connection_string, baud_rate
    disconnect_requested = Signal()
    
    def __init__(self, signal_manager: SignalManager):
        super().__init__(signal_manager)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Creates and arranges the header layout."""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Connection controls
        self.connection_view = ConnectionView(signal_manager=self.signal_manager)
        layout.addWidget(self.connection_view)
        
        # Status label
        self.status_label = QLabel("Not Connected")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.setFixedHeight(50)
        
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect view signals
        self.connection_view.connect_clicked.connect(self.on_connect_clicked)
        self.connection_view.disconnect_clicked.connect(self.on_disconnect_clicked)
        self.connection_view.status_changed.connect(self.update_connection_status)
        
    def update_view(self, data):
        """Update the view based on the provided data."""
        print(f"HeaderView received data: {data}")
        
        if isinstance(data, dict):
            # Update status label
            status = data.get('status', 'Not Connected')
            message = data.get('message', '')
            self.update_connection_status(status, message)
            
    def update_connection_status(self, status, message=""):
        """Update the connection status display."""
        print(f"HeaderView updating status: {status}, message: {message}")  # Debug print
        status_text = f"Status: {status}"
        if message:
            status_text += f" - {message}"
        self.status_label.setText(status_text)
            
    def on_connect_clicked(self, connection_string, baud_rate):
        """Handle connect button click."""
        try:
            baud = int(baud_rate)
            self.connect_requested.emit(connection_string, baud)
        except ValueError:
            QMessageBox.critical(self, "Connection Error", "Please select a valid baud rate.")
            
    def on_disconnect_clicked(self):
        """Handle disconnect button click."""
        self.disconnect_requested.emit() 