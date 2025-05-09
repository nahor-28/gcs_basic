from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt

from views.base_view import BaseView

class MapView(BaseView):
    """Map view component for displaying vehicle position on a map."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
        self.current_position = None
        
    def setup_ui(self):
        """Setup the map UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view for map
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(400)
        
        # Load the map HTML file
        self.web_view.load(QUrl.fromLocalFile("ui/layouts/map.html"))
        
        # Add web view to layout
        layout.addWidget(self.web_view)
        
    def connect_signals(self):
        """Connect signals to slots."""
        # No direct signal connections needed as updates come through update_view
        pass
        
    def update_view(self, data):
        """Update the map with new position data."""
        if data.get("type") == "GLOBAL_POSITION_INT":
            lat = data.get('lat')
            lon = data.get('lon')
            if lat is not None and lon is not None:
                self.update_position(lat, lon)
                
    def update_position(self, lat, lon):
        """Update the vehicle position on the map."""
        self.current_position = (lat, lon)
        # Call JavaScript function to update marker position
        js_code = f"updateMarker({lat}, {lon});"
        self.web_view.page().runJavaScript(js_code) 