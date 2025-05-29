from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
import json
import time
from views.base_view import BaseView

class MapView(BaseView):
    """Interactive map view component for displaying vehicle location."""
    
    def __init__(self, signal_manager):
        # Initialize instance variables BEFORE calling super().__init__()
        self.current_position = None
        self.flight_path = []
        self.map_center = [22.719568, 75.857727]  # Default: Indore
        self.current_zoom = 15
        self.map_initialized = False
        self.last_update_time = 0
        self.update_threshold = 5.0  # Update map visual every 3 seconds
        self.first_gps_fix = True
        
        # Now call parent constructor
        super().__init__(signal_manager)

    def setup_ui(self):
        """Setup the interactive map UI components."""
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create group box
        group = QGroupBox("Vehicle Map")
        group_layout = QVBoxLayout()
        
        # Create web engine view for map
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(400)
        
        # Initialize the map once
        self._initialize_map()
        
        group_layout.addWidget(self.web_view)
        
        # Enhanced status display
        self.status_label = QLabel("Waiting for GPS fix...")
        self.status_label.setStyleSheet("""
            color: #333; 
            font-weight: bold; 
            padding: 8px; 
            background-color: #f0f0f0; 
            border: 1px solid #ccc; 
            border-radius: 4px;
        """)
        group_layout.addWidget(self.status_label)
        
        # Set group layout
        group.setLayout(group_layout)
        
        # Add group to main layout
        main_layout.addWidget(group)
        
        # Set main layout
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect signals to slots."""
        if self.signal_manager:
            self.signal_manager.telemetry_update.connect(self.update_map)
    
    def _initialize_map(self):
        """Initialize the folium map once."""
        # Create folium map
        self.folium_map = folium.Map(
            location=self.map_center,
            zoom_start=self.current_zoom,
            tiles='OpenStreetMap'
        )
        
        # Add initial placeholder marker
        folium.Marker(
            self.map_center,
            popup="Waiting for vehicle position...",
            tooltip="GPS fix pending",
            icon=folium.Icon(color='gray', icon='question-sign')
        ).add_to(self.folium_map)
        
        # Load initial map
        html_string = self.folium_map._repr_html_()
        self.web_view.setHtml(html_string)
        self.map_initialized = True
    
    def _update_map_display(self):
        """Update the map display with current position and flight path."""
        if not self.current_position:
            return
        
        lat, lon = self.current_position
        
        # Create new map centered on current position
        self.folium_map = folium.Map(
            location=[lat, lon],
            zoom_start=16,  # Good detail level for vehicle tracking
            tiles='OpenStreetMap'
        )
        
        # Add flight path if available
        if len(self.flight_path) > 1:
            folium.PolyLine(
                self.flight_path,
                color='blue',
                weight=3,
                opacity=0.7,
                popup='Flight Path'
            ).add_to(self.folium_map)
        
        # Add current vehicle marker
        folium.Marker(
            [lat, lon],
            popup=f"Vehicle Position\nLat: {lat:.6f}\nLon: {lon:.6f}",
            tooltip="Current Vehicle Position",
            icon=folium.Icon(color='red', icon='glyphicon-plane', prefix='glyphicon')
        ).add_to(self.folium_map)
        
        # Add accuracy circle
        folium.Circle(
            [lat, lon],
            radius=15,  # 15 meters
            color='red',
            fillColor='red',
            fillOpacity=0.1,
            weight=1,
            popup='GPS Accuracy'
        ).add_to(self.folium_map)
        
        # Generate and load HTML
        html_string = self.folium_map._repr_html_()
        self.web_view.setHtml(html_string)
        
        print(f"Map visual updated: {lat:.6f}, {lon:.6f}")
    
    def update_map(self, data):
        """
        Update the map with new vehicle position.
        
        Args:
            data: Telemetry data dictionary
        """
        if not isinstance(data, dict) or not self.map_initialized:
            return
        
        # Extract position data
        lat, lon = self._extract_position(data)
        if lat is None or lon is None:
            return
        
        # Update current position
        self.current_position = (lat, lon)
        
        # Always update status text immediately (real-time feedback)
        self.status_label.setText(f"GPS: {lat:.6f}, {lon:.6f} | Flight Path: {len(self.flight_path)} points")
        
        # Add to flight path
        self.flight_path.append((lat, lon))
        if len(self.flight_path) > 50:  # Keep more points for better path visualization
            self.flight_path.pop(0)
        
        # Smart map visual updates
        current_time = time.time()
        should_update = False
        
        # Always update on first GPS fix
        if self.first_gps_fix:
            should_update = True
            self.first_gps_fix = False
            print(f"First GPS fix - immediate map update: {lat:.6f}, {lon:.6f}")
        
        # Then update every 3 seconds
        elif current_time - self.last_update_time >= self.update_threshold:
            should_update = True
            print(f"Scheduled map update: {lat:.6f}, {lon:.6f}")
        
        # Update map visual if needed
        if should_update:
            self._update_map_display()
            self.last_update_time = current_time
        else:
            # Show that we received the coordinates but didn't update visual
            next_update = self.update_threshold - (current_time - self.last_update_time)
            print(f"GPS update received: {lat:.6f}, {lon:.6f} (next map update in {next_update:.1f}s)")
    
    def _extract_position(self, data):
        """Extract lat/lon from telemetry data."""
        # Handle TelemetryManager data format (raw format)
        msg_type = data.get('type', '')
        if msg_type == 'GLOBAL_POSITION_INT' and 'lat' in data and 'lon' in data:
            lat = data.get('lat', 0)  # Already in decimal degrees
            lon = data.get('lon', 0)  # Already in decimal degrees
            return lat, lon
        
        # Handle structured format (for test scripts)
        if 'position' in data:
            position = data.get('position', {})
            lat = position.get('lat', 0)
            lon = position.get('lon', 0)
            return lat, lon
        
        return None, None
    
    def update_view(self, data):
        """
        Update the view with new data.
        
        Args:
            data: Telemetry data dictionary
        """
        self.update_map(data)
