from controllers.base_controller import BaseController

class VehicleController(BaseController):
    """Controller for vehicle-related operations."""
    
    def __init__(self, vehicle_model, telemetry_view, signal_manager):
        """
        Initialize the vehicle controller.
        
        Args:
            vehicle_model: The vehicle model
            telemetry_view: The telemetry view
            signal_manager: The application's signal manager
        """
        # The view is no longer directly updated by this controller for telemetry data
        super().__init__(vehicle_model, None, signal_manager) # Pass None for view if it's not used
        # If the view (telemetry_view) is needed for other controller actions (e.g. user input from it),
        # it can still be stored: self.telemetry_view = telemetry_view 
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to the raw telemetry_update signal from TelemetryManager
            self.signal_manager.telemetry_update.connect(self.handle_raw_telemetry_update)
    
    def handle_raw_telemetry_update(self, raw_data):
        """
        Handle raw telemetry update from TelemetryManager.
        Parse it and update the VehicleModel accordingly.
        The VehicleModel will then emit specific signals for views.
        
        Args:
            raw_data: Dictionary with raw telemetry data (e.g., from MAVLink)
                      This data often includes a 'type' field indicating the message type.
        """
        if not self.model or not isinstance(raw_data, dict):
            return

        msg_type = raw_data.get('type')

        # Example parsing logic based on assumed MAVLink-like message types
        # This will need to be adapted to the actual structure of raw_data
        if msg_type == 'ATTITUDE':
            attitude_data = {
                'roll': raw_data.get('roll'),
                'pitch': raw_data.get('pitch'),
                'yaw': raw_data.get('yaw')
            }
            # Filter out None values before updating
            attitude_data = {k: v for k, v in attitude_data.items() if v is not None}
            if attitude_data:
                self.model.update_attitude(attitude_data)
        
        elif msg_type == 'GLOBAL_POSITION_INT':
            position_data = {
                'lat': raw_data.get('lat'),
                'lon': raw_data.get('lon'),
                'alt_msl': raw_data.get('alt'),      # MAVLink GLOBAL_POSITION_INT uses 'alt' for MSL
                'alt_agl': raw_data.get('relative_alt') # MAVLink GLOBAL_POSITION_INT uses 'relative_alt' for AGL
            }
            position_data = {k: v for k, v in position_data.items() if v is not None}
            if position_data:
                self.model.update_position(position_data)

        elif msg_type == 'GPS_RAW_INT': # Example for GPS specific data
            gps_data = {
                'fix_type': raw_data.get('fix_type'),
                'satellites_visible': raw_data.get('satellites_visible'),
                # Potentially 'eph', 'epv', 'vel', 'cog' (course over ground)
                'heading': raw_data.get('cog') # if cog is used for heading, typically /100 for degrees
            }
            gps_data = {k: v for k, v in gps_data.items() if v is not None}
            if 'heading' in gps_data and gps_data['heading'] != 65535: # MAVLink COG invalid if 65535
                gps_data['heading'] /= 100.0
            else:
                gps_data.pop('heading', None)
            if gps_data:
                self.model.update_gps_info(gps_data)

        elif msg_type == 'SYS_STATUS':
            status_update = {
                'battery_voltage': raw_data.get('voltage_battery'), # MAVLink uses voltage_battery (mV)
                'battery_current': raw_data.get('current_battery'), # MAVLink uses current_battery (cA)
                'battery_remaining': raw_data.get('battery_remaining') # MAVLink uses battery_remaining (%)
            }
            status_update = {k: v for k, v in status_update.items() if v is not None}
            if 'battery_voltage' in status_update: status_update['battery_voltage'] /= 1000.0 # mV to V
            if 'battery_current' in status_update: status_update['battery_current'] /= 100.0 # cA to A
            if status_update:
                self.model.update_system_status(status_update) # Assuming battery is part of general system status

        elif msg_type == 'VFR_HUD': # Often contains airspeed, groundspeed, climb rate, heading
            # This data often overlaps or complements other messages.
            # Decide where each piece of data best fits (position, attitude, or a new speed category)
            position_speed_update = {}
            attitude_heading_update = {}

            if raw_data.get('airspeed') is not None: position_speed_update['airspeed'] = raw_data['airspeed']
            if raw_data.get('groundspeed') is not None: position_speed_update['groundspeed'] = raw_data['groundspeed']
            if raw_data.get('climb') is not None: position_speed_update['climb_rate'] = raw_data['climb']
            if raw_data.get('heading') is not None: attitude_heading_update['heading'] = raw_data['heading']

            if position_speed_update: # Could also be self.model.update_speed_info(data)
                self.model.update_position(position_speed_update) # Augment position data with speeds
            if attitude_heading_update:
                self.model.update_attitude(attitude_heading_update) # Augment attitude with heading

    def set_mode(self, mode):
        """
        Set the vehicle flight mode.
        
        Args:
            mode: Flight mode string
        """
        if self.signal_manager:
            # self.signal_manager.set_mode_request.emit(mode) # Example: send command
            pass
        # Update model if mode change is confirmed by vehicle
        # self.model.update_system_status({'mode': new_mode})
    
    def arm_vehicle(self):
        """Arm the vehicle."""
        if self.signal_manager:
            # self.signal_manager.arm_vehicle_request.emit()
            pass
        # Update model if arming is confirmed
        # self.model.update_system_status({'armed': True})
    
    def disarm_vehicle(self):
        """Disarm the vehicle."""
        if self.signal_manager:
            # self.signal_manager.disarm_vehicle_request.emit()
            pass
        # Update model if disarming is confirmed
        # self.model.update_system_status({'armed': False})
