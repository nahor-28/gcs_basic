import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from core.signal_manager import SignalManager
from models.vehicle_model import VehicleModel
from models.connection_model import ConnectionModel
from models.status_model import StatusModel

def test_mvc_models():
    """Test the MVC model layer."""
    app = QApplication(sys.argv)
    
    # Create signal manager
    signal_manager = SignalManager()
    
    # Create models
    vehicle_model = VehicleModel(signal_manager)
    connection_model = ConnectionModel(signal_manager)
    status_model = StatusModel(signal_manager)
    
    # Connect model signals
    def on_vehicle_data_changed(data):
        print(f"Vehicle data changed: {data}")
        
    def on_connection_status_changed(status, message):
        print(f"Connection status: {status} - {message}")
        
    def on_status_message_added(text, severity):
        print(f"Status message: [{severity}] {text}")
        
    vehicle_model.data_changed.connect(on_vehicle_data_changed)
    connection_model.status_changed.connect(on_connection_status_changed)
    status_model.message_added.connect(on_status_message_added)
    
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
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_mvc_models()) 