#!/usr/bin/env python3
"""
Manual connection test script for GCS Basic
Tests the signal flow from TelemetryManager to UI components
"""

import sys
import time
import logging
from pathlib import Path

# Add parent directory to path so we can import from the project
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import QTimer

from core.signal_manager import SignalManager
from core.telemetry_manager import TelemetryManager
from models.vehicle_model import VehicleModel
from controllers.vehicle_controller import VehicleController
from views.layouts.telemetry_view import TelemetryView

# Configure logging to show everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SignalFlowTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GCS Signal Flow Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize signal manager
        self.signal_manager = SignalManager()
        
        # Initialize telemetry manager (default to UDP)
        self.telemetry_manager = TelemetryManager(
            initial_conn_string='udp:0.0.0.0:14550',
            initial_baud=115200,
            signal_manager=self.signal_manager
        )
        
        # Initialize MVC components
        self.vehicle_model = VehicleModel(self.signal_manager)
        self.vehicle_controller = VehicleController(
            self.vehicle_model,
            None,  # No view passed to controller
            self.signal_manager
        )
        
        # Initialize telemetry view
        self.telemetry_view = TelemetryView(self.signal_manager)
        
        self.setup_ui()
        self.setup_signal_monitoring()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status labels
        self.connection_status = QLabel("Status: DISCONNECTED")
        layout.addWidget(self.connection_status)
        
        # Connect/Disconnect buttons
        self.connect_btn = QPushButton("Connect to localhost:14550")
        self.connect_btn.clicked.connect(self.connect_to_vehicle)
        layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_from_vehicle)
        self.disconnect_btn.setEnabled(False)
        layout.addWidget(self.disconnect_btn)
        
        # Add telemetry view
        layout.addWidget(self.telemetry_view)
        
        # Log area
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(150)
        layout.addWidget(self.log_area)
        
        self.setLayout(layout)
        
        # Set up a timer to check for log messages
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_log_display)
        self.log_timer.start(100)  # Update every 100ms
        
    def setup_signal_monitoring(self):
        """Set up monitoring of key signals to track flow"""
        # Monitor connection status changes
        self.signal_manager.connection_status_changed.connect(self.on_connection_status_changed)
        
        # Monitor telemetry updates at different levels
        self.signal_manager.telemetry_update.connect(self.on_raw_telemetry_received)
        self.signal_manager.vehicle_attitude_updated.connect(self.on_attitude_signal_received)
        self.signal_manager.vehicle_position_updated.connect(self.on_position_signal_received)
        self.signal_manager.vehicle_status_updated.connect(self.on_status_signal_received)
        
    def on_connection_status_changed(self, status, message, conn_string):
        """Handle connection status changes"""
        self.connection_status.setText(f"Status: {status} - {message}")
        self.log_message(f"Connection Status: {status} - {message}")
        
        if status == "CONNECTED":
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
        else:
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            
    def on_raw_telemetry_received(self, data):
        """Monitor raw telemetry from TelemetryManager"""
        msg_type = data.get('type', 'UNKNOWN')
        self.log_message(f"RAW TELEMETRY: {msg_type} - {data}")
        
    def on_attitude_signal_received(self, data):
        """Monitor attitude signals from VehicleModel"""
        self.log_message(f"ATTITUDE SIGNAL: {data}")
        
    def on_position_signal_received(self, data):
        """Monitor position signals from VehicleModel"""
        self.log_message(f"POSITION SIGNAL: {data}")
        
    def on_status_signal_received(self, data):
        """Monitor status signals from VehicleModel"""
        self.log_message(f"STATUS SIGNAL: {data}")
        
    def log_message(self, message):
        """Add a message to the log display"""
        timestamp = time.strftime("%H:%M:%S")
        if not hasattr(self, '_log_buffer'):
            self._log_buffer = []
        self._log_buffer.append(f"[{timestamp}] {message}")
        
        # Keep only last 50 messages
        if len(self._log_buffer) > 50:
            self._log_buffer = self._log_buffer[-50:]
            
    def update_log_display(self):
        """Update the log display with buffered messages"""
        if hasattr(self, '_log_buffer') and self._log_buffer:
            current_text = self.log_area.toPlainText()
            new_text = '\n'.join(self._log_buffer)
            if new_text != current_text:
                self.log_area.setPlainText(new_text)
                # Auto-scroll to bottom
                cursor = self.log_area.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                self.log_area.setTextCursor(cursor)
                
    def connect_to_vehicle(self):
        """Connect to vehicle using signal system"""
        self.log_message("User clicked Connect - emitting connection_request signal")
        self.signal_manager.connection_request.emit('udp:localhost:14550', 115200)
        
    def disconnect_from_vehicle(self):
        """Disconnect from vehicle using signal system"""
        self.log_message("User clicked Disconnect - emitting disconnect_request signal")
        self.signal_manager.disconnect_request.emit()
        
    def closeEvent(self, event):
        """Clean shutdown"""
        if self.telemetry_manager:
            self.telemetry_manager.stop()
        event.accept()

def main():
    """Run the signal flow test"""
    print("=== GCS Signal Flow Test ===")
    print("This test will:")
    print("1. Set up the complete MVC signal flow")
    print("2. Attempt to connect to localhost:14550 (SITL/MAVProxy)")
    print("3. Display detailed logging of signal flow")
    print("4. Show telemetry updates in the UI")
    print("")
    print("To test with ArduPilot SITL:")
    print("  1. Run: sim_vehicle.py -v ArduCopter --out=udp:localhost:14550")
    print("  2. Or run MAVProxy and forward to localhost:14550")
    print("")
    print("Expected signal flow:")
    print("  TelemetryManager -> VehicleController -> VehicleModel -> TelemetryView")
    print("")
    
    app = QApplication(sys.argv)
    window = SignalFlowTestWindow()
    window.show()
    
    print("Test window opened. Check console for detailed logging.")
    print("Click 'Connect' to test signal flow.")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 