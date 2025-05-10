from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt
from views.base_view import BaseView

class TelemetryView(BaseView):
    """Telemetry view component for displaying vehicle telemetry data."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the telemetry UI components."""
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create group boxes for different telemetry categories
        attitude_group = self._create_attitude_group()
        position_group = self._create_position_group()
        battery_group = self._create_battery_group()
        speed_group = self._create_speed_group()
        
        # Add groups to layout
        main_layout.addWidget(attitude_group)
        main_layout.addWidget(position_group)
        main_layout.addWidget(speed_group)
        main_layout.addWidget(battery_group)
        
        # Set main layout
        self.setLayout(main_layout)
    
    def _create_attitude_group(self):
        """Create the attitude telemetry group."""
        group = QGroupBox("Attitude")
        layout = QGridLayout()
        
        # Create labels
        self.roll_label = QLabel("Roll: -- deg")
        self.pitch_label = QLabel("Pitch: -- deg")
        self.yaw_label = QLabel("Yaw: -- deg")
        self.heading_label = QLabel("Heading: -- deg")
        
        # Add labels to layout
        layout.addWidget(QLabel("Roll:"), 0, 0)
        layout.addWidget(self.roll_label, 0, 1)
        layout.addWidget(QLabel("Pitch:"), 1, 0)
        layout.addWidget(self.pitch_label, 1, 1)
        layout.addWidget(QLabel("Yaw:"), 2, 0)
        layout.addWidget(self.yaw_label, 2, 1)
        layout.addWidget(QLabel("Heading:"), 3, 0)
        layout.addWidget(self.heading_label, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def _create_position_group(self):
        """Create the position telemetry group."""
        group = QGroupBox("Position")
        layout = QGridLayout()
        
        # Create labels
        self.lat_label = QLabel("Latitude: --")
        self.lon_label = QLabel("Longitude: --")
        self.alt_label = QLabel("Altitude: -- m")
        self.rel_alt_label = QLabel("Relative Alt: -- m")
        
        # Add labels to layout
        layout.addWidget(QLabel("Latitude:"), 0, 0)
        layout.addWidget(self.lat_label, 0, 1)
        layout.addWidget(QLabel("Longitude:"), 1, 0)
        layout.addWidget(self.lon_label, 1, 1)
        layout.addWidget(QLabel("Altitude:"), 2, 0)
        layout.addWidget(self.alt_label, 2, 1)
        layout.addWidget(QLabel("Relative Alt:"), 3, 0)
        layout.addWidget(self.rel_alt_label, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def _create_battery_group(self):
        """Create the battery telemetry group."""
        group = QGroupBox("Battery")
        layout = QGridLayout()
        
        # Create labels
        self.voltage_label = QLabel("Voltage: -- V")
        self.current_label = QLabel("Current: -- A")
        self.level_label = QLabel("Level: -- %")
        
        # Add labels to layout
        layout.addWidget(QLabel("Voltage:"), 0, 0)
        layout.addWidget(self.voltage_label, 0, 1)
        layout.addWidget(QLabel("Current:"), 1, 0)
        layout.addWidget(self.current_label, 1, 1)
        layout.addWidget(QLabel("Level:"), 2, 0)
        layout.addWidget(self.level_label, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def _create_speed_group(self):
        """Create the speed telemetry group."""
        group = QGroupBox("Speed")
        layout = QGridLayout()
        
        # Create labels
        self.groundspeed_label = QLabel("Ground Speed: -- m/s")
        self.airspeed_label = QLabel("Air Speed: -- m/s")
        self.climb_label = QLabel("Climb Rate: -- m/s")
        
        # Add labels to layout
        layout.addWidget(QLabel("Ground Speed:"), 0, 0)
        layout.addWidget(self.groundspeed_label, 0, 1)
        layout.addWidget(QLabel("Air Speed:"), 1, 0)
        layout.addWidget(self.airspeed_label, 1, 1)
        layout.addWidget(QLabel("Climb Rate:"), 2, 0)
        layout.addWidget(self.climb_label, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def connect_signals(self):
        """Connect signals to slots."""
        if self.signal_manager:
            # Connect directly to telemetry updates
            self.signal_manager.telemetry_update.connect(self.update_view)
    
    def update_view(self, data):
        """Update the telemetry display with new data."""
        if not isinstance(data, dict):
            return
            
        # Get message type from data
        msg_type = data.get('type', '')
        
        # Process by message type
        if msg_type == 'ATTITUDE':
            # Update attitude information
            if 'roll' in data:
                self.roll_label.setText(f"{data['roll']:.1f} deg")
            if 'pitch' in data:
                self.pitch_label.setText(f"{data['pitch']:.1f} deg")
            if 'yaw' in data:
                self.yaw_label.setText(f"{data['yaw']:.1f} deg")
        
        elif msg_type == 'VFR_HUD' and 'heading' in data:
            # Update heading from VFR_HUD
            self.heading_label.setText(f"{data['heading']:.1f} deg")
                
        elif msg_type == 'GLOBAL_POSITION_INT':
            # Update position information
            if 'lat' in data:
                self.lat_label.setText(f"{data['lat']:.7f}")
            if 'lon' in data:
                self.lon_label.setText(f"{data['lon']:.7f}")
            if 'alt_msl' in data:
                self.alt_label.setText(f"{data['alt_msl']:.1f} m")
            if 'alt_agl' in data:
                self.rel_alt_label.setText(f"{data['alt_agl']:.1f} m")
                
        elif msg_type == 'SYS_STATUS':
            # Update battery information
            if 'battery_voltage' in data:
                self.voltage_label.setText(f"{data['battery_voltage']:.2f} V")
            if 'battery_current' in data:
                current = data['battery_current']
                if current is not None:
                    self.current_label.setText(f"{current:.2f} A")
            if 'battery_remaining' in data:
                level = data['battery_remaining']
                if level is not None:
                    self.level_label.setText(f"{level}%")
                
        elif msg_type == 'VFR_HUD':
            # Update speed information
            if 'groundspeed' in data:
                self.groundspeed_label.setText(f"{data['groundspeed']:.1f} m/s")
            if 'airspeed' in data:
                self.airspeed_label.setText(f"{data['airspeed']:.1f} m/s")
            if 'climb_rate' in data:
                self.climb_label.setText(f"{data['climb_rate']:.1f} m/s")
        
        # Process by nested data structure too (for the test script and compatibility)
        self._process_structured_data(data)
    
    def _process_structured_data(self, data):
        """Process data in the structured format (for test script compatibility)."""
        # Update attitude
        if 'attitude' in data:
            attitude = data['attitude']
            if 'roll' in attitude:
                self.roll_label.setText(f"{attitude['roll']:.1f} deg")
            if 'pitch' in attitude:
                self.pitch_label.setText(f"{attitude['pitch']:.1f} deg")
            if 'yaw' in attitude:
                self.yaw_label.setText(f"{attitude['yaw']:.1f} deg")
            if 'heading' in attitude:
                self.heading_label.setText(f"{attitude['heading']:.1f} deg")
                
        # Update position
        if 'position' in data:
            position = data['position']
            if 'lat' in position:
                self.lat_label.setText(f"{position['lat']:.7f}")
            if 'lon' in position:
                self.lon_label.setText(f"{position['lon']:.7f}")
            if 'alt' in position:
                self.alt_label.setText(f"{position['alt']:.1f} m")
            if 'relative_alt' in position:
                self.rel_alt_label.setText(f"{position['relative_alt']:.1f} m")
                
        # Update battery
        if 'battery' in data:
            battery = data['battery']
            if 'voltage' in battery:
                self.voltage_label.setText(f"{battery['voltage']:.2f} V")
            if 'current' in battery:
                self.current_label.setText(f"{battery['current']:.2f} A")
            if 'level' in battery:
                self.level_label.setText(f"{battery['level']}%")
                
        # Update speed
        if 'speed' in data:
            speed = data['speed']
            if 'groundspeed' in speed:
                self.groundspeed_label.setText(f"{speed['groundspeed']:.1f} m/s")
            if 'airspeed' in speed:
                self.airspeed_label.setText(f"{speed['airspeed']:.1f} m/s")
            if 'climb' in speed:
                self.climb_label.setText(f"{speed['climb']:.1f} m/s")
