import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MVCApplication(QMainWindow):
    """Main application class that integrates all MVC components."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GCS - Observer MVC Architecture")
        self.resize(1200, 800)
        
        # logger.debug("Initializing MVCApplication components")
        
        self.signal_manager = SignalManager()
        
        self.telemetry_manager = TelemetryManager(
            initial_conn_string='udp:0.0.0.0:14550',
            initial_baud=115200,
            signal_manager=self.signal_manager
        )
        
        self.vehicle_model = VehicleModel(self.signal_manager)
        self.connection_model = ConnectionModel(self.signal_manager)
        self.status_model = StatusModel(self.signal_manager)
        
        self.main_view = MainView(self.signal_manager)
        self.setCentralWidget(self.main_view)
        
        self.vehicle_controller = VehicleController(
            self.vehicle_model,
            None,
            self.signal_manager
        )
        self.connection_controller = ConnectionController(
            self.connection_model,
            None,
            self.signal_manager
        )
        self.status_controller = StatusController(
            self.status_model,
            None,
            self.signal_manager
        )
        
        # logger.debug("All MVCApplication components initialized")
        self._initialize_ui()
        
        # Wire up HeaderView with VehicleController after everything is initialized
        if hasattr(self.main_view, 'header_view'):
            self.main_view.header_view.set_vehicle_controller(self.vehicle_controller)
            # logger.debug("HeaderView wired to VehicleController")
        
    def _initialize_ui(self):
        self.show()
        self.status_model.add_message("Application initialized (Event-Driven)", 0)
        # logger.debug("MVCApplication UI initialized")
        
    def closeEvent(self, event):
        # logger.debug("MVCApplication closing")
        if self.telemetry_manager:
            self.telemetry_manager.stop()
        self.status_model.add_message("Application closing", 0)
        event.accept()

def main():
    logger.info("Starting GCS Basic application")
    app = QApplication(sys.argv)
    window = MVCApplication()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 