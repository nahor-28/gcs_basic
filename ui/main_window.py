from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt, Slot

from ui.layouts.header_layout import HeaderLayout
from ui.layouts.telemetry_layout import TelemetryLayout
from ui.layouts.map_layout import MapLayout
from ui.layouts.status_layout import StatusLayout
from core.signal_manager import SignalManager

class MainWindow(QMainWindow):
    def __init__(self, signal_manager: SignalManager):
        super().__init__()
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Creates and arranges the UI elements."""
        self.setWindowTitle("ArduPilot GCS - Basic Telemetry")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        # main_layout.setSpacing(0)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add header
        self.header_layout = HeaderLayout()
        main_layout.addWidget(self.header_layout)
        
        # Create content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        # content_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for controls and telemetry
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Add telemetry layout
        self.telemetry_layout = TelemetryLayout()
        left_layout.addWidget(self.telemetry_layout)
        
        # Add status layout at the bottom of left panel
        self.status_layout = StatusLayout()
        left_layout.addWidget(self.status_layout)
        
        # Add left panel to splitter
        splitter.addWidget(left_panel)
        
        # Right panel for map
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.map_layout = MapLayout()
        right_layout.addWidget(self.map_layout)
        
        # Add right panel to splitter
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (40% left, 60% right)
        splitter.setSizes([400, 600])
        
        # Add splitter to content layout
        content_layout.addWidget(splitter)
        
        # Add content area to main layout
        main_layout.addWidget(content_widget)
        
    def connect_signals(self):
        """Connects UI signals to slots."""
        # Connect button signals
        self.header_layout.connection_layout.connect_button.clicked.connect(self.on_connect_clicked)
        self.header_layout.arm_button.clicked.connect(self.on_arm_clicked)
        
        # Connect signal manager signals to slots
        self.signal_manager.telemetry_update.connect(self.update_telemetry)
        self.signal_manager.connection_status_changed.connect(self.update_connection_status)
        self.signal_manager.status_text_received.connect(self.update_status_message)
        
    def update_telemetry(self, data):
        """Update telemetry display with new data."""
        # Update telemetry layout
        self.telemetry_layout.update_telemetry(data)
        
        # Update header with relevant information
        if data.get("type") == "HEARTBEAT":
            self.header_layout.update_mode(data.get("mode", "---"))
            
        elif data.get("type") == "GPS_RAW_INT":
            self.header_layout.update_gps_status(
                data.get("gps_fix_type", 0),
                data.get("gps_satellites", 0)
            )
            
        elif data.get("type") == "SYS_STATUS":
            self.header_layout.update_battery(
                data.get("battery_voltage", 0),
                data.get("battery_remaining", 0)
            )
            
        # Update map if position data is available
        if data.get("type") == "GLOBAL_POSITION_INT":
            lat = data.get('lat')
            lon = data.get('lon')
            self.map_layout.update_position(lat, lon)
            
    def update_connection_status(self, status, message=""):
        """Update connection status display."""
        self.header_layout.update_connection_status(status, message)
            
    def update_status_message(self, text, severity):
        """Update status message display."""
        self.status_layout.add_message(text, severity)
        
    def on_connect_clicked(self):
        """Handles connect button click."""
        if self.header_layout.connection_layout.connect_button.text() == "Connect":
            conn_str = self.header_layout.connection_layout.connection_input.currentText()
            baud_str = self.header_layout.connection_layout.baud_rate_combo.currentText()
            
            if not conn_str:
                QMessageBox.critical(self, "Connection Error", "Please select a valid connection string.")
                return
                
            try:
                baud = int(baud_str)
            except ValueError:
                QMessageBox.critical(self, "Connection Error", "Please select a valid baud rate.")
                return
                
            # Emit connection request signal
            self.signal_manager.connection_request.emit(conn_str, baud)
        else:
            # Emit disconnect request signal
            self.signal_manager.disconnect_request.emit()
            
    def on_arm_clicked(self):
        """Handles arm/disarm button click."""
        # TODO: Implement arm/disarm functionality
        pass