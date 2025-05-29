from models.base_model import BaseModel
import logging

# Configure logging for debug output
logger = logging.getLogger(__name__)

class VehicleModel(BaseModel):
    """Model for vehicle-related data."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the vehicle model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.attitude = {}
        self.position = {}
        self.gps_info = {}
        self.system_status = {} # e.g., arming state, mode
        logger.info("VehicleModel initialized")
        # self.connect_signals() # Remove direct connection to raw telemetry_update

    # Remove connect_signals as the model no longer directly listens to raw telemetry_update
    # def connect_signals(self):
    #     """Connect signal handlers."""
    #     if self.signal_manager:
    #         self.signal_manager.telemetry_update.connect(
    #             lambda data: self.update_from_raw_telemetry(data, from_signal=True)
    #         )

    def update_attitude(self, data):
        """Update attitude data and emit a signal."""
        # logger.debug(f"VehicleModel: update_attitude called with data: {data}")
        self.attitude.update(data)
        # logger.debug(f"VehicleModel: Updated attitude storage to: {self.attitude}")
        if self.signal_manager:
            attitude_copy = self.attitude.copy()
            # logger.debug(f"VehicleModel: Emitting vehicle_attitude_updated signal with data: {attitude_copy}")
            self.signal_manager.vehicle_attitude_updated.emit(attitude_copy)
            # logger.debug("VehicleModel: vehicle_attitude_updated signal emitted successfully")
        else:
            logger.error("VehicleModel: No signal_manager available to emit vehicle_attitude_updated")

    def update_position(self, data):
        """Update position data and emit a signal."""
        # logger.debug(f"VehicleModel: update_position called with data: {data}")
        self.position.update(data)
        # logger.debug(f"VehicleModel: Updated position storage to: {self.position}")
        if self.signal_manager:
            position_copy = self.position.copy()
            # logger.debug(f"VehicleModel: Emitting vehicle_position_updated signal with data: {position_copy}")
            self.signal_manager.vehicle_position_updated.emit(position_copy)
            # logger.debug("VehicleModel: vehicle_position_updated signal emitted successfully")
        else:
            logger.error("VehicleModel: No signal_manager available to emit vehicle_position_updated")
            
    def update_gps_info(self, data):
        """Update GPS info data and emit a signal."""
        # logger.debug(f"VehicleModel: update_gps_info called with data: {data}")
        self.gps_info.update(data)
        # logger.debug(f"VehicleModel: Updated gps_info storage to: {self.gps_info}")
        if self.signal_manager:
            gps_copy = self.gps_info.copy()
            # logger.debug(f"VehicleModel: Emitting vehicle_gps_updated signal with data: {gps_copy}")
            self.signal_manager.vehicle_gps_updated.emit(gps_copy)
            # logger.debug("VehicleModel: vehicle_gps_updated signal emitted successfully")
        else:
            logger.error("VehicleModel: No signal_manager available to emit vehicle_gps_updated")

    def update_system_status(self, data):
        """Update system status (e.g., arming, mode) and emit a signal."""
        # logger.debug(f"VehicleModel: update_system_status called with data: {data}")
        self.system_status.update(data)
        # logger.debug(f"VehicleModel: Updated system_status storage to: {self.system_status}")
        if self.signal_manager:
            status_copy = self.system_status.copy()
            # logger.debug(f"VehicleModel: Emitting vehicle_status_updated signal with data: {status_copy}")
            self.signal_manager.vehicle_status_updated.emit(status_copy)
            # logger.debug("VehicleModel: vehicle_status_updated signal emitted successfully")
        else:
            logger.error("VehicleModel: No signal_manager available to emit vehicle_status_updated")

    # The controller will now call these specific update methods
    # instead of a generic `update` method.
    # def update(self, data, from_signal=False):
    #     """
    #     Update the model with new telemetry data.
    #     This method is now replaced by more specific update methods
    #     called by the VehicleController.
    #     """
    #     pass # Keep for compatibility or remove if not needed

    def get_attitude_data(self):
        # logger.debug(f"VehicleModel: get_attitude_data called, returning: {self.attitude}")
        return self.attitude.copy()

    def get_position_data(self):
        # logger.debug(f"VehicleModel: get_position_data called, returning: {self.position}")
        return self.position.copy()
        
    def get_gps_data(self):
        # logger.debug(f"VehicleModel: get_gps_data called, returning: {self.gps_info}")
        return self.gps_info.copy()

    def get_system_status_data(self):
        # logger.debug(f"VehicleModel: get_system_status_data called, returning: {self.system_status}")
        return self.system_status.copy()

    def get_all_data(self):
        """
        Get all current vehicle data.
        
        Returns:
            dict: A dictionary containing all vehicle data.
        """
        all_data = {
            "attitude": self.attitude.copy(),
            "position": self.position.copy(),
            "gps": self.gps_info.copy(),
            "status": self.system_status.copy(),
        }
        # logger.debug(f"VehicleModel: get_all_data called, returning: {all_data}")
        return all_data

    # get_data can be an alias for get_all_data or be removed if specific getters are preferred.
    def get_data(self):
        return self.get_all_data()
