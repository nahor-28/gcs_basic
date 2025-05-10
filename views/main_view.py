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
        # VehicleController listens to telemetry_update to update VehicleModel.
        # TelemetryView and MapView listen to specific model update signals (e.g., vehicle_position_updated).
        # So, MainView no longer needs to connect to telemetry_update directly.
        # self.signal_manager.telemetry_update.connect(
        #     lambda data: self.update_telemetry(data, from_signal=True)
        # )
        
        # StatusModel should ideally listen to status_text_received if it needs to process these.
        # StatusView listens to status_model_new_message.
        # Removing the connection here as the current update_status_message is a no-op.
        # If StatusModel is not yet handling status_text_received, this might mean
        # raw status texts are not displayed. This points to a needed change in StatusModel.
        # self.signal_manager.status_text_received.connect(self.update_status_message)
        pass # No connections needed in MainView connect_signals for now
    
    # Remove update_telemetry as TelemetryView and MapView should be event-driven from model signals
    # def update_telemetry(self, data, from_signal=False):
    #     """Update telemetry display with new data."""
    #     # Update telemetry view
    #     # self.telemetry_view.update_view(data) # TelemetryView now uses specific model signals
    #     # Update map
    #     # self.map_view.update_view(data) # MapView should also use specific model signals

    # Remove update_status_message as it's a no-op and StatusView handles its own updates.
    # StatusModel should be responsible for processing raw status texts if needed.
    # def update_status_message(self, text, severity):
    #     """Update status message display."""
    #     # Status view handles this directly through its signal connection
    #     pass
    
    def update_view(self, data):
        """Update the view with new data."""
        # Main view doesn't need to handle this, as sub-views
        # are updated through their individual update methods
        pass
