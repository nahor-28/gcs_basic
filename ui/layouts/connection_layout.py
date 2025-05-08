from PySide6.QtWidgets import (
    QGroupBox, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
import serial.tools.list_ports

class ConnectionLayout(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Connection", parent)
        self.setup_ui()
        
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
            
    def set_connected(self, connected: bool):
        """Update the connect button state based on connection status."""
        if connected:
            self.connect_button.setText("Disconnect")
            self.connection_input.setEnabled(False)
            self.baud_rate_combo.setEnabled(False)
        else:
            self.connect_button.setText("Connect")
            self.connection_input.setEnabled(True)
            self.baud_rate_combo.setEnabled(True) 