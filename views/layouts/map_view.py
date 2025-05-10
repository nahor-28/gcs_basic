from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox
)
from PySide6.QtCore import Qt
from views.base_view import BaseView

class MapView(BaseView):
    """Map view component for displaying vehicle location."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the map UI components."""
        # Create layout
        main_layout = QVBoxLayout()
        
        # Create group box
        group = QGroupBox("Map")
        group_layout = QVBoxLayout()
        
        # For now, just a placeholder for the map
        # In a real application, this would be a map widget
        self.map_placeholder = QLabel("Map Display (Placeholder)")
        self.map_placeholder.setAlignment(Qt.AlignCenter)
        self.map_placeholder.setStyleSheet("background-color: #f0f0f0; min-height: 300px;")
        group_layout.addWidget(self.map_placeholder)
        
        # Set group layout
        group.setLayout(group_layout)
        
        # Add group to main layout
        main_layout.addWidget(group)
        
        # Set main layout
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect signals to slots."""
        if self.signal_manager:
            # Connect to signal but don't create a cycle
            # We don't react to our own signals
            self.signal_manager.telemetry_update.connect(self.update_map)
    
    def update_map(self, data):
        """
        Update the map with new vehicle position.
        
        Args:
            data: Telemetry data dictionary
        """
        if not isinstance(data, dict):
            return
            
        # Check data format - handle both raw and structured formats
        
        # Handle TelemetryManager data format (raw format)
        msg_type = data.get('type', '')
        if msg_type == 'GLOBAL_POSITION_INT' and 'lat' in data and 'lon' in data:
            lat = data.get('lat', 0)  # Already in decimal degrees
            lon = data.get('lon', 0)  # Already in decimal degrees
            
            # Update map placeholder with position info
            self.map_placeholder.setText(f"Map Display\nLat: {lat:.6f}, Lon: {lon:.6f}")
            return
        
        # Handle structured format (for test scripts)
        if 'position' in data:
            position = data.get('position', {})
            lat = position.get('lat', 0)
            lon = position.get('lon', 0)
            
            # Update map placeholder with position info
            # In a real application, this would update a map widget
            self.map_placeholder.setText(f"Map Display\nLat: {lat:.6f}, Lon: {lon:.6f}")
    
    def update_view(self, data):
        """
        Update the view with new data.
        
        Args:
            data: Telemetry data dictionary
        """
        self.update_map(data)
