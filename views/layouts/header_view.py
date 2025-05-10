from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from core.signal_manager import SignalManager
from views.base_view import BaseView
from views.layouts.connection_view import ConnectionView

class HeaderView(BaseView):
    """Header view component for the application."""
    
    def __init__(self, signal_manager: SignalManager):
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the header UI components."""
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Add logo or title
        title_label = QLabel("GCS - MVC Architecture")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)
        
        # Add connection view
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
        # print(f"HeaderView received data: {data}")
        
        if isinstance(data, dict):
            # Update status label
            status = data.get('status', 'Not Connected')
            message = data.get('message', '')
            self.update_connection_status(status, message)
            
    def update_connection_status(self, status, message=""):
        """Update the connection status display."""
        # print(f"HeaderView updating status: {status}, message: {message}")  # Debug print
        status_text = f"Status: {status}"
        if message:
            status_text += f" - {message}"
        self.status_label.setText(status_text)
            
    def on_connect_clicked(self, connection_string, baud_rate):
        """Handle connect button click."""
        if self.signal_manager:
            # Forward the connection request to the signal manager
            self.signal_manager.connection_request.emit(connection_string, baud_rate)
    
    def on_disconnect_clicked(self):
        """Handle disconnect button click."""
        if self.signal_manager:
            # Forward the disconnect request to the signal manager
            self.signal_manager.disconnect_request.emit()
