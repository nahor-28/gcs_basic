from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter
)
from PySide6.QtCore import Qt

from views.base_view import BaseView
from core.signal_manager import SignalManager

# Import layout views
from views.layouts.header_view import HeaderView
from views.layouts.telemetry_view import TelemetryView
from views.layouts.status_view import StatusView
from views.layouts.map_view import MapView

class MainView(BaseView):
    """Main view for the application that integrates all sub-views."""
    
    def __init__(self, signal_manager: SignalManager):
        """Initialize the main view."""
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the UI components."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add header
        self.header_view = HeaderView(self.signal_manager)
        main_layout.addWidget(self.header_view)
        
        # Create a splitter for the main content area
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for controls and telemetry
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add telemetry view
        self.telemetry_view = TelemetryView(self.signal_manager)
        left_layout.addWidget(self.telemetry_view)
        
        # Add status view
        self.status_view = StatusView(self.signal_manager)
        left_layout.addWidget(self.status_view)
        
        # Add left panel to splitter
        splitter.addWidget(left_widget)
        
        # Right panel for map
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add map view
        self.map_view = MapView(self.signal_manager)
        right_layout.addWidget(self.map_view)
        
        # Add right panel to splitter
        splitter.addWidget(right_widget)
        
        # Set initial sizes for the splitter
        splitter.setSizes([400, 800])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter, 1)  # 1 = stretch factor
        
        # Set main layout
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect to signals from signal manager
        # Use lambda to allow distinguishing between signal-driven updates and direct calls
        self.signal_manager.telemetry_update.connect(
            lambda data: self.update_telemetry(data, from_signal=True)
        )
        self.signal_manager.connection_status_changed.connect(self.update_connection_status)
        self.signal_manager.status_text_received.connect(self.update_status_message)
    
    def update_telemetry(self, data, from_signal=False):
        """Update telemetry display with new data."""
        # Update telemetry view
        self.telemetry_view.update_view(data)
        # Update map
        self.map_view.update_view(data)
    
    def update_connection_status(self, status, message):
        """Update the connection status."""
        # Update header view
        self.header_view.update_connection_status(status, message)
    
    def update_status_message(self, text, severity):
        """Update status message display."""
        # Status view handles this directly through its signal connection
        pass
    
    def update_view(self, data):
        """Update the view with new data."""
        # Main view doesn't need to handle this, as sub-views
        # are updated through their individual update methods
        pass
