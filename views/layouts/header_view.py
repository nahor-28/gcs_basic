from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from views.base_view import BaseView

class HeaderView(BaseView):
    """Header view component for the GCS application."""
    
    # View signals
    connect_requested = Signal(str, int)  # connection_string, baud_rate
    disconnect_requested = Signal()
    arm_requested = Signal()
    disarm_requested = Signal()
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
        
    def setup_ui(self):
        """Setup the header UI components."""
        layout = QHBoxLayout(self)
        
        # Connection controls
        self.connection_input = QComboBox()
        self.connection_input.setEditable(True)
        self.connection_input.addItems([
            'udp:localhost:14550',  # SITL UDP
            '/dev/tty.usbmodem101'  # Mac serial
        ])
        
        self.baud_rate_combo = QComboBox()
        self.baud_rate_combo.addItems(['115200', '57600', '38400'])
        self.baud_rate_combo.setCurrentText('115200')
        
        self.connect_button = QPushButton("Connect")
        
        # Status indicators
        self.mode_label = QLabel("Mode: ---")
        self.gps_label = QLabel("GPS: No Fix")
        self.battery_label = QLabel("Battery: ---")
        self.connection_status = QLabel("Status: Disconnected")
        
        # Arm button
        self.arm_button = QPushButton("Arm")
        self.arm_button.setEnabled(False)
        
        # Add widgets to layout
        layout.addWidget(QLabel("Connection:"))
        layout.addWidget(self.connection_input)
        layout.addWidget(QLabel("Baud:"))
        layout.addWidget(self.baud_rate_combo)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.gps_label)
        layout.addWidget(self.battery_label)
        layout.addWidget(self.connection_status)
        layout.addStretch()
        layout.addWidget(self.arm_button)
        
    def connect_signals(self):
        """Connect signals to slots."""
        self.connect_button.clicked.connect(self.on_connect_clicked)
        self.arm_button.clicked.connect(self.on_arm_clicked)
        
    def update_view(self, data):
        """Update the header view with new data."""
        data_type = data.get('type')
        
        if data_type == 'status':
            status = data['data']['status']
            message = data['data']['message']
            self.update_connection_status(status, message)
            
        elif data_type == 'connection':
            connected = data['data']['connected']
            message = data['data']['message']
            if connected:
                self.connection_status.setText(f"Status: Connected - {message}")
                self.connect_button.setText("Disconnect")
                self.arm_button.setEnabled(True)
            else:
                self.connection_status.setText(f"Status: Disconnected - {message}")
                self.connect_button.setText("Connect")
                self.arm_button.setEnabled(False)
                
    def update_mode(self, mode):
        """Update the flight mode display."""
        self.mode_label.setText(f"Mode: {mode}")
        
    def update_gps_status(self, fix_type, satellites):
        """Update the GPS status display."""
        fix_types = {
            0: "No Fix",
            1: "No GPS",
            2: "2D Fix",
            3: "3D Fix",
            4: "DGPS",
            5: "RTK Float",
            6: "RTK Fixed"
        }
        fix_str = fix_types.get(fix_type, "Unknown")
        self.gps_label.setText(f"GPS: {fix_str} ({satellites} sats)")
        
    def update_battery(self, voltage, remaining):
        """Update the battery status display."""
        self.battery_label.setText(f"Battery: {voltage:.1f}V ({remaining}%)")
        
    def update_connection_status(self, status, message=""):
        """Update the connection status display."""
        self.connection_status.setText(f"Status: {status}")
        if status == "CONNECTED":
            self.connect_button.setText("Disconnect")
            self.arm_button.setEnabled(True)
        else:
            self.connect_button.setText("Connect")
            self.arm_button.setEnabled(False)
            
    def on_connect_clicked(self):
        """Handle connect button click."""
        if self.connect_button.text() == "Connect":
            conn_str = self.connection_input.currentText()
            baud_str = self.baud_rate_combo.currentText()
            
            if not conn_str:
                QMessageBox.critical(self, "Connection Error", "Please select a valid connection string.")
                return
                
            try:
                baud = int(baud_str)
            except ValueError:
                QMessageBox.critical(self, "Connection Error", "Please select a valid baud rate.")
                return
                
            # Emit connection request signal
            self.connect_requested.emit(conn_str, baud)
        else:
            # Emit disconnect request signal
            self.disconnect_requested.emit()
            
    def on_arm_clicked(self):
        """Handle arm button click."""
        if self.arm_button.text() == "Arm":
            self.arm_requested.emit()
            self.arm_button.setText("Disarm")
        else:
            self.disarm_requested.emit()
            self.arm_button.setText("Arm") 