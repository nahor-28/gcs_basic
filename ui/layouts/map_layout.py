from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QWidget, QSizePolicy
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
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
        
        # Create and configure WebEngineView
        self.map_view = QWebEngineView()
        self.map_view.setMinimumSize(600, 600)  # Minimum size for map
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.map_view)
        self.setLayout(layout)
        self.init_map()
        
    def on_load_finished(self, ok):
        """Handle page load finished event."""
        if ok:
            print("Map page loaded successfully")
        else:
            print("Failed to load map page")
        
    def init_map(self):
        """Initialize the map with OpenStreetMap."""
        # Ensure local Leaflet files exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        leaflet_js = os.path.join(script_dir, 'leaflet/leaflet.js')
        leaflet_css = os.path.join(script_dir, 'leaflet/leaflet.css')
        
        if not os.path.exists(leaflet_js) or not os.path.exists(leaflet_css):
            print("Error: 'leaflet.js' and/or 'leaflet.css' not found in the script directory.")
            print("Please download Leaflet (https://leafletjs.com/) and place 'leaflet.js' and 'leaflet.css' here.")
            return

         # Create the HTML content with offline fallback and fixed CSS
        html_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' data: gap: https://ssl.gstatic.com 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src *; img-src 'self' data: content: https://*.tile.openstreetmap.org;">
    <title>Drone Map</title>
    <link rel="stylesheet" href="./leaflet/leaflet.css" />
    <script src="./leaflet/leaflet.js"></script>
    <style>
        html, body { 
            height: 100%; 
            width: 100%;
            margin: 0; 
            padding: 0; 
        }
        #map { 
            height: 100%; 
            width: 100%;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Initialize the map
        var map = L.map('map').setView([21.146, 79.08], 10);
        
        // Try multiple tile providers
        function addTileLayer() {
            // First try OpenStreetMap
            var osmTiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                subdomains: 'abc'
            });
            
            // Add the tile layer to the map
            osmTiles.addTo(map);
            
            // Handle tile loading errors
            osmTiles.on('tileerror', function(error) {
                console.log('OSM Tile loading error, trying alternative source');
                osmTiles.remove();
                
                // Try Carto as a fallback
                var cartoTiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(map);
            });
        }
        
        // Add tile layer
        addTileLayer();
        
        var droneIcon = L.icon({
            iconUrl: 'images/drone-icon.png',
            shadowUrl: 'images/shadow-icon.png',

            iconSize:     [64, 64], // size of the icon
            shadowSize:   [48, 48], // size of the shadow
        });

        // Add initial marker
        var marker = L.marker([0, 0], {icon: droneIcon}).addTo(map);
        
        // Function to update marker position
        function updateMarkerPosition(lat, lon) {
            if (marker) {
                marker.setLatLng([lat, lon]);
                map.panTo([lat, lon]);
            }
        }
        
        // Debug tile loading
        map.on('tileerror', function(e) {
            console.log('Tile error:', e);
        });
        
        // Log when map is ready
        map.whenReady(function() {
            console.log('Map is ready and initialized');
        });
    </script>
</body>
</html>
'''
        
        # Save the HTML content to a temporary file
        temp_file = os.path.join(script_dir, 'map.html')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Configure QWebEngineView for better web access
        self.map_view.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Create a custom page to handle console messages with improved logging
        class MapWebPage(QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, line, source):
                levels = {
                    QWebEnginePage.InfoMessageLevel: "INFO",
                    QWebEnginePage.WarningMessageLevel: "WARNING",
                    QWebEnginePage.ErrorMessageLevel: "ERROR"
                }
                level_str = levels.get(level, "UNKNOWN")
                print(f"JS {level_str}: {message} (line {line}, source: {source})")
        
        # Set up the custom page
        self.page = MapWebPage(self.map_view)
        self.page.loadFinished.connect(self.on_load_finished)
        
        # Enhanced settings for web content
        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        
        # Apply the custom page to the map view
        self.map_view.setPage(self.page)
        # Load the map in the web view
        self.map_view.page().setBackgroundColor(Qt.white)
        url = QUrl.fromLocalFile(temp_file)
        self.map_view.load(url)
        
    def update_position(self, lat, lon):
        """Update the map with the current vehicle position."""
        if lat is not None and lon is not None:
            self.current_position = (lat, lon)
            js_code = f"updateMarkerPosition({lat}, {lon});"
            self.map_view.page().runJavaScript(js_code)
            # print(f"Updating map position to: {lat}, {lon}") 