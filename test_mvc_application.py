import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from mvc_application import MVCApplication

def simulate_telemetry(app):
    """Simulate telemetry data for testing."""
    # Get the signal manager from the application
    signal_manager = app.signal_manager
    
    # Simulate connection
    signal_manager.connection_status.emit("CONNECTING", "Connecting to test vehicle...")
    QTimer.singleShot(1000, lambda: signal_manager.connection_request.emit("CONNECTED", "Connected successfully"))
    
    # Simulate periodic telemetry updates
    def send_telemetry():
        # Simulate HEARTBEAT
        signal_manager.telemetry_received.emit({
            "type": "HEARTBEAT",
            "mode": "GUIDED",
            "armed": True
        })
        
        # Simulate GPS data
        signal_manager.telemetry_received.emit({
            "type": "GPS_RAW_INT",
            "gps_fix_type": 3,
            "gps_satellites": 8
        })
        
        # Simulate battery data
        signal_manager.telemetry_received.emit({
            "type": "SYS_STATUS",
            "battery_voltage": 12.6,
            "battery_current": 5.2,
            "battery_remaining": 85
        })
        
        # Simulate position data
        signal_manager.telemetry_received.emit({
            "type": "GLOBAL_POSITION_INT",
            "lat": 37.7749,
            "lon": -122.4194,
            "alt_msl": 100.0,
            "alt_agl": 95.0
        })
        
        # Schedule next update
        QTimer.singleShot(1000, send_telemetry)
    
    # Start telemetry simulation after connection
    QTimer.singleShot(2000, send_telemetry)

def test_mvc_application():
    """Test the complete MVC application."""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MVCApplication()
    
    # Start telemetry simulation
    simulate_telemetry(window)
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_mvc_application()) 