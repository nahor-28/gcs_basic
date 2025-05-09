import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from core.signal_manager import SignalManager
from views.main_view import MainView

def test_mvc_view():
    """Test the new MVC view structure."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Create signal manager
    signal_manager = SignalManager()
    
    # Create main view
    window = MainView(signal_manager)
    window.show()
    
    # Simulate some telemetry data
    def simulate_telemetry():
        # Simulate HEARTBEAT
        signal_manager.telemetry_update.emit({
            "type": "HEARTBEAT",
            "mode": "GUIDED",
            "armed": True
        })
        
        # Simulate GPS data
        signal_manager.telemetry_update.emit({
            "type": "GPS_RAW_INT",
            "gps_fix_type": 3,
            "gps_satellites": 8
        })
        
        # Simulate battery data
        signal_manager.telemetry_update.emit({
            "type": "SYS_STATUS",
            "battery_voltage": 12.6,
            "battery_remaining": 85
        })
        
        # Simulate position data
        signal_manager.telemetry_update.emit({
            "type": "GLOBAL_POSITION_INT",
            "lat": 37.7749,
            "lon": -122.4194
        })
        
        # Simulate status message
        signal_manager.status_text_received.emit("Test status message", 0)
    
    # Simulate data after a short delay
    QTimer.singleShot(1000, simulate_telemetry)
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_mvc_view()) 