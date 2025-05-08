from PySide6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel
)

class TelemetryLayout(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Telemetry", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Creates and arranges the telemetry display."""
        layout = QGridLayout()
        
        # Position
        layout.addWidget(QLabel("Latitude:"), 0, 0)
        self.latitude_label = QLabel("0.0")
        layout.addWidget(self.latitude_label, 0, 1)
        
        layout.addWidget(QLabel("Longitude:"), 1, 0)
        self.longitude_label = QLabel("0.0")
        layout.addWidget(self.longitude_label, 1, 1)
        
        layout.addWidget(QLabel("Altitude:"), 2, 0)
        self.altitude_label = QLabel("0.0")
        layout.addWidget(self.altitude_label, 2, 1)
        
        # Attitude
        layout.addWidget(QLabel("Roll:"), 3, 0)
        self.roll_label = QLabel("0.0°")
        layout.addWidget(self.roll_label, 3, 1)
        
        layout.addWidget(QLabel("Pitch:"), 4, 0)
        self.pitch_label = QLabel("0.0°")
        layout.addWidget(self.pitch_label, 4, 1)
        
        layout.addWidget(QLabel("Yaw:"), 5, 0)
        self.yaw_label = QLabel("0.0°")
        layout.addWidget(self.yaw_label, 5, 1)
        
        # GPS Info
        layout.addWidget(QLabel("GPS Fix:"), 6, 0)
        self.gps_fix_label = QLabel("No Fix")
        layout.addWidget(self.gps_fix_label, 6, 1)
        
        layout.addWidget(QLabel("GPS Sats:"), 7, 0)
        self.gps_sats_label = QLabel("0")
        layout.addWidget(self.gps_sats_label, 7, 1)
        
        # Other telemetry
        layout.addWidget(QLabel("Heading:"), 8, 0)
        self.heading_label = QLabel("0.0°")
        layout.addWidget(self.heading_label, 8, 1)
        
        layout.addWidget(QLabel("Ground Speed:"), 9, 0)
        self.ground_speed_label = QLabel("0.0 m/s")
        layout.addWidget(self.ground_speed_label, 9, 1)
        
        layout.addWidget(QLabel("Battery:"), 10, 0)
        self.battery_label = QLabel("0%")
        layout.addWidget(self.battery_label, 10, 1)
        
        self.setLayout(layout)
        
    def update_telemetry(self, data):
        """Update telemetry display with new data."""
        update_type = data.get("type")
        
        if update_type == "GLOBAL_POSITION_INT":
            lat = data.get('lat')
            lon = data.get('lon')
            alt = data.get('alt_agl')
            
            if lat is not None:
                self.latitude_label.setText(f"{lat:.6f}")
            if lon is not None:
                self.longitude_label.setText(f"{lon:.6f}")
            if alt is not None:
                self.altitude_label.setText(f"{alt:.1f} m")
                
        elif update_type == "ATTITUDE":
            roll = data.get('roll')
            pitch = data.get('pitch')
            yaw = data.get('yaw')
            
            if roll is not None:
                self.roll_label.setText(f"{roll:.1f}°")
            if pitch is not None:
                self.pitch_label.setText(f"{pitch:.1f}°")
            if yaw is not None:
                self.yaw_label.setText(f"{yaw:.1f}°")
                
        elif update_type == "GPS_RAW_INT":
            fix = data.get('gps_fix_type')
            sats = data.get('gps_satellites')
            
            if fix is not None:
                fix_map = {0: "No Fix", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
                self.gps_fix_label.setText(fix_map.get(fix, f"Unknown ({fix})"))
            if sats is not None:
                self.gps_sats_label.setText(str(sats))
                
        elif update_type == "VFR_HUD":
            heading = data.get('heading')
            groundspeed = data.get('groundspeed')
            
            if heading is not None:
                self.heading_label.setText(f"{heading:.1f}°")
            if groundspeed is not None:
                self.ground_speed_label.setText(f"{groundspeed:.1f} m/s")
                
        elif update_type == "SYS_STATUS":
            battery = data.get('battery_remaining')
            if battery is not None:
                self.battery_label.setText(f"{battery:.1f}%") 