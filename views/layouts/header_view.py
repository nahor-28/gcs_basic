from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
import logging
from core.signal_manager import SignalManager
from views.base_view import BaseView
from views.layouts.connection_view import ConnectionView

# Configure logging
logger = logging.getLogger(__name__)

class HeaderView(BaseView):
    """Header view component for the application."""
    
    def __init__(self, signal_manager: SignalManager):
        super().__init__(signal_manager)
        logger.debug("HeaderView initialized")
    
    def setup_ui(self):
        """Setup the header UI components."""
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Add logo or title
        # title_label = QLabel("GCS - Observer MVC")
        # title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        # layout.addWidget(title_label)
        
        # Add connection view
        self.connection_view = ConnectionView(signal_manager=self.signal_manager)
        layout.addWidget(self.connection_view)
        
        # Status label
        self.status_label = QLabel("Status: DISCONNECTED")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.setFixedHeight(50)
        logger.debug("HeaderView UI setup complete")
        
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect view signals
        self.connection_view.connect_clicked.connect(self.on_connect_clicked)
        self.connection_view.disconnect_clicked.connect(self.on_disconnect_clicked)
        
        # HeaderView itself listens to connection_model_changed to update its status_label
        if self.signal_manager:
            logger.debug("HeaderView: Connecting to connection_model_changed signal")
            self.signal_manager.connection_model_changed.connect(self._update_status_label_from_model)
        else:
            logger.error("HeaderView: No signal_manager available for signal connections")
        
    def _update_status_label_from_model(self, model_data: dict):
        """Update the connection status display based on model data."""
        logger.debug(f"HeaderView: Received connection_model_changed with data: {model_data}")
        
        status = model_data.get('status', 'UNKNOWN')
        message = model_data.get('message', '')
        conn_str = model_data.get('connection_string', '-')

        if status == "CONNECTED":
            status_text = f"Status: CONNECTED to {conn_str}"
        elif status == "CONNECTING":
            status_text = f"Status: CONNECTING to {conn_str}..."
            if message: # Add specific message if available (e.g. "Waiting for heartbeat")
                status_text = f"Status: CONNECTING - {message}"
        elif status == "RECONNECTING":
            status_text = f"Status: RECONNECTING to {conn_str}..."
            if message: 
                status_text = f"Status: RECONNECTING - {message}"
        elif status == "DISCONNECTED":
            status_text = "Status: DISCONNECTED"
            if message and message != "Disconnected": # Show specific disconnect message if not generic
                 status_text = f"Status: DISCONNECTED - {message}"
        elif status == "ERROR":
            status_text = f"Status: ERROR"
            if message:
                status_text += f" - {message}"
        else: # Catch any other statuses
            status_text = f"Status: {status}"
            if message:
                status_text += f" - {message}"

        logger.debug(f"HeaderView: Setting status label to: {status_text}")
        self.status_label.setText(status_text)
            
    def on_connect_clicked(self, connection_string, baud_rate):
        """Handle connect button click."""
        if self.signal_manager:
            logger.debug(f"HeaderView: Emitting connection_request with {connection_string}, {baud_rate}")
            # Forward the connection request to the signal manager
            self.signal_manager.connection_request.emit(connection_string, baud_rate)
    
    def on_disconnect_clicked(self):
        """Handle disconnect button click."""
        if self.signal_manager:
            logger.debug("HeaderView: Emitting disconnect_request")
            # Forward the disconnect request to the signal manager
            self.signal_manager.disconnect_request.emit()
