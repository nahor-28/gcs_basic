from controllers.base_controller import BaseController
import logging

# Configure logging for debug output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info("VehicleController initialized")
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to the raw telemetry_update signal from TelemetryManager
            self.signal_manager.telemetry_update.connect(self.handle_raw_telemetry_update)
            logger.info("VehicleController: Connected to telemetry_update signal")
        else:
            logger.error("VehicleController: No signal_manager available for signal connections")
    
    def handle_raw_telemetry_update(self, raw_data):
        """
        Handle raw telemetry update from TelemetryManager.
        Parse it and update the VehicleModel accordingly.
        The VehicleModel will then emit specific signals for views.
        
        Args:
            raw_data: Dictionary with raw telemetry data (e.g., from MAVLink)
                      This data often includes a 'type' field indicating the message type.
        """
        logger.debug(f"VehicleController: Received raw telemetry data: {raw_data}")
        
        if not self.model or not isinstance(raw_data, dict):
            logger.warning(f"VehicleController: Invalid model ({self.model}) or data type ({type(raw_data)})")
            return

        msg_type = raw_data.get('type')
        logger.debug(f"VehicleController: Processing message type: {msg_type}")

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
                logger.debug(f"VehicleController: Updating attitude with data: {attitude_data}")
                self.model.update_attitude(attitude_data)
                logger.debug("VehicleController: Called model.update_attitude()")
            else:
                logger.warning("VehicleController: ATTITUDE message had no valid data")
        
        elif msg_type == 'GLOBAL_POSITION_INT':
            position_data = {
                'lat': raw_data.get('lat'),
                'lon': raw_data.get('lon'),
                'alt_msl': raw_data.get('alt_msl'),      # MAVLink GLOBAL_POSITION_INT uses 'alt' for MSL
                'alt_agl': raw_data.get('alt_agl') # MAVLink GLOBAL_POSITION_INT uses 'relative_alt' for AGL
            }
            position_data = {k: v for k, v in position_data.items() if v is not None}
            if position_data:
                logger.debug(f"VehicleController: Updating position with data: {position_data}")
                self.model.update_position(position_data)
                logger.debug("VehicleController: Called model.update_position()")
            else:
                logger.warning("VehicleController: GLOBAL_POSITION_INT message had no valid data")

        elif msg_type == 'GPS_RAW_INT': # Example for GPS specific data
            gps_data = {
                'fix_type': raw_data.get('gps_fix_type'),
                'satellites_visible': raw_data.get('gps_satellites'),
                # Potentially 'eph', 'epv', 'vel', 'cog' (course over ground)
                'heading': raw_data.get('cog') # if cog is used for heading, typically /100 for degrees
            }
            gps_data = {k: v for k, v in gps_data.items() if v is not None}
            if 'heading' in gps_data and gps_data['heading'] != 65535: # MAVLink COG invalid if 65535
                gps_data['heading'] /= 100.0
            else:
                gps_data.pop('heading', None)
            if gps_data:
                logger.debug(f"VehicleController: Updating GPS info with data: {gps_data}")
                self.model.update_gps_info(gps_data)
                logger.debug("VehicleController: Called model.update_gps_info()")
            else:
                logger.warning("VehicleController: GPS_RAW_INT message had no valid data")

        elif msg_type == 'SYS_STATUS':
            status_update = {
                'battery_voltage': raw_data.get('battery_voltage'), # MAVLink uses voltage_battery (mV)
                'battery_current': raw_data.get('battery_current'), # MAVLink uses current_battery (cA)
                'battery_remaining': raw_data.get('battery_remaining') # MAVLink uses battery_remaining (%)
            }
            status_update = {k: v for k, v in status_update.items() if v is not None}
            if status_update:
                logger.debug(f"VehicleController: Updating system status with data: {status_update}")
                self.model.update_system_status(status_update) # Assuming battery is part of general system status
                logger.debug("VehicleController: Called model.update_system_status()")
            else:
                logger.warning("VehicleController: SYS_STATUS message had no valid data")

        elif msg_type == 'VFR_HUD': # Often contains airspeed, groundspeed, climb rate, heading
            # This data often overlaps or complements other messages.
            # Decide where each piece of data best fits (position, attitude, or a new speed category)
            position_speed_update = {}
            attitude_heading_update = {}

            if raw_data.get('airspeed') is not None: position_speed_update['airspeed'] = raw_data['airspeed']
            if raw_data.get('groundspeed') is not None: position_speed_update['groundspeed'] = raw_data['groundspeed']
            if raw_data.get('climb_rate') is not None: position_speed_update['climb_rate'] = raw_data['climb_rate']
            if raw_data.get('heading') is not None: attitude_heading_update['heading'] = raw_data['heading']

            if position_speed_update: # Could also be self.model.update_speed_info(data)
                logger.debug(f"VehicleController: Updating position with speed data: {position_speed_update}")
                self.model.update_position(position_speed_update) # Augment position data with speeds
                logger.debug("VehicleController: Called model.update_position() for VFR_HUD speeds")
            if attitude_heading_update:
                logger.debug(f"VehicleController: Updating attitude with heading data: {attitude_heading_update}")
                self.model.update_attitude(attitude_heading_update) # Augment attitude with heading
                logger.debug("VehicleController: Called model.update_attitude() for VFR_HUD heading")
        
        elif msg_type == 'HEARTBEAT':
            heartbeat_data = {
                'armed': raw_data.get('armed'),
                'mode': raw_data.get('mode'),
                'system_status': raw_data.get('system_status')
            }
            heartbeat_data = {k: v for k, v in heartbeat_data.items() if v is not None}
            if heartbeat_data:
                logger.debug(f"VehicleController: Updating system status with heartbeat data: {heartbeat_data}")
                self.model.update_system_status(heartbeat_data)
                logger.debug("VehicleController: Called model.update_system_status() for HEARTBEAT")
            else:
                logger.warning("VehicleController: HEARTBEAT message had no valid data")
        
        else:
            logger.debug(f"VehicleController: Ignoring message type: {msg_type}")

    def set_mode(self, mode):
        """
        Set the vehicle flight mode.
        
        Args:
            mode: Flight mode string
        """
        logger.info(f"VehicleController: set_mode called with mode: {mode}")
        if self.signal_manager:
            # self.signal_manager.set_mode_request.emit(mode) # Example: send command
            logger.warning("VehicleController: set_mode not yet implemented - signal not defined")
            pass
        # Update model if mode change is confirmed by vehicle
        # self.model.update_system_status({'mode': new_mode})
    
    def arm_vehicle(self):
        """Arm the vehicle."""
        logger.info("VehicleController: arm_vehicle called")
        if self.signal_manager:
            # self.signal_manager.arm_vehicle_request.emit()
            logger.warning("VehicleController: arm_vehicle not yet implemented - signal not defined")
            pass
        # Update model if arming is confirmed
        # self.model.update_system_status({'armed': True})
    
    def disarm_vehicle(self):
        """Disarm the vehicle."""
        logger.info("VehicleController: disarm_vehicle called")
        if self.signal_manager:
            # self.signal_manager.disarm_vehicle_request.emit()
            logger.warning("VehicleController: disarm_vehicle not yet implemented - signal not defined")
            pass
        # Update model if disarming is confirmed
        # self.model.update_system_status({'armed': False})
