from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QGroupBox,
    QStatusBar, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Slot
import serial.tools.list_ports
import time

class MainWindow(QMainWindow):
    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Creates and arranges the UI elements."""
        self.setWindowTitle("ArduPilot GCS - Basic Telemetry")
        self.resize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel for telemetry
        telemetry_panel = QWidget()
        telemetry_layout = QVBoxLayout(telemetry_panel)
        
        # Create right panel for connection
        connection_panel = self.create_connection_panel()
        
        # Add panels to main layout
        main_layout.addWidget(telemetry_panel, 7)  # 70% of width
        main_layout.addWidget(connection_panel, 3)  # 30% of width
        
        # Create telemetry sections
        self.create_status_bar()
        self.create_flight_status_section(telemetry_layout)
        self.create_position_section(telemetry_layout)
        self.create_attitude_section(telemetry_layout)
        self.create_speed_section(telemetry_layout)
        self.create_gps_battery_section(telemetry_layout)
        self.create_status_text_section(telemetry_layout)
        
    def create_connection_panel(self):
        """Creates the connection panel with controls."""
        panel = QGroupBox("Connection")
        layout = QVBoxLayout(panel)
        
        # Port selection
        layout.addWidget(QLabel("Port/Address:"))
        self.port_combo = QComboBox()
        self.populate_ports()
        layout.addWidget(self.port_combo)
        
        # Baud rate
        layout.addWidget(QLabel("Baud Rate:"))
        self.baud_edit = QLineEdit("115200")
        layout.addWidget(self.baud_edit)
        
        # Buttons
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setEnabled(False)
        
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.disconnect_btn)
        layout.addStretch()
        
        return panel
        
    def create_status_bar(self):
        """Creates the status bar at the bottom of the window."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Connection status
        self.connection_status_label = QLabel("Status: DISCONNECTED")
        self.status_bar.addWidget(self.connection_status_label)
        
        # Last message type
        self.last_msg_type_label = QLabel("Last Msg Type: None")
        self.status_bar.addPermanentWidget(self.last_msg_type_label)
        
    def create_flight_status_section(self, parent_layout):
        """Creates the flight status section."""
        group = QGroupBox("Flight Status")
        layout = QHBoxLayout(group)
        
        self.mode_label = QLabel("Mode: ---")
        self.arm_label = QLabel("Armed: ---")
        
        layout.addWidget(self.mode_label)
        layout.addWidget(self.arm_label)
        
        parent_layout.addWidget(group)
        
    def create_position_section(self, parent_layout):
        """Creates the position and altitude section."""
        group = QGroupBox("Position & Altitude")
        layout = QVBoxLayout(group)
        
        self.lat_label = QLabel("Lat: ---")
        self.lon_label = QLabel("Lon: ---")
        self.alt_agl_label = QLabel("Alt (AGL): --- m")
        self.alt_msl_label = QLabel("Alt (MSL): --- m")
        
        layout.addWidget(self.lat_label)
        layout.addWidget(self.lon_label)
        layout.addWidget(self.alt_agl_label)
        layout.addWidget(self.alt_msl_label)
        
        parent_layout.addWidget(group)
        
    def create_attitude_section(self, parent_layout):
        """Creates the attitude section."""
        group = QGroupBox("Attitude")
        layout = QVBoxLayout(group)
        
        self.roll_label = QLabel("Roll: --- °")
        self.pitch_label = QLabel("Pitch: --- °")
        self.yaw_label = QLabel("Yaw: --- °")
        self.heading_label = QLabel("Heading: --- °")
        
        layout.addWidget(self.roll_label)
        layout.addWidget(self.pitch_label)
        layout.addWidget(self.yaw_label)
        layout.addWidget(self.heading_label)
        
        parent_layout.addWidget(group)
        
    def create_speed_section(self, parent_layout):
        """Creates the speed and climb section."""
        group = QGroupBox("Speed & Climb")
        layout = QVBoxLayout(group)
        
        self.airspeed_label = QLabel("Airspeed: --- m/s")
        self.groundspeed_label = QLabel("Groundspeed: --- m/s")
        self.climb_rate_label = QLabel("Climb Rate: --- m/s")
        
        layout.addWidget(self.airspeed_label)
        layout.addWidget(self.groundspeed_label)
        layout.addWidget(self.climb_rate_label)
        
        parent_layout.addWidget(group)
        
    def create_gps_battery_section(self, parent_layout):
        """Creates the GPS and battery section."""
        group = QGroupBox("GPS & Battery")
        layout = QVBoxLayout(group)
        
        self.gps_fix_label = QLabel("GPS Fix: ---")
        self.gps_sats_label = QLabel("GPS Sats: ---")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        
        self.batt_volt_label = QLabel("Batt V: --- V")
        self.batt_curr_label = QLabel("Batt A: --- A")
        self.batt_rem_label = QLabel("Batt Rem: --- %")
        
        layout.addWidget(self.gps_fix_label)
        layout.addWidget(self.gps_sats_label)
        layout.addWidget(separator)
        layout.addWidget(self.batt_volt_label)
        layout.addWidget(self.batt_curr_label)
        layout.addWidget(self.batt_rem_label)
        
        parent_layout.addWidget(group)
        
    def create_status_text_section(self, parent_layout):
        """Creates the status text section."""
        group = QGroupBox("Vehicle Messages")
        layout = QVBoxLayout(group)
        
        self.status_text_label = QLabel("---")
        self.status_text_label.setWordWrap(True)
        layout.addWidget(self.status_text_label)
        
        parent_layout.addWidget(group)
        
    def populate_ports(self):
        """Populates the port combo box with available serial ports."""
        try:
            ports = [p.device for p in serial.tools.list_ports.comports()]
            # Add common UDP addresses
            ports.extend(['udp:localhost:14550', 'udp:0.0.0.0:14550'])
        except Exception as e:
            print(f"Warning: Could not list serial ports - {e}")
            ports = ['udp:localhost:14550', '/dev/ttyACM0', 'COM3']  # Fallback
            
        self.port_combo.addItems(ports)
        
    def connect_signals(self):
        """Connects UI signals to slots."""
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        self.disconnect_btn.clicked.connect(self.on_disconnect_clicked)
        
        # Connect signal manager signals to slots
        self.signal_manager.telemetry_update.connect(self.handle_telemetry_update)
        self.signal_manager.connection_status_changed.connect(self.handle_connection_status_change)
        self.signal_manager.status_text_received.connect(self.handle_status_text)
        
    @Slot()
    def on_connect_clicked(self):
        """Handles connect button click."""
        conn_str = self.port_combo.currentText()
        baud_str = self.baud_edit.text()
        
        if not conn_str:
            QMessageBox.critical(self, "Connection Error", "Please select a connection port/address.")
            return
            
        try:
            baud = int(baud_str)
        except ValueError:
            QMessageBox.critical(self, "Connection Error", "Please enter a valid integer baud rate.")
            return
            
        # Emit connection request signal
        self.signal_manager.connection_request.emit(conn_str, baud)
        
    @Slot()
    def on_disconnect_clicked(self):
        """Handles disconnect button click."""
        self.signal_manager.disconnect_request.emit()
        
    @Slot(dict)
    def handle_telemetry_update(self, data_update):
        """Handles telemetry update signal."""
        update_type = data_update.get("type")
        self.last_msg_type_label.setText(f"Last Msg Type: {update_type}")
        
        if update_type == "HEARTBEAT":
            self.mode_label.setText(f"Mode: {data_update.get('mode', 'N/A')}")
            armed_status = data_update.get('armed')
            self.arm_label.setText(f"Armed: {'Yes' if armed_status else 'No'}")
            
        elif update_type == "GLOBAL_POSITION_INT":
            self.lat_label.setText(f"Lat: {data_update.get('lat', 'N/A'):.7f}")
            self.lon_label.setText(f"Lon: {data_update.get('lon', 'N/A'):.7f}")
            self.alt_agl_label.setText(f"Alt (AGL): {data_update.get('alt_agl', 'N/A'):.2f} m")
            self.alt_msl_label.setText(f"Alt (MSL): {data_update.get('alt_msl', 'N/A'):.2f} m")
            
        elif update_type == "ATTITUDE":
            self.roll_label.setText(f"Roll: {data_update.get('roll', 'N/A'):.1f} °")
            self.pitch_label.setText(f"Pitch: {data_update.get('pitch', 'N/A'):.1f} °")
            self.yaw_label.setText(f"Yaw: {data_update.get('yaw', 'N/A'):.1f} °")
            
        elif update_type == "VFR_HUD":
            airspeed = data_update.get('airspeed')
            groundspeed = data_update.get('groundspeed')
            heading = data_update.get('heading')
            climb_rate = data_update.get('climb_rate')
            
            self.airspeed_label.setText(f"Airspeed: {airspeed:.2f} m/s" if airspeed is not None else "Airspeed: ---")
            self.groundspeed_label.setText(f"Groundspeed: {groundspeed:.2f} m/s" if groundspeed is not None else "Groundspeed: ---")
            self.heading_label.setText(f"Heading: {heading}°" if heading is not None else "Heading: ---")
            self.climb_rate_label.setText(f"Climb Rate: {climb_rate:.2f} m/s" if climb_rate is not None else "Climb Rate: ---")
            
        elif update_type == "GPS_RAW_INT":
            fix = data_update.get('gps_fix_type', -1)
            sats = data_update.get('gps_satellites', -1)
            fix_map = {0: "No Fix", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
            self.gps_fix_label.setText(f"GPS Fix: {fix_map.get(fix, f'Unknown ({fix})')}")
            self.gps_sats_label.setText(f"GPS Sats: {sats if sats != -1 else '---'}")
            
        elif update_type == "SYS_STATUS":
            voltage = data_update.get('battery_voltage')
            current = data_update.get('battery_current')
            remaining = data_update.get('battery_remaining')
            
            self.batt_volt_label.setText(f"Batt V: {voltage:.2f} V" if voltage is not None else "Batt V: ---")
            self.batt_curr_label.setText(f"Batt A: {current:.2f} A" if current is not None else "Batt A: ---")
            self.batt_rem_label.setText(f"Batt Rem: {remaining} %" if remaining is not None else "Batt Rem: ---")
            
    @Slot(str, str)
    def handle_connection_status_change(self, status, message=""):
        """Handles connection status change signal."""
        display_message = f"Status: {status}"
        if message:
            # Shorten long error messages for display
            if len(message) > 50:
                message = message[:47] + "..."
            display_message += f" ({message})"
        self.connection_status_label.setText(display_message)
        
        # Enable/Disable widgets based on status
        if status == "CONNECTED":
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.port_combo.setEnabled(False)
            self.baud_edit.setEnabled(False)
        elif status == "DISCONNECTED" or status == "ERROR":
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.port_combo.setEnabled(True)
            self.baud_edit.setEnabled(True)
        elif status == "CONNECTING" or status == "DISCONNECTING":
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(False)
            self.port_combo.setEnabled(False)
            self.baud_edit.setEnabled(False)
            
    @Slot(str, int)
    def handle_status_text(self, text, severity, **kwargs):
        """Handles status text signal."""
        self.status_text_label.setText(text) 