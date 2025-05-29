from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
import logging
from core.signal_manager import SignalManager
from views.base_view import BaseView
from views.layouts.connection_view import ConnectionView
from views.dialogs.arm_takeoff_dialog import ArmTakeoffDialog

# Configure logging
logger = logging.getLogger(__name__)

class HeaderView(BaseView):
    """Header view component for the application."""
    
    def __init__(self, signal_manager: SignalManager):
        super().__init__(signal_manager)
        self.vehicle_controller = None  # Will be set by main application
        self.current_mode = "UNKNOWN"
        self.armed_status = False
        self.connected = False
        # logger.debug("HeaderView initialized")
    
    def set_vehicle_controller(self, vehicle_controller):
        """Set the vehicle controller reference."""
        self.vehicle_controller = vehicle_controller
        # logger.debug("HeaderView: Vehicle controller set")
        
    def setup_ui(self):
        """Setup the header UI components."""
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Add logo or title
        # title_label = QLabel("GCS - Observer MVC")
        # title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        # layout.addWidget(title_label)
        
        # Add connection view
        self.connection_view = ConnectionView(signal_manager=self.signal_manager)
        layout.addWidget(self.connection_view)
        
        # Status label
        self.status_label = QLabel("Status: DISCONNECTED")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.status_label)
        
        # Arm & Takeoff button
        self.arm_takeoff_button = QPushButton("🚁 ARM & TAKEOFF")
        self.arm_takeoff_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #ef6c00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.arm_takeoff_button.setEnabled(False)  # Disabled until connected
        self.arm_takeoff_button.clicked.connect(self.on_arm_takeoff_clicked)
        layout.addWidget(self.arm_takeoff_button)
        
        self.setLayout(layout)
        self.setFixedHeight(50)
        # logger.debug("HeaderView UI setup complete")
        
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect view signals
        self.connection_view.connect_clicked.connect(self.on_connect_clicked)
        self.connection_view.disconnect_clicked.connect(self.on_disconnect_clicked)
        
        # HeaderView itself listens to connection_model_changed to update its status_label
        if self.signal_manager:
            # logger.debug("HeaderView: Connecting to connection_model_changed signal")
            self.signal_manager.connection_model_changed.connect(self._update_status_label_from_model)
            # Listen to vehicle status updates to enable/disable arm button
            self.signal_manager.vehicle_status_updated.connect(self._update_vehicle_status)
            # Listen to command responses
            self.signal_manager.command_response.connect(self._handle_command_response)
        else:
            logger.error("HeaderView: No signal_manager available for signal connections")
    
    def _update_vehicle_status(self, status_data):
        """Update vehicle status and button state."""
        # logger.debug(f"HeaderView: Received vehicle status update: {status_data}")
        
        self.current_mode = status_data.get('mode', 'UNKNOWN')
        self.armed_status = status_data.get('armed', False)
        
        # Update button state based on connection and arming status
        self._update_arm_button_state()
        
    def _update_arm_button_state(self):
        """Update the arm & takeoff button enabled state."""
        # Enable button only if connected and not already armed
        should_enable = self.connected and not self.armed_status
        self.arm_takeoff_button.setEnabled(should_enable)
        
        if self.armed_status:
            self.arm_takeoff_button.setText("🚁 ARMED")
            self.arm_takeoff_button.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
        elif not self.connected:
            self.arm_takeoff_button.setText("🚁 ARM & TAKEOFF")
            self.arm_takeoff_button.setStyleSheet("""
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
        else:
            self.arm_takeoff_button.setText("🚁 ARM & TAKEOFF")
            # Reset to normal orange style
            self.arm_takeoff_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #f57c00;
                }
                QPushButton:pressed {
                    background-color: #ef6c00;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
            """)
            
        logger.debug(f"HeaderView: Arm button state - enabled: {should_enable}, armed: {self.armed_status}, connected: {self.connected}")
    
    def _handle_command_response(self, command_type, success, message):
        """Handle command response from telemetry manager."""
        if command_type == "arm_takeoff":
            if success:
                QMessageBox.information(self, "Command Sent", message)
                logger.info(f"HeaderView: Arm & takeoff success: {message}")
            else:
                QMessageBox.warning(self, "Command Failed", message)
                logger.warning(f"HeaderView: Arm & takeoff failed: {message}")
    
    def on_arm_takeoff_clicked(self):
        """Handle arm & takeoff button click."""
        logger.info("HeaderView: Arm & takeoff button clicked")
        
        if not self.vehicle_controller:
            QMessageBox.warning(self, "Error", "Vehicle controller not available")
            return
            
        if not self.connected:
            QMessageBox.warning(self, "Not Connected", "Please connect to vehicle first")
            return
            
        if self.armed_status:
            QMessageBox.information(self, "Already Armed", "Vehicle is already armed")
            return
        
        # Show confirmation dialog
        dialog = ArmTakeoffDialog(self, self.current_mode, self.armed_status)
        dialog.arm_takeoff_confirmed.connect(self._execute_arm_takeoff)
        dialog.exec()
        
    def _execute_arm_takeoff(self, altitude):
        """Execute the arm & takeoff command."""
        logger.info(f"HeaderView: Executing arm & takeoff to {altitude}m")
        
        if self.vehicle_controller:
            self.vehicle_controller.request_arm_takeoff(altitude)
        else:
            logger.error("HeaderView: No vehicle controller available for arm & takeoff")
    
    def _update_status_label_from_model(self, model_data: dict):
        """Update the connection status display based on model data."""
        # logger.debug(f"HeaderView: Received connection_model_changed with data: {model_data}")
        
        status = model_data.get('status', 'UNKNOWN')
        message = model_data.get('message', '')
        conn_str = model_data.get('connection_string', '-')
        
        # Update connection state
        self.connected = (status == "CONNECTED")
        self._update_arm_button_state()

        if status == "CONNECTED":
            status_text = f"Status: CONNECTED to {conn_str}"
        elif status == "CONNECTING":
            status_text = f"Status: CONNECTING to {conn_str}..."
            if message: # Add specific message if available (e.g. "Waiting for heartbeat")
                status_text = f"Status: CONNECTING - {message}"
        elif status == "RECONNECTING":
            status_text = f"Status: RECONNECTING to {conn_str}..."
            if message: 
                status_text = f"Status: RECONNECTING - {message}"
        elif status == "DISCONNECTED":
            status_text = "Status: DISCONNECTED"
            if message and message != "Disconnected": # Show specific disconnect message if not generic
                 status_text = f"Status: DISCONNECTED - {message}"
        elif status == "ERROR":
            status_text = f"Status: ERROR"
            if message:
                status_text += f" - {message}"
        else: # Catch any other statuses
            status_text = f"Status: {status}"
            if message:
                status_text += f" - {message}"

        # logger.debug(f"HeaderView: Setting status label to: {status_text}")
        self.status_label.setText(status_text)
            
    def on_connect_clicked(self, connection_string, baud_rate):
        """Handle connect button click."""
        if self.signal_manager:
            # logger.debug(f"HeaderView: Emitting connection_request with {connection_string}, {baud_rate}")
            # Forward the connection request to the signal manager
            self.signal_manager.connection_request.emit(connection_string, baud_rate)
    
    def on_disconnect_clicked(self):
        """Handle disconnect button click."""
        if self.signal_manager:
            # logger.debug("HeaderView: Emitting disconnect_request")
            # Forward the disconnect request to the signal manager
            self.signal_manager.disconnect_request.emit()
