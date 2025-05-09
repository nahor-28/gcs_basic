from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt, Slot

from views.base_view import BaseView
from views.layouts.header_view import HeaderView
from views.layouts.telemetry_view import TelemetryView
from views.layouts.map_view import MapView
from views.layouts.status_view import StatusView
from core.signal_manager import SignalManager

class MainView(QMainWindow):
    """Main view for the GCS application using MVC architecture."""
    
    def __init__(self, signal_manager: SignalManager):
        super().__init__()
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Creates and arranges the UI elements."""
        self.setWindowTitle("ArduPilot GCS - MVC Architecture")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add header
        self.header_view = HeaderView(self.signal_manager)
        main_layout.addWidget(self.header_view)
        
        # Create content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for controls and telemetry
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Add telemetry view
        self.telemetry_view = TelemetryView(self.signal_manager)
        left_layout.addWidget(self.telemetry_view)
        
        # Add status view at the bottom of left panel
        self.status_view = StatusView(self.signal_manager)
        left_layout.addWidget(self.status_view)
        
        # Add left panel to splitter
        splitter.addWidget(left_panel)
        
        # Right panel for map
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.map_view = MapView(self.signal_manager)
        right_layout.addWidget(self.map_view)
        
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
        # Connect signal manager signals to slots
        self.signal_manager.telemetry_update.connect(self.update_telemetry)
        self.signal_manager.connection_status_changed.connect(self.update_connection_status)
        self.signal_manager.status_text_received.connect(self.update_status_message)
        
    def update_telemetry(self, data):
        """Update telemetry display with new data."""
        # Update telemetry view
        self.telemetry_view.update_view(data)
        
        # Update header with relevant information
        if data.get("type") == "HEARTBEAT":
            self.header_view.update_mode(data.get("mode", "---"))
            
        elif data.get("type") == "GPS_RAW_INT":
            self.header_view.update_gps_status(
                data.get("gps_fix_type", 0),
                data.get("gps_satellites", 0)
            )
            
        elif data.get("type") == "SYS_STATUS":
            self.header_view.update_battery(
                data.get("battery_voltage", 0),
                data.get("battery_remaining", 0)
            )
            
        # Update map if position data is available
        if data.get("type") == "GLOBAL_POSITION_INT":
            lat = data.get('lat')
            lon = data.get('lon')
            self.map_view.update_position(lat, lon)
            
    def update_connection_status(self, status, message=""):
        """Update connection status display."""
        self.header_view.update_connection_status(status, message)
            
    def update_status_message(self, text, severity):
        """Update status message display."""
        self.status_view.add_message(text, severity) 