from PySide6.QtWidgets import (
    QGroupBox, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
import serial.tools.list_ports

class ConnectionView(QGroupBox):
    # Define signals
    connect_clicked = Signal(str, str)  # connection_string, baud_rate
    disconnect_clicked = Signal()
    status_changed = Signal(str, str)  # status, message
    
    def __init__(self, signal_manager=None, parent=None):
        super().__init__("", parent)
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Creates and arranges the connection controls."""
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Reduce spacing
        layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Connection input
        self.connection_input = QComboBox()
        self.connection_input.setEditable(True)
        self.connection_input.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.connection_input.setFixedWidth(150)
        self.connection_input.setFixedHeight(30)
        self.populate_ports()
        layout.addWidget(self.connection_input)
        
        # Baud rate
        self.baud_rate_combo = QComboBox()
        self.baud_rate_combo.addItems(["57600", "115200", "921600"])
        self.baud_rate_combo.setFixedWidth(80)
        self.baud_rate_combo.setFixedHeight(30)
        layout.addWidget(self.baud_rate_combo)
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFixedHeight(30)
        layout.addWidget(self.connect_button)
        
        self.setLayout(layout)
        self.setFixedHeight(50)  # Fixed height for the entire layout
        
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect button click handler
        self.connect_button.clicked.connect(self._handle_connect_click)
        
        # Connect to signal manager if available
        if self.signal_manager:
            self.signal_manager.connection_status_changed.connect(self._handle_connection_status)
        
    def populate_ports(self):
        """Populates the connection combo box with available serial ports."""
        try:
            # Get list of serial ports
            ports = [p.device for p in serial.tools.list_ports.comports()]
            
            # Add common UDP addresses
            udp_ports = [
                'udpin:localhost:14550',
                'udpin:0.0.0.0:14550',
                'udpout:localhost:14550',
                'udpout:0.0.0.0:14550'
            ]
            
            # Clear and add all ports
            self.connection_input.clear()
            self.connection_input.addItems(ports + udp_ports)
            
            # Set default to first UDP port
            self.connection_input.setCurrentText('udpin:localhost:14550')
            
        except Exception as e:
            print(f"Warning: Could not list serial ports - {e}")
            # Add fallback options
            self.connection_input.addItems([
                'udpin:localhost:14550',
                '/dev/ttyACM0',
                'COM3'
            ])
            
    def _handle_connection_status(self, status, message):
        """Handle connection status changes from signal manager."""
        print(f"ConnectionView received status: {status}, message: {message}")
        is_connected = status == 'CONNECTED'
        self.set_connected(is_connected)
        # Emit status change to parent
        self.status_changed.emit(status, message)
            
    def set_connected(self, connected: bool):
        """Update the connect button state based on connection status."""
        print(f"Setting connected state: {connected}")
        if connected:
            self.connect_button.setText("Disconnect")
            self.connection_input.setEnabled(False)
            self.baud_rate_combo.setEnabled(False)
        else:
            self.connect_button.setText("Connect")
            self.connection_input.setEnabled(True)
            self.baud_rate_combo.setEnabled(True)
            
    def _handle_connect_click(self):
        """Handle connect button click."""
        print(f"Connect button clicked, current text: {self.connect_button.text()}")
        if self.connect_button.text() == "Connect":
            self.connect_clicked.emit(
                self.connection_input.currentText(),
                self.baud_rate_combo.currentText()
            )
        else:
            self.disconnect_clicked.emit() 