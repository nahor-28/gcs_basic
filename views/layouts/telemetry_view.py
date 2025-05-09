from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt

from views.base_view import BaseView

class TelemetryView(BaseView):
    """Telemetry view component for displaying vehicle telemetry data."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
        
    def setup_ui(self):
        """Setup the telemetry UI components."""
        layout = QVBoxLayout(self)
        
        # Create group boxes for different telemetry categories
        self.attitude_group = self._create_attitude_group()
        self.position_group = self._create_position_group()
        self.battery_group = self._create_battery_group()
        self.speed_group = self._create_speed_group()
        
        # Add groups to layout
        layout.addWidget(self.attitude_group)
        layout.addWidget(self.position_group)
        layout.addWidget(self.battery_group)
        layout.addWidget(self.speed_group)
        layout.addStretch()
        
    def _create_attitude_group(self):
        """Create the attitude telemetry group."""
        group = QGroupBox("Attitude")
        layout = QGridLayout()
        
        # Create labels
        self.roll_label = QLabel("Roll: ---")
        self.pitch_label = QLabel("Pitch: ---")
        self.yaw_label = QLabel("Yaw: ---")
        self.heading_label = QLabel("Heading: ---")
        
        # Add labels to layout
        layout.addWidget(QLabel("Roll:"), 0, 0)
        layout.addWidget(self.roll_label, 0, 1)
        layout.addWidget(QLabel("Pitch:"), 0, 2)
        layout.addWidget(self.pitch_label, 0, 3)
        layout.addWidget(QLabel("Yaw:"), 1, 0)
        layout.addWidget(self.yaw_label, 1, 1)
        layout.addWidget(QLabel("Heading:"), 1, 2)
        layout.addWidget(self.heading_label, 1, 3)
        
        group.setLayout(layout)
        return group
        
    def _create_position_group(self):
        """Create the position telemetry group."""
        group = QGroupBox("Position")
        layout = QGridLayout()
        
        # Create labels
        self.lat_label = QLabel("Latitude: ---")
        self.lon_label = QLabel("Longitude: ---")
        self.alt_label = QLabel("Altitude: ---")
        self.gps_label = QLabel("GPS: ---")
        
        # Add labels to layout
        layout.addWidget(QLabel("Latitude:"), 0, 0)
        layout.addWidget(self.lat_label, 0, 1)
        layout.addWidget(QLabel("Longitude:"), 0, 2)
        layout.addWidget(self.lon_label, 0, 3)
        layout.addWidget(QLabel("Altitude:"), 1, 0)
        layout.addWidget(self.alt_label, 1, 1)
        layout.addWidget(QLabel("GPS:"), 1, 2)
        layout.addWidget(self.gps_label, 1, 3)
        
        group.setLayout(layout)
        return group
        
    def _create_battery_group(self):
        """Create the battery telemetry group."""
        group = QGroupBox("Battery")
        layout = QGridLayout()
        
        # Create labels
        self.voltage_label = QLabel("Voltage: ---")
        self.current_label = QLabel("Current: ---")
        self.remaining_label = QLabel("Remaining: ---")
        
        # Add labels to layout
        layout.addWidget(QLabel("Voltage:"), 0, 0)
        layout.addWidget(self.voltage_label, 0, 1)
        layout.addWidget(QLabel("Current:"), 0, 2)
        layout.addWidget(self.current_label, 0, 3)
        layout.addWidget(QLabel("Remaining:"), 1, 0)
        layout.addWidget(self.remaining_label, 1, 1)
        
        group.setLayout(layout)
        return group
        
    def _create_speed_group(self):
        """Create the speed telemetry group."""
        group = QGroupBox("Speed")
        layout = QGridLayout()
        
        # Create labels
        self.airspeed_label = QLabel("Airspeed: ---")
        self.groundspeed_label = QLabel("Groundspeed: ---")
        self.climb_rate_label = QLabel("Climb Rate: ---")
        self.throttle_label = QLabel("Throttle: ---")
        
        # Add labels to layout
        layout.addWidget(QLabel("Airspeed:"), 0, 0)
        layout.addWidget(self.airspeed_label, 0, 1)
        layout.addWidget(QLabel("Groundspeed:"), 0, 2)
        layout.addWidget(self.groundspeed_label, 0, 3)
        layout.addWidget(QLabel("Climb Rate:"), 1, 0)
        layout.addWidget(self.climb_rate_label, 1, 1)
        layout.addWidget(QLabel("Throttle:"), 1, 2)
        layout.addWidget(self.throttle_label, 1, 3)
        
        group.setLayout(layout)
        return group
        
    def connect_signals(self):
        """Connect signals to slots."""
        # No direct signal connections needed as updates come through update_view
        pass
        
    def update_view(self, data):
        """Update the telemetry display with new data."""
        # Update attitude
        attitude = data.get('attitude', {})
        self.roll_label.setText(f"Roll: {attitude.get('roll', '---'):.1f}°")
        self.pitch_label.setText(f"Pitch: {attitude.get('pitch', '---'):.1f}°")
        self.yaw_label.setText(f"Yaw: {attitude.get('yaw', '---'):.1f}°")
        self.heading_label.setText(f"Heading: {data.get('heading', '---'):.1f}°")
        
        # Update position
        position = data.get('position', {})
        self.lat_label.setText(f"Latitude: {position.get('lat', '---'):.6f}°")
        self.lon_label.setText(f"Longitude: {position.get('lon', '---'):.6f}°")
        self.alt_label.setText(f"Altitude: {position.get('alt', '---'):.1f}m")
        
        # Update GPS
        gps = data.get('gps', {})
        fix_types = {
            0: "No Fix",
            1: "No GPS",
            2: "2D Fix",
            3: "3D Fix",
            4: "DGPS",
            5: "RTK Float",
            6: "RTK Fixed"
        }
        fix_type = fix_types.get(gps.get('fix_type', 0), "Unknown")
        self.gps_label.setText(f"GPS: {fix_type} ({gps.get('satellites', 0)} sats)")
        
        # Update battery
        battery = data.get('battery', {})
        self.voltage_label.setText(f"Voltage: {battery.get('voltage', '---'):.1f}V")
        if battery.get('current') is not None:
            self.current_label.setText(f"Current: {battery.get('current', '---'):.1f}A")
        if battery.get('remaining') is not None:
            self.remaining_label.setText(f"Remaining: {battery.get('remaining', '---')}%")
            
        # Update speed
        speed = data.get('speed', {})
        self.airspeed_label.setText(f"Airspeed: {speed.get('air', '---'):.1f} m/s")
        self.groundspeed_label.setText(f"Groundspeed: {speed.get('ground', '---'):.1f} m/s")
        self.climb_rate_label.setText(f"Climb Rate: {data.get('climb_rate', '---'):.1f} m/s")
        self.throttle_label.setText(f"Throttle: {data.get('throttle', '---'):.0f}%") 