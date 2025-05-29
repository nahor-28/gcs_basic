from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
import tempfile
import os
from views.base_view import BaseView

class MapView(BaseView):
    """Interactive map view component for displaying vehicle location."""
    
    def __init__(self, signal_manager):
        # Initialize instance variables BEFORE calling super().__init__()
        self.current_position = None
        self.vehicle_marker = None
        self.flight_path = []
        self.map_center = [37.7749, -122.4194]  # Default: San Francisco
        self.current_zoom = 15
        self.map_style = 'OpenStreetMap'
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._update_map_display)
        self.pending_update = False
        
        # Now call parent constructor
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the interactive map UI components."""
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create group box
        group = QGroupBox("Interactive Map")
        group_layout = QVBoxLayout()
        
        # Create map controls
        controls_layout = QHBoxLayout()
        
        # Map style selector
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            'OpenStreetMap',
            'Stamen Terrain',
            'Stamen Toner',
            'CartoDB positron',
            'CartoDB dark_matter'
        ])
        self.style_combo.currentTextChanged.connect(self._on_style_changed)
        controls_layout.addWidget(QLabel("Map Style:"))
        controls_layout.addWidget(self.style_combo)
        
        # Center on vehicle button
        self.center_button = QPushButton("Center on Vehicle")
        self.center_button.clicked.connect(self._center_on_vehicle)
        self.center_button.setEnabled(False)
        controls_layout.addWidget(self.center_button)
        
        # Clear path button
        self.clear_path_button = QPushButton("Clear Path")
        self.clear_path_button.clicked.connect(self._clear_flight_path)
        controls_layout.addWidget(self.clear_path_button)
        
        controls_layout.addStretch()
        
        # Status label
        self.status_label = QLabel("Waiting for GPS fix...")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        controls_layout.addWidget(self.status_label)
        
        group_layout.addLayout(controls_layout)
        
        # Create web engine view for map
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(350)
        
        # Initialize the map
        self._initialize_map()
        
        group_layout.addWidget(self.web_view)
        
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
        """Initialize the folium map."""
        # Create folium map
        self.folium_map = folium.Map(
            location=self.map_center,
            zoom_start=self.current_zoom,
            tiles=self.map_style
        )
        
        # Add a marker for initial position (will be updated with real data)
        folium.Marker(
            self.map_center,
            popup="Waiting for vehicle position...",
            tooltip="Vehicle position unknown",
            icon=folium.Icon(color='gray', icon='question-sign')
        ).add_to(self.folium_map)
        
        # Convert to HTML and load
        self._load_map_html()
    
    def _load_map_html(self):
        """Load the folium map into the web view."""
        # Generate HTML
        html_string = self.folium_map._repr_html_()
        
        # Load HTML into web view
        self.web_view.setHtml(html_string)
    
    def update_map(self, data):
        """
        Update the map with new vehicle position.
        
        Args:
            data: Telemetry data dictionary
        """
        if not isinstance(data, dict):
            return
        
        # Extract position data
        lat, lon = self._extract_position(data)
        if lat is None or lon is None:
            return
        
        # Update current position
        self.current_position = (lat, lon)
        
        # Add to flight path (limit to last 100 points for performance)
        self.flight_path.append((lat, lon))
        if len(self.flight_path) > 100:
            self.flight_path.pop(0)
        
        # Update status
        self.status_label.setText(f"Position: {lat:.6f}, {lon:.6f}")
        self.center_button.setEnabled(True)
        
        # Throttle map updates to avoid excessive rendering
        if not self.pending_update:
            self.pending_update = True
            self.update_timer.start(500)  # Update every 500ms max
    
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
    
    def _update_map_display(self):
        """Update the actual map display (called by timer)."""
        self.pending_update = False
        
        if not self.current_position:
            return
        
        lat, lon = self.current_position
        
        # Create new map
        self.folium_map = folium.Map(
            location=[lat, lon],
            zoom_start=self.current_zoom,
            tiles=self.map_style
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
            icon=folium.Icon(color='red', icon='plane', prefix='fa')
        ).add_to(self.folium_map)
        
        # Add circle showing GPS accuracy (if available)
        folium.Circle(
            [lat, lon],
            radius=10,  # 10 meters default
            color='red',
            fillColor='red',
            fillOpacity=0.2,
            popup='GPS Position'
        ).add_to(self.folium_map)
        
        # Load updated map
        self._load_map_html()
    
    def _on_style_changed(self, style):
        """Handle map style change."""
        self.map_style = style
        if self.current_position:
            self._update_map_display()
        else:
            self._initialize_map()
    
    def _center_on_vehicle(self):
        """Center the map on current vehicle position."""
        if self.current_position:
            lat, lon = self.current_position
            self.map_center = [lat, lon]
            self._update_map_display()
    
    def _clear_flight_path(self):
        """Clear the flight path history."""
        self.flight_path = []
        if self.current_position:
            self._update_map_display()
    
    def update_view(self, data):
        """
        Update the view with new data.
        
        Args:
            data: Telemetry data dictionary
        """
        self.update_map(data)
