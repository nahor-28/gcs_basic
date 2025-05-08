from PySide6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QComboBox,
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
        layout = QGridLayout()
        layout.setSpacing(5)  # Reduce spacing
        layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Connection input
        layout.addWidget(QLabel("Connection:"), 0, 0)
        self.connection_input = QComboBox()
        self.connection_input.setEditable(True)
        self.connection_input.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.connection_input.setMaximumWidth(200)  # Limit width
        self.populate_ports()
        layout.addWidget(self.connection_input, 0, 1)
        
        # Baud rate
        layout.addWidget(QLabel("Baud Rate:"), 1, 0)
        self.baud_rate_combo = QComboBox()
        self.baud_rate_combo.addItems(["57600", "115200", "921600"])
        self.baud_rate_combo.setMaximumWidth(200)  # Limit width
        layout.addWidget(self.baud_rate_combo, 1, 1)
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setMaximumWidth(200)  # Limit width
        layout.addWidget(self.connect_button, 2, 0, 1, 2)
        
        self.setLayout(layout)
        self.setMaximumHeight(120)  # Limit height
        
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