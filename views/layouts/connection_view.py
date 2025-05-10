from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal
from views.base_view import BaseView

class ConnectionView(BaseView):
    """Connection view component for managing vehicle connections."""
    
    # Define signals
    connect_clicked = Signal(str, int)  # connection_string, baud_rate
    disconnect_clicked = Signal()
    status_changed = Signal(str, str)  # status, message
    
    def __init__(self, signal_manager=None, parent=None):
        self.parent = parent
        self.signal_manager = signal_manager
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the connection UI components."""
        # Create layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)  # Reduce spacing
        
        # Connection string input - make it fixed width
        self.conn_string_input = QLineEdit("udp:localhost:14550")
        self.conn_string_input.setPlaceholderText("Connection String")
        self.conn_string_input.setFixedWidth(180)  # Set fixed width
        
        # Baud rate selection (for serial connections) - make it compact
        self.baud_combo = QComboBox()
        for baud in ["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]:
            self.baud_combo.addItem(baud)
        self.baud_combo.setCurrentText("115200")
        self.baud_combo.setFixedWidth(80)  # Set fixed width
        
        # Create form layout for inputs
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  # Reduce margins
        form_layout.setSpacing(2)  # Reduce spacing
        form_layout.addRow("Connection:", self.conn_string_input)
        form_layout.addRow("Baud Rate:", self.baud_combo)
        
        # Create buttons - make them smaller and fixed size
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFixedWidth(70)  # Set fixed width
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setFixedWidth(70)  # Set fixed width
        self.disconnect_button.setEnabled(False)  # Initially disabled
        
        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout.setSpacing(5)  # Reduce spacing
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        
        # Create wrapper layout
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        wrapper_layout.setSpacing(2)  # Reduce spacing
        wrapper_layout.addLayout(form_layout)
        wrapper_layout.addLayout(button_layout)
        
        # Add to main layout
        main_layout.addLayout(wrapper_layout)
        
        # Set main layout
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect button signals
        self.connect_button.clicked.connect(self._on_connect_clicked)
        self.disconnect_button.clicked.connect(self._on_disconnect_clicked)
        
        # Connect signal manager signals
        if self.signal_manager:
            self.signal_manager.connection_status_changed.connect(self._handle_connection_status)
    
    def _on_connect_clicked(self):
        """Handle connect button click."""
        conn_string = self.conn_string_input.text()
        baud_rate = int(self.baud_combo.currentText())
        
        # Emit signal
        self.connect_clicked.emit(conn_string, baud_rate)
    
    def _on_disconnect_clicked(self):
        """Handle disconnect button click."""
        # Emit signal
        self.disconnect_clicked.emit()
    
    def _handle_connection_status(self, status, message):
        """
        Handle connection status changes.
        
        Args:
            status: Connection status string
            message: Status message
        """
        # Update button states based on connection status
        if status == "CONNECTED":
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.conn_string_input.setEnabled(False)
            self.baud_combo.setEnabled(False)
        else:
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.conn_string_input.setEnabled(True)
            self.baud_combo.setEnabled(True)
        
        # Emit status changed signal
        self.status_changed.emit(status, message)
    
    def update_view(self, data):
        """
        Update the view with connection data.
        
        Args:
            data: Connection data dictionary
        """
        if not isinstance(data, dict):
            return
            
        # Update connection string and baud rate
        if 'connection_string' in data:
            self.conn_string_input.setText(data['connection_string'])
        
        if 'baud_rate' in data:
            self.baud_combo.setCurrentText(str(data['baud_rate']))
        
        # Update connection status
        if 'status' in data and 'message' in data:
            self._handle_connection_status(data['status'], data['message'])
