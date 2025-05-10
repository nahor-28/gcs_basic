import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from core.signal_manager import SignalManager
from mvc_application import MVCApplication

def emit_test_telemetry(app_window):
    """Emit test telemetry data to verify views update correctly."""
    print("Sending test telemetry data...")
    
    # Emit attitude data
    app_window.signal_manager.telemetry_update.emit({
        'attitude': {
            'roll': 5.2,
            'pitch': -2.1,
            'yaw': 178.5,
            'heading': 180.0
        }
    })
    
    # Emit position data
    app_window.signal_manager.telemetry_update.emit({
        'position': {
            'lat': 37.7749,
            'lon': -122.4194,
            'alt': 150.5,
            'relative_alt': 50.2
        }
    })
    
    # Emit battery data
    app_window.signal_manager.telemetry_update.emit({
        'battery': {
            'voltage': 12.4,
            'current': 15.2,
            'level': 85
        }
    })
    
    # Emit speed data
    app_window.signal_manager.telemetry_update.emit({
        'speed': {
            'airspeed': 12.3,
            'groundspeed': 11.8,
            'climb': -0.5
        }
    })
    
    print("Test telemetry data sent")

def main():
    """Run the application with test telemetry data."""
    app = QApplication(sys.argv)
    
    # Create the main application window
    window = MVCApplication()
    
    # Schedule the test telemetry to emit after the UI is shown
    QTimer.singleShot(2000, lambda: emit_test_telemetry(window))
    
    # Update telemetry regularly
    test_timer = QTimer()
    test_timer.timeout.connect(lambda: emit_test_telemetry(window))
    test_timer.start(3000)  # Send new test data every 3 seconds
    
    # Start the application event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
