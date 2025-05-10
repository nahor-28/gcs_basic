import sys
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

class MVCApplication(QMainWindow):
    """Main application class that integrates all MVC components."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GCS - Observer MVC Architecture")
        self.resize(1200, 800)
        
        self.signal_manager = SignalManager()
        
        self.telemetry_manager = TelemetryManager(
            initial_conn_string='udp:localhost:14550',
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
        
        self._initialize_ui()
        
    def _initialize_ui(self):
        self.show()
        self.status_model.add_message("Application initialized (Event-Driven)", 0)
        
    def closeEvent(self, event):
        if self.telemetry_manager:
            self.telemetry_manager.stop()
        self.status_model.add_message("Application closing", 0)
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MVCApplication()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 