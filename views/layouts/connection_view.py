from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from views.base_view import BaseView
from core.utils import get_connection_strings
import logging

logger = logging.getLogger(__name__)

class ConnectionView(BaseView):
    """Connection view component for managing vehicle connections."""
    
    connect_clicked = Signal(str, int)  # connection_string, baud_rate
    disconnect_clicked = Signal()
    
    def __init__(self, signal_manager=None, parent=None):
        super().__init__(signal_manager)
        self.available_ports = []
        # logger.debug("ConnectionView initialized")
    
    def setup_ui(self):
        """Setup the connection UI components."""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # Connection String (Serial Port or UDP)
        self.serial_port_combo = QComboBox()
        self.serial_port_combo.setEditable(True)
        self.serial_port_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.serial_port_combo.setPlaceholderText("Enter UDP (e.g., udp:localhost:14550) or select port")
        main_layout.addWidget(self.serial_port_combo)
        self._on_scan_ports() # Populate initially

        # Scan button
        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self._on_scan_ports)
        main_layout.addWidget(self.scan_button)

        # Baud Rate
        self.baud_rate_combo = QComboBox()
        common_baud_rates = ["38400", "57600", "115200", "921600"]
        self.baud_rate_combo.addItems(common_baud_rates)
        self.baud_rate_combo.setCurrentText("115200")
        main_layout.addWidget(self.baud_rate_combo)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self._on_connect_clicked)
        main_layout.addWidget(self.connect_button)

        # Disconnect Button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setEnabled(False) # Disabled until connected
        self.disconnect_button.clicked.connect(self.disconnect_clicked) # Emit signal
        main_layout.addWidget(self.disconnect_button)

        self.setLayout(main_layout)
        
        # Store current connection status, primarily for button logic
        self._current_status = "DISCONNECTED" 
        
        # logger.debug("ConnectionView UI setup complete")
    
    def connect_signals(self):
        """Connect signals to slots."""
        # Connect own button clicks to internal handlers or emit signals
        # self.connect_button.clicked.connect(self._on_connect_clicked) # Now handled by setup_ui
        # self.disconnect_button.clicked.connect(self.disconnect_clicked) # Now handled by setup_ui
        
        if self.signal_manager:
            # Listen to the model changed signal
            # logger.debug("ConnectionView: Connecting to connection_model_changed signal")
            self.signal_manager.connection_model_changed.connect(self._handle_connection_model_changed)
        else:
            logger.error("ConnectionView: No signal_manager available for signal connections")
    
    def _on_connect_clicked(self):
        """Handle the connect button click."""
        connection_string = self.serial_port_combo.currentText()
        baud_rate = self.baud_rate_combo.currentText()
        # logger.debug(f"ConnectionView: Connect clicked - {connection_string} at {baud_rate}")
        self.connect_clicked.emit(connection_string, int(baud_rate))
    
    def _handle_connection_model_changed(self, model_data: dict):
        """
        Handle connection model changes.
        Updates UI elements based on the new model state.
        
        Args:
            model_data: Dictionary containing the full connection model state.
        """
        # logger.debug(f"ConnectionView: Received connection_model_changed with data: {model_data}")
        
        status = model_data.get('status', 'DISCONNECTED')
        self._current_status = status # Update internal status tracker

        connection_string = model_data.get('connection_string', "")
        baud_rate = model_data.get('baud_rate', 115200)
        available_ports = model_data.get('available_ports', [])

        # Update input fields with model data
        if self.serial_port_combo.currentText() != connection_string:
            self.serial_port_combo.setCurrentText(connection_string)
        if self.baud_rate_combo.currentText() != str(baud_rate):
            self.baud_rate_combo.setCurrentText(str(baud_rate))

        # Update available ports if they changed
        # Simple check by length and first element if not empty
        if (not self.available_ports and available_ports) or \
           (self.available_ports and not available_ports) or \
           (self.available_ports and available_ports and 
            (len(self.available_ports) != len(available_ports) or self.available_ports[0] != available_ports[0])):
            self.available_ports = available_ports
            self._populate_serial_ports()

        # Update button states
        if status == "CONNECTED":
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.serial_port_combo.setEnabled(False)
            self.scan_button.setEnabled(False)
            self.baud_rate_combo.setEnabled(False)
        elif status == "CONNECTING":
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True) # Allow disconnect during connection attempt
            self.serial_port_combo.setEnabled(False)
            self.scan_button.setEnabled(False)
            self.baud_rate_combo.setEnabled(False)
        else: # DISCONNECTED, ERROR, etc.
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.serial_port_combo.setEnabled(True)
            self.scan_button.setEnabled(True)
            self.baud_rate_combo.setEnabled(True)

        # logger.debug(f"ConnectionView: Updated UI state - Connect enabled: {self.connect_button.isEnabled()}, Disconnect enabled: {self.disconnect_button.isEnabled()}")

    def _on_scan_ports(self):
        """Scan for available serial ports and update the combo box."""
        # logger.debug("ConnectionView: Scanning for serial ports")
        self.available_ports = get_connection_strings()
        self._populate_serial_ports()

    def _populate_serial_ports(self):
        current_selection = self.serial_port_combo.currentText()
        self.serial_port_combo.clear()
        if self.available_ports:
            self.serial_port_combo.addItems(self.available_ports)
            self.serial_port_combo.setEnabled(True)
            # Try to restore previous selection if it's still valid
            if current_selection in self.available_ports:
                self.serial_port_combo.setCurrentText(current_selection)
            elif self.available_ports: # Select the first one if previous is gone
                self.serial_port_combo.setCurrentIndex(0)
        else:
            self.serial_port_combo.addItem("No ports found")
            self.serial_port_combo.setEnabled(False)
        # logger.debug(f"ConnectionView: Populated serial ports. Current: {self.serial_port_combo.currentText()}")
        
    # The update_view method is no longer needed as updates are event-driven by _handle_connection_model_changed
    # def update_view(self, data):
    #     """Update the view with new data."""
    #     # logger.debug(f"ConnectionView: update_view called with data: {data}")
    #     self.connection_string = data.get('connection_string', self.connection_string)
    #     self.baud_rate = data.get('baud_rate', self.baud_rate)
    #     self.status = data.get('status', self.status)
    #     self.message = data.get('message', self.message)
    #     self.available_ports = data.get('available_ports', self.available_ports)
        
    #     self.serial_port_combo.setCurrentText(self.connection_string)
    #     self.baud_rate_combo.setCurrentText(str(self.baud_rate))

    #     if self.status == "CONNECTED":
    #         self.connect_button.setEnabled(False)
    #         self.disconnect_button.setEnabled(True)
    #     else:
    #         self.connect_button.setEnabled(True)
    #         self.disconnect_button.setEnabled(False)

    #     # logger.debug(f"ConnectionView: Updated state - Connect enabled: {self.connect_button.isEnabled()}, Disconnect enabled: {self.disconnect_button.isEnabled()}")
