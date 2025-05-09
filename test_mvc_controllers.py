import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from core.signal_manager import SignalManager
from models.vehicle_model import VehicleModel
from models.connection_model import ConnectionModel
from models.status_model import StatusModel
from views.layouts.telemetry_view import TelemetryView
from views.layouts.header_view import HeaderView
from views.layouts.status_view import StatusView
from controllers.vehicle_controller import VehicleController
from controllers.connection_controller import ConnectionController
from controllers.status_controller import StatusController

def test_mvc_controllers():
    """Test the MVC controller layer."""
    app = QApplication(sys.argv)
    
    # Create signal manager
    signal_manager = SignalManager()
    
    # Create models
    vehicle_model = VehicleModel(signal_manager)
    connection_model = ConnectionModel(signal_manager)
    status_model = StatusModel(signal_manager)
    
    # Create views
    telemetry_view = TelemetryView()
    header_view = HeaderView()
    status_view = StatusView()
    
    # Create controllers
    vehicle_controller = VehicleController(vehicle_model, telemetry_view, signal_manager)
    connection_controller = ConnectionController(connection_model, header_view, signal_manager)
    status_controller = StatusController(status_model, status_view, signal_manager)
    
    # Simulate some telemetry data
    def simulate_telemetry():
        # Simulate connection
        connection_model.connect('udp:localhost:14550', 115200)
        
        # Simulate HEARTBEAT
        vehicle_model.update_telemetry({
            "type": "HEARTBEAT",
            "mode": "GUIDED",
            "armed": True
        })
        
        # Simulate GPS data
        vehicle_model.update_telemetry({
            "type": "GPS_RAW_INT",
            "gps_fix_type": 3,
            "gps_satellites": 8
        })
        
        # Simulate battery data
        vehicle_model.update_telemetry({
            "type": "SYS_STATUS",
            "battery_voltage": 12.6,
            "battery_current": 5.2,
            "battery_remaining": 85
        })
        
        # Simulate position data
        vehicle_model.update_telemetry({
            "type": "GLOBAL_POSITION_INT",
            "lat": 37.7749,
            "lon": -122.4194,
            "alt_msl": 100.0,
            "alt_agl": 95.0
        })
        
        # Simulate status message
        status_model.add_message("Test status message", 0)
        
        # Simulate connection status
        connection_model.handle_connection_status("CONNECTED", "Connected successfully")
        
    # Simulate data after a short delay
    QTimer.singleShot(1000, simulate_telemetry)
    
    # Show views
    telemetry_view.show()
    header_view.show()
    status_view.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_mvc_controllers()) 