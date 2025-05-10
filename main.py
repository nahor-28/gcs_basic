import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
from core.signal_manager import SignalManager
from core.telemetry_manager import TelemetryManager

# Import models
from models.vehicle_model import VehicleModel
from models.connection_model import ConnectionModel
from models.status_model import StatusModel

# Import views
from views.main_view import MainView

# Import controllers
from controllers.vehicle_controller import VehicleController
from controllers.connection_controller import ConnectionController
from controllers.status_controller import StatusController

class MVCApplication(QMainWindow):
    """Main application class that integrates all MVC components."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GCS - MVC Architecture")
        self.resize(1200, 800)
        
        # Initialize signal manager
        self.signal_manager = SignalManager()
        
        # Initialize telemetry manager
        self.telemetry_manager = TelemetryManager(
            initial_conn_string='udp:localhost:14550',
            initial_baud=115200,
            signal_manager=self.signal_manager
        )
        
        # Create models
        self.vehicle_model = VehicleModel(self.signal_manager)
        self.connection_model = ConnectionModel(self.signal_manager)
        self.status_model = StatusModel(self.signal_manager)
        
        # Create main view
        self.main_view = MainView(self.signal_manager)
        self.setCentralWidget(self.main_view)
        
        # Create controllers
        self.vehicle_controller = VehicleController(
            self.vehicle_model,
            self.main_view.telemetry_view,
            self.signal_manager
        )
        self.connection_controller = ConnectionController(
            self.connection_model,
            self.main_view.header_view,
            self.signal_manager
        )
        self.status_controller = StatusController(
            self.status_model,
            self.main_view.status_view,
            self.signal_manager
        )
        
        # Set up update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_views)
        self.update_timer.start(100)  # Update every 100ms
        
        # Initialize UI
        self._initialize_ui()
        
    def update_views(self):
        """Update all views with current model data."""
        self.vehicle_controller.update_view()
        self.connection_controller.update_view()
        self.status_controller.update_view()
        
    def _initialize_ui(self):
        """Initialize the UI components."""
        # Set initial window state
        self.show()
        
        # Add initial status message
        self.status_model.add_message("Application initialized", 0)
        
    def closeEvent(self, event):
        """Handle application close event."""
        # Stop telemetry manager
        if self.telemetry_manager:
            self.telemetry_manager.stop()
            
        # Add closing message
        self.status_model.add_message("Application closing", 0)
        
        # Accept the close event
        event.accept()

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MVCApplication()
    
    # Start the application event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 