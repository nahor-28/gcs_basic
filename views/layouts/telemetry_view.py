from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt
from views.base_view import BaseView
import logging

# Configure logging for debug output
logger = logging.getLogger(__name__)

class TelemetryView(BaseView):
    """Telemetry view component for displaying vehicle telemetry data."""
    
    def __init__(self, signal_manager):
        super().__init__(signal_manager)
        logger.info("TelemetryView initialized")
    
    def setup_ui(self):
        """Setup the telemetry UI components."""
        logger.debug("TelemetryView: Setting up UI components")
        # Create layout
        layout = QVBoxLayout()
        
        # Create telemetry groups
        layout.addWidget(self._create_attitude_group())
        layout.addWidget(self._create_position_group())
        layout.addWidget(self._create_speed_group())
        layout.addWidget(self._create_battery_group())
        layout.addWidget(self._create_status_group())
        
        # Add stretch to fill remaining space
        layout.addStretch()
        
        self.setLayout(layout)
        # logger.debug("TelemetryView UI setup complete")
    
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
        # logger.debug("TelemetryView: Created attitude group")
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
        # Add GPS labels that were missing
        self.gps_fix_label = QLabel("GPS Fix: --")
        self.gps_sats_label = QLabel("Satellites: --")
        
        # Add labels to layout
        layout.addWidget(QLabel("Latitude:"), 0, 0)
        layout.addWidget(self.lat_label, 0, 1)
        layout.addWidget(QLabel("Longitude:"), 1, 0)
        layout.addWidget(self.lon_label, 1, 1)
        layout.addWidget(QLabel("Altitude:"), 2, 0)
        layout.addWidget(self.alt_label, 2, 1)
        layout.addWidget(QLabel("Relative Alt:"), 3, 0)
        layout.addWidget(self.rel_alt_label, 3, 1)
        layout.addWidget(QLabel("GPS Fix:"), 4, 0)
        layout.addWidget(self.gps_fix_label, 4, 1)
        layout.addWidget(QLabel("Satellites:"), 5, 0)
        layout.addWidget(self.gps_sats_label, 5, 1)
        
        group.setLayout(layout)
        # logger.debug("TelemetryView: Created position group with GPS labels")
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
        # logger.debug("TelemetryView: Created battery group")
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
        # logger.debug("TelemetryView: Created speed group")
        return group
    
    def _create_status_group(self):
        """Create the status telemetry group."""
        group = QGroupBox("Status")
        layout = QGridLayout()
        
        # Create labels
        self.flight_mode_label = QLabel("Flight Mode: --")
        self.arming_status_label = QLabel("Arming Status: --")
        
        # Add labels to layout
        layout.addWidget(QLabel("Flight Mode:"), 0, 0)
        layout.addWidget(self.flight_mode_label, 0, 1)
        layout.addWidget(QLabel("Arming Status:"), 1, 0)
        layout.addWidget(self.arming_status_label, 1, 1)
        
        group.setLayout(layout)
        # logger.debug("TelemetryView: Created status group")
        return group
    
    def connect_signals(self):
        """Connect signals to slots."""
        # logger.debug("TelemetryView: Connecting signals")
        if self.signal_manager:
            self.signal_manager.vehicle_attitude_updated.connect(self.update_attitude_display)
            self.signal_manager.vehicle_position_updated.connect(self.update_position_display)
            self.signal_manager.vehicle_gps_updated.connect(self.update_gps_display)
            self.signal_manager.vehicle_status_updated.connect(self.update_status_display)
            logger.info("TelemetryView: Connected to all vehicle update signals")
        else:
            logger.error("TelemetryView: No signal_manager available for signal connections")
    
    def update_attitude_display(self, attitude_data):
        """Update attitude related labels."""
        # logger.debug(f"TelemetryView: update_attitude_display called with data: {attitude_data}")
        try:
            if 'roll' in attitude_data:
                self.roll_label.setText(f"{attitude_data['roll']:.1f} deg")
                # logger.debug(f"TelemetryView: Updated roll label to: {attitude_data['roll']:.1f} deg")
            if 'pitch' in attitude_data:
                self.pitch_label.setText(f"{attitude_data['pitch']:.1f} deg")
                # logger.debug(f"TelemetryView: Updated pitch label to: {attitude_data['pitch']:.1f} deg")
            if 'yaw' in attitude_data:
                self.yaw_label.setText(f"{attitude_data['yaw']:.1f} deg")
                # logger.debug(f"TelemetryView: Updated yaw label to: {attitude_data['yaw']:.1f} deg")
            if 'heading' in attitude_data:
                self.heading_label.setText(f"{attitude_data['heading']:.1f} deg")
                # logger.debug(f"TelemetryView: Updated heading label to: {attitude_data['heading']:.1f} deg")
            # logger.debug("TelemetryView: Attitude display update completed")
        except Exception as e:
            logger.error(f"TelemetryView: Error updating attitude display: {e}")

    def update_position_display(self, position_data):
        """Update position related labels and speed if it's included."""
        # logger.debug(f"TelemetryView: update_position_display called with data: {position_data}")
        try:
            if 'lat' in position_data:
                self.lat_label.setText(f"{position_data['lat']:.7f}")
                # logger.debug(f"TelemetryView: Updated latitude label to: {position_data['lat']:.7f}")
            if 'lon' in position_data:
                self.lon_label.setText(f"{position_data['lon']:.7f}")
                # logger.debug(f"TelemetryView: Updated longitude label to: {position_data['lon']:.7f}")
            if 'alt_msl' in position_data:
                self.alt_label.setText(f"{position_data['alt_msl']:.1f} m")
                # logger.debug(f"TelemetryView: Updated altitude label to: {position_data['alt_msl']:.1f} m")
            if 'alt_agl' in position_data:
                self.rel_alt_label.setText(f"{position_data['alt_agl']:.1f} m")
                # logger.debug(f"TelemetryView: Updated relative altitude label to: {position_data['alt_agl']:.1f} m")
            
            if 'groundspeed' in position_data:
                self.groundspeed_label.setText(f"{position_data['groundspeed']:.1f} m/s")
                # logger.debug(f"TelemetryView: Updated groundspeed label to: {position_data['groundspeed']:.1f} m/s")
            if 'airspeed' in position_data:
                self.airspeed_label.setText(f"{position_data['airspeed']:.1f} m/s")
                # logger.debug(f"TelemetryView: Updated airspeed label to: {position_data['airspeed']:.1f} m/s")
            if 'climb_rate' in position_data:
                self.climb_label.setText(f"{position_data['climb_rate']:.1f} m/s")
                # logger.debug(f"TelemetryView: Updated climb rate label to: {position_data['climb_rate']:.1f} m/s")
            # logger.debug("TelemetryView: Position display update completed")
        except Exception as e:
            logger.error(f"TelemetryView: Error updating position display: {e}")

    def update_gps_display(self, gps_data):
        """Update GPS specific labels."""
        # logger.debug(f"TelemetryView: update_gps_display called with data: {gps_data}")
        try:
            if 'fix_type' in gps_data:
                self.gps_fix_label.setText(f"{gps_data['fix_type']}")
                # logger.debug(f"TelemetryView: Updated GPS fix label to: {gps_data['fix_type']}")
            if 'satellites_visible' in gps_data:
                self.gps_sats_label.setText(f"{gps_data['satellites_visible']}")
                # logger.debug(f"TelemetryView: Updated GPS satellites label to: {gps_data['satellites_visible']}")
            if 'heading' in gps_data and not hasattr(self, 'heading_from_attitude'):
                 self.heading_label.setText(f"{gps_data['heading']:.1f} deg")
                 # logger.debug(f"TelemetryView: Updated heading from GPS to: {gps_data['heading']:.1f} deg")
            # logger.debug("TelemetryView: GPS display update completed")
        except Exception as e:
            logger.error(f"TelemetryView: Error updating GPS display: {e}")

    def update_status_display(self, status_data):
        """Update status related labels (e.g., battery)."""
        # logger.debug(f"TelemetryView: update_status_display called with data: {status_data}")
        try:
            if 'battery_voltage' in status_data:
                self.voltage_label.setText(f"{status_data['battery_voltage']:.2f} V")
                # logger.debug(f"TelemetryView: Updated voltage label to: {status_data['battery_voltage']:.2f} V")
            if 'battery_current' in status_data:
                current = status_data['battery_current']
                self.current_label.setText(f"{current:.2f} A" if current is not None else "-- A")
                # logger.debug(f"TelemetryView: Updated current label to: {current:.2f} A" if current is not None else "-- A")
            if 'battery_remaining' in status_data:
                level = status_data['battery_remaining']
                self.level_label.setText(f"{level}%" if level is not None else "-- %")
                # logger.debug(f"TelemetryView: Updated battery level to: {level}%" if level is not None else "-- %")
            if 'flight_mode' in status_data:
                self.flight_mode_label.setText(f"{status_data['flight_mode']}")
                # logger.debug(f"TelemetryView: Updated flight mode label to: {status_data['flight_mode']}")
            if 'arming_status' in status_data:
                self.arming_status_label.setText(f"{status_data['arming_status']}")
                # logger.debug(f"TelemetryView: Updated arming status label to: {status_data['arming_status']}")
            # logger.debug("TelemetryView: Status display update completed")
        except Exception as e:
            logger.error(f"TelemetryView: Error updating status display: {e}")
