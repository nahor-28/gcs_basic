from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QWidget, QSizePolicy
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import folium
import os

class MapLayout(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Map", parent)
        self.setup_ui()
        self.current_position = (0.0, 0.0)
        
    def setup_ui(self):
        """Creates and arranges the map display."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        self.map_view = QWebEngineView()
        self.map_view.setMinimumSize(600, 600)  # Minimum size for map
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow expansion
        layout.addWidget(self.map_view)
        
        self.setLayout(layout)
        self.init_map()
        
    def init_map(self):
        """Initialize the map with OpenStreetMap."""
        # Create a map centered at (0, 0)
        m = folium.Map(
            location=[0, 0],
            zoom_start=2,
            tiles='OpenStreetMap',
            attr='© OpenStreetMap contributors',
            prefer_canvas=True  # Use canvas renderer for better performance
        )
        
        # Add a marker for the vehicle
        folium.Marker(
            location=[0, 0],
            popup='Vehicle',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        # Save the map to a temporary HTML file with proper styling
        temp_file = os.path.join(os.path.dirname(__file__), 'temp_map.html')
        m.save(temp_file)
        
        # Create a custom HTML with proper styling and script loading
        with open(temp_file, 'r') as f:
            html_content = f.read()
            
        # Add custom CSS to ensure map visibility
        html_content = html_content.replace('</head>', '''
            <style>
                #map { 
                    width: 100%; 
                    height: 100%; 
                    position: absolute; 
                    top: 0; 
                    left: 0; 
                }
                body { 
                    margin: 0; 
                    padding: 0; 
                }
            </style>
            </head>
        ''')
        
        # Write the modified HTML back
        with open(temp_file, 'w') as f:
            f.write(html_content)
        
        # Load the map in the web view with proper settings
        self.map_view.page().setBackgroundColor(Qt.white)
        self.map_view.settings().setAttribute(
            self.map_view.settings().WebAttribute.LocalContentCanAccessFileUrls, 
            True
        )
        self.map_view.load(f"file://{temp_file}")
        
    def update_position(self, lat, lon):
        """Update the map with the current vehicle position."""
        if lat is not None and lon is not None:
            self.current_position = (lat, lon)
            # Create JavaScript to update the marker position
            js_code = f"""
            var map = document.querySelector('#map');
            if (map && map._leaflet_id) {{
                var marker = map._markers[0];
                if (marker) {{
                    marker.setLatLng([{lat}, {lon}]);
                    map.setView([{lat}, {lon}], 15);
                }}
            }}
            """
            self.map_view.page().runJavaScript(js_code) 